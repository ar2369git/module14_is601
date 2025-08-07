from typing import Union
import logging
from app.models.calculation import CalculationType

# Initialize logger for this module
logger = logging.getLogger(__name__)

Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    result = a + b
    logger.info(f"add: {a} + {b} = {result}")
    return result

def subtract(a: Number, b: Number) -> Number:
    result = a - b
    logger.info(f"subtract: {a} - {b} = {result}")
    return result

def multiply(a: Number, b: Number) -> Number:
    result = a * b
    logger.info(f"multiply: {a} * {b} = {result}")
    return result

def divide(a: Number, b: Number) -> float:
    if b == 0:
        logger.error(f"divide: attempt to divide {a} by zero")
        raise ValueError("Cannot divide by zero!")
    result = a / b
    logger.info(f"divide: {a} / {b} = {result}")
    return result
def perform_operation(calc_type: CalculationType, a: float, b: float) -> float:
    """
    Execute the calculation for the given type and operands.
    Raises ValueError on divide-by-zero or unsupported types.
    """
    if calc_type == CalculationType.Add:
        return a + b
    elif calc_type == CalculationType.Subtract:
        return a - b
    elif calc_type == CalculationType.Multiply:
        return a * b
    elif calc_type == CalculationType.Divide:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    else:
        raise ValueError(f"Unsupported calculation type: {calc_type}")