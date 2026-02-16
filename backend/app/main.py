"""
SAR Narrative Generator — FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

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
