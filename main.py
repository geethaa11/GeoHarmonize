from fastapi import FastAPI

app = FastAPI(
    title="GeoHarmonize API",
    description="Backend API for multi-source geospatial land record management",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "GeoHarmonize API is running"}


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}