# Multi-Developer Integration Guide

This document explains how each developer branch interacts with the shared contracts defined in `API_CONTRACT.md`.

## 1. Dev 1 (Geospatial Data + ETL)
- **Role**: Ingest raw source data, normalize it, and push it to the backend.
- **Contract Interaction**: You are the primary *producer* for `POST /api/v1/parcels`.
- **Requirements**:
  - You must convert all raw geometries into WKT format.
  - You must map arbitrary source land types to our unified types (e.g., 'Residential').
  - You must inject the appropriate `source` label ('cadastral', 'survey', or 'municipal').

## 2. Dev 2 (Backend + PostgreSQL/PostGIS)
- **Role**: Serve the API and manage the database.
- **Contract Interaction**: You own the implementation of `app/main.py` and must strictly route the endpoints documented in `API_CONTRACT.md`.
- **Requirements**:
  - Setup the PostGIS connection using the variables in `.env.example`.
  - Validate incoming payloads against the Parcel Schema using Pydantic.
  - Ensure API endpoints match the HTTP methods, paths, and response codes explicitly.

## 3. Dev 4 (Conflict Detection)
- **Role**: Analyze the normalized data to find and record discrepancies.
- **Contract Interaction**: You will read from the DB (or via internal Dev 2 services) and generate objects matching the Conflict Schema.
- **Requirements**:
  - When comparing records, output your findings appending to a parcel's `conflicts` array or the dedicated conflicts tables.
  - Output strict `severity` ('low', 'medium', 'high', 'critical') and `conflict_type` values.
  - Only execute conflict detection on valid geometry (WKT).

## 4. Dev 3 (Frontend + GIS Dashboard)
- **Role**: Visualize parcels and conflicts, allowing for human review.
- **Contract Interaction**: You are the primary *consumer* of `GET /api/v1/parcels` and `GET /api/v1/conflicts`.
- **Requirements**:
  - Parse WKT geometries to render on your mapping library (Leaflet/Mapbox).
  - Use the `status` and `conflicts` arrays to color-code map polygons.
  - Do not assume the backend will return un-paginated data (handle `limit` and `offset`).

## Local Setup
To run the database locally for testing your respective modules:
```bash
docker-compose up -d
```
Copy `.env.example` to `.env` and adjust if necessary. Install project dependencies via `pip install -r requirements.txt`.
