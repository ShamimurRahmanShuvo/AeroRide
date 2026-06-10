from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.aero_user_model import User
from app.models.aero_airport_model import Airport
from app.schemas.aero_airport_schema import AirportCreateSchema, AirportResponseSchema
from app.core.auth import require_role

router = APIRouter(prefix="/airports", tags=["Airports"])


@router.post("/add-airport", response_model=AirportResponseSchema)
def add_airport(airport_data: AirportCreateSchema,
                db: Session = Depends(get_db),
                current_user: User = Depends(require_role("admin"))):
    """Add a new airport (admin only)."""
    existing_airport = db.query(Airport).filter(Airport.code == airport_data.code).first()
    if existing_airport:
        raise HTTPException(status_code=400, detail="Airport with this code already exists")

    new_airport = Airport(
        code=airport_data.code,
        name=airport_data.name,
        city=airport_data.city,
        country=airport_data.country
    )
    db.add(new_airport)
    db.commit()
    db.refresh(new_airport)

    return new_airport


@router.get("/all-airports", response_model=List[AirportResponseSchema])
def get_all_airports(db: Session = Depends(get_db)):
    """Get a list of all airports."""
    airports = db.query(Airport).all()
    return airports


@router.get("/airport/{airport_code}", response_model=AirportResponseSchema)
def get_airport_by_code(airport_code: str, db: Session = Depends(get_db)):
    """Get airport details by airport code."""
    airport = db.query(Airport).filter(Airport.code == airport_code).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport
