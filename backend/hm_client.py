import os
import httpx

from dotenv import load_dotenv

load_dotenv()


RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "apidojo-hm-hennes-mauritz-v1.p.rapidapi.com")
HM_COUNTRY = os.getenv("HM_COUNTRY", "us")
HM_LANG = os.getenv("HM_LANG", "en")

if not RAPIDAPI_KEY:
    raise RuntimeError("RAPIDAPI_KEY is missing. Add it in backend/.env")

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
    "Accept": "application/json",
}

BASE = f"https://{RAPIDAPI_HOST }"

async def hm_list_products(categories: str, page: int = 0, size: int = 30) -> dict:
    params = {
    "country": HM_COUNTRY,
    "lang": HM_LANG,
    "page": page,
    "pageSize": size,
    "categoryId": categories,
    "sort": "RELEVANCE",
}

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"{BASE}/products/v2/list", headers=HEADERS, params=params)
        r.raise_for_status()
        return r.json()
