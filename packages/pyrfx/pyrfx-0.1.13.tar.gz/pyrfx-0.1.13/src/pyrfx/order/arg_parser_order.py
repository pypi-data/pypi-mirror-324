import logging
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Final

from eth_typing import ChecksumAddress

from pyrfx.config_manager import ConfigManager
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.get.pool_tvl import PoolTVL
from pyrfx.order.swap_router import SwapRouter
from pyrfx.utils import PRECISION, get_available_tokens, to_decimal


class OrderArgumentParser:
    """
    A parser to handle and process order arguments for increase, decrease, or swap operations on the RFX Exchange.

    This class processes user-supplied order parameters, ensures all required parameters are present,
    fills in missing parameters where possible, and raises exceptions for critical missing data.

    :param config: Configuration object containing network details.
    :param operation_type: The type of operation ('increase', 'decrease', 'swap', 'limit_cancel', 'limit_increase',
        'limit_ioc').
    """

    def __init__(self, config: ConfigManager, operation_type: str) -> None:
        """
        Initializes the OrderArgumentParser class with the necessary configuration and operation type.

        :param config: Configuration object containing chain and market settings.
        :param operation_type: Specifies the type of operation ('increase', 'decrease', 'swap', 'limit_cancel',
            'limit_increase', 'limit_ioc').
        :raises ValueError: If an unknown operation type is provided.
        """
        self.config: ConfigManager = config
        self.parameters: dict = {}
        self.operation_type: str = operation_type
        self._allowed_operation_types: Final[list[str]] = [
            "increase",
            "decrease",
            "swap",
            "limit_cancel",
            "limit_increase",
            "limit_ioc",
        ]
        if operation_type not in self._allowed_operation_types:
            error_message: str = (
                f'Operation type "{operation_type}" is not valid. '
                f'Valid types: {", ".join(self._allowed_operation_types)}.'
            )
            logging.error(error_message)
            raise ValueError(error_message)

        # Set required keys based on operation type
        self.required_keys: list[str] = self._set_required_keys()

        self._available_markets: dict[str, dict[str, Any]] | None = None

        self.missing_base_key_methods: dict[str, Callable[[], None]] = {
            "collateral_address": self._handle_missing_collateral_address,
            "index_token_address": self._handle_missing_index_token_address,
            "initial_collateral_delta": self._handle_missing_initial_collateral_delta,
            "position_type": self._handle_missing_position_type,
            "leverage": self._handle_missing_leverage,
            "market_address": self._handle_missing_market_address,
            "out_token_address": self._handle_missing_out_token_address,
            "slippage_percent": self._handle_missing_slippage_percent,
            "start_token_address": self._handle_missing_start_token_address,
            "swap_path": self._handle_missing_swap_path,
            "cancel_time": self._handle_missing_cancel_time,
        }

    def process_parameters(self, parameters: dict) -> dict[str, Any]:
        """
        Processes the input dictionary and fills in missing keys if possible. Raises exceptions if
        critical data is missing.

        The method:
        - Identifies missing keys in the supplied parameters.
        - Fills in missing data like `swap_path`, `collateral_address`, etc.
        - Validates parameters, including position size and maximum leverage limits for non-swap operations.

        :param parameters: Dictionary containing order parameters.
        :return: Processed dictionary with missing keys filled in.
        :raises Exception: If critical data is missing or validation fails.
        """
        self.parameters: dict[str, Any] = parameters
        missing_keys: list[str] = self._determine_missing_keys()

        for missing_key in missing_keys:
            if missing_key in self.missing_base_key_methods:
                self.missing_base_key_methods[missing_key]()

        if self.operation_type == "swap":
            self.calculate_missing_position_size_info_keys()
            self._check_if_max_leverage_exceeded()

        if self.operation_type == "increase":
            # Define collateral threshold as Decimal
            collateral_threshold = Decimal("2")
            # Calculate initial_collateral_usd as Decimal
            initial_collateral_usd: Decimal = self._calculate_initial_collateral_usd()
            if initial_collateral_usd < collateral_threshold:
                raise Exception("Position size must be backed by >= $2 of collateral!")

        self._format_size_info()
        return self.parameters

    def _set_required_keys(self) -> list[str]:
        """
        Set the list of required keys based on the operation type (increase, decrease, swap, limit_increase,
        limit_decrease, limit_ioc).

        :return: A list of required keys for the specified operation.
        """
        operation_required_keys = {
            "increase": [
                "index_token_address",
                "market_address",
                "start_token_address",
                "collateral_address",
                "swap_path",
                "position_type",
                "size_delta_usd",
                "initial_collateral_delta",
                "slippage_percent",
                "leverage",
            ],
            "decrease": [
                "index_token_address",
                "market_address",
                "start_token_address",
                "collateral_address",
                "position_type",
                "size_delta_usd",
                "initial_collateral_delta",
                "slippage_percent",
                "leverage",
            ],
            "swap": [
                "start_token_address",
                "out_token_address",
                "initial_collateral_delta",
                "swap_path",
                "slippage_percent",
                "leverage",
            ],
            "limit_cancel": [],
            "limit_increase": [
                "index_token_address",
                "market_address",
                "start_token_address",
                "collateral_address",
                "size_delta_usd",
                "initial_collateral_delta",
                "trigger_price",
                "slippage_percent",
            ],
            "limit_ioc": [
                "index_token_address",
                "market_address",
                "start_token_address",
                "collateral_address",
                "size_delta_usd",
                "initial_collateral_delta",
                "trigger_price",
                "slippage_percent",
                "cancel_time",
            ],
        }
        return operation_required_keys.get(self.operation_type, [])

    def _determine_missing_keys(self) -> list[str]:
        """
        Compare the supplied dictionary keys with the required keys for creating an order.

        :return: A list of missing keys.
        """
        return [key for key in self.required_keys if key not in self.parameters]

    def _handle_missing_index_token_address(self) -> None:
        """
        Handles missing 'index_token_address'. Attempts to infer the address from the token symbol.
        Raises an exception if neither index token address nor symbol is provided.

        :raises Exception: If neither index token address nor symbol is provided.
        :return: None.
        """
        selected_market: str | None = self.parameters.get("selected_market")

        if not selected_market:
            logging.error("'selected_market' does not exist in parameters!")
            raise Exception("'selected_market' does not exist in parameters!")

        # Retrieve the token address by symbol
        self.parameters["index_token_address"] = self._find_token_address_by_token_symbol(
            input_dict=get_available_tokens(config=self.config), token_symbol=selected_market
        )

    def _handle_missing_market_address(self) -> None:
        """
        Handles the case where the 'market_address' is missing. Attempts to infer the market address based on the
        provided 'index_token_address'. Handles specific known exceptions for certain token addresses.
        Raises a ValueError if the 'index_token_address' is missing or if no market address can be inferred.

        :raises ValueError: If the 'index_token_address' is missing or cannot infer the market key.
        """
        if not self.parameters.get("selected_market"):
            logging.error("Selected market is missing.")
            raise ValueError("Selected market is missing.")

        # Attempt to find the market key from available markets using the index token address
        self.parameters["market_address"] = self._find_market_address(
            selected_market=self.parameters["selected_market"]
        )

    def _find_market_address(self, selected_market: str) -> str:
        """
        Finds the market address for the given index token address.

        :param selected_market: Selected market.
        :return: The market key corresponding to the index token address.
        :raises ValueError: If the index token address is not found.
        """
        if not self._available_markets:
            self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(
                self.config
            ).get_available_markets()

        market_address: ChecksumAddress | None = None
        for rfx_market_address, market_info in self._available_markets.items():
            if market_info["market_symbol"] == selected_market:
                market_address = rfx_market_address
                break

        if market_address:
            logging.info(f"Market address found {market_address} for market '{selected_market}'.")
            return market_address

        e_msg: str = f"Market address was not found for market: '{selected_market}'."
        logging.error(e_msg)
        raise ValueError(e_msg)

    def _handle_missing_token_address(self, token_type: str, token_symbol_key: str, address_key: str) -> None:
        """
        General handler for missing token addresses. Infers the address from the token symbol.

        :param token_type: A string describing the type of token (e.g., 'start', 'out', 'collateral').
        :param token_symbol_key: The token symbol key in the parameters.
        :param address_key: The key to be retrieved and stored in the parameters.
        :raises ValueError: If the token symbol or address is not provided or cannot be inferred.
        """
        token_symbol: str | None = self.parameters.get(token_symbol_key)
        if not token_symbol:
            logging.error(f"{token_type.capitalize()} Token Address and Symbol not provided!")
            raise ValueError(f"{token_type.capitalize()} Token Address and Symbol not provided!")

        # Infer the token address from the symbol
        self.parameters[address_key] = self._find_token_address_by_token_symbol(
            input_dict=get_available_tokens(config=self.config), token_symbol=token_symbol
        )

    def _handle_missing_start_token_address(self) -> None:
        """
        Handles missing 'start_token_address'. Infers the address from the token symbol.
        """
        self._handle_missing_token_address(
            token_type="start", token_symbol_key="start_token_symbol", address_key="start_token_address"
        )

    def _handle_missing_out_token_address(self) -> None:
        """
        Handles missing 'out_token_address'. Infers the address from the token symbol.
        """
        self._handle_missing_token_address(
            token_type="out", token_symbol_key="out_token_symbol", address_key="out_token_address"
        )

    def _handle_missing_collateral_address(self) -> None:
        """
        Handles missing 'collateral_address'. Infers the address from the collateral token symbol.

        Validates whether the collateral can be used in the requested market.
        """
        self._handle_missing_token_address(
            token_type="collateral", token_symbol_key="collateral_token_symbol", address_key="collateral_address"
        )

        # Validate collateral usage
        collateral_address = self.parameters["collateral_address"]
        if self._check_if_valid_collateral_for_market(collateral_address) and self.operation_type != "swap":
            self.parameters["collateral_address"] = collateral_address

    @staticmethod
    def _find_token_address_by_token_symbol(
        input_dict: dict[ChecksumAddress, dict[str, Any]], token_symbol: str
    ) -> ChecksumAddress:
        """
        Finds the token address in the input dictionary that matches the given token symbol.

        :param input_dict: Dictionary containing token information.
        :param token_symbol: The symbol of the token to search for.
        :return: The token address corresponding to the token symbol.
        :raises ValueError: If the token symbol is not found in the input dictionary.
        """
        address: ChecksumAddress | None = next(
            (k for k, v in input_dict.items() if v.get("symbol") == token_symbol), None
        )

        if address:
            return address
        else:
            # Attempt to standardize common token symbols
            token_symbol = token_symbol.split(" ")[0].split("/")[0]
            if token_symbol == "BTC":
                token_symbol = "WBTC"
            if token_symbol == "ETH":
                token_symbol = "WETH"
            address = next((k for k, v in input_dict.items() if v.get("symbol") == token_symbol), None)

        if not address:
            logging.error(f'"{token_symbol}" is not a known token!')
            raise ValueError(f'"{token_symbol}" is not a known token!')

        return address

    def _handle_missing_swap_path(self) -> None:
        """
        Handles missing 'swap_path'. Determines the appropriate swap route based on the operation type
        and the relationship between the start, out, and collateral tokens.

        - If the operation is a token swap, the swap path is calculated between start and out tokens.
        - If the start token matches the collateral token, no swap path is needed.
        - Otherwise, the swap path is determined between the start token and collateral.

        :raises ValueError: If required tokens are missing and cannot determine the swap route.
        :return: None
        """
        start_address: ChecksumAddress | None = self.config.to_checksum_address(
            address=self.parameters.get("start_token_address")
        )
        if not start_address:
            logging.error("Start token address is missing!")
            raise ValueError("Start token address is missing!")

        if self.operation_type == "swap":
            out_address: ChecksumAddress | None = self.config.to_checksum_address(
                address=self.parameters.get("out_token_address")
            )
            if not out_address:
                raise ValueError("Out token address is missing!")

            self.parameters["swap_path"] = self._determine_swap_path(
                start_address=start_address, end_address=out_address
            )
        else:
            collateral_address: ChecksumAddress | None = self.config.to_checksum_address(
                self.parameters.get("collateral_address")
            )
            if not collateral_address:
                logging.error("Collateral address is missing!")
                raise ValueError("Collateral address is missing!")

            if start_address == collateral_address:
                self.parameters["swap_path"] = []
            else:
                self.parameters["swap_path"] = self._determine_swap_path(
                    start_address=start_address, end_address=collateral_address
                )

    def _handle_missing_cancel_time(self) -> None:
        """
        Handles missing 'cancel_time'.

        :return: None
        """
        self.parameters["cancel_time"] = 10

    def _determine_swap_path(self, start_address: ChecksumAddress, end_address: ChecksumAddress) -> list:
        """
        Determines the swap path between two token addresses using available markets.

        :param start_address: Address of the start token.
        :param end_address: Address of the end token.
        :return: The swap path as a list.
        """
        if not self._available_markets:
            self._available_markets = Markets(self.config).get_available_markets()

        pool_tvl: dict[str, dict[str, Any]] = PoolTVL(config=self.config).get_pool_balances()
        swap_router: SwapRouter = SwapRouter(config=self.config, pool_tvl=pool_tvl)
        swap_route: list[ChecksumAddress] = swap_router.determine_swap_route(
            available_markets=self._available_markets,
            in_token_address=start_address,
            out_token_address=end_address,
        )
        return swap_route

    def _handle_missing_parameter(self, param_name: str, message: str) -> None:
        """
        General handler for missing parameters.

        :param param_name: The name of the missing parameter.
        :param message: The error message to display when the parameter is missing.
        :raises ValueError: Always raises a ValueError with the provided message.
        :return: None
        """
        raise ValueError(f"Missing parameter: {param_name}. {message}")

    def _handle_missing_position_type(self) -> None:
        """
        Handles the case where 'position_type' is missing from the parameter's dictionary.

        :raises ValueError: If 'position_type' is not provided, which indicates whether the position is long or short.
        :return: None
        """
        self._handle_missing_parameter(
            param_name="position_type",
            message=(
                "Please indicate if the position is "
                "long ('position_type': 'long') or "
                "short ('position_type': 'short')."
            ),
        )

    def _handle_missing_leverage(self) -> None:
        """
        Handles the case where 'leverage' is missing from the parameter's dictionary.

        :return: None
        """
        if self.operation_type in ["swap", "decrease"]:
            self.parameters["leverage"] = Decimal("1")
        elif self.operation_type == "increase":
            if not self.parameters.get("leverage"):
                logging.warning("Using default leverage 1!")
                self.parameters["leverage"] = Decimal("1")
        else:
            logging.error("Leverage parameter is missing!")
            raise ValueError("Leverage parameter is missing!")

    def _handle_missing_slippage_percent(self) -> None:
        """
        Handles the case where 'slippage_percent' is missing from the parameter's dictionary.

        :raises ValueError: If 'slippage_percent' is not provided, which is the percentage of acceptable slippage.
        :return: None
        """
        self._handle_missing_parameter(
            param_name="slippage_percent", message="Please provide the slippage percentage ('slippage_percent')."
        )

    def _handle_missing_initial_collateral_delta(self) -> None:
        """
        Handles the case where 'initial_collateral_delta' is missing from the parameter's dictionary.

        :return: None
        """
        if "size_delta_usd" in self.parameters and "leverage" in self.parameters:
            size_delta_usd: Decimal = to_decimal(self.parameters["size_delta_usd"])
            leverage: Decimal = to_decimal(self.parameters["leverage"])
            collateral_usd: Decimal = size_delta_usd / leverage
            self.parameters["initial_collateral_delta"] = self._calculate_initial_collateral_tokens(collateral_usd)

    def _check_if_valid_collateral_for_market(self, collateral_address: str) -> bool:
        """
        Checks if the provided collateral address is valid for the requested market.

        :param collateral_address: The address of the collateral token.
        :return: True if valid collateral, otherwise raises a ValueError.
        """
        market_address: ChecksumAddress | None = self.parameters.get("market_address")

        # Fetch the market information
        if not self._available_markets:
            self._available_markets = Markets(self.config).get_available_markets()
        market: dict | None = self._available_markets.get(market_address)

        if market and (
            collateral_address == market.get("long_token_address")
            or collateral_address == market.get("short_token_address")
        ):
            return True

        logging.error(f"Collateral {collateral_address} is not valid for the selected market.")
        raise ValueError(f"Collateral {collateral_address} is not valid for the selected market.")

    @staticmethod
    def find_key_by_symbol(input_dict: dict, search_symbol: str) -> str:
        """
        Finds the key (token address) in the input_dict that matches the provided symbol.

        :param input_dict: Dictionary of tokens with token symbols as values.
        :param search_symbol: The token symbol to search for.
        :return: The token address corresponding to the symbol.
        :raises ValueError: If the token symbol is not found.
        """
        key: str | None = next((key for key, value in input_dict.items() if value.get("symbol") == search_symbol), None)

        if key is None:
            logging.error(f'"{search_symbol}" not recognized as a valid token.')
            raise ValueError(f'"{search_symbol}" not recognized as a valid token.')

        return key

    def calculate_missing_position_size_info_keys(self) -> dict:
        """
        Calculates missing size-related parameters (e.g., size_delta_usd, initial_collateral_delta)
        if possible. Raises a ValueError if required parameters are missing.

        :raises ValueError: If the required parameters `size_delta_usd`, `initial_collateral_delta`, or `leverage`
            are missing, making the calculations impossible.
        :return: The updated parameters dictionary with `size_delta_usd` and `initial_collateral_delta` filled in, if
            calculated.
        """
        if "size_delta_usd" in self.parameters and "initial_collateral_delta" in self.parameters:
            return self.parameters

        if "leverage" in self.parameters and "initial_collateral_delta" in self.parameters:
            # Convert leverage to Decimal
            leverage: Decimal = to_decimal(self.parameters["leverage"])
            # Calculate initial_collateral_usd as Decimal
            initial_collateral_usd: Decimal = self._calculate_initial_collateral_usd()
            # Calculate size_delta_usd as leverage * initial_collateral_usd
            size_delta_usd: Decimal = leverage * initial_collateral_usd
            self.parameters["size_delta_usd"] = size_delta_usd
            return self.parameters

        if "size_delta_usd" in self.parameters and "leverage" in self.parameters:
            # Convert leverage and size_delta_usd to Decimal
            leverage: Decimal = to_decimal(self.parameters["leverage"])
            size_delta_usd: Decimal = to_decimal(self.parameters["size_delta_usd"])
            # Calculate collateral_usd as size_delta_usd / leverage
            collateral_usd: Decimal = size_delta_usd / leverage
            # Calculate initial_collateral_delta using Decimal
            initial_collateral_delta: Decimal = self._calculate_initial_collateral_tokens(collateral_usd)
            self.parameters["initial_collateral_delta"] = initial_collateral_delta
            return self.parameters

        logging.error('Missing required keys: "size_delta_usd", "initial_collateral_delta", or "leverage".')
        raise ValueError('Missing required keys: "size_delta_usd", "initial_collateral_delta", or "leverage".')

    def _calculate_initial_collateral_usd(self) -> Decimal:
        """
        Calculates the USD value of the collateral from the initial collateral delta.

        :return: The USD value of the initial collateral as a Decimal.
        :raises ValueError: If price data is invalid or scaling results in precision loss.
        """
        # Convert collateral_amount to Decimal
        collateral_amount: Decimal = to_decimal(self.parameters["initial_collateral_delta"])

        # Retrieve recent prices
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        token_address: ChecksumAddress = self.parameters["start_token_address"]

        try:
            # Calculate median price as Decimal
            max_price_full = Decimal(prices[token_address]["maxPriceFull"])
            min_price_full = Decimal(prices[token_address]["minPriceFull"])
            price: Decimal = (max_price_full + min_price_full) / 2

            # Calculate oracle_factor
            token_decimals: int = get_available_tokens(config=self.config)[token_address]["decimals"]
            oracle_factor: int = token_decimals - PRECISION

            # Calculate USD value
            scaling_factor = Decimal(10) ** oracle_factor
            collateral_usd: Decimal = price * scaling_factor * collateral_amount

            return collateral_usd

        except (KeyError, InvalidOperation) as e:
            logging.error(f"Error calculating initial collateral USD: {e}")
            raise ValueError(f"Error calculating initial collateral USD: {e}")

    def _calculate_initial_collateral_tokens(self, collateral_usd: Decimal) -> Decimal:
        """
        Calculates the amount of tokens based on the collateral's USD value.

        :param collateral_usd: The dollar value of the collateral as a Decimal.
        :return: The amount of tokens equivalent to the collateral value as a Decimal.
        :raises ValueError: If price data is invalid or scaling results in precision loss.
        """
        try:
            # Retrieve recent prices
            prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
            token_address: ChecksumAddress = self.parameters["start_token_address"]

            # Calculate median price as Decimal
            max_price_full = Decimal(prices[token_address]["maxPriceFull"])
            min_price_full = Decimal(prices[token_address]["minPriceFull"])
            price: Decimal = (max_price_full + min_price_full) / 2

            # Calculate oracle_factor
            oracle_factor: int = get_available_tokens(config=self.config)[token_address]["decimals"] - PRECISION

            # Calculate token amount
            token_amount: Decimal = collateral_usd / (price * Decimal("10") ** oracle_factor)
            return token_amount

        except (KeyError, InvalidOperation, ZeroDivisionError) as e:
            logging.error(f"Error calculating initial collateral tokens: {e}")
            raise ValueError(f"Error calculating initial collateral tokens: {e}")


    def _format_size_info(self) -> None:
        """
        Formats size_delta and initial_collateral_delta to the correct precision for on-chain use.

        This method converts Decimal financial parameters to integers by scaling them
        according to the required precision. It ensures that the values are accurately represented
        without precision loss, which is essential for blockchain transactions and smart contract interactions.

        Raises:
            ValueError: If the scaled value contains a fractional component, indicating a precision mismatch.
        """
        # Format size_delta if the operation is not a swap
        if self.operation_type != "swap":
            # Convert size_delta_usd from float to Decimal for precise scaling
            size_delta_usd: Decimal = to_decimal(self.parameters["size_delta_usd"])
            # Scale the size_delta_usd
            size_delta_scaled: Decimal = size_delta_usd * Decimal(10) ** PRECISION

            try:
                # Ensure the scaled value is an integer (no fractional part)
                size_delta_scaled = size_delta_scaled.to_integral_exact()
            except InvalidOperation:
                # Raise an error if there is a fractional component
                logging.error(
                    f"Scaled size_delta_usd ({size_delta_usd}) * 10**{PRECISION} results in "
                    f"a non-integer value: {size_delta_scaled}"
                )
                raise ValueError(
                    f"Scaled size_delta_usd ({size_delta_usd}) * 10**{PRECISION} results in "
                    f"a non-integer value: {size_delta_scaled}"
                )

            # Convert the scaled Decimal to int for on-chain compatibility
            self.parameters["size_delta"] = int(size_delta_scaled)
            logging.debug(f"Scaled size_delta: {self.parameters['size_delta']}")

        # Retrieve the number of decimals for the start token to determine the scaling factor
        start_token_decimals: int = get_available_tokens(config=self.config)[self.parameters["start_token_address"]][
            "decimals"
        ]
        # Convert initial_collateral_delta from float to Decimal
        initial_collateral_delta: Decimal = to_decimal(self.parameters["initial_collateral_delta"])
        scaling_factor_collateral = Decimal(10) ** start_token_decimals
        # Scale the initial_collateral_delta
        initial_collateral_scaled: Decimal = initial_collateral_delta * scaling_factor_collateral

        try:
            # Ensure the scaled value is an integer (no fractional part)
            initial_collateral_scaled = initial_collateral_scaled.to_integral_exact()
        except InvalidOperation:
            # Raise an error if there is a fractional component
            logging.error(
                f"Scaled initial_collateral_delta ({initial_collateral_delta}) * 10**{start_token_decimals} results in "
                f"a non-integer value: {initial_collateral_scaled}"
            )
            raise ValueError(
                f"Scaled initial_collateral_delta ({initial_collateral_delta}) * 10**{start_token_decimals} results in "
                f"a non-integer value: {initial_collateral_scaled}"
            )

        # Convert to int for on-chain use
        self.parameters["initial_collateral_delta"] = int(initial_collateral_scaled)
        logging.debug(f"Scaled initial_collateral_delta: {self.parameters['initial_collateral_delta']}")

        # Format trigger_price for specific operation types
        if self.operation_type in ["limit_increase", "limit_ioc"]:
            # Convert trigger_price from float to Decimal
            trigger_price: Decimal = to_decimal(self.parameters["trigger_price"])
            # Retrieve the number of decimals for the index token
            index_token_decimals: int = get_available_tokens(config=self.config)[
                self.parameters["index_token_address"]
            ]["decimals"]
            # Define the scaling factor with additional precision (e.g., oraclePrecision = 8 and 4 decimals -> +4)
            scaling_factor_trigger: Decimal = Decimal(10) ** (PRECISION - index_token_decimals)
            # Scale the trigger_price
            trigger_price_scaled: Decimal = trigger_price * scaling_factor_trigger

            try:
                # Ensure the scaled value is an integer (no fractional part)
                trigger_price_scaled = trigger_price_scaled.to_integral_exact()
            except InvalidOperation:
                # Raise an error if there is a fractional component
                logging.error(
                    f"Scaled trigger_price ({trigger_price}) * 10**{PRECISION - index_token_decimals} results in "
                    f"a non-integer value: {trigger_price_scaled}"
                )
                raise ValueError(
                    f"Scaled trigger_price ({trigger_price}) * 10**{PRECISION - index_token_decimals} results in "
                    f"a non-integer value: {trigger_price_scaled}"
                )

            # Convert to int for on-chain use
            self.parameters["trigger_price"] = int(trigger_price_scaled)
            logging.debug(f"Scaled trigger_price: {self.parameters['trigger_price']}")

    def _check_if_max_leverage_exceeded(self):
        """
        Checks if the requested leverage exceeds the maximum allowed leverage.

        :raises ValueError: If the requested leverage exceeds the maximum limit.
        """
        # Calculate collateral_usd_value as Decimal
        collateral_usd_value: Decimal = self._calculate_initial_collateral_usd()
        size_delta_usd: Decimal = to_decimal(self.parameters["size_delta_usd"])

        # Calculate leverage_requested as Decimal
        leverage_requested: Decimal = size_delta_usd / collateral_usd_value

        # Define max_leverage as Decimal (replace with dynamic retrieval if available)
        # TODO: Example value, should be queried from the contract
        max_leverage: Decimal = Decimal("100.0")

        if leverage_requested > max_leverage:
            error_message: str = (
                f'Requested leverage "x{leverage_requested}" '
                f"exceeds the maximum allowed leverage of x{max_leverage}."
            )
            logging.error(error_message)
            raise ValueError(error_message)
