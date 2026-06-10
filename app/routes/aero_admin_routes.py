from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.aero_user_model import User
from app.schemas.aero_user_schema import UserResponseSchema
from app.core.auth import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Get user details by user ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[UserResponseSchema])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Get a list of all users (admin only)."""
    users = db.query(User).all()
    return users
