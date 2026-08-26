"""
demo_run.py
===========
Standalone script: loads the synthetic demo dataset and prints the
detected conflicts as JSON. Useful for a quick manual sanity check or
for Developer 2 to see the exact output shape before wiring up real
ingestion.

Run from the repo root:
    python -m conflict_detection.demo_run
"""

import json
from pathlib import Path

from conflict_detection import detect_conflicts_as_dicts

DEMO_DATA_PATH = Path(__file__).resolve().parent / "demo_data" / "synthetic_parcels.json"


def main():
    with open(DEMO_DATA_PATH) as f:
        data = json.load(f)

    records = data["records"]
    conflicts = detect_conflicts_as_dicts(records)

    print(f"Loaded {len(records)} synthetic parcel records ({data['_label']})")
    print(f"Detected {len(conflicts)} conflicts:\n")
    print(json.dumps(conflicts, indent=2))


if __name__ == "__main__":
    main()
