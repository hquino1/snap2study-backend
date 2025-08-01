from fastapi import APIRouter, Request
from app.utils.image_text_extraction import image_text_extraction

router = APIRouter()


@router.post("/analyze-image")
async def analyze_image(request: Request):
    try:
        body = await request.json()
        text = image_text_extraction(body["image"])
        return {"text": text}

    except Exception as e:
        return {"error": "Analyze Image internal server error"}
