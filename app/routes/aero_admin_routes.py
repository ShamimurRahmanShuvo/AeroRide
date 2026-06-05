from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.aero_user_model import AeroUser, Role, UserRole
from app.schemas.aero_user_schema import (
    CurrentUserResponseSchema,
    RoleRequestSchema,
    RoleResponseSchema,
    UserRoleAssignmentSchema,
    UserProfileSchema
)
from app.core.auth import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/create-role", response_model=RoleRequestSchema)
def create_role(role_data: RoleRequestSchema,
                db: Session = Depends(get_db),
                current_user=Depends(require_role("admin"))):
    """Create a new role (admin only)."""
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role(name=role_data.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return new_role


@router.get("/roles", response_model=List[RoleResponseSchema])
def get_roles(db: Session = Depends(get_db), current_user=Depends(require_role("admin"))):
    """Get a list of all roles (admin only)."""
    roles = db.query(Role).all()
    return roles


@router.post("/assign-role", response_model=UserRoleAssignmentSchema)
def assign_role_to_user(assignment_data: UserRoleAssignmentSchema,
                        db: Session = Depends(get_db),
                        current_user=Depends(require_role("admin"))):
    """Assign a role to a user (admin only)."""
    user = db.query(AeroUser).filter(AeroUser.id == assignment_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = db.query(Role).filter(Role.id == assignment_data.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    existing_assignment = db.query(UserRole).filter(
        UserRole.user_id == assignment_data.user_id,
        UserRole.role_id == assignment_data.role_id
    ).first()
    if existing_assignment:
        raise HTTPException(status_code=400, detail="User already has this role")

    new_assignment = UserRole(user_id=assignment_data.user_id, role_id=assignment_data.role_id)
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment


@router.get("/users/{user_id}", response_model=CurrentUserResponseSchema)
def get_user_details(user_id: int,
                     db: Session = Depends(get_db),
                     current_user=Depends(require_role("admin"))):
    """Get details of a specific user (admin only)."""
    user = db.query(AeroUser).filter(AeroUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return CurrentUserResponseSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_varified=user.is_varified,
        created_at=user.created_at,
        updated_at=user.updated_at,
        roles=[user_role.roles.name for user_role in current_user.roles],
        profile=UserProfileSchema.from_orm(user.profiles) if user.profiles else None
    )


@router.get("/users", response_model=List[CurrentUserResponseSchema])
def get_all_users(db: Session = Depends(get_db),
                  current_user=Depends(require_role("admin"))):
    """Get a list of all users (admin only)."""
    users = db.query(AeroUser).all()
    return [
        CurrentUserResponseSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_varified=user.is_varified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=[user_role.roles.name for user_role in current_user.roles],
            profile=UserProfileSchema.from_orm(user.profiles) if user.profiles else None
        )
        for user in users
    ]
