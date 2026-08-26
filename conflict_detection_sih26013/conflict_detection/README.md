# Conflict Detection Module — GeoHarmonize (SIH26013)

**Team:** WHAT IF? (TQ-1787301581589)
**Developer:** Developer 4
**Branch:** `feature/conflict-detection`

Compares standardized parcel records coming from multiple geospatial
sources (cadastral maps, field surveys, satellite/GIS layers, etc.) and
flags conflicts between them — rule-based, deterministic, and explainable.

## What it detects

| # | Conflict type | Trigger |
|---|---|---|
| 1 | `AREA_MISMATCH` | Reported area differs by more than a threshold % between sources, same parcel |
| 2 | `GEOMETRY_OVERLAP` | Two *different* parcels' boundaries physically overlap |
| 3 | `DUPLICATE_PARCEL_ID` | Same parcel ID used by two sources for locations far apart |
| 4 | `MISSING_ATTRIBUTES` | A record is missing required attributes (land_type, owner, zone) |
| 5 | `ATTRIBUTE_MISMATCH` | Attribute values (land_type, or any shared key in `attributes`) disagree between sources |
| 6 | `SPATIAL_DEVIATION` | Same parcel ID, but boundary shapes differ significantly (low IoU) even if area is similar |

All rules are deterministic and threshold-based (see `rules.DEFAULT_CONFIG`).
No ML is used — this keeps the module explainable and fast to demo, per
the team's "rule-based first" guidance. An anomaly-score extension is
possible later (see `Future work` below) but was not needed to hit T-4.

## Install

```bash
pip install shapely pytest
```

(Both are lightweight — no GDAL/GEOS system package needed beyond what
`shapely` ships with its wheel.)

## Usage

```python
from conflict_detection import detect_conflicts_as_dicts

records = [
    {
        "parcel_id": "P001",
        "geometry": {"type": "Polygon", "coordinates": [[[0,0],[30,0],[30,40],[0,40],[0,0]]]},
        "area": 1200.0,
        "land_type": "residential",
        "source": "cadastral",
        "attributes": {"owner": "S. Nair", "zone": "R2"},
        "confidence": 0.9,
    },
    {
        "parcel_id": "P001",
        "geometry": {"type": "Polygon", "coordinates": [[[0,0],[30,0],[30,46],[0,46],[0,0]]]},
        "area": 1380.0,
        "land_type": "residential",
        "source": "survey",
        "attributes": {"owner": "S. Nair", "zone": "R2"},
        "confidence": 0.93,
    },
]

conflicts = detect_conflicts_as_dicts(records)
# -> [{"parcel_id": "P001", "conflict_type": "AREA_MISMATCH", "severity": "MEDIUM",
#      "confidence": 0.73, "description": "...", "source_a": "cadastral", "source_b": "survey"}]
```

See `INTEGRATION.md` for the full contract Developer 2 (or anyone
consuming this module) should rely on.

## Run the demo

```bash
python -m conflict_detection.demo_run
```

Loads `demo_data/synthetic_parcels.json` (15 illustrative parcel
records covering every conflict type, clearly labeled as synthetic —
not real cadastral data) and prints all detected conflicts as JSON.

## Run the tests

```bash
python -m pytest conflict_detection/tests/ -v
```

26 tests, all passing:
- `tests/test_rules.py` — unit tests per rule (positive + negative cases)
- `tests/test_detector.py` — end-to-end tests against the synthetic dataset, confirming all six conflict types are detected and the output schema is correct

## Files

```
conflict_detection/
├── __init__.py          # public exports
├── schemas.py            # ParcelRecord / Conflict dataclasses (shared field contract)
├── rules.py               # the 6 deterministic rule functions + DEFAULT_CONFIG thresholds
├── detector.py            # detect_conflicts() / detect_conflicts_as_dicts() — the entry point
├── demo_run.py            # standalone script to print demo output
├── demo_data/
│   └── synthetic_parcels.json   # ILLUSTRATIVE/DEMO DATA, all 6 conflict types + clean match
├── tests/
│   ├── test_rules.py
│   └── test_detector.py
├── README.md
└── INTEGRATION.md
```

## Design notes

- **Pure functions, no I/O.** Nothing in this module touches a database,
  filesystem (beyond the demo script reading its own demo data), or
  network. Developer 2's module is expected to call `detect_conflicts()`
  directly and persist/serve the results.
- **Field names are fixed** per the shared contract: `parcel_id`,
  `geometry`, `area`, `land_type`, `source`, `attributes`, `confidence`,
  `conflicts`, `status`. Nothing here renames or restructures them.
- **Geometry** is expected as GeoJSON-style dicts (Polygon/MultiPolygon)
  in a *projected, meters-based* CRS — not raw lat/lon degrees — because
  the distance/overlap thresholds (in meters and m²) assume that.
  If upstream ingestion produces WGS84 lat/lon, reproject (e.g. to a
  suitable UTM zone) before calling `detect_conflicts()`.
- **Config is overridable** — pass a `config` dict to `detect_conflicts()`
  to override any threshold in `DEFAULT_CONFIG` without touching rule code.

## Future work (optional, not required for T-4)

- Simple explainable anomaly score (e.g. weighted sum of area diff %,
  1-IoU, missing-attribute count, mismatch count) as an additional
  `anomaly_score` field, computed *after* rule-based conflicts are found —
  not a replacement for them.
- Multi-way (3+ source) comparison summaries per parcel, if the team
  wants a single "reconciliation confidence" per parcel rather than a
  flat conflict list.
