from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class CalculationType(str, Enum):
    Add = "Add"
    Subtract = "Subtract"
    Multiply = "Multiply"
    Divide = "Divide"


class CalculationBase(BaseModel):
    a: float = Field(..., description="Left operand")
    b: float = Field(..., description="Right operand")
    type: CalculationType = Field(..., description="Operation type")

    @model_validator(mode="before")
    def no_divide_by_zero(cls, values: dict):
        # only validate raw JSON input (a dict)
        if isinstance(values, dict):
            t = values.get("type")
            b = values.get("b")
            if t in (CalculationType.Divide, "Divide") and b == 0:
                raise ValueError("Division by zero is not allowed")
        return values


class CalculationCreate(CalculationBase):
    """Payload for POST /calculations"""
    pass


class CalculationRead(CalculationBase):
    """Response model for GET endpoints"""
    id: int
    result: float
    created_at: datetime

    model_config = {"from_attributes": True}


class CalculationUpdate(BaseModel):
    """Payload for PUT/PATCH /calculations/{id}"""
    a: Optional[float] = Field(None, description="Left operand")
    b: Optional[float] = Field(None, description="Right operand")
    type: Optional[CalculationType] = Field(None, description="Operation type")

    @model_validator(mode="before")
    def no_divide_by_zero_on_update(cls, values: dict):
        if isinstance(values, dict):
            t = values.get("type")
            b = values.get("b")
            if t in (CalculationType.Divide, "Divide") and b == 0:
                raise ValueError("Division by zero is not allowed")
        return values


# Aliases to match existing imports:
CalculationIn = CalculationCreate
CalculationOut = CalculationRead