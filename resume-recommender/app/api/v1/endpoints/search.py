
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.search_service import search_candidates

router = APIRouter()


# -----------------------------
# Request Schema
# -----------------------------
class SearchRequest(BaseModel):
    query: str


# -----------------------------
# Endpoint
# -----------------------------
@router.post("/")
def search(request: SearchRequest):
    return search_candidates(request.query)