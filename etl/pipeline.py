import geopandas as gpd
import pandas as pd
from shapely import wkt
from shapely.geometry import Point
from shapely.validation import make_valid
import os

REQUIRED_FIELDS = [
    "parcel_id",
    "geometry",
    "area",
    "land_type",
    "source",
    "attributes",
    "confidence",
    "conflicts",
    "status"
]

def load_data(filepath: str, file_type: str = None) -> gpd.GeoDataFrame:
    """Loads geospatial data from a file."""
    if file_type is None:
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ['.shp']:
            file_type = 'shapefile'
        elif ext in ['.geojson', '.json']:
            file_type = 'geojson'
        elif ext in ['.csv']:
            file_type = 'csv'
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    if file_type in ['shapefile', 'geojson']:
        gdf = gpd.read_file(filepath)
    elif file_type == 'csv':
        df = pd.read_csv(filepath)
        # Check for geometry in WKT
        if 'geometry' in df.columns or 'wkt' in df.columns:
            geom_col = 'geometry' if 'geometry' in df.columns else 'wkt'
            df['geometry'] = df[geom_col].apply(lambda x: wkt.loads(x) if isinstance(x, str) else x)
            gdf = gpd.GeoDataFrame(df, geometry='geometry')
        # Check for lat/lon
        elif {'lat', 'lon'}.issubset(set(df.columns)):
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat))
        elif {'latitude', 'longitude'}.issubset(set(df.columns)):
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
        else:
            raise ValueError("CSV must contain either a WKT 'geometry' column or 'lat'/'lon' columns.")
        
        # Set default CRS if not present
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    return gdf

def validate_and_clean_geometries(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Validates and fixes invalid geometries. Drops empty ones."""
    # Drop rows with null geometries
    gdf = gdf[gdf.geometry.notnull()]
    gdf = gdf[~gdf.geometry.is_empty]
    
    # Make geometries valid
    gdf['geometry'] = gdf['geometry'].apply(lambda geom: make_valid(geom) if not geom.is_valid else geom)
    return gdf

def transform_crs(gdf: gpd.GeoDataFrame, target_crs: str = "EPSG:4326") -> gpd.GeoDataFrame:
    """Transforms geometries to the target CRS."""
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    if gdf.crs != target_crs:
        gdf = gdf.to_crs(target_crs)
    return gdf

def calculate_area(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Calculates area in square meters (approximate via EPSG:3857 if geographic)."""
    # Create a temporary geodataframe in a projected CRS to calculate area accurately
    temp_gdf = gdf.to_crs("EPSG:3857")
    gdf['computed_area'] = temp_gdf.geometry.area
    return gdf

def standardize_schema(gdf: gpd.GeoDataFrame, source_name: str, field_mapping: dict = None) -> gpd.GeoDataFrame:
    """Standardizes the dataframe schema to the expected data contract."""
    if field_mapping is None:
        field_mapping = {}

    # Rename columns based on mapping
    inv_map = {v: k for k, v in field_mapping.items()}
    # But usually mapping is target_field: source_field or target_field: [possible_source_fields]
    # Let's support target_field: source_field
    rename_dict = {}
    for target_col, source_col in field_mapping.items():
        if isinstance(source_col, list):
            for col in source_col:
                if col in gdf.columns:
                    rename_dict[col] = target_col
                    break
        elif source_col in gdf.columns:
            rename_dict[source_col] = target_col
            
    gdf = gdf.rename(columns=rename_dict)

    # Ensure required columns exist
    if 'parcel_id' not in gdf.columns:
        # Generate generic IDs if missing
        gdf['parcel_id'] = [f"{source_name}_{i}" for i in range(len(gdf))]
        
    if 'land_type' not in gdf.columns:
        gdf['land_type'] = "Unknown"
        
    if 'area' not in gdf.columns:
        if 'computed_area' in gdf.columns:
            gdf['area'] = gdf['computed_area']
        else:
            gdf['area'] = 0.0
            
    gdf['source'] = source_name
    
    if 'confidence' not in gdf.columns:
        gdf['confidence'] = 0.9  # Default confidence for newly ingested data

    # Create attributes dict for remaining columns
    standard_cols = ['parcel_id', 'geometry', 'area', 'land_type', 'source', 'confidence', 'computed_area']
    other_cols = [c for c in gdf.columns if c not in standard_cols and c != 'geometry']
    
    def row_to_attributes(row):
        return {col: row[col] for col in other_cols if pd.notnull(row[col])}
        
    gdf['attributes'] = gdf.apply(row_to_attributes, axis=1)
    
    # Add empty default fields for integration
    gdf['conflicts'] = [[] for _ in range(len(gdf))]
    gdf['status'] = "pending"

    # Select and order standard columns
    result_gdf = gdf[REQUIRED_FIELDS]
    return result_gdf

def run_pipeline(filepath: str, source_name: str, field_mapping: dict = None) -> list:
    """Runs the full ETL pipeline and returns a list of dictionaries adhering to the schema."""
    # 1. Load data
    gdf = load_data(filepath)
    
    # 2. Geometry normalization and validation
    gdf = validate_and_clean_geometries(gdf)
    
    # 3. CRS Transformation (Standardize to WGS84)
    gdf = transform_crs(gdf, target_crs="EPSG:4326")
    
    # 4. Compute area
    gdf = calculate_area(gdf)
    
    # 5. Schema Standardization
    gdf = standardize_schema(gdf, source_name, field_mapping)
    
    # Convert to dictionary format as required by the backend
    # GeoPandas to_dict doesn't serialize geometries nicely to WKT directly in a standard to_dict
    # So we handle geometry conversion manually
    records = []
    for _, row in gdf.iterrows():
        record = row.to_dict()
        record['geometry'] = record['geometry'].wkt
        records.append(record)
        
    return records

def export_data(records: list, output_filepath: str):
    """Exports standardized records to JSON."""
    import json
    # Add demo label as requested
    for rec in records:
        if "_note" not in rec:
            rec["_note"] = "Illustrative / Demo Data"
            
    with open(output_filepath, 'w') as f:
        json.dump(records, f, indent=2)

