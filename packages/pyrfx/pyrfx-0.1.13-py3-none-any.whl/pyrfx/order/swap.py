import logging
from decimal import Decimal
from logging import Logger
from typing import Any

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_execution_fee, get_gas_limits
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.order.base_order import Order
from pyrfx.utils import DecreasePositionSwapTypes, OrderTypes, get_data_store_contract, get_estimated_swap_output


class SwapOrder(Order):
    """
    A class to handle opening a swap order.
    Extends the base Order class to manage swap logic between tokens in a given market.
    """

    def __init__(
        self,
        config: ConfigManager,
        start_token_address: ChecksumAddress,
        out_token_address: ChecksumAddress,
        market_address: ChecksumAddress,
        collateral_address: ChecksumAddress,
        index_token_address: ChecksumAddress,
        initial_collateral_delta: int,
        slippage_percent: float,
        swap_path: list[ChecksumAddress],
        size_delta: int = 0,
        is_long: bool = False,
        max_fee_per_gas: int | None = None,
        auto_cancel: bool = False,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the SwapOrder class, extending the base Order class.

        :param config: Configuration manager containing blockchain settings.
        :param start_token_address: Address of the token to swap from.
        :param out_token_address: Address of the token to swap to.
        :param market_address: The address representing the RFX market.
        :param collateral_address: The contract address of the collateral token.
        :param index_token_address: The contract address of the index token.
        :param initial_collateral_delta: The amount of initial collateral in the order.
        :param slippage_percent: Allowed slippage for the price in percentage.
        :param swap_path: List of contract addresses representing the swap path for token exchanges.
        :param size_delta: Change in position size for the order.
        :param is_long: Boolean indicating whether the order is long or short.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param auto_cancel: Boolean indicating whether the order should be auto-canceled if unfilled.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # Input validation for slippage_percent
        if not isinstance(slippage_percent, (float, int, str)):
            self.logger.error("slippage_percent must be a float, int, or string representing a number.")
            raise TypeError("slippage_percent must be a float, int, or string representing a number.")

        # Call parent class constructor
        super().__init__(
            config=config,
            market_address=market_address,
            collateral_address=collateral_address,
            index_token_address=index_token_address,
            is_long=is_long,
            size_delta=size_delta,
            initial_collateral_delta=initial_collateral_delta,
            slippage_percent=Decimal(str(slippage_percent)),
            order_type="swap",
            swap_path=swap_path,
            max_fee_per_gas=max_fee_per_gas,
            auto_cancel=auto_cancel,
            debug_mode=debug_mode,
            log_level=log_level,
        )

        # Set start and out token addresses
        self.start_token: ChecksumAddress = start_token_address
        self.out_token: ChecksumAddress = out_token_address

        # Determine gas limits
        self._determine_gas_limits()

    def _determine_gas_limits(self) -> None:
        """
        Determine the gas limits required for placing a swap order.

        This method queries the datastore contract to get the relevant gas limits and
        sets the gas limit for the swap operation.
        """
        try:
            # Retrieve the datastore contract
            datastore: Contract = get_data_store_contract(self.config)

            if not datastore:
                raise ValueError("Datastore contract was not found.")

            # Fetch the gas limits from the datastore
            self._gas_limits: dict[str, ContractFunction] = get_gas_limits(datastore)

            if not self._gas_limits:
                raise ValueError("Gas limits could not be retrieved.")

            # Retrieve the specific gas limit for the 'swap_order' operation
            self._gas_limits_order_type_contract_function: ContractFunction | None = self._gas_limits.get(
                "multiple_swap_order"
            )

            if not self._gas_limits_order_type_contract_function:
                raise KeyError("Gas limit for 'swap_order' not found.")

            if self.debug_mode:
                # Get the actual gas limit value by calling the contract function
                gas_limit_value: int = self._gas_limits_order_type_contract_function.call()
                self.logger.info(f"Gas limit for 'swap_order' is: {gas_limit_value}")

        except KeyError as e:
            self.logger.error(f"KeyError - Gas limit for 'swap_order' not found: {e}")
            raise Exception(f"Gas limit for 'swap_order' not found: {e}")

        except ValueError as e:
            self.logger.error(f"ValueError - Issue with datastore or gas limits: {e}")
            raise Exception(f"Error with datastore or gas limits: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error while determining gas limits: {e}")
            raise Exception(f"Unexpected error while determining gas limits: {e}")

    def _estimated_swap_output(
        self, market: dict[str, Any], in_token: ChecksumAddress, in_token_amount: Decimal
    ) -> dict[str, Decimal]:
        """
        Estimate the output of a token swap given a market and input token amount.

        :param market: Full market details containing token addresses and metadata.
        :param in_token: Contract address of the input token.
        :param in_token_amount: Amount of input token to swap.
        :return: A dictionary containing the estimated token output and price impact.
        """
        try:
            # Fetch recent prices from the Oracle
            prices: dict[str, dict[str, int]] = OraclePrices(config=self.config).get_recent_prices()

            # Prepare the swap estimation parameters
            swap_parameters: dict[str, Any] = self._prepare_swap_parameters(
                market=market, prices=prices, in_token_address=in_token, in_token_amount=in_token_amount
            )

            # Get estimated swap output
            estimated_output: dict[str, Decimal] = get_estimated_swap_output(config=self.config, params=swap_parameters)

            self.logger.info(f"Estimated swap output: {estimated_output}")
            return estimated_output

        except KeyError as e:
            self.logger.error(f"Missing data in swap output estimation parameters: {e}")
            return {"out_token_amount": Decimal("0"), "price_impact_usd": Decimal("0")}

        except Exception as e:
            self.logger.error(f"Unexpected error while estimating swap output: {e}")
            return {"out_token_amount": Decimal("0"), "price_impact_usd": Decimal("0")}

    def _prepare_swap_parameters(
        self,
        market: dict[str, Any],
        prices: dict[str, dict[str, int]],
        in_token_address: ChecksumAddress,
        in_token_amount: Decimal,
    ) -> dict[str, Any]:
        """
        Helper method to prepare the parameters for the swap estimation.

        :param market: Full market details containing token addresses and metadata.
        :param prices: Recent prices for tokens from the Oracle.
        :param in_token_address: The checksum address of the input token.
        :param in_token_amount: Amount of input token to swap.
        :return: A dictionary of parameters required for the swap estimation.
        """
        return {
            "data_store_address": self.config.contracts.data_store.contract_address,
            "market_addresses": [
                market["rfx_market_address"],
                market["index_token_address"],
                market["long_token_address"],
                market["short_token_address"],
            ],
            "token_prices_tuple": [
                [
                    int(prices[market["index_token_address"]]["maxPriceFull"]),
                    int(prices[market["index_token_address"]]["minPriceFull"]),
                ],
                [
                    int(prices[market["long_token_address"]]["maxPriceFull"]),
                    int(prices[market["long_token_address"]]["minPriceFull"]),
                ],
                [
                    int(prices[market["short_token_address"]]["maxPriceFull"]),
                    int(prices[market["short_token_address"]]["minPriceFull"]),
                ],
            ],
            "token_in": in_token_address,
            "token_amount_in": int(in_token_amount),
            "ui_fee_receiver": self.config.zero_address,
        }

    def create_and_execute(self) -> dict[str, HexBytes | None]:
        """
        Build and submit a swap order, ensuring correct gas limits, fees, and execution parameters are set.

        :return: The dictionary with transaction hash.
        :raises Exception: If the execution price falls outside the acceptable range for the swap order.
        """
        # Set execution fee
        execution_fee: Decimal = Decimal(
            get_execution_fee(
                gas_limits=self._gas_limits,
                estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                gas_price=self.config.connection.eth.gas_price,
            )
        )

        # Adjust execution fee for swap orders due to complexity
        execution_fee_multiplier: Decimal = Decimal("1.5")
        execution_fee = (execution_fee * execution_fee_multiplier).to_integral_value()  # Uses default rounding

        available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(config=self.config).get_available_markets()

        # Ensure wallet addresses are converted to checksum format
        collateral_address: ChecksumAddress = self.config.to_checksum_address(address=self.collateral_address)

        # Estimate the output token amount for the swap
        swap_order_type: str = "single_swap_order"
        estimated_output: dict[str, Decimal] = self._estimated_swap_output(
            market=available_markets[self.swap_path[0]],
            in_token=self.collateral_address,
            in_token_amount=self.initial_collateral_delta,
        )

        if len(self.swap_path) > 1:
            # Assuming the second swap is from USDC or another stablecoin to out_token
            # Adjust the in_token_amount based on slippage_percent
            slippage_multiplier: Decimal = Decimal("1") - (self.slippage_percent / Decimal("100"))
            adjusted_in_token_amount: Decimal = Decimal(estimated_output["out_token_amount"]) * slippage_multiplier
            estimated_output: dict[str, Decimal] = self._estimated_swap_output(
                market=available_markets[self.swap_path[1]],
                in_token=self.config.usdc_address,  # Assuming USDC is the intermediary
                in_token_amount=adjusted_in_token_amount,
            )
            swap_order_type = "multiple_swap_order"

        # Retrieve the appropriate gas limit contract function
        self._gas_limits_order_type_contract_function: ContractFunction = self._gas_limits.get(swap_order_type)
        if not self._gas_limits_order_type_contract_function:
            self.logger.error(f"Gas limit contract function for '{swap_order_type}' not found.")
            raise Exception(f"Gas limit contract function for '{swap_order_type}' not found.")

        # Calculate minimum output amount based on slippage_percent
        slippage_multiplier = Decimal("1") - self.slippage_percent
        min_output_amount: Decimal = Decimal(estimated_output["out_token_amount"]) * slippage_multiplier

        # Build the order arguments
        arguments: tuple = (
            (
                self.config.user_wallet_address,
                self.config.user_wallet_address,  # Cancellation receiver
                self.config.zero_address,
                self.config.zero_address,
                self.config.zero_address,  # RFX market address is not relevant for swap
                collateral_address,
                self.swap_path,
            ),
            (
                int(self.size_delta),
                int(self.initial_collateral_delta),
                0,  # Mark price
                0,  # Acceptable price
                int(execution_fee),  # Execution fee as int
                0,  # Callback gas limit
                int(min_output_amount),  # Minimum output amount
            ),
            OrderTypes.MARKET_SWAP.value,
            DecreasePositionSwapTypes.NO_SWAP.value,
            self.is_long,
            True,  # Should unwrap native token
            self.auto_cancel,
            HexBytes("0x" + "0" * 64),  # referral_code
        )

        tx_hashes: dict[str, HexBytes | None] = {}
        value_amount: Decimal = execution_fee
        if collateral_address == self.config.weth_address:
            # When collateral is WETH, send WETH and create order
            value_amount += self.initial_collateral_delta
            tx_hashes["send_wnt_hash"] = self._send_wnt(value_amount)
            tx_hashes["create_order_hash"] = self._create_order(arguments)
            multicall_args: list[HexBytes] = [tx_hashes["send_wnt_hash"], tx_hashes["create_order_hash"]]

        else:
            # When collateral is not WETH, send tokens, send WETH, and create order
            tx_hashes["send_wnt_hash"] = self._send_wnt(value_amount)
            tx_hashes["send_tokens_hash"] = self._send_tokens(self.collateral_address, self.initial_collateral_delta)
            tx_hashes["create_order_hash"] = self._create_order(arguments)
            multicall_args: list[HexBytes] = [
                tx_hashes["send_wnt_hash"],
                tx_hashes["send_tokens_hash"],
                tx_hashes["create_order_hash"],
            ]

        # Submit the transaction
        tx_hashes["tx_hash"] = self._multicall_transaction(
            value_amount=int(value_amount), multicall_args=multicall_args
        )
        return tx_hashes
