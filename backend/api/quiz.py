from fastapi import APIRouter
from model import QuizInput
from ai_model  import generate_style

import uuid
from datetime import datetime

router = APIRouter()

@router.post("/submit")
async def submit_quiz(data: QuizInput):
    print("\nQUIZ RECEIVED:")
    print(data, "\n")

    quiz_response = {
        "_id": str(uuid.uuid4()),
        "user_id": user_id,
        "answers": data.dict(),
        "created_at": datetime.utcnow()
       }
    quiz_responses_collection.insert_one(quiz_response)

    result = {
        "message": "AI recommendation generation here",
        "products": []  # Add H&M products here
    }

    return {
        "status": "success",
        "quiz_id": quiz_response["_id"],
        "recommendation": result
    }

   

