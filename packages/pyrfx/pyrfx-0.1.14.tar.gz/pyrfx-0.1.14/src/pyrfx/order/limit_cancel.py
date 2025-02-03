import logging
from decimal import Decimal
from logging import Logger
from typing import Any

from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import GasLimits, get_execution_fee, get_gas_limits
from pyrfx.order.base_order import Order
from pyrfx.utils import get_account_orders, get_bytes_32_count, get_bytes_32_values_at, get_data_store_contract


class LimitCancelOrder(Order):
    """
    A class to handle limit cancel orders on the blockchain.
    Extends the base Order class to manage the logic for cancel orders.
    """

    def __init__(
        self,
        config: ConfigManager,
        order_position: int = -1,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the LimitCancelOrder class, extending the base Order class.

        :param config: Configuration manager containing blockchain settings.
        :param order_position: Order position to cancel. Can be:
            - -1 for the last order
            - an integer from 0 to (number_of_orders - 1)
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # Call parent class constructor
        super().__init__(
            config=config,
            market_address=config.zero_address,
            collateral_address=config.zero_address,
            index_token_address=config.zero_address,
            is_long=False,
            size_delta=Decimal("0"),
            initial_collateral_delta=Decimal("0"),
            slippage_percent=Decimal("0"),
            order_type="limit_cancel",
            swap_path=None,
            max_fee_per_gas=None,
            auto_cancel=False,
            debug_mode=debug_mode,
            log_level=log_level,
        )

        # Set order position and validate if that position exist
        self._order_position: int = order_position
        self._validate_order_position()

        # Determine gas limits
        self._determine_gas_limits()

    @property
    def order_position(self) -> int:
        """
        Get the current order position.

        :return: The current order position.
        """
        return self._order_position

    @order_position.setter
    def order_position(self, position: int) -> None:
        """
        Set a new order position and validate it.

        :param position: The new order position.
        :raises ValueError: If the order position is invalid.
        """
        self._order_position: int = position
        self._validate_order_position()

    def _validate_order_position(self) -> None:
        """
        Validate the order_position parameter.

        :return: None
        """
        order_count: int = get_bytes_32_count(config=self.config)
        self.logger.info(f"Total number of open orders is: {order_count}")

        if order_count < -1:
            self.logger.error("Order position parameter must be >= 0. Or -1 for last order.")
            raise ValueError("Order position parameter must be >= 0. Or -1 for last order.")

        elif self._order_position == -1:
            if order_count == 0:
                self.logger.error("There are no orders to cancel.")
                raise ValueError("There are no orders to cancel.")

        else:
            if self._order_position >= order_count:
                self.logger.error(
                    "Order position parameter must be >= 0. "
                    f"Order position parameter can not be greater than number of open orders."
                )
                raise ValueError(
                    "Order position parameter must be >= 0. "
                    f"Order position parameter can not be greater than number of open orders."
                )

    def _determine_gas_limits(self) -> None:
        """
        Determine the gas limits required for placing a limit cancel order.

        This method queries the datastore contract to get the relevant gas limits
        and sets the gas limit for the limit cancel order operation.

        Logs an error if gas limits cannot be retrieved or if any other exception occurs.
        """
        try:
            # Retrieve the datastore contract
            datastore: Contract = get_data_store_contract(self.config)

            if not datastore:
                raise ValueError("Datastore contract was not found.")

            # Fetch the gas limits from the datastore
            self._gas_limits: GasLimits = get_gas_limits(datastore)

            if not self._gas_limits:
                raise ValueError("Gas limits could not be retrieved.")

            # Retrieve the specific gas limit for the 'increase_order' operation
            # TODO: figure out how to set cancel order gas limit, or hardcode. For now use "increase_order".
            self._gas_limits_order_type_contract_function: ContractFunction | None = self._gas_limits.get(
                "increase_order"
            )

            if not self._gas_limits_order_type_contract_function:
                raise KeyError("Gas limit for 'increase_order' not found.")

            if self.debug_mode:
                # Get the actual gas limit value by calling the contract function
                gas_limit_value: int = self._gas_limits_order_type_contract_function.call()
                self.logger.info(f"Gas limit for 'increase_order' is: {gas_limit_value}")

        except KeyError as e:
            self.logger.error(f"KeyError - Gas limit for 'increase_order' not found: {e}")
            raise Exception(f"Gas limit for 'increase_order' not found: {e}")

        except ValueError as e:
            self.logger.error(f"ValueError - Issue with datastore or gas limits: {e}")
            raise Exception(f"Error with datastore or gas limits: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error while determining gas limits: {e}")
            raise Exception(f"Unexpected error while determining gas limits: {e}")

    def list_orders(self) -> list[dict[str, Any]]:
        """
        Lists all currently open orders for the user's address.

        :return: A list of order dictionary objects.
        """
        # Log what position user wants to cancel
        account_orders: list[dict[str, Any]] = get_account_orders(config=self.config)
        self.logger.info(f"Existing orders for address: {self.config.user_wallet_address}")
        for idx, order in enumerate(account_orders):
            self.logger.info(f"{idx}) Order: {order}")
        return account_orders

    def create_and_execute(self) -> dict[str, HexBytes | None]:
        """
        Build and submit a limit increase order, ensuring correct gas limits, fees, and execution parameters are set.

        :return: The dictionary with transaction hash.
        :raises Exception: If the execution price falls outside the acceptable range for the limit increase order.
        """
        # Log what position will be canceled
        parsed_orders: list[dict[str, Any]] = get_account_orders(config=self.config)
        self.logger.info(f"Order that will be canceled: {parsed_orders[self._order_position]}")

        # Set execution fee
        gas_price: Decimal = Decimal(self.config.connection.eth.gas_price)
        execution_fee: Decimal = Decimal(
            get_execution_fee(
                gas_limits=self._gas_limits,
                estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                gas_price=int(gas_price),  # Assuming get_execution_fee expects int
            )
        )

        # Adjust execution fee for limit increase orders due to complexity
        execution_fee_multiplier: Decimal = Decimal("3")
        execution_fee = (execution_fee * execution_fee_multiplier).to_integral_value()  # Uses default rounding

        # Build the order arguments
        keys: list[HexBytes] = get_bytes_32_values_at(config=self.config)

        # Build multicall args
        tx_hashes: dict[str, HexBytes | None] = {"cancel_order_hash": self._cancel_order(keys[self._order_position])}
        multicall_args: list[HexBytes] = [tx_hashes["cancel_order_hash"]]

        # Submit the transaction
        tx_hashes["tx_hash"] = self._multicall_transaction(
            value_amount=int(execution_fee), multicall_args=multicall_args
        )
        return tx_hashes
