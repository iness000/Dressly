from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


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

    # Auth Models
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

class Token(BaseModel):
    token: str
    user: UserResponse
