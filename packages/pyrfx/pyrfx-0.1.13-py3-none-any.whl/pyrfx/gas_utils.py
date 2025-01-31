import logging
from decimal import Decimal, InvalidOperation
from typing import Optional, TypedDict, Union

from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import BlockData

from pyrfx.config_manager import ConfigManager
from pyrfx.keys import KEYS, deposit_gas_limit_key
from pyrfx.utils import to_decimal


# Define a TypedDict for gas_limits to ensure type safety and clarity
class GasLimits(TypedDict):
    single_deposit: ContractFunction
    multiple_deposit: ContractFunction
    decrease_order: ContractFunction
    increase_order: ContractFunction
    single_swap_order: ContractFunction
    multiple_swap_order: ContractFunction
    withdraw: ContractFunction
    execution_base_amount: ContractFunction
    execution_multiplier_factor: ContractFunction


def get_execution_fee(
    gas_limits: GasLimits,
    estimated_gas_limit_contract_function: ContractFunction,
    gas_price: Union[int, str, float, Decimal],
) -> Decimal:
    """
    Calculate the minimum execution fee required to perform an action based on gas limits and gas price.

    :param gas_limits: A dictionary of uncalled datastore limit functions.
    :param estimated_gas_limit_contract_function: The uncalled datastore contract function specific to the operation
        being undertaken.
    :param gas_price: The current gas price. Can be int, float, str, or Decimal.
    :return: The adjusted gas fee as a Decimal to cover the execution cost.
    :raises ValueError: If any of the required gas limit functions fail or return invalid data.
    """

    try:
        # Fetch base gas limit and multiplier factor using ContractFunction.call()
        base_gas_limit = to_decimal(gas_limits["execution_base_amount"].call())
        multiplier_factor = to_decimal(gas_limits["execution_multiplier_factor"].call())
        estimated_gas = to_decimal(estimated_gas_limit_contract_function.call())

        logging.debug(f"Base Gas Limit: {base_gas_limit}")
        logging.debug(f"Multiplier Factor: {multiplier_factor}")
        logging.debug(f"Estimated Gas: {estimated_gas}")

        # Calculate adjusted gas limit
        adjusted_gas_limit = base_gas_limit + (estimated_gas * multiplier_factor) / Decimal(10**30)
        logging.debug(f"Adjusted Gas Limit: {adjusted_gas_limit}")

        # Convert gas_price to Decimal
        gas_price_decimal = to_decimal(gas_price)
        logging.debug(f"Gas Price: {gas_price_decimal}")

        # Calculate execution fee: adjusted_gas_limit * gas_price
        execution_fee = adjusted_gas_limit * gas_price_decimal
        logging.info(f"Calculated Execution Fee: {execution_fee}")

        return execution_fee

    except KeyError as e:
        logging.error(f"Missing gas limit key: {e}")
        raise ValueError(f"Missing gas limit key: {e}") from e
    except (InvalidOperation, TypeError) as e:
        logging.error(f"Invalid data type encountered during execution fee calculation: {e}")
        raise ValueError(f"Invalid data type encountered during execution fee calculation: {e}") from e
    except Exception as e:
        logging.error(f"Error calculating execution fee: {e}")
        raise ValueError(f"Error calculating execution fee: {e}") from e


def get_gas_limits(datastore_object: Contract) -> GasLimits:
    """
    Retrieve gas limit functions from the datastore contract for various operations requiring execution fees.

    :param datastore_object: A Web3 contract object for accessing the datastore.
    :return: A dictionary of uncalled gas limit functions corresponding to various operations.
    :raises ValueError: If any of the required gas limit functions are missing or invalid.
    """
    try:
        # Define the gas limit keys
        gas_limit_keys = {
            "single_deposit": deposit_gas_limit_key(single_token=True),
            "multiple_deposit": deposit_gas_limit_key(single_token=False),
            "decrease_order": KEYS["DECREASE_ORDER_GAS_LIMIT"],
            "increase_order": KEYS["INCREASE_ORDER_GAS_LIMIT"],
            "single_swap_order": KEYS["SINGLE_SWAP_GAS_LIMIT"],
            "multiple_swap_order": KEYS["SWAP_ORDER_GAS_LIMIT"],
            "withdraw": KEYS["WITHDRAWAL_GAS_LIMIT"],
            "execution_base_amount": KEYS["EXECUTION_GAS_FEE_BASE_AMOUNT"],
            "execution_multiplier_factor": KEYS["EXECUTION_GAS_FEE_MULTIPLIER_FACTOR"],
        }

        # Retrieve ContractFunction instances for each gas limit
        gas_limits: GasLimits = {}
        for key, gas_key in gas_limit_keys.items():
            try:
                contract_function = datastore_object.functions.getUint(gas_key)
                if not isinstance(contract_function, ContractFunction):
                    logging.error(f"Gas limit function for '{key}' is not a valid ContractFunction.")
                    raise ValueError(f"Gas limit function for '{key}' is not a valid ContractFunction.")
                gas_limits[key] = contract_function
                logging.debug(f"Gas limit function for '{key}' retrieved successfully.")
            except AttributeError as e:
                logging.error(f"ContractFunction retrieval failed for key '{key}': {e}")
                raise ValueError(f"ContractFunction retrieval failed for key '{key}': {e}") from e

        logging.info("All gas limit functions retrieved successfully.")
        return gas_limits

    except KeyError as e:
        logging.error(f"Missing key in KEYS dictionary: {e}")
        raise ValueError(f"Missing key in KEYS dictionary: {e}") from e
    except Exception as e:
        logging.error(f"Unexpected error while retrieving gas limits: {e}")
        raise ValueError(f"Unexpected error while retrieving gas limits: {e}") from e


def get_max_fee_per_gas(config: ConfigManager) -> Decimal:
    """
    Retrieve the latest block base fee and calculate the max fee per gas with a multiplier.

    :return: Max fee per gas as Decimal.
    :raises ValueError: If base fee per gas is not available.
    """
    try:
        latest_block: BlockData = config.connection.eth.get_block("latest")
        base_fee_per_gas: Optional[int] = latest_block.get("baseFeePerGas")

        if base_fee_per_gas is None:
            # Fallback mechanism or raise an error if EIP-1559 is not supported
            logging.error("Base fee per gas is not available for the latest block.")
            raise ValueError("Base fee per gas is not available for the latest block.")

        max_fee = to_decimal(base_fee_per_gas) * Decimal("1.35")
        logging.debug(f"Calculated max_fee_per_gas: {max_fee}")
        return max_fee

    except Exception as e:
        logging.error(f"Failed to retrieve max fee per gas: {e}")
        raise Exception(f"Failed to retrieve max fee per gas: {e}")
