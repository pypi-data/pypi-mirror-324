import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import Enum
from pathlib import Path
from typing import Any, Final, Union

import pandas as pd
import requests
from eth_account import Account
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from pandas import DataFrame
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential
from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.custom_error_parser import CustomErrorParser
from pyrfx.keys import account_order_list_key

PRECISION: Final[int] = 30


# Enum for Order Types
class OrderTypes(Enum):
    MARKET_SWAP = 0
    LIMIT_SWAP = 1
    MARKET_INCREASE = 2
    LIMIT_INCREASE = 3
    MARKET_DECREASE = 4
    LIMIT_DECREASE = 5
    STOP_LOSS_DECREASE = 6
    LIQUIDATION = 7


# Enum for Decrease Position Swap Types
class DecreasePositionSwapTypes(Enum):
    NO_SWAP = 0
    SWAP_PNL_TOKEN_TO_COLLATERAL_TOKEN = 1
    SWAP_COLLATERAL_TOKEN_TO_PNL_TOKEN = 2


# Enum for Swap
class SwapPricingTypes(Enum):
    TWO_STEPS = 0
    SHIFT = 1
    ATOMIC = 2


# Constants for rate limiting
CALLS_PER_SECOND: Final[int] = 3
ONE_SECOND: Final[int] = 1


# Custom JSON Encoder to handle Decimal serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


# Combined retrier and rate limiter decorator
@sleep_and_retry
@limits(calls=CALLS_PER_SECOND, period=ONE_SECOND)
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_call(call: ContractFunction) -> Any:
    """
    Executes a Web3 call with retry logic and rate limiting.

    :param call: Web3 call to be executed.
    :return: The result of the Web3 call.
    :raises Exception: Propagates exceptions from the call.
    """
    try:
        result = call.call()
        logging.debug("Web3 call executed successfully.")
        return result
    except Exception as e:
        logging.error(f"Error executing Web3 call: {e}")
        raise


# Executes multiple Web3 calls concurrently using ThreadPoolExecutor
def execute_threading(function_calls: list) -> list[Any]:
    """
    Execute multiple Web3 function calls concurrently using ThreadPoolExecutor.

    :param function_calls: A list of Web3 function calls to execute.
    :return: A list of results from the executed Web3 calls.
    """
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_call, call) for call in function_calls]
        results = []
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logging.error(f"Error in threaded Web3 call: {e}")
                results.append(None)
    logging.info("All Web3 calls executed successfully.")
    return results


def load_contract_abi(abi_file_path: Path) -> list[dict[str, Any]]:
    """
    Load the ABI file from the specified path.

    :param abi_file_path: Path to the ABI JSON file.
    :return: Loaded ABI as a list of dictionaries.
    :raises FileNotFoundError: If the file doesn't exist.
    :raises json.JSONDecodeError: If the JSON content is invalid.
    """
    try:
        abi_content = abi_file_path.read_text(encoding="utf-8")
        contract_abi = json.loads(abi_content)
        logging.debug(f"ABI loaded successfully from {abi_file_path}.")
        return contract_abi
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading ABI from {abi_file_path}: {e}")
        raise


def get_token_balance_contract(config: ConfigManager, contract_address: str) -> Contract | None:
    """
    Retrieve the contract object required to query a user's token balance.

    :param config: Configuration object containing RPC and chain details.
    :param contract_address: The token contract address to query balance from.
    :return: Web3 contract object or None if an error occurs.
    """
    abi_file_path = Path(__file__).parent / "contracts" / "balance_abi.json"

    try:
        # Load contract ABI and instantiate the contract
        contract_abi = load_contract_abi(abi_file_path)
        checksum_address = config.to_checksum_address(contract_address)
        contract = config.connection.eth.contract(address=checksum_address, abi=contract_abi)
        logging.debug(f"Contract for token balance at address {checksum_address} successfully created.")
        return contract
    except Exception as e:
        logging.error(f"Error loading ABI or creating contract for address '{contract_address}': {e}")
        return None


