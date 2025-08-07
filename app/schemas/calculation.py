# app/schemas/calculation.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator
from app.models.calculation import CalculationType


class CalculationBase(BaseModel):
    a: float
    b: float
    type: CalculationType

    @model_validator(mode="after")
    def check_divide_by_zero(cls, model):
        if model.type == CalculationType.Divide and model.b == 0:
            raise ValueError("Division by zero is not allowed")
        return model


class CalculationCreate(CalculationBase):
    """Payload for creating a new calculation."""
    pass


class CalculationRead(CalculationBase):
    id: int
    result: float
    created_at: datetime
    owner_id: int

    model_config = {"from_attributes": True}


class CalculationUpdate(BaseModel):
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[CalculationType] = None

    @model_validator(mode="after")
    def check_divide_by_zero_on_update(cls, model):
        # Only enforce when both type and b are provided
        if model.type == CalculationType.Divide and model.b == 0:
            raise ValueError("Division by zero is not allowed")
        return model


# ─── Compatibility aliases ────────────────────────────────────────────────────

# main.py and routers still expect these names:
CalculationIn = CalculationCreate
CalculationOut = CalculationRead
