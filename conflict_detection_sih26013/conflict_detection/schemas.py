"""
schemas.py
==========
Shared parcel record schema for GeoHarmonize (SIH26013).

This mirrors the field names agreed across the team's shared input contract.
DO NOT rename these fields — Developer 2's ingestion/normalization module
and any downstream consumer rely on these exact keys.

A "parcel record" is one standardized observation of a land parcel coming
from a single source (e.g. cadastral map, field survey, satellite/GIS layer).
The conflict detector compares records that share the same parcel_id (or,
for geometry overlap, records from different parcels) across sources.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ParcelRecord:
    parcel_id: str
    geometry: Dict[str, Any]          # GeoJSON-style geometry dict, e.g. {"type": "Polygon", "coordinates": [...]}
    area: float                        # area in square meters, as reported by the source
    land_type: Optional[str] = None    # e.g. "residential", "agricultural"
    source: str = "unknown"            # e.g. "cadastral", "survey", "satellite", "gis"
    attributes: Dict[str, Any] = field(default_factory=dict)  # free-form extra attributes (owner, zone, etc.)
    confidence: float = 1.0            # source's own confidence in this record (0-1), if provided
    conflicts: List[Dict[str, Any]] = field(default_factory=list)  # populated by the detector
    status: str = "pending"            # "pending" | "reviewed" | "resolved" — set by downstream review UI

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ParcelRecord":
        return ParcelRecord(
            parcel_id=d["parcel_id"],
            geometry=d["geometry"],
            area=d["area"],
            land_type=d.get("land_type"),
            source=d.get("source", "unknown"),
            attributes=d.get("attributes", {}) or {},
            confidence=d.get("confidence", 1.0),
            conflicts=d.get("conflicts", []) or [],
            status=d.get("status", "pending"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "parcel_id": self.parcel_id,
            "geometry": self.geometry,
            "area": self.area,
            "land_type": self.land_type,
            "source": self.source,
            "attributes": self.attributes,
            "confidence": self.confidence,
            "conflicts": self.conflicts,
            "status": self.status,
        }


@dataclass
class Conflict:
    """The structured output every rule must produce."""
    parcel_id: str
    conflict_type: str
    severity: str        # "LOW" | "MEDIUM" | "HIGH"
    confidence: float    # 0-1, how sure the detector is this is a real conflict
    description: str
    source_a: str
    source_b: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "parcel_id": self.parcel_id,
            "conflict_type": self.conflict_type,
            "severity": self.severity,
            "confidence": round(self.confidence, 2),
            "description": self.description,
            "source_a": self.source_a,
            "source_b": self.source_b,
        }
