from fastapi import APIRouter
from model import QuizInput
from ai_model  import generate_style
router = APIRouter()

@router.post("/submit")
async def submit_quiz(data: QuizInput):
    print("\nQUIZ RECEIVED:")
    print(data, "\n")

    result= generate_style(data)

    return {
        "status": "success",
        "input": data,
        "recommendation":result
    }

