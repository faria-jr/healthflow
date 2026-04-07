"""Routers."""

from .patients import router as patients_router
from .doctors import router as doctors_router
from .appointments import router as appointments_router
from .payments import router as payments_router
from .reviews import router as reviews_router
from .notifications import router as notifications_router
from .chat import router as chat_router
from .lab_results import router as lab_results_router

__all__ = [
    "patients_router",
    "doctors_router",
    "appointments_router",
    "payments_router",
    "reviews_router",
    "notifications_router",
    "chat_router",
    "lab_results_router",
]
