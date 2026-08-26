import pytest
# import httpx # Uncomment when testing real API

# Mocking the FastAPI contract as it's not yet delivered (Phase 1)
class MockAPIClient:
    def get(self, url):
        if "P006" in url:
            return {"status_code": 200, "json": lambda: {"parcel_id": "P006", "status": "harmonized"}}
        return {"status_code": 404, "json": lambda: {"detail": "Not found"}}
        
    def post(self, url, json):
        if not json.get("parcel_id"):
            return {"status_code": 400, "json": lambda: {"detail": "Invalid payload"}}
        return {"status_code": 201, "json": lambda: {"status": "created"}}

@pytest.fixture
def client():
    return MockAPIClient()

def test_get_parcel(client):
    response = client.get("/api/v1/parcels/P006")
    assert response["status_code"] == 200
    assert response["json"]()["parcel_id"] == "P006"

def test_create_parcel_invalid(client):
    response = client.post("/api/v1/parcels", json={"area": 100})
    assert response["status_code"] == 400

def test_create_parcel_valid(client):
    response = client.post("/api/v1/parcels", json={"parcel_id": "P010", "area": 100})
    assert response["status_code"] == 201
