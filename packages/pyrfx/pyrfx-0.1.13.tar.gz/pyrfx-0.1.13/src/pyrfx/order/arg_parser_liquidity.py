import logging
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Final

from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import PRECISION, get_available_tokens, to_decimal


class LiquidityArgumentParser:
    """
    A utility class to parse and process liquidity arguments for deposit and withdrawal orders.
    This class ensures that all required parameters are present and properly formatted.
    """

    def __init__(self, config: ConfigManager, operation_type: str) -> None:
        """
        Initialize the LiquidityArgumentParser with necessary configurations and parameters.

        :param config: Configuration object containing chain and market settings.
        :param operation_type: The type of operation to be performed, either 'deposit' or 'withdraw'.
        :raises ValueError: If the operation_type is not 'deposit' or 'withdraw'.
        """
        self.config: ConfigManager = config
        self.operation_type: str = operation_type
        self.parameters: dict = {}
        self._allowed_operation_types: Final[list[str]] = ["deposit", "withdraw"]
        self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(self.config).get_available_markets()

        if self.operation_type not in self._allowed_operation_types:
            error_message: str = (
                f'Operation type "{operation_type}" is not valid. '
                f'Valid types: {", ".join(self._allowed_operation_types)}.'
            )
            logging.error(error_message)
            raise ValueError(error_message)

        # Cache token addresses dictionary to avoid repeated lookups
        self.available_tokens: dict[ChecksumAddress, dict[str, Any]] = get_available_tokens(config=self.config)

        # Set required keys based on operation type
        self.required_keys: list[str] = self._set_required_keys()

        self.missing_base_key_methods: dict[str, Callable[[], None]] = {
            "long_token_symbol": self._handle_missing_long_token_symbol,
            "short_token_symbol": self._handle_missing_short_token_symbol,
            "long_token_address": self._handle_missing_long_token_address,
            "short_token_address": self._handle_missing_short_token_address,
            "long_token_amount": self._handle_missing_long_token_amount,
            "short_token_amount": self._handle_missing_short_token_amount,
            "out_token_address": self._handle_missing_out_token_address,
            "market_address": self._handle_missing_market_address,
            "rp_amount": self._handle_missing_rp_amount,  # Added handler for rp_amount
        }

    def process_parameters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """
        Process and validate the input parameters, ensuring all required keys are present.
        If a key is missing, the corresponding handler is called to resolve it.

        :param parameters: Dictionary containing the necessary parameters.
        :return: A fully populated and validated parameters' dictionary.
        :raises Exception: If critical data is missing or validation fails.
        """
        self.parameters: dict[str, Any] = parameters
        missing_keys: list[str] = self._determine_missing_keys(parameters)

        for missing_key in missing_keys:
            if missing_key in self.missing_base_key_methods:
                self.missing_base_key_methods[missing_key]()

        if self.operation_type == "withdraw":
            # Convert rp_amount from Decimal to integer representation (e.g., wei)
            rp_amount_decimal: Decimal = to_decimal(self.parameters.get("rp_amount", "0"))
            scaling_factor_rp = Decimal("1e18")
            try:
                rp_amount_scaled: Decimal = rp_amount_decimal * scaling_factor_rp
                rp_amount_integral: Decimal = rp_amount_scaled.to_integral_exact()
            except InvalidOperation as e:
                logging.error(f"Invalid rp_amount scaling: {e}")
                raise ValueError(f"Invalid rp_amount scaling: {e}")

            self.parameters["rp_amount"] = int(rp_amount_integral)
            logging.debug(f"Scaled rp_amount: {self.parameters['rp_amount']}")

        return self.parameters

    def _set_required_keys(self) -> list[str]:
        """
        Set the list of required keys based on the operation type (deposit or withdrawal).

        :return: A list of required keys for the specified operation.
        """
        operation_required_keys = {
            "deposit": [
                "long_token_symbol",
                "short_token_symbol",
                "long_token_address",
                "short_token_address",
                "long_token_amount",
                "short_token_amount",
                "market_address",
            ],
            "withdraw": [
                "long_token_symbol",
                "short_token_symbol",
                "long_token_address",
                "short_token_address",
                "market_address",
                "out_token_address",
                "rp_amount",
            ],
        }
        return operation_required_keys.get(self.operation_type, [])

    def _determine_missing_keys(self, parameters: dict[str, Any]) -> list[str]:
        """
        Compare the provided parameters against the required keys for the operation.

        :param parameters: Dictionary of user-supplied parameters.
        :return: A list of missing keys.
        """
        return [key for key in self.required_keys if key not in parameters]

    def _handle_missing_index_token_address(self) -> None:
        """
        Handle missing index token address by attempting to find it via the market token symbol.

        :raises ValueError: If the market token address and symbol are not provided.
        """
        # Retrieve market token symbol from parameters
        selected_market: str | None = self.parameters.get("selected_market")
        if not selected_market:
            logging.error("Selected market not provided in parameters.")
            raise ValueError("Selected market is not provided in parameters.")

        self.parameters["market_token_address"] = self._find_token_address_by_token_symbol(
            input_dict=self.available_tokens, token_symbol=selected_market
        )

    def _handle_missing_market_address(self) -> None:
        """
        Handle missing market address by using the index token address.

        :raises ValueError: If the market token address and symbol are not provided.
        """
        self._handle_missing_index_token_address()
        for market_metadata in self._available_markets.values():
            if (
                market_metadata["long_token_address"] == self.parameters["long_token_address"]
                and market_metadata["short_token_address"] == self.parameters["short_token_address"]
                and market_metadata["market_symbol"] == self.parameters["selected_market"]
            ) or (
                market_metadata["short_token_address"] == self.parameters["short_token_address"]
                and market_metadata["long_token_address"] == self.parameters["long_token_address"]
                and market_metadata["market_symbol"] == self.parameters["selected_market"]
            ):
                self.parameters["market_address"] = market_metadata["rfx_market_address"]
                logging.info(
                    f"Market address set to {self.parameters['market_address']} for market "
                    f"'{self.parameters['selected_market']}'."
                )
                return

        logging.error(
            f"Market address could not be determined for the provided tokens and market symbol "
            f"'{self.parameters['selected_market']}'."
        )
        raise ValueError(
            f"Market address could not be determined for the provided tokens and market symbol "
            f"'{self.parameters['selected_market']}'."
        )

    def _handle_missing_token_address(self, token_type: str) -> None:
        """
        General handler for missing token addresses (long/short).

        :param token_type: Either 'long' or 'short' indicating the token type.
        :raises ValueError: If the token symbol is not provided or the token address cannot be found.
        """
        token_symbol: str | None = self.parameters.get(f"{token_type}_token_symbol")
        if not token_symbol:
            logging.error(f"{token_type.capitalize()} token symbol is not provided in parameters.")
            raise ValueError(f"{token_type.capitalize()} token symbol is not provided.")

        try:
            self.parameters[f"{token_type}_token_address"] = self._find_token_address_by_token_symbol(
                input_dict=self.available_tokens, token_symbol=token_symbol
            )
            logging.info(
                f"{token_type.capitalize()} token address set to {self.parameters[f'{token_type}_token_address']}."
            )
        except ValueError as e:
            logging.error(f"Error finding {token_type} token address: {e}")
            raise

    def _handle_missing_long_token_symbol(self) -> None:
        """
        Handle missing long token symbol.
        """
        selected_market: str | None = self.parameters.get("selected_market")
        if not selected_market:
            logging.error("Selected market not provided for inferring long token symbol.")
            raise ValueError("Selected market not provided for inferring long token symbol.")

        try:
            # Assuming the market symbol format allows splitting to get token symbols
            # Example market symbol: "BTC-ETH Market [LONG-ETH]"
            # Adjust the splitting logic based on actual market symbol format
            market_parts = selected_market.split(" ")
            token_symbols = market_parts[1].split("-")
            self.parameters["long_token_symbol"] = token_symbols[0].replace("[", "").replace("]", "")
            logging.info(f"Long token symbol inferred as {self.parameters['long_token_symbol']}.")
        except (IndexError, AttributeError) as e:
            logging.error(f"Error inferring long token symbol from selected market '{selected_market}': {e}")
            raise ValueError(f"Error inferring long token symbol from selected market '{selected_market}': {e}")

    def _handle_missing_short_token_symbol(self) -> None:
        """
        Handle missing short token symbol.
        """
        selected_market: str | None = self.parameters.get("selected_market")
        if not selected_market:
            logging.error("Selected market not provided for inferring short token symbol.")
            raise ValueError("Selected market not provided for inferring short token symbol.")

        try:
            # Assuming the market symbol format allows splitting to get token symbols
            # Example market symbol: "BTC-ETH Market [LONG-ETH]"
            # Adjust the splitting logic based on actual market symbol format
            market_parts = selected_market.split(" ")
            token_symbols = market_parts[1].split("-")
            self.parameters["short_token_symbol"] = token_symbols[1].replace("[", "").replace("]", "")
            logging.info(f"Short token symbol inferred as {self.parameters['short_token_symbol']}.")
        except (IndexError, AttributeError) as e:
            logging.error(f"Error inferring short token symbol from selected market '{selected_market}': {e}")
            raise ValueError(f"Error inferring short token symbol from selected market '{selected_market}': {e}")

    def _handle_missing_long_token_address(self) -> None:
        """
        Handle missing long token address by searching with the token symbol.
        """
        self._handle_missing_token_address(token_type="long")

    def _handle_missing_short_token_address(self) -> None:
        """
        Handle missing short token address by searching with the token symbol.
        """
        self._handle_missing_token_address(token_type="short")

    def _handle_missing_out_token_address(self) -> None:
        """
        Handle missing out token address by searching with the token symbol.

        :raises ValueError: If the out token address or symbol is not provided.
        """
        # Get out token symbol, raise an error if not provided
        out_token_symbol: str | None = self.parameters.get("out_token_symbol")
        if not out_token_symbol:
            logging.error("Out token symbol is not provided.")
            raise ValueError("Out token symbol is not provided.")

        try:
            out_token_address: ChecksumAddress = self._find_token_address_by_token_symbol(
                input_dict=self.available_tokens, token_symbol=out_token_symbol
            )
        except ValueError as e:
            logging.error(f"Error finding out token address: {e}")
            raise

        market_metadata: dict[str, Any] = self._available_markets.get(self.parameters.get("market_address"))
        if not market_metadata:
            logging.error(f"Market metadata not found for market address: {self.parameters.get('market_address')}")
            raise ValueError(f"Market metadata not found for market address: {self.parameters.get('market_address')}")

        if out_token_address not in [market_metadata["long_token_address"], market_metadata["short_token_address"]]:
            logging.error(
                f"Out token '{out_token_address}' must be either "
                f"the long '{market_metadata['long_token_address']}' or "
                f"short '{market_metadata['short_token_address']}' token of the market."
            )
            raise ValueError(
                f"Out token '{out_token_address}' must be either "
                f"the long '{market_metadata['long_token_address']}' or "
                f"short '{market_metadata['short_token_address']}' token of the market."
            )
        else:
            self.parameters["out_token_address"] = out_token_address
            logging.info(f"Out token address set to {self.parameters['out_token_address']}.")

    def _handle_missing_token_amount(self, token_type: str, usd_key: str) -> None:
        """
        Generic handler for missing long or short token amounts.

        :param token_type: Either 'long' or 'short' indicating the token type.
        :param usd_key: The key for USD value in the parameters.
        :raises ValueError: If price data is missing or invalid.
        """
        token_address: ChecksumAddress | None = self.parameters.get(f"{token_type}_token_address")
        if not token_address:
            self.parameters[f"{token_type}_token_amount"] = 0
            logging.info(f"No {token_type} token address provided. Setting {token_type}_token_amount to 0.")
            return

        try:
            prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
            price_data: dict | None = prices.get(token_address)

            if not price_data:
                logging.error(f"Price data not found for {token_type} token address: {token_address}")
                raise ValueError(f"Price data not found for {token_type} token address: {token_address}")

            # Calculate median price using Decimal
            max_price_full = Decimal(price_data["maxPriceFull"])
            min_price_full = Decimal(price_data["minPriceFull"])
            price: Decimal = (max_price_full + min_price_full) / Decimal("2")

            # Calculate adjusted price
            decimal_places: int = self.available_tokens.get(token_address).get("decimals")
            oracle_factor: int = decimal_places - PRECISION
            scaling_factor: Decimal = Decimal(10) ** oracle_factor
            adjusted_price: Decimal = price * scaling_factor

            # Get token USD amount
            token_usd: Decimal = to_decimal(self.parameters.get(usd_key, "0"))

            # Calculate token amount
            token_amount_decimal: Decimal = (token_usd / adjusted_price) * (Decimal(10) ** decimal_places)
            token_amount_integral: Decimal = token_amount_decimal.to_integral_exact()

            self.parameters[f"{token_type}_token_amount"] = int(token_amount_integral)
            logging.debug(f"Scaled {token_type}_token_amount: {self.parameters[f'{token_type}_token_amount']}")
        except (KeyError, InvalidOperation, ZeroDivisionError) as e:
            logging.error(f"Error calculating {token_type} token amount: {e}")
            raise ValueError(f"Error calculating {token_type} token amount: {e}")

    def _handle_missing_long_token_amount(self) -> None:
        """
        Handle missing long token amount by calculating it based on the USD value.

        :raises ValueError: If the long token address is not provided.
        """
        self._handle_missing_token_amount(token_type="long", usd_key="long_token_usd")

    def _handle_missing_short_token_amount(self) -> None:
        """
        Handle missing short token amount by calculating it based on the USD value.

        :raises ValueError: If the short token address is not provided or price data is missing.
        """
        self._handle_missing_token_amount(token_type="short", usd_key="short_token_usd")

    def _handle_missing_rp_amount(self) -> None:
        """
        Handle missing 'rp_amount' by setting it to zero.

        :return: None
        """
        self.parameters["rp_amount"] = Decimal("0")
        logging.info("rp_amount not provided. Setting rp_amount to 0.")

    @staticmethod
    def _find_token_address_by_token_symbol(
        input_dict: dict[ChecksumAddress, dict[str, Any]], token_symbol: str
    ) -> ChecksumAddress:
        """
        Find the token contract address by its symbol.

        :param input_dict: Dictionary containing token information.
        :param token_symbol: The token symbol to search for.
        :return: The contract checksum address of the token.
        :raises ValueError: If the token symbol is not found.
        """
        address: ChecksumAddress | None = next(
            (k for k, v in input_dict.items() if v.get("symbol") == token_symbol), None
        )

        if address:
            logging.info(f"Token address found for symbol '{token_symbol}': {address}")
            return address
        else:
            # Attempt to standardize common token symbols
            standardized_symbol = token_symbol.split(" ")[0].split("/")[0]
            if standardized_symbol == "BTC":
                standardized_symbol = "WBTC"
            if standardized_symbol == "ETH":
                standardized_symbol = "WETH"
            address = next((k for k, v in input_dict.items() if v.get("symbol") == standardized_symbol), None)

        if not address:
            logging.error(f'"{token_symbol}" is not a known token!')
            raise ValueError(f'"{token_symbol}" is not a known token!')

        logging.info(f"Token address found for standardized symbol '{standardized_symbol}': {address}")
        return address

    @staticmethod
    def find_market_by_address(markets: dict[ChecksumAddress, dict[str, Any]], token_address: ChecksumAddress) -> str:
        """
        Find the market key by index token address.

        :param markets: Dictionary containing market information.
        :param token_address: The index token checksum address to search for.
        :return: The market key corresponding to the index token, or raises ValueError if not found.
        """
        market: str | None = next(
            (key for key, value in markets.items() if value.get("index_token_address") == token_address), None
        )

        if not market:
            logging.error(f"Market address was not found for token address: {token_address}")
            raise ValueError(f"Market address was not found for token address: {token_address}")

        logging.info(f"Market found for token address '{token_address}': {market}")
        return market
