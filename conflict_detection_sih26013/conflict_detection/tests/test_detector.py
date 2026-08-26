"""
test_detector.py
=================
End-to-end tests for detect_conflicts() / detect_conflicts_as_dicts()
running against the synthetic demo dataset. These confirm the module
finds every conflict type it's supposed to, on realistic multi-source
input, not just isolated rule calls.
"""

import json
from pathlib import Path

import pytest

from conflict_detection import detect_conflicts, detect_conflicts_as_dicts
from conflict_detection.schemas import ParcelRecord, Conflict

DEMO_DATA_PATH = Path(__file__).resolve().parent.parent / "demo_data" / "synthetic_parcels.json"


@pytest.fixture(scope="module")
def demo_records():
    with open(DEMO_DATA_PATH) as f:
        data = json.load(f)
    return data["records"]


def test_demo_data_loads(demo_records):
    assert len(demo_records) > 0


def test_detect_conflicts_returns_conflict_objects(demo_records):
    conflicts = detect_conflicts(demo_records)
    assert all(isinstance(c, Conflict) for c in conflicts)


def test_detect_conflicts_as_dicts_has_required_output_fields(demo_records):
    output = detect_conflicts_as_dicts(demo_records)
    required_fields = {
        "parcel_id", "conflict_type", "severity",
        "confidence", "description", "source_a", "source_b",
    }
    assert len(output) > 0
    for row in output:
        assert required_fields.issubset(row.keys())


def test_matching_parcel_p000_has_no_conflicts(demo_records):
    output = detect_conflicts_as_dicts(demo_records)
    p000_conflicts = [c for c in output if c["parcel_id"] == "P000"]
    assert p000_conflicts == []


def test_all_six_conflict_types_detected(demo_records):
    output = detect_conflicts_as_dicts(demo_records)
    found_types = {c["conflict_type"] for c in output}
    expected_types = {
        "AREA_MISMATCH",
        "GEOMETRY_OVERLAP",
        "DUPLICATE_PARCEL_ID",
        "MISSING_ATTRIBUTES",
        "ATTRIBUTE_MISMATCH",
        "SPATIAL_DEVIATION",
    }
    missing = expected_types - found_types
    assert not missing, f"Rule types never triggered on demo data: {missing}"


def test_p001_area_mismatch(demo_records):
    output = detect_conflicts_as_dicts(demo_records)
    p001 = [c for c in output if c["parcel_id"] == "P001" and c["conflict_type"] == "AREA_MISMATCH"]
    assert len(p001) == 1
    assert p001[0]["severity"] in ("MEDIUM", "HIGH")


def test_p004_duplicate_id(demo_records):
    output = detect_conflicts_as_dicts(demo_records)
    p004 = [c for c in output if c["parcel_id"] == "P004" and c["conflict_type"] == "DUPLICATE_PARCEL_ID"]
    assert len(p004) == 1
    assert p004[0]["severity"] == "HIGH"


def test_p005_missing_attributes(demo_records):
    output = detect_conflicts_as_dicts(demo_records)
    p005 = [c for c in output if c["parcel_id"] == "P005" and c["conflict_type"] == "MISSING_ATTRIBUTES"]
    assert len(p005) == 1


def test_p008_multiple_conflicts(demo_records):
    output = detect_conflicts_as_dicts(demo_records)
    p008 = [c for c in output if c["parcel_id"] == "P008"]
    types = {c["conflict_type"] for c in p008}
    # P008 is designed to trip area mismatch, attribute mismatch, and missing attributes at once
    assert {"AREA_MISMATCH", "ATTRIBUTE_MISMATCH", "MISSING_ATTRIBUTES"}.issubset(types)


def test_accepts_plain_dicts_and_parcelrecord_objects_interchangeably(demo_records):
    as_objects = [ParcelRecord.from_dict(r) for r in demo_records]
    out_from_dicts = detect_conflicts_as_dicts(demo_records)
    out_from_objects = detect_conflicts_as_dicts(as_objects)
    assert len(out_from_dicts) == len(out_from_objects)


def test_config_override_changes_sensitivity(demo_records):
    default_output = detect_conflicts_as_dicts(demo_records)
    loose_output = detect_conflicts_as_dicts(
        demo_records, config={"area_mismatch_pct_threshold": 0.99}
    )
    default_area_mismatches = [c for c in default_output if c["conflict_type"] == "AREA_MISMATCH"]
    loose_area_mismatches = [c for c in loose_output if c["conflict_type"] == "AREA_MISMATCH"]
    assert len(loose_area_mismatches) < len(default_area_mismatches)
