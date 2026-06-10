from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.aero_user_model import AeroUser, Role, UserRole
from app.models.aero_airport_model import AeroAirport
from app.schemas.aero_airport_schema import AeroAirportRegisterSchema, AeroAirportResponseSchema
from app.core.auth import require_role

router = APIRouter(prefix="/airports", tags=["Airports"])


@router.post("/register-airport", response_model=AeroAirportRegisterSchema)
def register_airport(airport_data: AeroAirportRegisterSchema,
                     db: Session = Depends(get_db),
                     current_user=Depends(require_role("admin"))):
    """Register a new airport (admin only)."""
    existing_airport = db.query(AeroAirport).filter(AeroAirport.code == airport_data.code).first()
    if existing_airport:
        raise HTTPException(status_code=400, detail="Airport with this code already exists")

    new_airport = AeroAirport(
        name=airport_data.name,
        code=airport_data.code,
        city=airport_data.city,
        country=airport_data.country,
        timezone=airport_data.timezone,
        created_at=airport_data.created_at,
        updated_at=airport_data.updated_at
    )
    db.add(new_airport)
    db.commit()
    db.refresh(new_airport)

    return new_airport


@router.get("/all-airports", response_model=List[AeroAirportResponseSchema])
def get_airports(db: Session = Depends(get_db)):
    """Get a list of all airports."""
    airports = db.query(AeroAirport).all()
    return airports


@router.get("/airport/{airport_code}", response_model=AeroAirportResponseSchema)
def get_airport_by_code(airport_code: str, db: Session = Depends(get_db)):
    """Get airport details by ID."""
    airport = db.query(AeroAirport).filter(AeroAirport.code == airport_code).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport
