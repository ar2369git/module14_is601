# app/routers/calculations.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.calculation import Calculation as CalculationModel
from app.models.user import User as UserModel
from app.schemas.calculation import CalculationIn, CalculationOut
from app.operations import perform_operation
from app.security import get_current_user
from app.models.calculation import Calculation
from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
    CalculationUpdate,
)

router = APIRouter(
    prefix="/calculations",
    tags=["calculations"],
)


@router.get(
    "/",
    response_model=List[CalculationOut],
    summary="List all calculations for the current user",
)
def list_calculations(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return (
        db.query(CalculationModel)
          .filter(CalculationModel.user_id == current_user.id)
          .all()
    )


@router.post(
    "/",
    response_model=CalculationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new calculation",
)
def create_calculation(
    data: CalculationIn,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # perform the math
    result = perform_operation(data.type, data.a, data.b)
    # build and persist
    calc = CalculationModel(
        a=data.a,
        b=data.b,
        type=data.type,
        result=result,
        user_id=current_user.id,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


@router.get(
    "/{calc_id}",
    response_model=CalculationOut,
    summary="Get a single calculation by ID",
)
def read_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    calc = (
        db.query(CalculationModel)
          .filter(
              CalculationModel.id == calc_id,
              CalculationModel.user_id == current_user.id
          )
          .first()
    )
    if not calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    return calc


@router.put(
    "/{calc_id}",
    response_model=CalculationOut,
    summary="Update an existing calculation",
)
def update_calculation(
    calc_id: int,
    data: CalculationIn,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    calc = (
        db.query(CalculationModel)
          .filter(
              CalculationModel.id == calc_id,
              CalculationModel.user_id == current_user.id
          )
          .first()
    )
    if not calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    calc.a = data.a
    calc.b = data.b
    calc.type = data.type
    calc.result = perform_operation(data.type, data.a, data.b)
    db.commit()
    db.refresh(calc)
    return calc


@router.delete(
    "/{calc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a calculation",
)
def delete_calculation(
    calc_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    calc = (
        db.query(CalculationModel)
          .filter(
              CalculationModel.id == calc_id,
              CalculationModel.user_id == current_user.id
          )
          .first()
    )
    if not calc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    db.delete(calc)
    db.commit()
    # 204 No Content returns an empty body

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

    # apply updates
    for field, val in payload.dict(exclude_unset=True).items():
        setattr(calc, field, val)

    # re-compute result if a/b/type changed
    try:
        calc.result = perform_operation(calc.type, calc.a, calc.b)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    db.commit()
    db.refresh(calc)
    return calc