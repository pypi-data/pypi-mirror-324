import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

from hexbytes import HexBytes

from pyrfx.config_manager import ConfigManager


def wrap_or_unwrap_eth(
    config: ConfigManager,
    amount: int,
    is_wrap: bool,
    logger: Logger | None = None,
    debug_mode: bool = False,
) -> dict[str, HexBytes | None]:
    """
    Wrap or unwrap ETH <-> WETH.

    :param config: A Pyrfx ConfigManager object containing chain settings and wallet info.
    :param amount: The amount (in wei) to wrap or unwrap.
    :param is_wrap: True to wrap ETH -> WETH, False to unwrap WETH -> ETH.
    :param logger: Optional Python Logger for debug/info messages.
    :param debug_mode: True to enable debug mode.
    :return: A dictionary with the transaction hash keyed by "wrapped" or "unwrapped".
    """
    # Set up logger if not provided.
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    try:
        # 1. Load WETH ABI from JSON.
        abi_path: Path = Path(__file__).parent / "contracts" / "weth.json"
        if not abi_path.exists():
            raise FileNotFoundError(f"ABI file not found: {abi_path}")

        with abi_path.open("r", encoding="utf-8") as f:
            weth_contract_abi: list[Any] = json.load(f)
        logger.debug(f"Loaded WETH ABI from {abi_path}")

        # 2. Instantiate the WETH contract.
        if not config.weth_address:
            raise ValueError("config.weth_address is not set. Unable to proceed with wrap/unwrap.")

        weth_contract = config.connection.eth.contract(address=config.weth_address, abi=weth_contract_abi)
        logger.debug(f"WETH contract instantiated at address: {config.weth_address}")

        # 3. Get the current nonce for the account.
        account_address = config.user_wallet_address
        nonce = config.connection.eth.get_transaction_count(account_address)
        logger.debug(f"Nonce for account {account_address}: {nonce}")

        # 4. Prepare the transaction data.
        if is_wrap:
            # deposit() is payable: send ETH as value.
            tx_data = weth_contract.functions.deposit().build_transaction(
                {
                    "chainId": config.chain_id,
                    "from": account_address,
                    "nonce": nonce,
                    "value": amount,
                }
            )
            eth_amount = config.connection.from_wei(amount, "ether")
            logger.info(f"Wrapping {eth_amount} ETH -> WETH.")
        else:
            # withdraw(uint wad) is nonpayable.
            tx_data = weth_contract.functions.withdraw(amount).build_transaction(
                {
                    "chainId": config.chain_id,
                    "from": account_address,
                    "nonce": nonce,
                    "value": 0,
                }
            )
            eth_amount = config.connection.from_wei(amount, "ether")
            logger.info(f"Unwrapping {eth_amount} WETH -> ETH.")

        # 5. Estimate gas required for the transaction.
        gas_estimate = config.connection.eth.estimate_gas(tx_data)
        logger.debug(f"Gas estimate: {gas_estimate}")

        # 6. Retrieve current gas price.
        gas_price = config.connection.eth.gas_price
        logger.debug(f"Gas price: {gas_price}")

        # 7. Update the transaction data with the gas estimate.
        tx_data.update(
            {
                "gas": gas_estimate,
                # Uncomment the following line to explicitly set gas price if needed:
                # "gasPrice": gas_price,
            }
        )

        # 8. Sign the transaction using the private key.
        signed_tx = config.connection.eth.account.sign_transaction(tx_data, private_key=str(config.private_key))
        logger.debug("Transaction signed successfully.")

        # 9. Send the signed transaction to the network.
        tx_hash: HexBytes = config.connection.eth.send_raw_transaction(signed_tx.raw_transaction)
        logger.info(f"Transaction submitted! Transaction hash: 0x{tx_hash.hex()}")

        tx_url: str = f"{config.block_explorer_url}/tx/0x{tx_hash.hex()}"
        logger.info(f"Check transaction status: {tx_url}")

        # Return the transaction hash in a dictionary.
        return {"wrapped": tx_hash} if is_wrap else {"unwrapped": tx_hash}

    except Exception as exc:
        logger.exception(f"An error occurred during wrap/unwrap operation: {exc}")
        raise
