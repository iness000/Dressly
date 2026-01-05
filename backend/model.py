from pydantic import BaseModel
from typing import List, Optional

class Height(BaseModel):
    ft: int
    in_: int | None = None

class Sizes(BaseModel):
    tops: str
    bottoms: str

class Budget(BaseModel):
    min: float
    max: float

class QuizInput(BaseModel):
    occasion: List[str]
    style_vibe: List[str]
    colors_like: Optional[List[str]] = None
    height: Optional[Height] = None
    sizes: Sizes
    budget: Budget
