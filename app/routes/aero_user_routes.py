from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.aero_user_model import AeroUser, Role, UserProfile, UserRole
from app.schemas.aero_user_schema import (RegisterUserSchema, LoginUserSchema, TokenResponseSchema, UserProfileSchema,
                                          CurrentUserResponseSchema, RoleResponseSchema, RoleRequestSchema,
                                          UserRoleAssignmentSchema)
from app.core.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register-user", response_model=CurrentUserResponseSchema)
def register_user(user_data: RegisterUserSchema, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(AeroUser).filter(
        (AeroUser.username == user_data.username) | (AeroUser.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = hash_password(user_data.password_hash)
    new_user = AeroUser(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        is_active=True,
        is_varified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Assign default role
    default_role = db.query(Role).filter(Role.name == "user").first()
    if default_role:
        user_role = UserRole(user_id=new_user.id, role_id=default_role.id)
        db.add(user_role)
        db.commit()
        db.refresh(user_role)

    db.commit()
    db.refresh(new_user)

    return CurrentUserResponseSchema(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        is_active=new_user.is_active,
        is_varified=new_user.is_varified,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
        roles=[default_role.name] if default_role else []
    )


@router.post("/login", response_model=TokenResponseSchema)
def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(AeroUser).filter(AeroUser.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Username")
    stored_hash = getattr(user, "password_hash", None) or getattr(user, "password_hash")

    if not verify_password(form_data.password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid Password")

    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})

    return TokenResponseSchema(access_token=access_token, token_type="bearer")


@router.get("/current-user", response_model=CurrentUserResponseSchema)
def get_current_user_info(current_user: AeroUser = Depends(get_current_user)):
    """Get current authenticated user information."""
    return CurrentUserResponseSchema(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        is_varified=current_user.is_varified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        roles=[user_role.roles.name for user_role in current_user.roles],
        profile=UserProfileSchema(
            user_id=current_user.id,
            first_name=current_user.profiles.first_name if current_user.profiles else None,
            last_name=current_user.profiles.last_name if current_user.profiles else None,
            date_of_birth=current_user.profiles.date_of_birth if current_user.profiles else None,
            phone_number=current_user.profiles.phone_number if current_user.profiles else None,
            address=current_user.profiles.address if current_user.profiles else None,
            city=current_user.profiles.city if current_user.profiles else None,
            province=current_user.profiles.province if current_user.profiles else None,
            country=current_user.profiles.country if current_user.profiles else None,
            postal_code=current_user.profiles.postal_code if current_user.profiles else None,
            profile_picture_url=current_user.profiles.profile_picture_url if current_user.profiles else None
        ) if current_user.profiles else None
    )


@router.post("/create-profile", response_model=UserProfileSchema)
def create_user_profile(profile_data: UserProfileSchema,
                        current_user: AeroUser = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    """Create or update user profile."""
    if current_user.id != profile_data.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to create profile for this user. "
                                                    "You can only create or update your own profile.")
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

    if existing_profile:
        existing_profile.first_name = profile_data.first_name
        existing_profile.last_name = profile_data.last_name
        existing_profile.date_of_birth = profile_data.date_of_birth
        existing_profile.phone_number = profile_data.phone_number
        existing_profile.address = profile_data.address
        existing_profile.city = profile_data.city
        existing_profile.province = profile_data.province
        existing_profile.country = profile_data.country
        existing_profile.postal_code = profile_data.postal_code
        existing_profile.profile_picture_url = profile_data.profile_picture_url
        db.add(existing_profile)
        db.commit()
        db.refresh(existing_profile)

        return existing_profile
    else:
        new_profile = UserProfile(
            user_id=current_user.id,
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            date_of_birth=profile_data.date_of_birth,
            phone_number=profile_data.phone_number,
            address=profile_data.address,
            city=profile_data.city,
            province=profile_data.province,
            country=profile_data.country,
            postal_code=profile_data.postal_code,
            profile_picture_url=profile_data.profile_picture_url
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)

        return new_profile
