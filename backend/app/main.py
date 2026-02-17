"""
SAR Narrative Generator — FastAPI Backend
"""
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

# Ensure project root is on sys.path so `ml_models` package is importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

app = FastAPI(
    title="SAR Narrative Generator",
    description="AI-powered Suspicious Activity Report drafting with audit trail",
    version="0.1.0",
)

# CORS — allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "SAR Narrative Generator API", "status": "running", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

