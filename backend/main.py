import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from hm_client import hm_list_products
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

load_dotenv()


print("RapidAPI key loaded:", bool(os.getenv("RAPIDAPI_KEY")))


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/hm/products")
async def hm_products(categories: str = Query(..., description="e.g. men_trousers"), page: int = 0, size: int = 30):
    try:
        return await hm_list_products(categories, page, size)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"H&M upstream error: {e}")


def pick_image(prod: dict) -> str | None:
    return (
        
       (prod.get("images") or [{}])[0].get("baseUrl")
        or (prod.get("allArticleBaseImages") or [None])[0]
        or (prod.get("normalPicture") or [{}])[0].get("baseUrl")
        or (prod.get("logoPicture") or [{}])[0].get("baseUrl")
        or (prod.get("images") or [{}])[0].get("url")
    )

@app.get("/hm/products/simple")
async def hm_products_simple(categories: str = "men_trousers", page: int = 0, size: int = 12):
    data = await hm_list_products(categories, page, size)
    results = data.get("results", [])
    simplified = []
    for p in results:
        simplified.append({
            "code": p.get("code"),
            "name": p.get("name"),
            "price": (p.get("price") or {}).get("formattedValue"),
            "image": pick_image(p),
        })
    return JSONResponse(simplified)


@app.get("/debug/hm", response_class=HTMLResponse)
async def debug_hm(categories: str = "men_trousers", page: int = 0, size: int = 12):
    data = await hm_list_products(categories, page, size)
    results = data.get("results", [])
    rows = []
    for p in results:
        img = pick_image(p)
        name = p.get("name", "")
        price = (p.get("price") or {}).get("formattedValue", "")
        code = p.get("code", "")
        # Make one card
        rows.append(f"""
          <div style="border:1px solid #ddd;border-radius:12px;padding:12px">
            <img src="{img}" alt="{name}" style="width:100%;height:260px;object-fit:cover;border-radius:10px" />
            <div style="margin-top:8px;font-weight:600">{name}</div>
            <div style="color:#555">{price}</div>
            <div style="color:#999;font-size:12px">{code}</div>
            <div style="margin-top:6px;word-break:break-all;font-size:11px;color:#666">{img}</div>
          </div>
        """)
    html = f"""
      <html>
      <head><title>H&M Debug</title></head>
      <body style="font-family:Arial,sans-serif;background:#fafafa;margin:0;padding:20px">
        <h2>H&M Debug — {categories}</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;">
          {''.join(rows)}
        </div>
      </body>
      </html>
    """
    return HTMLResponse(html)



