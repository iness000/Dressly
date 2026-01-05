import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.quiz import router as quiz_router  # ✔ correct

load_dotenv()

app = FastAPI(title="Dressly")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])

@app.get("/")
def home():
    return {"msg": "Dressly backend running"}
