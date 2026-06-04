import os
from dotenv import load_dotenv
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.aero_user_model import AeroUser, Role, UserRole

load_dotenv()

SECRET = os.getenv("SECRET", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRES", 30))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def normalize_password(password: str) -> str:
    """Normalize the password by hashing it."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    normalized = normalize_password(password)
    return pwd_context.hash(normalized)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the password by comparing the normalized plain password with the hashed password."""
    normalized = normalize_password(plain_password)
    return pwd_context.verify(normalized, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials/ token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> AeroUser:
    """Get the current user from the JWT token."""
    try:
        payload = decode_access_token(token)
        username: int = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials / token is invalid",
                                headers={"WWW-Authenticate": "Bearer"},)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials / token is invalid",
                            headers={"WWW-Authenticate": "Bearer"},)
    user = db.query(AeroUser).filter(AeroUser.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials / user not found",
                            headers={"WWW-Authenticate": "Bearer"},)
    return user


def require_role(*allowed_roles: str):
    """Dependency to require a specific role for access."""
    def role_dependency(current_user: AeroUser = Depends(get_current_user)):
        user_roles = [user_role.role.name for user_role in current_user.roles]
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to access this resource",)
        return current_user

    return role_dependency


def create_demo_admin():
    """Create a demo admin user if it doesn't exist."""
    db = next(get_db())
    admin_username = "admin"
    admin_password = "admin123"
    admin_email = "admin@aeroride.ca"
    existing_admin = db.query(AeroUser).filter(AeroUser.username == admin_username).first()
    if not existing_admin:
        hashed_password = hash_password(admin_password)
        admin_user = AeroUser(username=admin_username, password_hash=hashed_password, email=admin_email)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        # Create admin role
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

        # Assign admin role to the user
        user_role = UserRole(user_id=admin_user.id, role_id=admin_role.id)
        db.add(user_role)
        db.commit()
