# app/api/v1/endpoints/search.py
from fastapi import APIRouter
from app.services.search_service import search_candidates

router = APIRouter()

@router.post("/")
def search(query: str):
    return search_candidates(query)