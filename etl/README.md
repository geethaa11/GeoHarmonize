# Geospatial ETL Module

This module is responsible for loading, validating, and harmonizing heterogeneous geospatial data sources (GeoJSON, CSV, Shapefile) into a unified standard schema required by the backend.

## Features
- **Format Support:** GeoJSON, Shapefile, CSV (WKT or Lat/Lon columns)
- **Geometry Validation:** Automatically repairs invalid geometries using `shapely.validation.make_valid` and filters empty geometries.
- **CRS Normalization:** Reprojects all incoming data into `EPSG:4326` standard geographic coordinates.
- **Area Calculation:** Computes approximate area in square meters using a projected CRS (`EPSG:3857`).
- **Dynamic Field Mapping:** Maps non-standard input field names to standard target field names.
- **Schema Enforcement:** Enforces the shared data contract (parcel_id, geometry, area, land_type, source, attributes, confidence, conflicts, status).

## Usage

```python
from etl.pipeline import run_pipeline, export_data

# Define mapping from standardized field -> source field
field_mapping = {
    "parcel_id": "plot_id", 
    "land_type": "zoning_type"
}

# Run pipeline
records = run_pipeline("path/to/data.shp", source_name="municipal_gis", field_mapping=field_mapping)

# Export (or load to DB directly)
export_data(records, "path/to/output.json")
```

## Demo & Testing
Demo raw data generator `generate_raw_demo_data.py` creates illustrative examples in `raw_data/`.
The script `process_demo_data.py` outputs the harmonized structure in `standardized_data/`.
Run tests via `pytest tests/test_etl.py`.

## Note for Developer 2 (Backend)
- Output dictionaries are returned with WKT strings in the `geometry` field.
- The `attributes` field is a dictionary of all custom fields from the source data not captured by standard fields.
- `conflicts` list is empty by default and `status` is `pending`.

