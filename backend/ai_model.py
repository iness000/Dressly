import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_style(data: dict):
    prompt = f"""
    You are a professional fashion stylist.

    Here are the user's quiz answers:
    {data}

    Based on this, generate:
    - 1 complete outfit suggestion
    - 3 personalized styling tips
    - A color palette recommendation
    - Clothing items to avoid
    Make it short & practical.
    """

    client = genai.Client()

    response = client.models.generate_content(
        contents=prompt,
    )

    return response.text
