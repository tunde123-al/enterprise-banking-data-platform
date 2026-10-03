from fastapi import FastAPI
from .config import settings
from .models import HealthResponse
from .routes.transactions import router as transactions_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Enterprise Banking Operational Microservice for Transaction Simulation",
)

app.include_router(transactions_router)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.get("/")
def root():
    return {
        "message": "Enterprise Banking Data & Analytics Platform API",
        "docs": "/docs",
        "health": "/health",
    }
