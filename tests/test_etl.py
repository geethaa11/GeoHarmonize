import os
import pytest
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from etl.pipeline import load_data, validate_and_clean_geometries, transform_crs, calculate_area, standardize_schema, run_pipeline

@pytest.fixture
def dummy_gdf():
    data = {
        "parcel_no": ["P1", "P2"],
        "landuse": ["Res", "Com"],
        "geometry": [
            Polygon([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]),
            Polygon([(1, 1), (1, 2), (2, 2), (2, 1), (1, 1)])
        ]
    }
    return gpd.GeoDataFrame(data, crs="EPSG:4326")

def test_validate_geometries(dummy_gdf):
    # Just basic validation check
    clean = validate_and_clean_geometries(dummy_gdf)
    assert len(clean) == 2

def test_transform_crs(dummy_gdf):
    transformed = transform_crs(dummy_gdf, "EPSG:3857")
    assert transformed.crs.to_string() == "EPSG:3857"

def test_standardize_schema(dummy_gdf):
    mapping = {
        "parcel_id": "parcel_no",
        "land_type": "landuse"
    }
    standardized = standardize_schema(dummy_gdf, "test_source", mapping)
    
    assert "parcel_id" in standardized.columns
    assert "land_type" in standardized.columns
    assert "source" in standardized.columns
    assert "attributes" in standardized.columns
    assert "confidence" in standardized.columns
    assert "status" in standardized.columns
    
    assert standardized.iloc[0]["parcel_id"] == "P1"
    assert standardized.iloc[0]["land_type"] == "Res"
    assert standardized.iloc[0]["source"] == "test_source"

def test_run_pipeline():
    # Write a quick temp file to test full pipeline
    temp_csv = "temp_test.csv"
    df = pd.DataFrame({
        "id": ["T1"],
        "zoning": ["Agricultural"],
        "wkt": ["POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))"]
    })
    df.to_csv(temp_csv, index=False)
    
    mapping = {
        "parcel_id": "id",
        "land_type": "zoning"
    }
    
    try:
        results = run_pipeline(temp_csv, "csv_source", mapping)
        assert len(results) == 1
        res = results[0]
        assert res["parcel_id"] == "T1"
        assert res["land_type"] == "Agricultural"
        assert res["source"] == "csv_source"
        assert "POLYGON" in res["geometry"]
        assert "area" in res
        assert "attributes" in res
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
