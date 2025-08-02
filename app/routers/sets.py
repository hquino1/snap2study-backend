from fastapi import APIRouter, Request, Depends, HTTPException
from app.utils.auth import verify_auth
from app.utils.image_text_extraction import image_text_extraction
from app.db.sets import get_sets, get_set_content_by_id

router = APIRouter()


@router.get("/sets")
def sets(auth: str = Depends(verify_auth)):
    try:
        
        supabase, user = auth
        flashcards, practiceExams = get_sets(supabase, user.user.id)

        return {"flashcards": flashcards, "practiceExams": practiceExams}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Internal Server Error"))

@router.get("/sets/{setId}/{studyMethod}")
def set_id_content(setId: str, studyMethod: str, auth: str = Depends(verify_auth)):
    try:
        supabase, user = auth
        content, title = get_set_content_by_id(supabase, setId, studyMethod)

        return {"set_content": content, "title": title}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Internal Server Error"))