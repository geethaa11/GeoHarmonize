"""
detector.py
===========
Main entry point for the Conflict Detection module (SIH26013 / GeoHarmonize).

Usage
-----
    from conflict_detection import detect_conflicts

    records = [ParcelRecord.from_dict(r) for r in raw_records]
    conflicts = detect_conflicts(records)
    output = [c.to_dict() for c in conflicts]

`detect_conflicts` takes a flat list of ParcelRecord (or plain dicts using
the shared schema) coming from ANY number of sources, and returns a flat
list of Conflict objects. It does not touch a database and does not know
about HTTP — Developer 2's module is expected to call this function
directly and persist/serve the results.
"""

from __future__ import annotations
from itertools import combinations
from typing import List, Union, Dict, Any, Optional

from .schemas import ParcelRecord, Conflict
from .rules import (
    DEFAULT_CONFIG,
    check_area_mismatch,
    check_geometry_overlap,
    check_duplicate_parcel_id,
    check_missing_attributes,
    check_attribute_mismatch,
    check_spatial_deviation,
)


def _coerce_records(records: List[Union[ParcelRecord, Dict[str, Any]]]) -> List[ParcelRecord]:
    out = []
    for r in records:
        out.append(r if isinstance(r, ParcelRecord) else ParcelRecord.from_dict(r))
    return out


def detect_conflicts(
    records: List[Union[ParcelRecord, Dict[str, Any]]],
    config: Optional[dict] = None,
) -> List[Conflict]:
    """
    Compare parcel records across sources and return all detected conflicts.

    - records: flat list of ParcelRecord or dicts matching the shared schema.
      Can mix any number of sources and any number of parcel_ids.
    - config: optional override of thresholds in rules.DEFAULT_CONFIG.

    Returns a flat list of Conflict objects (use .to_dict() for JSON output).
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    parcels = _coerce_records(records)
    conflicts: List[Conflict] = []

    # ---- 4. Missing attributes: single-record check, run on everything ----
    for r in parcels:
        c = check_missing_attributes(r, cfg)
        if c:
            conflicts.append(c)

    # ---- Group records by parcel_id for same-parcel, cross-source checks ----
    by_parcel_id: Dict[str, List[ParcelRecord]] = {}
    for r in parcels:
        by_parcel_id.setdefault(r.parcel_id, []).append(r)

    for parcel_id, group in by_parcel_id.items():
        if len(group) < 2:
            continue
        for a, b in combinations(group, 2):
            if a.source == b.source:
                continue  # only compare across different sources for these checks
            for rule in (check_area_mismatch, check_attribute_mismatch, check_spatial_deviation):
                c = rule(a, b, cfg)
                if c:
                    conflicts.append(c)
            c = check_duplicate_parcel_id(a, b, cfg)
            if c:
                conflicts.append(c)

    # ---- 2. Geometry overlap: compare DIFFERENT parcel_ids across the
    #      whole dataset (their boundaries shouldn't overlap in reality) ----
    for a, b in combinations(parcels, 2):
        if a.parcel_id == b.parcel_id:
            continue
        c = check_geometry_overlap(a, b, cfg)
        if c:
            conflicts.append(c)

    return conflicts


def detect_conflicts_as_dicts(
    records: List[Union[ParcelRecord, Dict[str, Any]]],
    config: Optional[dict] = None,
) -> List[Dict[str, Any]]:
    """Convenience wrapper: same as detect_conflicts but returns plain dicts
    ready to json.dumps() — this is the shape Developer 2 should expect."""
    return [c.to_dict() for c in detect_conflicts(records, config)]
