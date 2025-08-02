from fastapi import APIRouter, Request, Depends
from app.utils.image_text_extraction import image_text_extraction
from app.utils.auth import verify_auth

router = APIRouter()


@router.post("/analyze-image")
async def analyze_image(request: Request, auth: str = Depends(verify_auth)):
    try:
        body = await request.json()
        text = image_text_extraction(body["image"])
        
        return {"text": text}

    except Exception as e:
        return {"error": "Analyze Image internal server error"}
