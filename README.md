# GeoHarmonize (SIH 2026 - TQ-1787301581589)

Multi-source geospatial data integration and harmonization platform for urban land record management.

## Setup Instructions

1. Clone this repository.
2. Install Python 3.10+ and standard tools.
3. Run `pip install -r requirements.txt` to install unified dependencies.
4. Copy `.env.example` to `.env` and fill in necessary details.
5. Run `docker-compose up -d` to start the local PostgreSQL/PostGIS database.

## Integration & Contracts
Please review the following documentation before beginning module development:
- **[API Contract & Schemas](API_CONTRACT.md)**: Exact JSON structures and endpoint definitions.
- **[Multi-Developer Integration Guide](INTEGRATION.md)**: How Dev 1-4 interact with the system.

## Running the Application

- **Backend:** `uvicorn app.main:app --reload` (Mocked for now)
- **Frontend:** To be determined (React/Vue)

## Test Instructions

To run the integration and API test suites:
```bash
pytest tests/
```

*Note: As of Phase 1, the test suite contains fixtures and mocks based on the Shared Data Contract to validate future modules.*

## Demo Data
Check the `demo_data/` folder for synthetic datasets representing cadastral, survey, and municipal sources covering core conflict scenarios. All data is for illustrative purposes only.
