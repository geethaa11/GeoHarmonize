import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from .database import Base


class Parcel(Base):
    __tablename__ = "land_parcels"

    id = Column(Integer, primary_key=True, index=True)
    parcel_id = Column(String, unique=True, nullable=False, index=True)

    geometry = Column(Geometry("POLYGON", srid=4326), nullable=False)
    area = Column(Float, nullable=False)
    land_type = Column(String, nullable=False)
    source = Column(String, nullable=False)

    attributes = Column(JSONB, default=dict)
    confidence = Column(Float, nullable=False)
    status = Column(String, default="pending", nullable=False)

    conflicts = relationship(
        "Conflict",
        back_populates="parcel",
        cascade="all, delete-orphan",
    )


class Conflict(Base):
    __tablename__ = "conflicts"

    conflict_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    parcel_id = Column(
        String,
        ForeignKey("land_parcels.parcel_id"),
        nullable=False,
        index=True,
    )

    conflict_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    source_a = Column(String, nullable=False)
    source_b = Column(String, nullable=False)

    parcel = relationship("Parcel", back_populates="conflicts")