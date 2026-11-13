from fastapi import FastAPI # type: ignore
from datetime import datetime
import os

app = FastAPI(
    title="Health Check API",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "backend-api",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/")
def root():
    return {"message": "FastAPI Backend is running!"}