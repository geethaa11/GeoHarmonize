"""
rules.py
========
Deterministic, explainable rules for detecting conflicts between parcel
records coming from different geospatial sources.

Each rule is a pure function: (record_a, record_b, config) -> Conflict | None
so they're easy to unit test and easy for Developer 2 to call individually
if needed, instead of only through the combined detector.

Geometry handling uses shapely. Geometries are expected as GeoJSON-style
dicts (Polygon/MultiPolygon), consistent with the shared `geometry` field.
"""

from __future__ import annotations
from typing import Optional, Dict, Any
from shapely.geometry import shape
from shapely.validation import make_valid

from .schemas import ParcelRecord, Conflict

# ---------------------------------------------------------------------------
# Config defaults — tune these without touching rule logic
# ---------------------------------------------------------------------------
DEFAULT_CONFIG = {
    "area_mismatch_pct_threshold": 0.10,     # >10% area difference -> conflict
    "area_mismatch_high_pct": 0.25,          # >25% -> HIGH severity
    "geometry_overlap_min_ratio": 0.05,      # >5% of either parcel's area overlapping -> conflict
    "geometry_overlap_high_ratio": 0.30,     # >30% overlap -> HIGH severity
    "duplicate_id_centroid_distance_m": 50,  # same ID, centroids >50m apart -> likely duplicate/misassigned ID
    "spatial_deviation_iou_threshold": 0.70, # IoU below this -> significant spatial deviation
    "spatial_deviation_iou_high": 0.40,      # IoU below this -> HIGH severity
    "required_attributes": ["land_type", "owner", "zone"],
}


def _safe_shape(geometry: Dict[str, Any]):
    """Parse a GeoJSON-style geometry dict into a valid shapely geometry, or None."""
    if not geometry:
        return None
    try:
        geom = shape(geometry)
        if not geom.is_valid:
            geom = make_valid(geom)
        return geom
    except Exception:
        return None


def _severity(value: float, high_threshold: float, low_is_bad: bool = False) -> str:
    """Simple two-tier severity bucket. If low_is_bad, smaller value = worse (e.g. IoU)."""
    if low_is_bad:
        if value < high_threshold:
            return "HIGH"
        return "MEDIUM"
    else:
        if value >= high_threshold:
            return "HIGH"
        return "MEDIUM"


# ---------------------------------------------------------------------------
# 1. AREA MISMATCH
# ---------------------------------------------------------------------------
def check_area_mismatch(a: ParcelRecord, b: ParcelRecord, config: dict = DEFAULT_CONFIG) -> Optional[Conflict]:
    if a.parcel_id != b.parcel_id:
        return None
    if a.area is None or b.area is None or a.area <= 0 or b.area <= 0:
        return None

    larger = max(a.area, b.area)
    smaller = min(a.area, b.area)
    pct_diff = (larger - smaller) / larger

    if pct_diff < config["area_mismatch_pct_threshold"]:
        return None

    severity = _severity(pct_diff, config["area_mismatch_high_pct"])
    confidence = min(0.99, 0.6 + pct_diff)  # bigger gap -> more confident it's a real mismatch

    return Conflict(
        parcel_id=a.parcel_id,
        conflict_type="AREA_MISMATCH",
        severity=severity,
        confidence=confidence,
        description=(
            f"Area differs between source records: {a.source}={a.area:.1f} m^2, "
            f"{b.source}={b.area:.1f} m^2 ({pct_diff*100:.1f}% difference)."
        ),
        source_a=a.source,
        source_b=b.source,
    )


# ---------------------------------------------------------------------------
# 2. GEOMETRY OVERLAP (between DIFFERENT parcels — e.g. two neighboring
#    parcels from different sources whose boundaries improperly overlap)
# ---------------------------------------------------------------------------
def check_geometry_overlap(a: ParcelRecord, b: ParcelRecord, config: dict = DEFAULT_CONFIG) -> Optional[Conflict]:
    if a.parcel_id == b.parcel_id:
        return None  # same parcel across sources is handled by spatial deviation, not overlap
    geom_a, geom_b = _safe_shape(a.geometry), _safe_shape(b.geometry)
    if geom_a is None or geom_b is None or geom_a.is_empty or geom_b.is_empty:
        return None
    if not geom_a.intersects(geom_b):
        return None

    intersection_area = geom_a.intersection(geom_b).area
    if intersection_area <= 0:
        return None

    smaller_area = min(geom_a.area, geom_b.area)
    if smaller_area == 0:
        return None
    overlap_ratio = intersection_area / smaller_area

    if overlap_ratio < config["geometry_overlap_min_ratio"]:
        return None

    severity = _severity(overlap_ratio, config["geometry_overlap_high_ratio"])
    confidence = min(0.99, 0.5 + overlap_ratio)

    return Conflict(
        parcel_id=f"{a.parcel_id}/{b.parcel_id}",
        conflict_type="GEOMETRY_OVERLAP",
        severity=severity,
        confidence=confidence,
        description=(
            f"Parcel {a.parcel_id} ({a.source}) and parcel {b.parcel_id} ({b.source}) "
            f"geometries overlap by {overlap_ratio*100:.1f}% of the smaller parcel's area."
        ),
        source_a=a.source,
        source_b=b.source,
    )


