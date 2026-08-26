from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Conflict
from ..schemas import ConflictListResponse, ConflictResponse

router = APIRouter(
    prefix="/api/v1/conflicts",
    tags=["Conflicts"],
)


@router.get("", response_model=ConflictListResponse)
def get_conflicts(
    severity: str | None = None,
    conflict_type: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Conflict)

    if severity:
        query = query.filter(Conflict.severity == severity)

    if conflict_type:
        query = query.filter(Conflict.conflict_type == conflict_type)

    conflicts = query.all()

    return {
        "total": len(conflicts),
        "conflicts": conflicts,
    }


@router.get("/{conflict_id}", response_model=ConflictResponse)
def get_conflict(
    conflict_id: str,
    db: Session = Depends(get_db),
):
    conflict = (
        db.query(Conflict)
        .filter(Conflict.conflict_id == conflict_id)
        .first()
    )

    if not conflict:
        raise HTTPException(
            status_code=404,
            detail="Conflict not found",
        )

    return conflict