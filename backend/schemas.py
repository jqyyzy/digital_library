from pydantic import BaseModel, Field
from typing import List, Optional

class ItemOut(BaseModel):
    id: int
    title: str
    author: str
    subject: str
    year: int | None = None
    abstract: str
    tags: str
    availability: str

class RecommendOut(BaseModel):
    item_id: int
    title: str
    author: str
    score: float
    reason: List[str] = Field(default_factory=list)

class FeedbackIn(BaseModel):
    uid: str
    item_id: int
    action: str
