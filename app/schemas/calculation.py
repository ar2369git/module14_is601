# app/schemas/calculation.py

from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, root_validator, Field

class CalculationType(str, Enum):
    Add = "Add"
    Subtract = "Subtract"
    Multiply = "Multiply"
    Divide = "Divide"


class CalculationBase(BaseModel):
    type: CalculationType = Field(..., description="The operation to perform")
    a: float = Field(..., description="Left operand")
    b: float = Field(..., description="Right operand")

    # Prevent divide-by-zero at the schema level
    @root_validator(skip_on_failure=True)
    def no_divide_by_zero(cls, values):
        if values.get("type") == CalculationType.Divide and values.get("b") == 0:
            raise ValueError("Division by zero is not allowed")
        return values


class CalculationIn(CalculationBase):
    """Input schema for creating or updating a calculation."""
    pass


class CalculationOut(CalculationBase):
    """What we send back to the client."""
    id: int
    result: float
    created_at: datetime

    class Config:
        # Pydantic v2: use from_attributes instead of orm_mode
        from_attributes = True

class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
    a: Optional[float] = Field(None, description="New left operand")
    b: Optional[float] = Field(None, description="New right operand")
    type: Optional[CalculationType] = Field(None, description="New operation type")

    # Only run this if both type and b are provided in the update
    @model_validator(mode="before", skip_on_failure=True)
    def no_divide_by_zero_on_update(cls, values):
        t = values.get("type")
        b = values.get("b")
        if t is CalculationType.Divide and b == 0:
            raise ValueError("Division by zero is not allowed")
        return values


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: float
    created_at: datetime

    class Config:
        from_attributes = True