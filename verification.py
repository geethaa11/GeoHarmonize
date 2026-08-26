from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Conflict, Parcel, Verification
from schemas import VerificationCreate

router = APIRouter(
    prefix="/api/v1/verification",
    tags=["Verification"],
)


@router.post("")
def create_verification(
    verification_data: VerificationCreate,
    db: Session = Depends(get_db),
):
    parcel = (
        db.query(Parcel)
        .filter(Parcel.parcel_id == verification_data.parcel_id)
        .first()
    )

    if not parcel:
        raise HTTPException(
            status_code=404,
            detail="Parcel not found",
        )

    if verification_data.conflict_id:
        conflict = (
            db.query(Conflict)
            .filter(
                Conflict.conflict_id == verification_data.conflict_id
            )
            .first()
        )

        if not conflict:
            raise HTTPException(
                status_code=404,
                detail="Conflict not found",
            )

    allowed_actions = {"accept", "reject", "modify"}

    if verification_data.action not in allowed_actions:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification action",
        )

    verification = Verification(
        parcel_id=verification_data.parcel_id,
        conflict_id=verification_data.conflict_id,
        action=verification_data.action,
        comment=verification_data.comment,
    )

    db.add(verification)

    if verification_data.action == "accept":
        parcel.status = "harmonized"
    elif verification_data.action == "reject":
        parcel.status = "flagged"
    else:
        parcel.status = "pending"

    db.commit()
    db.refresh(verification)

    return {
        "status": "stored",
        "verification_id": verification.id,
        "parcel_id": verification.parcel_id,
        "action": verification.action,
    }