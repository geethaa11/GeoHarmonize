# API Contract & Shared Schema

This document formalizes the exact API endpoints and JSON structures required by Dev 2 (Backend), used by Dev 3 (Frontend), and interacted with by Dev 1 and Dev 4.

## 1. Shared Schemas

### 1.1 Parcel Schema
Every parcel ingested or returned by the system MUST adhere to this structure:

```json
{
  "parcel_id": "string (Required) - Unique identifier for the parcel",
  "geometry": "string (Required) - WKT (Well-Known Text) representation of the geometry (e.g., POLYGON((...)))",
  "area": "float (Required) - Area in square meters",
  "land_type": "string (Required) - e.g., 'Residential', 'Commercial', 'Agricultural', 'Public'",
  "source": "string (Required) - Allowed values: 'cadastral', 'survey', 'municipal'",
  "attributes": "object (Optional) - Key-value pairs for source-specific extra data",
  "confidence": "float (Required) - Float between 0.0 and 1.0 representing data reliability",
  "conflicts": "array (Required) - List of conflict objects (can be empty [])",
  "status": "string (Required) - Allowed values: 'pending', 'harmonized', 'flagged'"
}
```

### 1.2 Conflict Schema
Used within the `conflicts` array of a Parcel, or returned by conflict endpoints:

```json
{
  "conflict_id": "string (Required) - Unique UUID for the conflict",
  "parcel_id": "string (Required) - The parcel this conflict pertains to",
  "conflict_type": "string (Required) - Allowed values: 'area_mismatch', 'geometry_overlap', 'attribute_mismatch', 'duplicate_id'",
  "severity": "string (Required) - Allowed values: 'low', 'medium', 'high', 'critical'",
  "confidence": "float (Required) - Float between 0.0 and 1.0 indicating model confidence in this conflict",
  "description": "string (Required) - Human-readable explanation of the issue",
  "source_a": "string (Required) - E.g., 'cadastral'",
  "source_b": "string (Required) - E.g., 'survey'"
}
```

---

## 2. API Endpoints

### 2.1 `GET /api/v1/parcels`
Fetches a list of parcels, optionally filtered.
- **Query Params**: `source` (optional), `status` (optional), `limit` (default 100), `offset` (default 0).
- **Response (200 OK)**:
  ```json
  {
    "total": 150,
    "parcels": [ { /* Parcel Schema */ } ]
  }
  ```

### 2.2 `GET /api/v1/parcels/{parcel_id}`
Fetches a specific parcel by its ID.
- **Path Params**: `parcel_id`
- **Response (200 OK)**: `{ /* Parcel Schema */ }`
- **Response (404 Not Found)**: `{"detail": "Parcel not found"}`

### 2.3 `POST /api/v1/parcels`
Ingests a new parcel or a batch of parcels into the system (Used by Dev 1 ETL).
- **Request Body**:
  ```json
  [
    { /* Parcel Schema without conflicts array (system handles that) */ }
  ]
  ```
- **Response (201 Created)**:
  ```json
  {
    "status": "created",
    "inserted_count": 1
  }
  ```
- **Response (400 Bad Request)**: `{"detail": "Invalid payload format"}`

### 2.4 `GET /api/v1/conflicts`
Fetches all detected conflicts across the system.
- **Query Params**: `severity` (optional), `conflict_type` (optional).
- **Response (200 OK)**:
  ```json
  {
    "total": 24,
    "conflicts": [ { /* Conflict Schema */ } ]
  }
  ```

### 2.5 `GET /api/v1/conflicts/{conflict_id}`
Fetches details of a specific conflict.
- **Path Params**: `conflict_id`
- **Response (200 OK)**: `{ /* Conflict Schema */ }`
- **Response (404 Not Found)**: `{"detail": "Conflict not found"}`
