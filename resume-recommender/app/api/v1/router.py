from fastapi import APIRouter

from app.api.v1.endpoints import search


# -----------------------------
# Main API Router (v1)
# -----------------------------
api_router = APIRouter()


# -----------------------------
# Include Feature Routers
# -----------------------------
api_router.include_router(
    search.router,
    prefix="/search",
    tags=["Search"]
)