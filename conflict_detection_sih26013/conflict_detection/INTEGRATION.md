# Integration Guide — for Developer 2

This module has **no database logic and no HTTP layer** by design, so it
drops straight into whatever ingestion/API code you're building.

## What you call

```python
from conflict_detection import detect_conflicts_as_dicts

conflicts = detect_conflicts_as_dicts(standardized_parcel_records)
```

- **Input:** a flat Python list. Each item can be either a plain `dict`
  matching the shared schema below, or a `ParcelRecord` object — both
  work interchangeably.
- **Output:** a flat list of plain `dict`s, ready for `json.dumps()` or
  to persist directly (e.g. one row per conflict in your DB / one
  document per conflict).
- It's fine to pass records from any number of sources and any number
  of distinct `parcel_id`s in a single call — grouping/comparison
  happens internally.

## Input schema (do not rename these fields)

```json
{
  "parcel_id": "P001",
  "geometry": { "type": "Polygon", "coordinates": [[[x,y], ...]] },
  "area": 1200.0,
  "land_type": "residential",
  "source": "cadastral",
  "attributes": { "owner": "S. Nair", "zone": "R2" },
  "confidence": 0.9,
  "conflicts": [],
  "status": "pending"
}
```

- `geometry` must be a GeoJSON-style Polygon/MultiPolygon dict, in a
  **projected CRS (meters)**, not raw lat/lon. If your ingestion
  pipeline works in WGS84 degrees, reproject before calling this module
  — the area/distance thresholds assume meters and m².
- `conflicts` and `status` are accepted but currently ignored by the
  detector (they're there for downstream review-UI use, not input to
  this module). You don't need to populate them before calling.
- Missing optional fields (`land_type`, `attributes`, `confidence`) are
  handled gracefully — `ParcelRecord.from_dict()` defaults them.

## Output schema (one dict per detected conflict)

```json
{
  "parcel_id": "P001",
  "conflict_type": "AREA_MISMATCH",
  "severity": "HIGH",
  "confidence": 0.91,
  "description": "Area differs between source records",
  "source_a": "cadastral",
  "source_b": "survey"
}
```

- `conflict_type` is one of: `AREA_MISMATCH`, `GEOMETRY_OVERLAP`,
  `DUPLICATE_PARCEL_ID`, `MISSING_ATTRIBUTES`, `ATTRIBUTE_MISMATCH`,
  `SPATIAL_DEVIATION`.
- `severity` is one of: `LOW`, `MEDIUM`, `HIGH` (currently the rules only
  emit `MEDIUM`/`HIGH` — `LOW` is reserved for future threshold tuning).
- `confidence` is a float 0–1, the detector's own confidence that this
  is a genuine conflict (not the source record's confidence).
- For `GEOMETRY_OVERLAP`, `parcel_id` is `"{id_a}/{id_b}"` since two
  different parcel IDs are involved — everything else is per-conflict,
  not per-parcel, so this is safe to key off directly.
- A single parcel can appear in **multiple** conflict dicts (e.g. it can
  have both an `AREA_MISMATCH` and an `ATTRIBUTE_MISMATCH` at once) —
  don't assume one row per parcel.

## Tuning thresholds

If your real ingestion data needs different sensitivity than the
defaults in `rules.DEFAULT_CONFIG`, pass an override — no need to touch
`rules.py`:

```python
conflicts = detect_conflicts_as_dicts(
    records,
    config={"area_mismatch_pct_threshold": 0.05},  # stricter than default 0.10
)
```

## Performance note

The current implementation is O(n²) per parcel-id group and O(n²) for
the cross-parcel geometry-overlap check (via `itertools.combinations`).
Fine for hackathon-scale demo data (dozens–hundreds of parcels). If you
feed it a genuinely large dataset, consider pre-filtering with a
spatial index (e.g. `shapely.STRtree`) before calling — flag this to
Developer 4 if it becomes a bottleneck.

## Sample end-to-end call

See `demo_run.py` in this directory, or:

```python
import json
from conflict_detection import detect_conflicts_as_dicts

with open("demo_data/synthetic_parcels.json") as f:
    records = json.load(f)["records"]

conflicts = detect_conflicts_as_dicts(records)
print(json.dumps(conflicts, indent=2))
```
