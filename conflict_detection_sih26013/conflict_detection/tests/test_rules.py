"""
test_rules.py
=============
Unit tests for the individual deterministic rule functions in rules.py.
Each test builds two minimal ParcelRecord objects by hand (not from the
demo dataset) so each rule can be verified in isolation.
"""

import pytest
from conflict_detection.schemas import ParcelRecord
from conflict_detection.rules import (
    DEFAULT_CONFIG,
    check_area_mismatch,
    check_geometry_overlap,
    check_duplicate_parcel_id,
    check_missing_attributes,
    check_attribute_mismatch,
    check_spatial_deviation,
)

SQUARE_A = {"type": "Polygon", "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]}
SQUARE_A_SHIFTED = {"type": "Polygon", "coordinates": [[[0, 100], [10, 100], [10, 110], [0, 110], [0, 100]]]}
SQUARE_OVERLAPPING = {"type": "Polygon", "coordinates": [[[5, 5], [15, 5], [15, 15], [5, 15], [5, 5]]]}
SQUARE_DEVIATED = {"type": "Polygon", "coordinates": [[[4, 4], [14, 4], [14, 14], [4, 14], [4, 4]]]}


def make(parcel_id="P1", source="cadastral", area=100.0, geometry=None, land_type="residential", attributes=None, confidence=1.0):
    return ParcelRecord(
        parcel_id=parcel_id,
        geometry=geometry if geometry is not None else SQUARE_A,
        area=area,
        land_type=land_type,
        source=source,
        attributes=attributes if attributes is not None else {"owner": "X", "zone": "R1"},
        confidence=confidence,
    )


# ---------------------------------------------------------------------
# AREA_MISMATCH
# ---------------------------------------------------------------------
def test_area_mismatch_detected_above_threshold():
    a = make(source="cadastral", area=1200.0)
    b = make(source="survey", area=1380.0)  # 13% diff
    c = check_area_mismatch(a, b, DEFAULT_CONFIG)
    assert c is not None
    assert c.conflict_type == "AREA_MISMATCH"
    assert c.severity in ("MEDIUM", "HIGH")


def test_area_mismatch_not_flagged_within_tolerance():
    a = make(source="cadastral", area=1000.0)
    b = make(source="survey", area=1030.0)  # 3% diff, below 10% threshold
    assert check_area_mismatch(a, b, DEFAULT_CONFIG) is None


def test_area_mismatch_ignores_different_parcel_ids():
    a = make(parcel_id="P1", area=1000.0)
    b = make(parcel_id="P2", area=5000.0)
    assert check_area_mismatch(a, b, DEFAULT_CONFIG) is None


# ---------------------------------------------------------------------
# GEOMETRY_OVERLAP
# ---------------------------------------------------------------------
def test_geometry_overlap_detected_for_different_parcels():
    a = make(parcel_id="P1", geometry=SQUARE_A)
    b = make(parcel_id="P2", geometry=SQUARE_OVERLAPPING)
    c = check_geometry_overlap(a, b, DEFAULT_CONFIG)
    assert c is not None
    assert c.conflict_type == "GEOMETRY_OVERLAP"


def test_geometry_overlap_ignored_when_same_parcel_id():
    a = make(parcel_id="P1", geometry=SQUARE_A)
    b = make(parcel_id="P1", geometry=SQUARE_OVERLAPPING)
    assert check_geometry_overlap(a, b, DEFAULT_CONFIG) is None


def test_geometry_overlap_none_when_disjoint():
    a = make(parcel_id="P1", geometry=SQUARE_A)
    b = make(parcel_id="P2", geometry=SQUARE_A_SHIFTED)
    assert check_geometry_overlap(a, b, DEFAULT_CONFIG) is None


# ---------------------------------------------------------------------
# DUPLICATE_PARCEL_ID
# ---------------------------------------------------------------------
def test_duplicate_parcel_id_detected_far_apart():
    a = make(parcel_id="P4", source="cadastral", geometry=SQUARE_A)
    b = make(parcel_id="P4", source="gis", geometry=SQUARE_A_SHIFTED)  # ~100m away
    c = check_duplicate_parcel_id(a, b, DEFAULT_CONFIG)
    assert c is not None
    assert c.conflict_type == "DUPLICATE_PARCEL_ID"
    assert c.severity == "HIGH"


def test_duplicate_parcel_id_not_flagged_when_close():
    a = make(parcel_id="P4", source="cadastral", geometry=SQUARE_A)
    b = make(parcel_id="P4", source="gis", geometry=SQUARE_OVERLAPPING)  # a few meters away
    assert check_duplicate_parcel_id(a, b, DEFAULT_CONFIG) is None


def test_duplicate_parcel_id_ignores_same_source():
    a = make(parcel_id="P4", source="cadastral", geometry=SQUARE_A)
    b = make(parcel_id="P4", source="cadastral", geometry=SQUARE_A_SHIFTED)
    assert check_duplicate_parcel_id(a, b, DEFAULT_CONFIG) is None


# ---------------------------------------------------------------------
# MISSING_ATTRIBUTES
# ---------------------------------------------------------------------
def test_missing_attributes_detected():
    a = make(land_type=None, attributes={})
    c = check_missing_attributes(a, DEFAULT_CONFIG)
    assert c is not None
    assert c.conflict_type == "MISSING_ATTRIBUTES"
    assert c.severity == "HIGH"  # missing all 3 required attrs


def test_missing_attributes_none_when_all_present():
    a = make(land_type="residential", attributes={"owner": "X", "zone": "R1"})
    assert check_missing_attributes(a, DEFAULT_CONFIG) is None


# ---------------------------------------------------------------------
# ATTRIBUTE_MISMATCH
# ---------------------------------------------------------------------
def test_attribute_mismatch_detected():
    a = make(land_type="residential", attributes={"owner": "X", "zone": "R1"})
    b = make(land_type="commercial", attributes={"owner": "X", "zone": "C2"})
    c = check_attribute_mismatch(a, b, DEFAULT_CONFIG)
    assert c is not None
    assert c.conflict_type == "ATTRIBUTE_MISMATCH"
    assert c.severity == "HIGH"  # two mismatches: land_type + zone


def test_attribute_mismatch_none_when_identical():
    a = make(land_type="residential", attributes={"owner": "X", "zone": "R1"})
    b = make(land_type="residential", attributes={"owner": "x", "zone": "r1"})  # case-insensitive match
    assert check_attribute_mismatch(a, b, DEFAULT_CONFIG) is None


# ---------------------------------------------------------------------
# SPATIAL_DEVIATION
# ---------------------------------------------------------------------
def test_spatial_deviation_detected_for_low_iou():
    a = make(parcel_id="P7", geometry=SQUARE_A)
    b = make(parcel_id="P7", geometry=SQUARE_DEVIATED)
    c = check_spatial_deviation(a, b, DEFAULT_CONFIG)
    assert c is not None
    assert c.conflict_type == "SPATIAL_DEVIATION"


def test_spatial_deviation_none_for_near_identical_geometry():
    a = make(parcel_id="P7", geometry=SQUARE_A)
    b = make(parcel_id="P7", geometry=SQUARE_A)
    assert check_spatial_deviation(a, b, DEFAULT_CONFIG) is None
