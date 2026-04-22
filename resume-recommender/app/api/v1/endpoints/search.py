from fastapi import APIRouter
from pydantic import BaseModel

from app.services.search_service import search_candidates
from app.models.candidate import SearchResponse

router = APIRouter()


# -----------------------------
# Request Schema
# -----------------------------
class SearchRequest(BaseModel):
    query: str


# -----------------------------
# Endpoint
# -----------------------------
@router.post("/", response_model=SearchResponse)
def search(request: SearchRequest):
    results = search_candidates(request.query)
    return {"results": results}
