import logging
from abc import ABC, abstractmethod
from decimal import Decimal
from logging import Logger
from typing import Any, Union

from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import ChecksumAddress, TxParams

from pyrfx.approve_token import check_if_approved
from pyrfx.config_manager import ConfigManager
from pyrfx.custom_error_parser import CustomErrorParser
from pyrfx.gas_utils import GasLimits, get_execution_fee, get_gas_limits, get_max_fee_per_gas
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.get.pool_tvl import PoolTVL
from pyrfx.order.swap_router import SwapRouter
from pyrfx.utils import (
    get_data_store_contract,
    get_estimated_deposit_amount_out,
    get_exchange_router_contract,
    to_decimal,
)


class Deposit(ABC):
    """
    A class to handle the creation and management of deposit orders in a decentralized exchange.

    This class is responsible for preparing deposit transactions, including setting up token paths,
    handling approvals, and submitting the final deposit transaction to the blockchain.
    It supports handling long and short token deposits, gas fee estimation, and token approvals.
    """

    @abstractmethod
    def __init__(
        self,
        config: ConfigManager,
        market_address: ChecksumAddress,
        initial_long_token_address: ChecksumAddress,
        initial_short_token_address: ChecksumAddress,
        long_token_amount: Union[int, str, float, Decimal],
        short_token_amount: Union[int, str, float, Decimal],
        max_fee_per_gas: Union[int, str, float, Decimal] | None = None,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the Deposit class with necessary configurations and contract objects.

        The constructor sets up various internal attributes based on the provided parameters, including
        initializing connections to blockchain contracts and retrieving market information. If `max_fee_per_gas`
        is not provided, it will be calculated based on the base fee of the latest block with a 35% multiplier.

        :param config: Configuration object containing blockchain network and contract settings.
        :param market_address: The address representing the market where the deposit will be made.
        :param initial_long_token_address: The address of the token to be deposited on the long side.
        :param initial_short_token_address: The address of the token to be deposited on the short side.
        :param long_token_amount: The amount of long tokens to be deposited in the market.
        :param short_token_amount: The amount of short tokens to be deposited in the market.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self.config: ConfigManager = config
        self.market_address: ChecksumAddress = market_address
        self.initial_long_token_address: ChecksumAddress = initial_long_token_address
        self.initial_short_token_address: ChecksumAddress = initial_short_token_address
        self.long_token_amount: Decimal = to_decimal(long_token_amount)
        self.short_token_amount: Decimal = to_decimal(short_token_amount)
        self.max_fee_per_gas: Decimal = (
            to_decimal(max_fee_per_gas) if max_fee_per_gas else get_max_fee_per_gas(self.config)
        )
        self.debug_mode: bool = debug_mode

        self.long_token_swap_path: list[ChecksumAddress] = []
        self.short_token_swap_path: list[ChecksumAddress] = []

        # Fetch the gas limits from the datastore
        self._gas_limits: GasLimits = get_gas_limits(get_data_store_contract(self.config))
        self._gas_limits_order_type_contract_function: ContractFunction | None = None

        # Internal setup of the blockchain connection and contracts
        self._exchange_router_contract: Contract = get_exchange_router_contract(self.config)
        self._available_markets: dict[ChecksumAddress, dict[str, Any]] = Markets(self.config).get_available_markets()

    @abstractmethod
    def determine_gas_limits(self) -> None:
        """
        Abstract method to determine gas limits for the deposit order.

        This method must be implemented by subclasses to handle the retrieval of
        gas limits specific to the operation being performed.
        """
        raise NotImplementedError("This method must be implemented by subclasses.")

    def check_for_approval(self) -> None:
        """
        Check if the long and short tokens are approved for spending. If not, approve them.

        :raises ValueError: If token approval fails.
        """
        spender: ChecksumAddress = self.config.contracts.router.contract_address

        tokens_to_check: list[tuple[ChecksumAddress, Decimal]] = [
            (self.initial_long_token_address, self.long_token_amount),
            (self.initial_short_token_address, self.short_token_amount),
        ]

        tokens_to_approve: list[ChecksumAddress] = [token for token, amount in tokens_to_check if amount > 0]

        if not tokens_to_approve:
            self.logger.info("No tokens need approval.")
            return

        for token_address in tokens_to_approve:
            try:
                check_if_approved(
                    config=self.config,
                    spender_address=spender,
                    token_to_approve_address=token_address,
                    max_fee_per_gas=int(self.max_fee_per_gas),
                    logger=self.logger,
                )
            except Exception as e:
                self.logger.error(f"Approval for token spending failed for {token_address}: {e}")
                raise ValueError(f"Approval for token spending failed for {token_address}: {e}")

    def create_and_execute(self) -> dict[str, HexBytes | None]:
        """
        Create a deposit order by estimating fees, setting up paths, and submitting the transaction.
        """
        try:
            # Check for token approvals unless in debug mode
            if not self.debug_mode:
                self.check_for_approval()

            min_market_tokens: int = self._estimate_deposit()
            execution_fee_decimal: Decimal = get_execution_fee(
                gas_limits=self._gas_limits,
                estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                gas_price=self.config.connection.eth.gas_price,
            )
            execution_fee: int = int(execution_fee_decimal * Decimal("3"))  # Apply multiplier

            # Validate initial tokens and determine swap paths
            self._check_initial_tokens()
            self._determine_swap_paths()

            arguments: tuple = (
                self.config.user_wallet_address,
                self.config.zero_address,
                self.config.zero_address,
                self.market_address,
                self.initial_long_token_address,
                self.initial_short_token_address,
                self.long_token_swap_path,
                self.short_token_swap_path,
                min_market_tokens,
                True,  # Should unwrap native token
                execution_fee,
                0,  # Callback gas limit
            )

            total_wnt_amount: int = 0
            multicall_args: list[HexBytes] = []
            tx_hashes: dict[str, HexBytes | None] = {}

            if self.long_token_amount > 0:
                if self.initial_long_token_address == self.config.weth_address:
                    total_wnt_amount += int(self.long_token_amount)
                else:
                    tx_hashes["send_tokens_hash"] = self._send_tokens(
                        token_address=self.initial_long_token_address,
                        amount=int(self.long_token_amount),
                    )
                    multicall_args.append(tx_hashes["send_tokens_hash"])

            if self.short_token_amount > 0:
                if self.initial_short_token_address == self.config.weth_address:
                    total_wnt_amount += int(self.short_token_amount)
                else:
                    tx_hashes["send_tokens_hash"] = self._send_tokens(
                        token_address=self.initial_short_token_address,
                        amount=int(self.short_token_amount),
                    )
                    multicall_args.append(tx_hashes["send_tokens_hash"])

            # Send total WNT amount including deposit amount
            tx_hashes["send_wnt_hash"] = self._send_wnt(int(total_wnt_amount + execution_fee))
            multicall_args.append(tx_hashes["send_wnt_hash"])

            # Send our deposit parameters
            tx_hashes["create_order_hash"] = self._create_order(arguments)
            multicall_args.append(tx_hashes["create_order_hash"])

            # Submit the final transaction
            tx_hashes["tx_hash"] = self._submit_transaction(
                value_amount=int(total_wnt_amount + execution_fee),
                multicall_args=multicall_args,
            )
            return tx_hashes

        except Exception as e:
            self.logger.error(f"Failed to create deposit order: {e}")
            # Try to parse error
            try:
                cap: CustomErrorParser = CustomErrorParser(config=self.config)
                error_reason: dict[str, Any] = cap.parse_error(error_bytes=e.args[0])
                error_message: str = cap.get_error_string(error_reason=error_reason)
                self.logger.info(f"Parsed error: {error_message}")
            except Exception as parse_e:
                self.logger.error(f"Failed to parse custom error: {parse_e}")
                raise Exception(f"Failed to parse custom error: {parse_e}")

            raise Exception(f"Failed to create deposit order and parse custom error: {e}.")

    def _submit_transaction(self, value_amount: int, multicall_args: list[HexBytes]) -> HexBytes | None:
        """
        Submit the deposit transaction to the blockchain.

        :param value_amount: The amount of WNT (ETH or equivalent) to send with the transaction.
        :param multicall_args: A list of encoded contract function calls.
        :return: The transaction hash.
        """
        self.logger.info("Building transaction ...")

        try:
            # Get the current nonce for the user’s wallet
            nonce: int = self.config.connection.eth.get_transaction_count(self.config.user_wallet_address)

            # Use the provided gas limits (or default to a safe estimate if not available)
            gas_estimate: int = self._gas_limits.get(
                "gas_estimate",
                (
                    2 * self._gas_limits_order_type_contract_function.call()
                    if self._gas_limits_order_type_contract_function
                    else 2_000_000
                ),
            )
            max_fee_per_gas: int = int(self._gas_limits.get("max_fee_per_gas", self.max_fee_per_gas))
            max_priority_fee_per_gas: int = int(self._gas_limits.get("max_priority_fee_per_gas", 0))

            # Build the transaction using the provided gas limits
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
                return None

        except Exception as e:
            self.logger.error(f"Failed to submit transaction: {e}")
            raise Exception(f"Failed to submit transaction: {e}")

    def _check_initial_tokens(self) -> None:
        """
        Check and set long or short token addresses if they are not defined.

        :return: None.
        :raises ValueError: If token address is missing in market info.
        """
        for token_type, token_amount, token_key, token_attr in [
            ("long", self.long_token_amount, "long_token_address", "initial_long_token_address"),
            ("short", self.short_token_amount, "short_token_address", "initial_short_token_address"),
        ]:
            if token_amount == 0:
                token_address: str | None = self._available_markets.get(self.market_address).get(token_key)
                if not token_address:
                    raise ValueError(f"{token_type.capitalize()} token address is missing in the market info.")
                setattr(self, token_attr, self.config.to_checksum_address(token_address))
                self.logger.debug(f"Set {token_attr} to {token_address} for token_type '{token_type}'.")

    def _determine_swap_paths(self) -> None:
        """
        Determine the required swap paths for the long and short tokens if their current addresses differ from the
        market-defined ones.

        :return: None.
        :raises ValueError: If swap path determination fails.
        """
        swap_router: SwapRouter | None = None

        for token_type, initial_token, market_token_key, swap_path_attr in [
            ("long", self.initial_long_token_address, "long_token_address", "long_token_swap_path"),
            ("short", self.initial_short_token_address, "short_token_address", "short_token_swap_path"),
        ]:
            market_token_address: ChecksumAddress = self.config.to_checksum_address(
                self._available_markets[self.market_address][market_token_key]
            )

            if market_token_address != initial_token:
                if not swap_router:
                    pool_tvl: dict[str, dict[str, Any]] = PoolTVL(config=self.config).get_pool_balances()
                    swap_router = SwapRouter(config=self.config, pool_tvl=pool_tvl)
                    self.logger.debug("SwapRouter initialized.")

                try:
                    swap_path: list[ChecksumAddress] = swap_router.determine_swap_route(
                        available_markets=self._available_markets,
                        in_token_address=initial_token,
                        out_token_address=market_token_address,
                    )
                    setattr(self, swap_path_attr, swap_path)
                    self.logger.debug(f"Determined swap path for {token_type} token: {swap_path}")
                except Exception as e:
                    self.logger.error(f"Failed to determine swap path for {token_type} token: {e}")
                    raise ValueError(f"Failed to determine swap path for {token_type} token: {e}")

    def _create_order(self, arguments: tuple) -> HexBytes:
        """
        Create the encoded order using the exchange contract's ABI.

        :param arguments: A tuple containing the arguments required for creating a deposit order.
        :return: Encoded transaction in HexBytes format.
        :raises ValueError: If arguments are invalid.
        """
        if not arguments:
            self.logger.error("Transaction arguments must not be empty.")
            raise ValueError("Transaction arguments must not be empty.")
        try:
            encoded_order = HexBytes(
                self._exchange_router_contract.encode_abi(
                    "createDeposit",
                    args=[arguments],
                )
            )
            self.logger.debug(f"Created encoded order: {encoded_order.hex()}")
            return encoded_order
        except Exception as e:
            self.logger.error(f"Failed to encode order: {e}")
            raise ValueError(f"Failed to encode order: {e}")

    def _send_tokens(self, token_address: ChecksumAddress, amount: int) -> HexBytes:
        """
        Send tokens to the exchange contract.

        :param token_address: The token address to send.
        :param amount: The amount of tokens to send.
        :return: Encoded transaction in HexBytes format.
        :raises ValueError: If token address or amount is invalid.
        """
        if not token_address or amount <= 0:
            self.logger.error("Invalid token address or amount")
            raise ValueError("Invalid token address or amount")
        try:
            encoded_tokens = HexBytes(
                self._exchange_router_contract.encode_abi(
                    "sendTokens",
                    args=[token_address, self.config.contracts.deposit_vault.contract_address, amount],
                )
            )
            self.logger.debug(f"Encoded sendTokens for {token_address}: {encoded_tokens.hex()}")
            return encoded_tokens
        except Exception as e:
            self.logger.error(f"Failed to encode sendTokens for {token_address}: {e}")
            raise ValueError(f"Failed to encode sendTokens for {token_address}: {e}")

    def _send_wnt(self, amount: int) -> HexBytes:
        """
        Send WNT to the exchange contract.

        :param amount: The amount of WNT to send.
        :return: Encoded transaction in HexBytes format.
        :raises ValueError: If amount is invalid.
        """
        if amount <= 0:
            self.logger.error("WNT amount must be greater than zero.")
            raise ValueError("WNT amount must be greater than zero.")
        try:
            encoded_wnt = HexBytes(
                self._exchange_router_contract.encode_abi(
                    "sendWnt",
                    args=[self.config.contracts.deposit_vault.contract_address, amount],
                )
            )
            self.logger.debug(f"Encoded sendWnt: {encoded_wnt.hex()}")
            return encoded_wnt
        except Exception as e:
            self.logger.error(f"Failed to encode sendWnt: {e}")
            raise ValueError(f"Failed to encode sendWnt: {e}")

    def _estimate_deposit(self) -> int:
        """
        Estimate the amount of RM tokens based on deposit amounts and current token prices.

        :return: Estimated RM tokens out.
        :raises ValueError: If estimation fails.
        """
        try:
            oracle_prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

            # Extract market and token prices
            market_addresses, prices = self._get_market_data_and_prices(
                market=self._available_markets[self.market_address],
                oracle_prices=oracle_prices,
            )

            parameters: dict[str, Any] = {
                "data_store_address": self.config.contracts.data_store.contract_address,
                "market_addresses": market_addresses,
                "token_prices_tuple": prices,
                "long_token_amount": int(self.long_token_amount),
                "short_token_amount": int(self.short_token_amount),
                "ui_fee_receiver": self.config.zero_address,
            }

            estimated_deposit: int = get_estimated_deposit_amount_out(config=self.config, params=parameters)
            self.logger.debug(f"Estimated deposit amount out: {estimated_deposit}")
            return estimated_deposit

        except Exception as e:
            self.logger.error(f"Failed to estimate deposit: {e}")
            raise ValueError(f"Failed to estimate deposit: {e}")

    def _get_market_data_and_prices(
        self, market: dict[str, Any], oracle_prices: dict[str, dict[str, Any]]
    ) -> tuple[list[str], list[tuple[int, int]]]:
        """
        Helper function to fetch market addresses and prices for the current market.

        :param market: Market information from all markets.
        :param oracle_prices: Dictionary of token prices fetched from Oracle.
        :return: A tuple containing market addresses and prices.
        :raises ValueError: If required price data is missing.
        """
        try:
            market_addresses = [
                self.market_address,
                market["index_token_address"],
                market["long_token_address"],
                market["short_token_address"],
            ]

            prices = [
                (int(oracle_prices[token]["minPriceFull"]), int(oracle_prices[token]["maxPriceFull"]))
                for token in [
                    market["index_token_address"],
                    market["long_token_address"],
                    market["short_token_address"],
                ]
            ]

            self.logger.debug(f"Market addresses: {market_addresses}")
            self.logger.debug(f"Prices: {prices}")

            return market_addresses, prices
        except KeyError as e:
            self.logger.error(f"Missing price data for token: {e}")
            raise ValueError(f"Missing price data for token: {e}") from e