# ---------------------------------------------------------------------------
# 3. DUPLICATE PARCEL ID (same ID reused for what appears to be a different
#    physical parcel — detected via large centroid distance)
# ---------------------------------------------------------------------------
def check_duplicate_parcel_id(a: ParcelRecord, b: ParcelRecord, config: dict = DEFAULT_CONFIG) -> Optional[Conflict]:
    if a.parcel_id != b.parcel_id or a.source == b.source:
        return None
    geom_a, geom_b = _safe_shape(a.geometry), _safe_shape(b.geometry)
    if geom_a is None or geom_b is None or geom_a.is_empty or geom_b.is_empty:
        return None

    distance = geom_a.centroid.distance(geom_b.centroid)
    # NOTE: geometries are assumed to be in a projected CRS (meters).
    # If your ingestion pipeline uses lat/lon (degrees), reproject before
    # calling the detector, or swap this for a haversine distance.
    if distance <= config["duplicate_id_centroid_distance_m"]:
        return None

    confidence = min(0.99, 0.5 + distance / (config["duplicate_id_centroid_distance_m"] * 4))

    return Conflict(
        parcel_id=a.parcel_id,
        conflict_type="DUPLICATE_PARCEL_ID",
        severity="HIGH",
        confidence=confidence,
        description=(
            f"Parcel ID {a.parcel_id} is used by both {a.source} and {b.source} for locations "
            f"~{distance:.0f}m apart, suggesting a duplicate/misassigned ID rather than the same parcel."
        ),
        source_a=a.source,
        source_b=b.source,
    )


# ---------------------------------------------------------------------------
# 4. MISSING ATTRIBUTES
# ---------------------------------------------------------------------------
def check_missing_attributes(a: ParcelRecord, config: dict = DEFAULT_CONFIG) -> Optional[Conflict]:
    missing = []
    for attr in config["required_attributes"]:
        if attr == "land_type":
            if not a.land_type:
                missing.append(attr)
        elif attr not in a.attributes or a.attributes.get(attr) in (None, "", []):
            missing.append(attr)

    if not missing:
        return None

    return Conflict(
        parcel_id=a.parcel_id,
        conflict_type="MISSING_ATTRIBUTES",
        severity="MEDIUM" if len(missing) == 1 else "HIGH",
        confidence=0.95,
        description=f"Record from {a.source} is missing required attribute(s): {', '.join(missing)}.",
        source_a=a.source,
        source_b=a.source,
    )


# ---------------------------------------------------------------------------
# 5. ATTRIBUTE MISMATCH
# ---------------------------------------------------------------------------
def check_attribute_mismatch(a: ParcelRecord, b: ParcelRecord, config: dict = DEFAULT_CONFIG) -> Optional[Conflict]:
    if a.parcel_id != b.parcel_id:
        return None

    mismatches = []
    # land_type is a first-class field but compared the same way as an attribute
    if a.land_type and b.land_type and a.land_type != b.land_type:
        mismatches.append(("land_type", a.land_type, b.land_type))

    shared_keys = set(a.attributes.keys()) & set(b.attributes.keys())
    for key in sorted(shared_keys):
        va, vb = a.attributes.get(key), b.attributes.get(key)
        if va is None or vb is None:
            continue
        if str(va).strip().lower() != str(vb).strip().lower():
            mismatches.append((key, va, vb))

    if not mismatches:
        return None

    details = "; ".join(f"{k}: '{va}' ({a.source}) vs '{vb}' ({b.source})" for k, va, vb in mismatches)
    severity = "HIGH" if len(mismatches) > 1 else "MEDIUM"

    return Conflict(
        parcel_id=a.parcel_id,
        conflict_type="ATTRIBUTE_MISMATCH",
        severity=severity,
        confidence=0.85,
        description=f"Attribute values differ between sources: {details}.",
        source_a=a.source,
        source_b=b.source,
    )


# ---------------------------------------------------------------------------
# 6. SIGNIFICANT SPATIAL DEVIATION (same parcel ID, boundaries drawn
#    differently even if area happens to be similar — caught via IoU)
# ---------------------------------------------------------------------------
def check_spatial_deviation(a: ParcelRecord, b: ParcelRecord, config: dict = DEFAULT_CONFIG) -> Optional[Conflict]:
    if a.parcel_id != b.parcel_id:
        return None
    geom_a, geom_b = _safe_shape(a.geometry), _safe_shape(b.geometry)
    if geom_a is None or geom_b is None or geom_a.is_empty or geom_b.is_empty:
        return None
    if not geom_a.intersects(geom_b):
        # Zero overlap between two records of the "same" parcel is the most
        # extreme form of spatial deviation.
        iou = 0.0
    else:
        intersection = geom_a.intersection(geom_b).area
        union = geom_a.union(geom_b).area
        iou = intersection / union if union > 0 else 0.0

    if iou >= config["spatial_deviation_iou_threshold"]:
        return None

    severity = _severity(iou, config["spatial_deviation_iou_high"], low_is_bad=True)
    confidence = min(0.99, 0.6 + (1 - iou) * 0.4)

    return Conflict(
        parcel_id=a.parcel_id,
        conflict_type="SPATIAL_DEVIATION",
        severity=severity,
        confidence=confidence,
        description=(
            f"Boundary shapes for the same parcel differ significantly between {a.source} and "
            f"{b.source} (IoU={iou:.2f}), even accounting for area alone."
        ),
        source_a=a.source,
        source_b=b.source,
    )
