from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.models.models import UserRole

router = APIRouter()

@router.post("/", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate
) -> Any:
    user = crud.crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    return crud.crud_user.create_user(db, obj_in=user_in)

@router.get("/me", response_model=schemas.user.User)
def read_user_me(
    current_user: models.models.User = Depends(deps.get_current_user),
) -> Any:
    return current_user

@router.get("/", response_model=List[schemas.user.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.models.User = Depends(deps.RoleChecker([UserRole.ADMIN])),
) -> Any:
    users = db.query(models.models.User).offset(skip).limit(limit).all()
    return users
