from fastapi import FastAPI

from .database import Base, engine

from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GeoHarmonize API",
    description="Backend API for urban land record management",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "GeoHarmonize API is running"}


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}