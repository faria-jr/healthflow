"""HealthFlow API - Main entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from interfaces.middleware.rate_limit import RateLimitMiddleware
from interfaces.routers.patients import router as patients_router
from interfaces.routers.doctors import router as doctors_router
from interfaces.routers.appointments import router as appointments_router
from interfaces.routers.payments import router as payments_router
from interfaces.routers.reviews import router as reviews_router
from interfaces.routers.notifications import router as notifications_router
from interfaces.routers.chat import router as chat_router
from interfaces.routers.lab_results import router as lab_results_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    # Shutdown
    print(f"Shutting down {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="HealthFlow - Sistema de Clínica Médica",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Rate limiting middleware
app.add_middleware(RateLimitMiddleware, requests_per_minute=60)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(patients_router, prefix="/api/v1")
app.include_router(doctors_router, prefix="/api/v1")
app.include_router(appointments_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(reviews_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(lab_results_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
