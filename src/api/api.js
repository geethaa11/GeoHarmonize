const API_BASE_URL = "http://localhost:8000/api/v1";

export async function getParcels({ source, status, limit = 100, offset = 0 } = {}) {
  const params = new URLSearchParams();

  if (source) params.set("source", source);
  if (status) params.set("status", status);
  params.set("limit", limit);
  params.set("offset", offset);

  const response = await fetch(`${API_BASE_URL}/parcels?${params.toString()}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch parcels: ${response.status}`);
  }

  return response.json();
}

export async function getParcel(parcelId) {
  const response = await fetch(
    `${API_BASE_URL}/parcels/${encodeURIComponent(parcelId)}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch parcel: ${response.status}`);
  }

  return response.json();
}

export async function getConflicts({ severity, conflictType } = {}) {
  const params = new URLSearchParams();

  if (severity) params.set("severity", severity);
  if (conflictType) params.set("conflict_type", conflictType);

  const query = params.toString();
  const url = query
    ? `${API_BASE_URL}/conflicts?${query}`
    : `${API_BASE_URL}/conflicts`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch conflicts: ${response.status}`);
  }

  return response.json();
}

export async function getConflict(conflictId) {
  const response = await fetch(
    `${API_BASE_URL}/conflicts/${encodeURIComponent(conflictId)}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch conflict: ${response.status}`);
  }

  return response.json();
}

export async function createVerification(data) {
  const response = await fetch(`${API_BASE_URL}/verification`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Failed to create verification: ${response.status}`);
  }

  return response.json();
}