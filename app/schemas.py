from pydantic import BaseModel
from typing import List, Optional


class AskRequest(BaseModel):
    question: str


class Source(BaseModel):
    document_name: str
    section_number: Optional[str]
    page_number: Optional[int]
    confidence_score: float


class AskResponse(BaseModel):
    answer: str
    sources: List[Source]
    overall_confidence: float