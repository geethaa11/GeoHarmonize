from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ConflictBase(BaseModel):
    parcel_id: str
    conflict_type: str
    severity: str
    confidence: float = Field(ge=0.0, le=1.0)
    description: str
    source_a: str
    source_b: str


class ConflictResponse(ConflictBase):
    conflict_id: str


class ParcelBase(BaseModel):
    parcel_id: str
    geometry: str
    area: float
    land_type: str
    source: str
    attributes: Dict[str, Any] = {}
    confidence: float = Field(ge=0.0, le=1.0)
    status: str = "pending"


class ParcelResponse(ParcelBase):
    conflicts: List[ConflictResponse] = []


class ParcelCreate(ParcelBase):
    pass


class ParcelListResponse(BaseModel):
    total: int
    parcels: List[ParcelResponse]


class ConflictListResponse(BaseModel):
    total: int
    conflicts: List[ConflictResponse]