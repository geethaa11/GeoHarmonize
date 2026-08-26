import json
import os

# Note: All generated files must be marked as "Illustrative / Demo Data"
os.makedirs("demo_data", exist_ok=True)

def make_parcel(pid, geom, area, ltype, source, attrs, conf=0.9):
    return {
        "parcel_id": pid,
        "geometry": geom,
        "area": area,
        "land_type": ltype,
        "source": source,
        "attributes": attrs,
        "confidence": conf,
        "conflicts": [],
        "status": "pending",
        "_note": "Illustrative / Demo Data"
    }

cadastral = []
survey = []
municipal = []

# P001: Area mismatch
cadastral.append(make_parcel("P001", "POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))", 100.0, "Residential", "cadastral", {"owner": "Alice"}))
survey.append(make_parcel("P001", "POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))", 120.0, "Residential", "survey", {"owner": "Alice"}))
municipal.append(make_parcel("P001", "POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))", 100.0, "Residential", "municipal", {"owner": "Alice"}))

# P002: Geometry overlap
cadastral.append(make_parcel("P002", "POLYGON((20 0, 20 10, 30 10, 30 0, 20 0))", 100.0, "Commercial", "cadastral", {}))
survey.append(make_parcel("P002", "POLYGON((25 0, 25 10, 35 10, 35 0, 25 0))", 100.0, "Commercial", "survey", {}))

# P003: Missing attribute
cadastral.append(make_parcel("P003", "POLYGON((40 0, 40 10, 50 10, 50 0, 40 0))", 100.0, "Agricultural", "cadastral", {"zone": "Agri-1"}))
survey.append(make_parcel("P003", "POLYGON((40 0, 40 10, 50 10, 50 0, 40 0))", 100.0, "Agricultural", "survey", {})) # Missing zone

# P004: Duplicate parcel ID (within Cadastral)
cadastral.append(make_parcel("P004", "POLYGON((60 0, 60 10, 70 10, 70 0, 60 0))", 100.0, "Residential", "cadastral", {"plot_no": "A"}))
cadastral.append(make_parcel("P004", "POLYGON((80 0, 80 10, 90 10, 90 0, 80 0))", 100.0, "Residential", "cadastral", {"plot_no": "B"}))

# P005: Attribute mismatch
cadastral.append(make_parcel("P005", "POLYGON((100 0, 100 10, 110 10, 110 0, 100 0))", 100.0, "Residential", "cadastral", {"owner": "Bob"}))
municipal.append(make_parcel("P005", "POLYGON((100 0, 100 10, 110 10, 110 0, 100 0))", 100.0, "Commercial", "municipal", {"owner": "Bob"}))

# P006: Consistent record
cadastral.append(make_parcel("P006", "POLYGON((120 0, 120 10, 130 10, 130 0, 120 0))", 100.0, "Public", "cadastral", {"use": "Park"}))
survey.append(make_parcel("P006", "POLYGON((120 0, 120 10, 130 10, 130 0, 120 0))", 100.0, "Public", "survey", {"use": "Park"}))
municipal.append(make_parcel("P006", "POLYGON((120 0, 120 10, 130 10, 130 0, 120 0))", 100.0, "Public", "municipal", {"use": "Park"}))

# Add P007-P015 for variety
for i in range(7, 16):
    pid = f"P{i:03d}"
    geom = f"POLYGON(({i*20} 20, {i*20} 30, {i*20+10} 30, {i*20+10} 20, {i*20} 20))"
    cadastral.append(make_parcel(pid, geom, 100.0, "Residential", "cadastral", {"note": "Standard plot"}))
    if i % 2 == 0:
        survey.append(make_parcel(pid, geom, 100.5, "Residential", "survey", {"note": "Surveyed plot"}))
    else:
        municipal.append(make_parcel(pid, geom, 100.0, "Residential", "municipal", {"tax_paid": True}))

with open("demo_data/cadastral.json", "w") as f:
    json.dump(cadastral, f, indent=2)

with open("demo_data/survey.json", "w") as f:
    json.dump(survey, f, indent=2)

with open("demo_data/municipal.json", "w") as f:
    json.dump(municipal, f, indent=2)

with open("demo_data/README.md", "w") as f:
    f.write("""# Demo Data (Illustrative Only)

**WARNING: ALL DATA IN THIS DIRECTORY IS SYNTHETIC, ILLUSTRATIVE, AND FOR DEMO PURPOSES ONLY. THESE ARE NOT REAL GOVERNMENT RECORDS.**

This dataset contains synthetic parcels covering the following core conflict scenarios:
- **P001:** Area mismatch
- **P002:** Geometry overlap
- **P003:** Missing attribute
- **P004:** Duplicate parcel ID
- **P005:** Attribute mismatch
- **P006:** Consistent record (no conflicts)
- **P007-P015:** Assorted parcels for testing system volume and harmonization flows.
""")
