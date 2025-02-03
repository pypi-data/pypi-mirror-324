import json
import logging
from decimal import Decimal
from logging import Logger
from pathlib import Path

from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.types import ChecksumAddress, TxParams

from pyrfx.config_manager import ConfigManager
from pyrfx.utils import to_decimal


def check_if_approved(
    config: ConfigManager,
    spender_address: str | ChecksumAddress,
    token_to_approve_address: str | ChecksumAddress,
    max_fee_per_gas: int | str | float | Decimal,
    approve: bool = True,
    amount_of_tokens_to_approve_to_spend: int | None = None,
    logger: Logger | None = None,
) -> None:
    """
    Check if a given amount of tokens is approved for spending by a contract, and approve if necessary.

    :param config: The configuration object containing network and user details.
    :param spender_address: The contract address of the requested spender.
    :param token_to_approve_address: The contract address of the token to spend.
    :param max_fee_per_gas: The maximum fee per gas to be used for the transaction.
    :param approve: Set to True to approve spending if not already approved.
    :param amount_of_tokens_to_approve_to_spend: The amount of tokens to approve to spend, in expanded decimals.
         If not provided, defaults to maximum uint256 (2**256 - 1).
    :param logger: The logger object.
    :raises Exception: If there is an insufficient approval or if approval is required but not granted.
    :return: None.
    """
    # If no amount is provided, set to maximum uint256 value.
    if amount_of_tokens_to_approve_to_spend is None:
        amount_of_tokens_to_approve_to_spend = 2**256 - 1

    # Set up logger if not provided.
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

    try:
        # Ensure addresses are in checksum format.
        if not config.connection.is_checksum_address(spender_address):
            spender_address = config.to_checksum_address(address=spender_address)
        if not config.connection.is_checksum_address(token_to_approve_address):
            token_to_approve_address = config.to_checksum_address(address=token_to_approve_address)

        user_wallet_address: str | ChecksumAddress = config.user_wallet_address
        if not config.connection.is_checksum_address(user_wallet_address):
            user_wallet_address = config.to_checksum_address(address=user_wallet_address)

        # Load ABI for the token contract.
        abi_file_path: Path = Path(__file__).parent / "contracts" / "token_approval.json"
        if not abi_file_path.exists():
            logger.error(f"The ABI file {abi_file_path} does not exist.")
            raise FileNotFoundError(f"The file {abi_file_path} does not exist.")

        with abi_file_path.open("r", encoding="utf-8") as file:
            token_contract_abi: list = json.load(file)
        logger.debug(f"Loaded token contract ABI from {abi_file_path}")

        # Instantiate the token contract object.
        token_contract_obj: Contract = config.connection.eth.contract(
            address=token_to_approve_address, abi=token_contract_abi
        )

        # Retrieve the currently approved amount.
        amount_approved: int = token_contract_obj.functions.allowance(user_wallet_address, spender_address).call()
        logger.info(f"Current allowance for spender {spender_address}: {amount_approved}")

        # Check if approval is required.
        if amount_approved < amount_of_tokens_to_approve_to_spend:
            if approve:
                if amount_of_tokens_to_approve_to_spend == 2**256 - 1:
                    logger.info(
                        f'Approving contract "{spender_address}" to spend maximum uint (2^256-1) tokens '
                        f"for token address: {token_to_approve_address}"
                    )
                else:
                    logger.info(
                        f'Approving contract "{spender_address}" to spend {amount_of_tokens_to_approve_to_spend} '
                        f"tokens for token address: {token_to_approve_address}"
                    )

                # Get the current transaction nonce for the user wallet.
                nonce: int = config.connection.eth.get_transaction_count(user_wallet_address)
                logger.debug(f"Using nonce {nonce} for wallet {user_wallet_address}")

                # Build the transaction for token approval.
                raw_txn: TxParams = token_contract_obj.functions.approve(
                    spender_address, amount_of_tokens_to_approve_to_spend
                ).build_transaction(
                    {
                        "value": 0,
                        "chainId": config.chain_id,
                        "gas": 500_000,
                        "maxFeePerGas": int(to_decimal(max_fee_per_gas)),
                        "maxPriorityFeePerGas": 0,
                        "nonce": nonce,
                    }
                )
                logger.debug(f"Built raw transaction for token approval: {raw_txn}")

                # Sign the transaction using the user's private key.
                signed_txn: SignedTransaction = config.connection.eth.account.sign_transaction(
                    raw_txn, config.private_key
                )
                logger.debug("Transaction signed successfully.")

                # Send the signed transaction.
                tx_hash: HexBytes = config.connection.eth.send_raw_transaction(signed_txn.raw_transaction)
                logger.info(f"Approval transaction submitted! Transaction hash: 0x{tx_hash.hex()}")

                tx_url: str = f"{config.block_explorer_url}/tx/0x{tx_hash.hex()}"
                logger.info(f"Check transaction status at: {tx_url}")
            else:
                logger.error("Token not approved for spend and 'approve' flag is False.")
                raise Exception("Token not approved for spend, please allow first!")
        else:
            logger.info(f"Sufficient allowance already exists: {amount_approved}")

        # Log confirmation of approval.
        if amount_of_tokens_to_approve_to_spend == 2**256 - 1:
            logger.info(
                f'Contract "{spender_address}" approved to spend maximum uint (2^256-1) tokens for token address: {token_to_approve_address}'
            )
        else:
            logger.info(
                f'Contract "{spender_address}" approved to spend {amount_of_tokens_to_approve_to_spend} tokens for token address: {token_to_approve_address}'
            )
        logger.info("Token approval process completed successfully.")

    except Exception as exc:
        logger.exception(f"An error occurred during token approval: {exc}")
        raise
