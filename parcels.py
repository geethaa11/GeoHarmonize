from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Parcel
from schemas import ParcelCreate, ParcelListResponse, ParcelResponse

router = APIRouter(
    prefix="/api/v1/parcels",
    tags=["Parcels"],
)


@router.get("", response_model=ParcelListResponse)
def get_parcels(
    source: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Parcel)

    if source:
        query = query.filter(Parcel.source == source)

    if status:
        query = query.filter(Parcel.status == status)

    total = query.count()
    parcels = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "parcels": parcels,
    }


@router.get("/{parcel_id}", response_model=ParcelResponse)
def get_parcel(
    parcel_id: str,
    db: Session = Depends(get_db),
):
    parcel = (
        db.query(Parcel)
        .filter(Parcel.parcel_id == parcel_id)
        .first()
    )

    if not parcel:
        raise HTTPException(
            status_code=404,
            detail="Parcel not found",
        )

    return parcel


@router.post("", status_code=201)
def create_parcels(
    parcels: list[ParcelCreate],
    db: Session = Depends(get_db),
):
    inserted_count = 0

    for parcel_data in parcels:
        parcel = Parcel(
            parcel_id=parcel_data.parcel_id,
            geometry=f"SRID=4326;{parcel_data.geometry}",
            area=parcel_data.area,
            land_type=parcel_data.land_type,
            source=parcel_data.source,
            attributes=parcel_data.attributes,
            confidence=parcel_data.confidence,
            status=parcel_data.status,
        )

        db.add(parcel)
        inserted_count += 1

    db.commit()

    return {
        "status": "created",
        "inserted_count": inserted_count,
    }