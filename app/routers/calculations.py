# app/routers/calculations.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate, CalculationRead, CalculationUpdate
from app.operations import perform_operation
from app.security import get_current_user

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.get("/", response_model=List[CalculationRead])
def browse_calculations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Retrieve all calculations belonging to the current user.
    """
    calculations = (
        db.query(Calculation)
          .filter(Calculation.owner_id == user.id)
          .order_by(Calculation.created_at.desc())
          .all()
    )
    return calculations

@router.get("/{calc_id}", response_model=CalculationRead)
def read_calculation(calc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    calc = db.get(Calculation, calc_id)
    if not calc or calc.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return calc

@router.post("/", response_model=CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(payload: CalculationCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # run the math
    try:
        result = perform_operation(payload.type, payload.a, payload.b)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    calc = Calculation(owner_id=user.id, a=payload.a, b=payload.b, type=payload.type, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

@router.put("/{calc_id}", response_model=CalculationRead)
@router.patch("/{calc_id}", response_model=CalculationRead)
def edit_calculation(
    calc_id: int,
    payload: CalculationUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    calc = db.get(Calculation, calc_id)
    if not calc or calc.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # update fields
    for field, val in payload.dict(exclude_unset=True).items():
        setattr(calc, field, val)
    # re-run the operation if any of a/b/type changed
    try:
        calc.result = perform_operation(calc.type, calc.a, calc.b)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    db.commit()
    db.refresh(calc)
    return calc

@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    calc = db.get(Calculation, calc_id)
    if not calc or calc.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(calc)
    db.commit()
    return
