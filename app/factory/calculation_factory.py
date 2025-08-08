# app/factory/calculation_factory.py

from typing import Union
from app.models.calculation import CalculationType
from app.operations import add, subtract, multiply, divide

Number = Union[int, float]

def compute(calc_type: Union[CalculationType, str], a: float, b: float) -> float:
    # allow passing the enum *or* its name as a string
    if isinstance(calc_type, str):
        try:
            calc_type = CalculationType[calc_type]
        except KeyError:
            raise ValueError(f"Unsupported calculation type: {calc_type}")

    if calc_type == CalculationType.Add:
        return add(a, b)
    elif calc_type == CalculationType.Subtract:
        return subtract(a, b)
    elif calc_type == CalculationType.Multiply:
        return multiply(a, b)
    elif calc_type == CalculationType.Divide:
        return divide(a, b)
    else:
        raise ValueError(f"Unsupported calculation type: {calc_type}")