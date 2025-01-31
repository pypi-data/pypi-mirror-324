import logging
from decimal import Decimal
from typing import Any, Final, Union

from eth_abi import encode
from web3 import Web3


def create_hash(data_types: list[str], data_values: list[Union[str, int, bool, Decimal]]) -> bytes:
    """
    Create a keccak hash using a list of data types and their corresponding values.

    :param data_types: List of data types as strings.
    :param data_values: List of values corresponding to the data types.
    :return: Encoded and hashed key in bytes.
    :raises ValueError: If data types and values lengths do not match.
    """
    if len(data_types) != len(data_values):
        logging.error("Data types and data values lists must have the same length.")
        raise ValueError("Data types and data values lists must have the same length.")

    try:
        # Convert Decimal to string to prevent encoding issues
        processed_values = [str(value) if isinstance(value, Decimal) else value for value in data_values]
        encoded_data = encode(data_types, processed_values)
        hash_key = Web3.keccak(encoded_data)
        logging.debug(f"Hash created successfully: {hash_key.hex()}")
        return hash_key
    except Exception as e:
        logging.error(f"Error creating hash: {e}")
        raise


def create_hash_string(string: str) -> bytes:
    """
    Create a keccak hash for a given string.

    :param string: The string to hash.
    :return: Hashed string in bytes.
    """
    return create_hash(["string"], [string])


# Precomputed hash strings for various keys
_PARTIAL_KEYS: Final[dict[str, bytes]] = {
    "ACCOUNT_ORDER_LIST": create_hash_string("ACCOUNT_ORDER_LIST"),
    "DEPOSIT_GAS_LIMIT": create_hash_string("DEPOSIT_GAS_LIMIT"),
    "ACCOUNT_POSITION_LIST": create_hash_string("ACCOUNT_POSITION_LIST"),
    "CLAIMABLE_FEE_AMOUNT": create_hash_string("CLAIMABLE_FEE_AMOUNT"),
    "MIN_COLLATERAL_FACTOR": create_hash_string("MIN_COLLATERAL_FACTOR"),
    "MAX_OPEN_INTEREST": create_hash_string("MAX_OPEN_INTEREST"),
    "MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS": create_hash_string("MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS"),
    "OPEN_INTEREST_IN_TOKENS": create_hash_string("OPEN_INTEREST_IN_TOKENS"),
    "OPEN_INTEREST": create_hash_string("OPEN_INTEREST"),
    "OPEN_INTEREST_RESERVE_FACTOR": create_hash_string("OPEN_INTEREST_RESERVE_FACTOR"),
    "POOL_AMOUNT": create_hash_string("POOL_AMOUNT"),
    "RESERVE_FACTOR": create_hash_string("RESERVE_FACTOR"),
    "VIRTUAL_TOKEN_ID": create_hash_string("VIRTUAL_TOKEN_ID"),
}

# Precomputed hash strings for various keys
KEYS: Final[dict[str, bytes]] = {
    "DECREASE_ORDER_GAS_LIMIT": create_hash_string("DECREASE_ORDER_GAS_LIMIT"),
    "EXECUTION_GAS_FEE_BASE_AMOUNT": create_hash_string("EXECUTION_GAS_FEE_BASE_AMOUNT_V2_1"),
    "EXECUTION_GAS_FEE_MULTIPLIER_FACTOR": create_hash_string("EXECUTION_GAS_FEE_MULTIPLIER_FACTOR"),
    "INCREASE_ORDER_GAS_LIMIT": create_hash_string("INCREASE_ORDER_GAS_LIMIT"),
    "MAX_PNL_FACTOR_FOR_DEPOSITS": create_hash_string("MAX_PNL_FACTOR_FOR_DEPOSITS"),
    "MAX_PNL_FACTOR_FOR_TRADERS": create_hash_string("MAX_PNL_FACTOR_FOR_TRADERS"),
    "MAX_PNL_FACTOR_FOR_WITHDRAWALS": create_hash_string("MAX_PNL_FACTOR_FOR_WITHDRAWALS"),
    "MIN_ADDITIONAL_GAS_FOR_EXECUTION": create_hash_string("MIN_ADDITIONAL_GAS_FOR_EXECUTION"),
    "MIN_COLLATERAL_USD": create_hash_string("MIN_COLLATERAL_USD"),
    "MIN_POSITION_SIZE_USD": create_hash_string("MIN_POSITION_SIZE_USD"),
    "ORDER_LIST_KEY": create_hash_string("ORDER_LIST_KEY"),
    "SINGLE_SWAP_GAS_LIMIT": create_hash_string("SINGLE_SWAP_GAS_LIMIT"),
    "SWAP_ORDER_GAS_LIMIT": create_hash_string("SWAP_ORDER_GAS_LIMIT"),
    "WITHDRAWAL_GAS_LIMIT": create_hash_string("WITHDRAWAL_GAS_LIMIT"),
}


