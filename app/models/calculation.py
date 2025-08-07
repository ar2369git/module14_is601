# app/models/calculation.py

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db import Base

class CalculationType(enum.Enum):
    Add = "Add"
    Subtract = "Subtract"
    Multiply = "Multiply"
    Divide = "Divide"


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(Enum(CalculationType), nullable=False)
    result = Column(Float, nullable=False)

    # This is your one and only FK to users
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="calculations")
