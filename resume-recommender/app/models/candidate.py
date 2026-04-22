from pydantic import BaseModel, Field
from typing import List, Optional


# -----------------------------
# Base Candidate Model
# -----------------------------
class CandidateBase(BaseModel):
    name: str = Field(..., example="John Doe")
    title: str = Field(..., example="ML Engineer")
    skills: List[str] = Field(default_factory=list, example=["Python", "NLP", "TensorFlow"])
    resume_text: str = Field(..., example="Experienced ML engineer with NLP expertise.")


# -----------------------------
# Candidate Model (DB)
# -----------------------------
class Candidate(CandidateBase):
    embedding: List[float] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


# -----------------------------
# Candidate Response Model
# -----------------------------
class CandidateResponse(BaseModel):
    name: str
    title: str
    final_score: float

    vector_score: Optional[float] = None
    llm_score: Optional[float] = None
    rule_score: Optional[float] = None

    # matched_skills: List[str] = []
    # missing_skills: List[str] = []
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    reasoning: Optional[str] = None


# -----------------------------
# Search Response Model
# -----------------------------
class SearchResponse(BaseModel):
    results: List[CandidateResponse]