def create_key(key_name: str, data_types: list[str], data_values: list[Any]) -> bytes:
    """
    Generic function to create a hash key.

    :param key_name: The key name in KEYS dictionary.
    :param data_types: The data types for hashing.
    :param data_values: The data values for hashing.
    :return: The hashed key.
    """
    return create_hash(data_types=data_types, data_values=[_PARTIAL_KEYS[key_name], *data_values])


def account_order_list_key(account: str) -> bytes:
    """
    Generate a hash key for the account orders list.

    :param account: The account address.
    :return: The hashed key for the account order list.
    """
    return create_key("ACCOUNT_ORDER_LIST", ["bytes32", "address"], [account])


def deposit_gas_limit_key(single_token: bool) -> bytes:
    """
    Generate a hash key for the deposit gas limit.

    :param single_token: True if it is a deposit for single token.
    :return: The hashed key for the deposit gas limit.
    """
    return create_key("DEPOSIT_GAS_LIMIT", ["bytes32", "bool"], [single_token])


def account_position_list_key(account: str) -> bytes:
    """
    Generate a hash key for the account position list.

    :param account: The account address.
    :return: The hashed key for the account position list.
    """
    return create_key("ACCOUNT_POSITION_LIST", ["bytes32", "address"], [account])


def claimable_fee_amount_key(market: str, token: str) -> bytes:
    """
    Generate a hash key for claimable fee amount.

    :param market: The market address.
    :param token: The token address.
    :return: The hashed key for the claimable fee amount.
    """
    return create_key("CLAIMABLE_FEE_AMOUNT", ["bytes32", "address", "address"], [market, token])


def min_collateral_factor_key(market: str) -> bytes:
    """
    Generate a hash key for the minimum collateral factor for a market.

    :param market: The market address.
    :return: The hashed key for the minimum collateral factor.
    """
    return create_key("MIN_COLLATERAL_FACTOR", ["bytes32", "address"], [market])


def max_open_interest_key(market: str, is_long: bool) -> bytes:
    """
    Generate a hash key for the maximum open interest in a market.

    :param market: The market address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for maximum open interest.
    """
    return create_key("MAX_OPEN_INTEREST", ["bytes32", "address", "bool"], [market, is_long])


def max_position_impact_factor_for_liquidations_key(market: str) -> bytes:
    """
    Generate a hash key for the maximum position impact factor for liquidations in a market.

    :param market: The market address.
    :return: The hashed key for the maximum position impact factor for liquidations.
    """
    return create_key("MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS", ["bytes32", "address"], [market])


def open_interest_in_tokens_key(market: str, collateral_token: str, is_long: bool) -> bytes:
    """
    Generate a hash key for open interest in tokens.

    :param market: The market address.
    :param collateral_token: The collateral token address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for open interest in tokens.
    """
    return create_key(
        "OPEN_INTEREST_IN_TOKENS", ["bytes32", "address", "address", "bool"], [market, collateral_token, is_long]
    )


def open_interest_key(market: str, collateral_token: str, is_long: bool) -> bytes:
    """
    Generate a hash key for open interest.

    :param market: The market address.
    :param collateral_token: The collateral token address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for open interest.
    """
    return create_key("OPEN_INTEREST", ["bytes32", "address", "address", "bool"], [market, collateral_token, is_long])


def open_interest_reserve_factor_key(market: str, is_long: bool) -> bytes:
    """
    Generate a hash key for the open interest reserve factor in a market.

    :param market: The market address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for open interest reserve factor.
    """
    return create_key("OPEN_INTEREST_RESERVE_FACTOR", ["bytes32", "address", "bool"], [market, is_long])


def pool_amount_key(market: str, token: str) -> bytes:
    """
    Generate a hash key for the pool amount in a market.

    :param market: The market address.
    :param token: The token address.
    :return: The hashed key for the pool amount.
    """
    return create_key("POOL_AMOUNT", ["bytes32", "address", "address"], [market, token])


def reserve_factor_key(market: str, is_long: bool) -> bytes:
    """
    Generate a hash key for the reserve factor in a market.

    :param market: The market address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for reserve factor.
    """
    return create_key("RESERVE_FACTOR", ["bytes32", "address", "bool"], [market, is_long])


def virtual_token_id_key(token: str) -> bytes:
    """
    Generate a hash key for the virtual token ID.

    :param token: The token address.
    :return: The hashed key for virtual token ID.
    """
    return create_key("VIRTUAL_TOKEN_ID", ["bytes32", "address"], [token])
