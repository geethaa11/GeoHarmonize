# Demo Data (Illustrative Only)

**WARNING: ALL DATA IN THIS DIRECTORY IS SYNTHETIC, ILLUSTRATIVE, AND FOR DEMO PURPOSES ONLY. THESE ARE NOT REAL GOVERNMENT RECORDS.**

This dataset contains synthetic parcels covering the following core conflict scenarios across `cadastral`, `survey`, and `municipal` sources:

- **P001:** Area mismatch (Cadastral: 100.0 vs Survey: 120.0)
- **P002:** Geometry overlap (Cadastral x=20 vs Survey x=25)
- **P003:** Missing attribute (Survey missing `zone`)
- **P004:** Duplicate parcel ID (Two P004s in Cadastral)
- **P005:** Attribute mismatch (Cadastral: Residential vs Municipal: Commercial)
- **P006:** Consistent record (All sources match)
- **P007-P010:** Assorted parcels for testing system volume and harmonization flows.

All JSON files comply with the Shared Data Contract specified in `AGENTS.md`.