def get_available_tokens(config: ConfigManager) -> dict[ChecksumAddress, dict[str, Union[ChecksumAddress, int, bool]]]:
    """
    Query the RFX API to generate a dictionary of available tokens for the specified chain.

    :param config: Configuration object containing the chain information.
    :return: Dictionary of available tokens.
    """
    try:
        response = requests.get(config.tokens_url, timeout=10)
        # Raise an HTTPError for bad responses
        response.raise_for_status()
        token_infos = response.json().get("tokens", [])
        logging.debug(f"Successfully fetched available tokens for chain {config.chain}.")

        # Ensure that address is in ChecksumAddress format
        processed_data: dict[ChecksumAddress, dict[str, Union[ChecksumAddress, int, bool]]] = {}
        for token_info in token_infos:
            token_address = config.to_checksum_address(token_info["address"])
            token_info["address"] = token_address
            processed_data[token_address] = token_info

        return processed_data

    except requests.RequestException as e:
        logging.error(f"Error fetching tokens from API for chain {config.chain}: {e}")
        return {}


def get_contract(config: ConfigManager, contract_name: str) -> Contract:
    """
    Retrieve a contract object for the specified contract name and chain.

    :param config: Configuration object containing blockchain settings.
    :param contract_name: Name of the contract to retrieve.
    :return: Web3 contract object for the specified contract.
    :raises ValueError: If the contract information or ABI file is missing or invalid.
    :raises FileNotFoundError: If the ABI file is not found.
    :raises json.JSONDecodeError: If the ABI file is not valid JSON.
    """
    try:
        # Retrieve contract information
        contract_info = config.contracts[contract_name]

        # Load contract ABI
        abi_file_path = Path(__file__).parent / contract_info.abi_path
        logging.info(f"Loading ABI file from {abi_file_path}")
        contract_abi = load_contract_abi(abi_file_path)

        # Instantiate and return the Web3 contract object
        contract = config.connection.eth.contract(address=contract_info.contract_address, abi=contract_abi)
        logging.info(f"Contract object for '{contract_name}' on chain '{config.chain}' created successfully.")
        return contract

    except KeyError as e:
        logging.error(f"Contract '{contract_name}' not found in configuration: {e}")
        raise ValueError(f"Contract '{contract_name}' not found in configuration.") from e
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading ABI for contract '{contract_name}': {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while creating contract object '{contract_name}': {e}")
        raise


def get_reader_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the reader contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the reader.
    """
    return get_contract(config, "reader")


def get_event_emitter_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the event emitter contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the event emitter.
    """
    return get_contract(config, "event_emitter")


def get_data_store_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the data store contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the data store.
    """
    return get_contract(config, "data_store")


def get_order_handler_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the order handler contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the order handler.
    """
    return get_contract(config, "order_handler")


def get_exchange_router_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the exchange router contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the exchange router.
    """
    return get_contract(config, "exchange_router")


def create_signer(config: ConfigManager) -> Account:
    """
    Create a signer for the given chain using the private key.

    :param config: Configuration object containing the private key and chain information.
    :return: Web3 account object initialized with the private key.
    :raises ValueError: If the private key is missing or invalid.
    """
    if not config.private_key:
        logging.error("Private key is missing in the configuration.")
        raise ValueError("Private key is missing in the configuration.")

    try:
        signer = config.connection.eth.account.from_key(config.private_key)
        logging.debug("Signer created successfully.")
        return signer
    except (ValueError, Exception) as e:
        logging.error(f"Error creating signer: {e}")
        raise ValueError("Invalid private key provided.") from e


def parse_account_orders(orders: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """

    :param orders:
    :return:
    """
    parsed_orders: list[dict[str, Any]] = []
    for order in orders:
        parsed_order: dict[str, Any] = {}
        part1, part2, part3 = order

        # Process part1
        parsed_order["account"] = part1[0]
        parsed_order["receiver"] = part1[1]
        parsed_order["cancellation_receiver"] = part1[2]
        parsed_order["callback_contract"] = part1[3]
        parsed_order["ui_fee_receiver"] = part1[4]
        parsed_order["market"] = part1[5]
        parsed_order["initial_collateral_token"] = part1[6]
        parsed_order["swap_path"] = part1[7]

        # Process part2
        parsed_order["order_type"] = part2[0]
        parsed_order["decrease_position_swap_type"] = part2[1]
        parsed_order["size_delta_usd"] = part2[2]
        parsed_order["init_collateral_delta_amount"] = part2[3]
        parsed_order["trigger_price"] = part2[4]
        parsed_order["acceptable_price"] = part2[5]
        parsed_order["execution_fee"] = part2[6]
        parsed_order["callback_gas_limit"] = part2[7]
        parsed_order["min_output_amount"] = part2[8]
        parsed_order["updated_at_block"] = part2[9]
        parsed_order["updated_at_time"] = part2[10]

        # Process part3
        parsed_order["is_long"] = part3[0]
        parsed_order["should_unwrap_native_token"] = part3[1]
        parsed_order["is_frozen"] = part3[2]
        parsed_order["auto_cancel"] = part3[3]

        parsed_orders.append(parsed_order)
    return parsed_orders


def get_account_orders(config: ConfigManager) -> list[dict[str, Any]]:
    """
    Get the account orders for the given chain.

    :param config: Configuration object.
    :return: A dictionary containing the account orders.
    """
    reader_contract = get_reader_contract(config)
    try:
        orders = reader_contract.functions.getAccountOrders(
            config.contracts.data_store.contract_address,
            config.user_wallet_address,
            0,
            1000,
        ).call()

        parsed_output: list[dict[str, Any]] = parse_account_orders(orders)
        return parsed_output

    except Exception as e:
        logging.error(f"Error fetching account orders: {e}")
        raise


def get_bytes_32_count(config: ConfigManager) -> int:
    """
    Get the bytes 32 count.

    :param config: Configuration object.
    :return: A dictionary containing the bytes 32 count.
    """
    data_store_contract = get_data_store_contract(config)
    try:
        output = data_store_contract.functions.getBytes32Count(
            account_order_list_key(config.user_wallet_address)
        ).call()

        return output
    except Exception as e:
        logging.error(f"Error fetching bytes 32 count: {e}")
        raise


def get_bytes_32_values_at(config: ConfigManager) -> list[HexBytes]:
    """
    Get the bytes 32 values.

    :param config: Configuration object.
    :return: A dictionary containing the bytes 32 values.
    """
    data_store_contract = get_data_store_contract(config)
    try:
        output = data_store_contract.functions.getBytes32ValuesAt(
            account_order_list_key(config.user_wallet_address),
            0,
            1000,
        ).call()

        return output
    except Exception as e:
        logging.error(f"Error fetching bytes 32 values: {e}")
        raise


def get_execution_price_and_price_impact(
    config: ConfigManager, params: dict[str, Any], decimals: int
) -> dict[str, Decimal]:
    """
    Get the execution price and price impact for a position.

    :param config: Configuration object.
    :param params: Dictionary of the position parameters.
    :param decimals: Number of decimals for the token being traded.
    :return: A dictionary containing the execution price and price impact.
    :raises Exception: If the Web3 call fails or returns invalid data.
    """
    reader_contract = get_reader_contract(config)

    try:
        output = reader_contract.functions.getExecutionPrice(
            params.get("data_store_address"),
            params.get("market_address"),
            params.get("index_token_price"),
            params.get("position_size_in_usd"),
            params.get("position_size_in_tokens"),
            params.get("size_delta"),
            params.get("is_long"),
        ).call()

        execution_price = (
            (to_decimal(output[2]) / Decimal(10) ** (30 - decimals)) if output and len(output) > 2 else Decimal("0")
        )
        price_impact_usd = (to_decimal(output[0]) / Decimal(10) ** 30) if output and len(output) > 0 else Decimal("0")

        logging.debug(f"Execution Price: {execution_price}, Price Impact USD: {price_impact_usd}")

        return {
            "execution_price": execution_price,
            "price_impact_usd": price_impact_usd,
        }

    except Exception as e:
        logging.error(f"Error fetching execution price and price impact: {e}")
        raise


def get_estimated_swap_output(config: ConfigManager, params: dict[str, Any]) -> dict[str, Decimal]:
    """
    Get the estimated swap output amount and price impact for a given chain and swap parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the swap parameters.
    :return: A dictionary with the estimated token output and price impact.
    :raises Exception: If the Web3 call fails or returns invalid data.
    """
    try:
        reader_contract: Contract = get_reader_contract(config)
        output: tuple[int, int, tuple] = reader_contract.functions.getSwapAmountOut(
            params.get("data_store_address"),
            params.get("market_addresses"),
            params.get("token_prices_tuple"),
            params.get("token_in"),
            params.get("token_amount_in"),
            params.get("ui_fee_receiver"),
        ).call()

        out_token_amount: Decimal = to_decimal(output[0])  # Assuming output[0] is token amount
        price_impact_usd: Decimal = to_decimal(output[1])  # Assuming output[1] is price impact

        logging.debug(f"Out Token Amount: {out_token_amount}, Price Impact USD: {price_impact_usd}")

        return {
            "out_token_amount": out_token_amount,
            "price_impact_usd": price_impact_usd,
        }

    except Exception as e:
        logging.error(f"Failed to get swap output: {e}")
        logging.info("Trying to decode custom error ...")

        try:
            cap: CustomErrorParser = CustomErrorParser(config=config)
            error_reason: dict[str, Any] = cap.parse_error(error_bytes=e.args[0])
            error_message: str = cap.get_error_string(error_reason=error_reason)
            logging.info(f"Parsed custom error: {error_message}")
        except Exception as parse_e:
            logging.error(f"Failed to parse custom error: {parse_e}")
            raise Exception("Failed to get swap output and parse custom error.") from e

        raise Exception("Failed to get swap output.")


def get_estimated_deposit_amount_out(config: ConfigManager, params: dict[str, Any]) -> int:
    """
    Get the estimated deposit amount output for a given chain and deposit parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the deposit parameters.
    :return: The output of the deposit amount calculation as an integer.
    :raises Exception: If the Web3 call fails or returns invalid data.
    """
    reader: Contract = get_reader_contract(config)

    try:
        output: int = reader.functions.getDepositAmountOut(
            params.get("data_store_address"),
            params.get("market_addresses"),
            params.get("token_prices_tuple"),
            params.get("long_token_amount"),
            params.get("short_token_amount"),
            params.get("ui_fee_receiver"),
            SwapPricingTypes.TWO_STEPS.value,
            True,
        ).call()

        logging.debug(f"Estimated Deposit Amount Out: {output}")

        return output

    except Exception as e:
        logging.error(f"Failed to get estimated deposit amount out: {e}")
        raise Exception("Failed to get estimated deposit amount out.") from e


def get_estimated_withdrawal_amount_out(config: ConfigManager, params: dict[str, Any]) -> tuple[Decimal, Decimal]:
    """
    Get the estimated withdrawal amount output for a given chain and withdrawal parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the withdrawal parameters.
    :return: The output of the withdrawal amount calculation as Decimal or None if an error occurs.
    :raises Exception: If the Web3 call fails or returns invalid data.
    """
    reader: Contract = get_reader_contract(config)

    try:
        output: int = reader.functions.getWithdrawalAmountOut(
            params.get("data_store_address"),
            params.get("market_addresses"),
            params.get("token_prices_tuple"),
            params.get("rp_amount"),
            params.get("ui_fee_receiver"),
            SwapPricingTypes.TWO_STEPS.value,
        ).call()

        min_long_token_amount: Decimal = to_decimal(output[0])
        min_short_token_amount: Decimal = to_decimal(output[1])
        logging.debug(f"Estimated Withdrawal Amount Out: {output}")

        return min_long_token_amount, min_short_token_amount

    except Exception as e:
        logging.error(f"Failed to get estimated withdrawal amount out: {e}")
        raise Exception("Failed to get estimated withdrawal amount out.") from e


def find_dictionary_by_key_value(
    outer_dict: dict[str, dict[str, Any]], key: str, value: Union[str, int, bool, Decimal]
) -> dict[str, Any]:
    """
    Search for a dictionary by key-value pair within an outer dictionary.

    :param outer_dict: The outer dictionary to search.
    :param key: The key to search for.
    :param value: The value to match.
    :return: The dictionary containing the matching key-value pair.
    :raises Exception: If no matching dictionary is found.
    """
    result: dict[str, Any] | None = next(
        (inner_dict for inner_dict in outer_dict.values() if inner_dict.get(key) == value), None
    )
    if result:
        logging.debug(f"Found dictionary for key='{key}', value='{value}'.")
        return result
    else:
        logging.error(f"No dictionary found for key='{key}', value='{value}'.")
        raise Exception(f"No dictionary found for key='{key}', value='{value}'.")


def save_json(output_data_path: Path, file_name: str, data: dict[str, Any]) -> None:
    """
    Save a dictionary as a JSON file in the specified directory.

    :param output_data_path: The output data path.
    :param file_name: Name of the JSON file.
    :param data: Dictionary data to save.
    """
    output_data_path.mkdir(parents=True, exist_ok=True)
    file_path = output_data_path / file_name
    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, cls=DecimalEncoder, ensure_ascii=False, indent=4)

        logging.info(f"Data saved to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save JSON data to {file_path}: {e}")
        raise


def save_csv(output_data_path: Path, file_name: str, data: DataFrame) -> None:
    """
    Save a Pandas DataFrame as a CSV file in the specified directory.

    :param output_data_path: The output data path.
    :param file_name: Name of the CSV file.
    :param data: Pandas DataFrame to save.
    """
    output_data_path.mkdir(parents=True, exist_ok=True)
    file_path = output_data_path / file_name
    try:
        # Convert Decimal columns to string to prevent issues with CSV serialization
        for column in data.select_dtypes(include=[Decimal]).columns:
            data[column] = data[column].astype(str)

        # Append to existing file if it exists
        if file_path.exists():
            existing_data = pd.read_csv(file_path, dtype=str)
            data = pd.concat([existing_data, data], ignore_index=True)

        data.to_csv(file_path, index=False)
        logging.info(f"DataFrame saved to: {file_path}")
    except Exception as e:
        logging.error(f"Failed to save CSV data to {file_path}: {e}")
        raise


def timestamp_df(data: dict[str, Any]) -> DataFrame:
    """
    Convert a dictionary into a Pandas DataFrame with a timestamp column.

    :param data: Dictionary data to convert.
    :return: DataFrame with timestamp column added.
    """
    data_with_timestamp = data.copy()
    data_with_timestamp["timestamp"] = datetime.now(timezone.utc)
    logging.debug("Timestamp added to DataFrame.")
    return DataFrame([data_with_timestamp])


def to_decimal(value: Union[float, str, int, Decimal, None]) -> Decimal | None:
    """
    Safely converts a floating-point number, integer, string, or Decimal to a Decimal object to preserve precision.

    :param value: The float, int, string, or Decimal number to convert.
    :return: The precise Decimal representation of the input.
    :raises ValueError: If the input cannot be converted to Decimal.
    """
    if isinstance(value, Decimal):
        return value  # Already a Decimal, no conversion needed

    if value is None:
        return None

    try:
        # Convert the value to string first to avoid floating-point issues
        decimal_value = Decimal(str(value))
        logging.debug(f"Converted value '{value}' to Decimal: {decimal_value}")
        return decimal_value
    except (InvalidOperation, ValueError, TypeError) as e:
        logging.error(f"Error converting value to Decimal: {value}. Error: {e}")
        raise ValueError(f"Cannot convert value to Decimal: {value}") from e
