"""Routers."""

from .patients import router as patients_router
from .doctors import router as doctors_router
from .appointments import router as appointments_router
from .payments import router as payments_router
from .reviews import router as reviews_router

__all__ = [
    "patients_router",
    "doctors_router",
    "appointments_router",
    "payments_router",
    "reviews_router",
]
