# app/routers/calculations.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.calculation import Calculation
from app.schemas.calculation import (
    CalculationCreate,
    CalculationUpdate,
    CalculationOut,
)
from app.operations import perform_operation
from app.dependencies import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.get("", response_model=List[CalculationOut])
def browse_calculations(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return (
        db.query(Calculation)
        .filter(Calculation.user_id == current_user.id)
        .all()
    )

@router.get("/{calc_id}", response_model=CalculationOut)
def read_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    calc = (
        db.query(Calculation)
        .filter_by(id=calc_id, user_id=current_user.id)
        .first()
    )
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

@router.post("", response_model=CalculationOut, status_code=status.HTTP_201_CREATED)
def add_calculation(
    payload: CalculationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = perform_operation(payload.type, payload.a, payload.b)
    calc = Calculation(
        a=payload.a,
        b=payload.b,
        type=payload.type,
        result=result,
        user_id=current_user.id,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

@router.put("/{calc_id}", response_model=CalculationOut)
def edit_calculation(
    calc_id: int,
    payload: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    calc = (
        db.query(Calculation)
        .filter_by(id=calc_id, user_id=current_user.id)
        .first()
    )
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    if payload.a is not None:
        calc.a = payload.a
    if payload.b is not None:
        calc.b = payload.b
    if payload.type is not None:
        calc.type = payload.type
    calc.result = perform_operation(calc.type, calc.a, calc.b)
    db.commit()
    db.refresh(calc)
    return calc

@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    calc = (
        db.query(Calculation)
        .filter_by(id=calc_id, user_id=current_user.id)
        .first()
    )
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()
    return
