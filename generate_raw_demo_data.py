import geopandas as gpd
from shapely.geometry import Polygon, Point
import pandas as pd
import os

os.makedirs("raw_data", exist_ok=True)

# 1. Raw Cadastral GeoJSON
cadastral_data = {
    "parcel_no": ["C001", "C002", "C003"],
    "landuse": ["Residential", "Commercial", "Agricultural"],
    "owner_name": ["Alice", "Bob", "Charlie"],
    "geometry": [
        Polygon([(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]),
        Polygon([(10, 0), (10, 10), (20, 10), (20, 0), (10, 0)]),
        Polygon([(20, 0), (20, 10), (30, 10), (30, 0), (20, 0)]) # Valid polygon
    ]
}
gdf_cadastral = gpd.GeoDataFrame(cadastral_data, crs="EPSG:4326")
gdf_cadastral.to_file("raw_data/raw_cadastral.geojson", driver="GeoJSON")

# 2. Raw Survey CSV (WKT)
survey_data = {
    "plot_id": ["S001", "S002"],
    "type": ["Residential", "Public"],
    "surveyor": ["John", "Jane"],
    "wkt": [
        "POLYGON((0 0, 0 10.1, 10.1 10.1, 10.1 0, 0 0))",
        "POLYGON((100 100, 100 110, 110 110, 110 100, 100 100))"
    ]
}
df_survey = pd.DataFrame(survey_data)
df_survey.to_csv("raw_data/raw_survey.csv", index=False)

# 3. Raw Municipal Shapefile
municipal_data = {
    "id": ["M001", "M002"],
    "zoning": ["Commercial", "Residential"],
    "tax_status": ["Paid", "Unpaid"],
    "geometry": [
        Polygon([(20, 0), (20, 10), (30, 10), (30, 0), (20, 0)]),
        Polygon([(30, 0), (30, 10), (40, 10), (40, 0), (30, 0)])
    ]
}
gdf_municipal = gpd.GeoDataFrame(municipal_data, crs="EPSG:3857") # Different CRS
gdf_municipal.to_file("raw_data/raw_municipal.shp")

print("Raw test datasets created in 'raw_data/'")
