from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.models import AuditLog

router = APIRouter()

@router.post("/login/access-token", response_model=schemas.user.Token)
def login_access_token(
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    
    # Audit Logging
    audit = AuditLog(
        user_id=user.id if user else None,
        action="LOGIN_ATTEMPT",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        details=f"Login attempt for email: {form_data.username} - {'SUCCESS' if user else 'FAILED'}"
    )
    db.add(audit)
    db.commit()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }
