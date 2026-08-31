import os
from etl.pipeline import run_pipeline, export_data

def main():
    os.makedirs("standardized_data", exist_ok=True)
    
    # Process Cadastral
    cad_mapping = {
        "parcel_id": "parcel_no",
        "land_type": "landuse"
    }
    cad_records = run_pipeline("raw_data/raw_cadastral.geojson", "cadastral", cad_mapping)
    export_data(cad_records, "standardized_data/std_cadastral.json")
    print(f"Processed {len(cad_records)} cadastral records.")
    
    # Process Survey
    survey_mapping = {
        "parcel_id": "plot_id",
        "land_type": "type"
    }
    survey_records = run_pipeline("raw_data/raw_survey.csv", "survey", survey_mapping)
    export_data(survey_records, "standardized_data/std_survey.json")
    print(f"Processed {len(survey_records)} survey records.")
    
    # Process Municipal
    mun_mapping = {
        "parcel_id": "id",
        "land_type": "zoning"
    }
    mun_records = run_pipeline("raw_data/raw_municipal.shp", "municipal", mun_mapping)
    export_data(mun_records, "standardized_data/std_municipal.json")
    print(f"Processed {len(mun_records)} municipal records.")

if __name__ == "__main__":
    main()
