import logging
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from logging import Logger
from statistics import median
from typing import Any, Union

from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import ChecksumAddress, TxParams

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_max_fee_per_gas
from pyrfx.utils import PRECISION, get_exchange_router_contract, get_order_handler_contract, to_decimal


class Order(ABC):
    """
    A class to handle the creation, approval, and submission of orders.
    Handles different types of orders such as buy, sell, and swap with configurable gas fees, slippage, and collateral.
    """

    @abstractmethod
    def __init__(
        self,
        config: ConfigManager,
        market_address: ChecksumAddress,
        collateral_address: ChecksumAddress,
        index_token_address: ChecksumAddress,
        is_long: bool,
        size_delta: Union[int, Decimal],
        initial_collateral_delta: Union[int, Decimal],
        slippage_percent: Union[float, Decimal],
        order_type: str,
        swap_path: list[ChecksumAddress] | None = None,
        max_fee_per_gas: Union[int, str, float, Decimal] | None = None,
        auto_cancel: bool = False,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initializes the Order class with the provided parameters and handles default behavior.

        :param config: Configuration manager containing blockchain settings.
        :param market_address: The address representing the RFX market.
        :param collateral_address: The contract address of the collateral token.
        :param index_token_address: The contract address of the index token.
        :param is_long: Boolean indicating whether the order is long or short.
        :param size_delta: Change in position size for the order.
        :param initial_collateral_delta: The amount of initial collateral in the order.
        :param slippage_percent: Allowed slippage for the price in percentage.
        :param order_type: The type of order to create.
        :param swap_path: List of contract addresses representing the swap path for token exchanges.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param auto_cancel: Boolean indicating whether the order should be auto-canceled if unfilled.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.config: ConfigManager = config
        self.market_address: ChecksumAddress = market_address
        self.collateral_address: ChecksumAddress = collateral_address
        self.index_token_address: ChecksumAddress = index_token_address
        self.is_long: bool = is_long
        self.size_delta: Decimal = to_decimal(size_delta)
        self.initial_collateral_delta: Decimal = to_decimal(initial_collateral_delta)
        self.slippage_percent: Decimal = to_decimal(slippage_percent)
        self.order_type: str = order_type
        self.swap_path: list[ChecksumAddress] = swap_path if swap_path else []
        self.max_fee_per_gas: Decimal | None = (
            to_decimal(max_fee_per_gas) if max_fee_per_gas else get_max_fee_per_gas(self.config)
        )
        self.auto_cancel: bool = auto_cancel
        self.debug_mode: bool = debug_mode

        self._gas_limits: dict[str, Any] = {}
        self._gas_limits_order_type_contract_function: ContractFunction | None = None

        self._exchange_router_contract: Contract = get_exchange_router_contract(config=self.config)
        self._order_handler_contract: Contract = get_order_handler_contract(config=self.config)

    @abstractmethod
    def _determine_gas_limits(self) -> None:
        """
        Determine and set gas limits for the order.
        This method is meant to be overridden by subclasses if custom gas limits are required.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def create_and_execute(self) -> dict[str, Any]:
        """
        Build and submit an order, determining whether it is an open, close, or swap order, and ensuring correct gas
        limits, fees, and execution parameters are set.

        :raises Exception: If the execution price falls outside the acceptable range for the order type.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def _multicall_transaction(self, value_amount: int, multicall_args: list[HexBytes]) -> HexBytes | None:
        """
        Builds and submits the transaction to the network.

        :param value_amount: The amount of value (in native tokens) to send along with the transaction.
        :param multicall_args: List of arguments for multicall operations in the transaction.
        :return: The transaction hash.
        """
        self.logger.info("Building transaction ...")

        if not isinstance(value_amount, int):
            value_amount: int = int(value_amount)

        try:
            # Get the current nonce for the user’s wallet
            nonce: int = self.config.connection.eth.get_transaction_count(self.config.user_wallet_address)

            # Determine gas parameters
            if self._gas_limits_order_type_contract_function:
                # Estimate gas limit using the contract function
                gas_estimate = 2 * self._gas_limits_order_type_contract_function.call()
                self.logger.debug(f"Estimated gas (from contract function): {gas_estimate}")
            else:
                gas_estimate = 2_000_000  # Default gas estimate
                self.logger.debug(f"Using default gas estimate: {gas_estimate}")

            max_fee_per_gas: int = int(self.max_fee_per_gas)
            max_priority_fee_per_gas: int = 0  # Can be set to a non-zero value if needed

            self.logger.debug(f"Nonce: {nonce}")
            self.logger.debug(f"Gas Estimate: {gas_estimate}")
            self.logger.debug(f"Max Fee Per Gas: {max_fee_per_gas}")
            self.logger.debug(f"Max Priority Fee Per Gas: {max_priority_fee_per_gas}")

            # Build the transaction using the determined gas parameters
            raw_tx: TxParams = self._exchange_router_contract.functions.multicall(multicall_args).build_transaction(
                {
                    "value": value_amount,
                    "chainId": self.config.chain_id,
                    "gas": gas_estimate,
                    "maxFeePerGas": max_fee_per_gas,
                    "maxPriorityFeePerGas": max_priority_fee_per_gas,
                    "nonce": nonce,
                }
            )

            self.logger.debug(f"Raw transaction: {raw_tx}")

            # Sign and submit the transaction if not in debug mode
            if not self.debug_mode:
                signed_txn: SignedTransaction = self.config.connection.eth.account.sign_transaction(
                    raw_tx, self.config.private_key
                )
                tx_hash: HexBytes = self.config.connection.eth.send_raw_transaction(signed_txn.raw_transaction)
                tx_url: str = f"{self.config.block_explorer_url}/tx/0x{tx_hash.hex()}"
                self.logger.info(f"Transaction submitted! Transaction hash: 0x{tx_hash.hex()}")
                self.logger.info(f"Transaction submitted! Check status: {tx_url}")
                return tx_hash
            else:
                self.logger.info("Debug mode enabled. Transaction not submitted.")
                return None

        except Exception as e:
            self.logger.error(f"Failed to submit transaction: {e}")
            raise Exception(f"Failed to submit transaction: {e}")

    def _get_prices(self, decimals: int, prices: dict[str, dict[str, Any]]) -> tuple[Decimal, Decimal, Decimal]:
        """
        Retrieves and calculates the acceptable prices for the order based on current market conditions and slippage.

        :param decimals: Decimal precision for the token.
        :param prices: Dictionary containing min and max prices from the Oracle.
        :return: A tuple containing the median price, slippage-adjusted price, and acceptable price in USD.
        """
        self.logger.info("Fetching current prices ...")

        try:
            price_values = [
                Decimal(prices[self.index_token_address]["maxPriceFull"]),
                Decimal(prices[self.index_token_address]["minPriceFull"]),
            ]
            price: Decimal = median(price_values)

            if self.order_type == "increase":
                acceptable_price: Decimal = (
                    price * (Decimal("1") + self.slippage_percent)
                    if self.is_long
                    else price * (Decimal("1") - self.slippage_percent)
                )
            elif self.order_type == "decrease":
                acceptable_price: Decimal = (
                    price * (Decimal("1") - self.slippage_percent)
                    if self.is_long
                    else price * (Decimal("1") + self.slippage_percent)
                )
            else:
                acceptable_price: Decimal = price

            acceptable_price_in_usd: Decimal = Decimal(acceptable_price) * Decimal(10) ** (decimals - PRECISION)

            self.logger.info(f"Mark Price: ${price * Decimal(10) ** (decimals - PRECISION):,.2f}")
            self.logger.info(f"Acceptable price: ${acceptable_price_in_usd:,.2f}")

            return price, acceptable_price, acceptable_price_in_usd

        except InvalidOperation as e:
            self.logger.error(f"Invalid operation in price calculation: {e}")
            raise ValueError(f"Invalid operation in price calculation: {e}") from e
        except KeyError as e:
            self.logger.error(f"Missing price data for token: {e}")
            raise ValueError(f"Missing price data for token: {e}") from e
        except Exception as e:
            self.logger.error(f"Failed to retrieve prices: {e}")
            raise ValueError(f"Failed to retrieve prices: {e}") from e

    def _cancel_order(self, argument: HexBytes) -> HexBytes:
        """
        Cancel an order using the encoded ABI payload.

        :param argument: A HexBytes containing the limit order key required by the 'cancelOrder' method
            of the `_order_handler_contract`.
        :return: The ABI-encoded string representing the 'cancelOrder' contract function call.
        :raises ValueError: If the arguments are empty or if encoding fails.
        """
        if not argument:
            self.logger.error("Transaction arguments must not be empty.")
            raise ValueError("Transaction arguments must not be empty.")
        try:
            encoded_order = HexBytes(
                self._order_handler_contract.encode_abi(
                    "cancelOrder",
                    args=[argument],
                )
            )
            self.logger.debug(f"Created encoded order: {encoded_order.hex()}")
            return encoded_order
        except Exception as e:
            self.logger.error(f"Failed to encode order: {e}")
            raise ValueError(f"Failed to encode order: {e}")

    def _create_order(self, arguments: tuple) -> HexBytes:
        """
        Create an order by encoding the contract function call.

        :param arguments: A tuple containing the necessary parameters for creating the order, such as wallet addresses,
                          market details, collateral amounts, and execution fees.
        :return: The ABI-encoded string representing the 'createOrder' contract function call.
        :raises ValueError: If arguments are invalid.
        """
        if not arguments:
            self.logger.error("Transaction arguments must not be empty.")
            raise ValueError("Transaction arguments must not be empty.")
        try:
            encoded_order = HexBytes(
                self._exchange_router_contract.encode_abi(
                    "createOrder",
                    args=[arguments],
                )
            )
            self.logger.debug(f"Created encoded order: {encoded_order.hex()}")
            return encoded_order
        except Exception as e:
            self.logger.error(f"Failed to encode order: {e}")
            raise ValueError(f"Failed to encode order: {e}")

    def _send_tokens(self, token_address: ChecksumAddress, amount: Decimal) -> HexBytes:
        """
        Send tokens to the exchange contract.

        :param token_address: The address of the token to send.
        :param amount: The amount of tokens to send.
        :return: The ABI-encoded string representing the 'sendTokens' contract function call.
        :raises ValueError: If token address or amount is invalid.
        """
        if not token_address or amount <= 0:
            self.logger.error("Invalid token address or amount")
            raise ValueError("Invalid token address or amount")
        try:
            encoded_tokens = HexBytes(
                self._exchange_router_contract.encode_abi(
                    "sendTokens",
                    args=[token_address, self.config.contracts.order_vault.contract_address, int(amount)],
                )
            )
            self.logger.debug(f"Encoded sendTokens for {token_address}: {encoded_tokens.hex()}")
            return encoded_tokens
        except Exception as e:
            self.logger.error(f"Failed to encode sendTokens for {token_address}: {e}")
            raise ValueError(f"Failed to encode sendTokens for {token_address}: {e}")

    def _send_wnt(self, amount: Decimal) -> HexBytes:
        """
        Send Wrapped Native Token (WNT) to the exchange contract.

        :param amount: The amount of WNT to send.
        :return: The ABI-encoded string representing the 'sendWnt' contract function call.
        :raises ValueError: If amount is invalid.
        """
        if amount <= 0:
            self.logger.error("WNT amount must be greater than zero.")
            raise ValueError("WNT amount must be greater than zero.")
        try:
            encoded_wnt = HexBytes(
                self._exchange_router_contract.encode_abi(
                    "sendWnt",
                    args=[self.config.contracts.order_vault.contract_address, int(amount)],
                )
            )
            self.logger.debug(f"Encoded sendWnt: {encoded_wnt.hex()}")
            return encoded_wnt
        except Exception as e:
            self.logger.error(f"Failed to encode sendWnt: {e}")
            raise ValueError(f"Failed to encode sendWnt: {e}")
