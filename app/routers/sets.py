from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from app.utils.auth import verify_auth
from app.utils.image_text_extraction import image_text_extraction
from app.db.sets import get_sets, get_set_content_by_id, create_set

router = APIRouter()
validStudyMethods = {"Flashcards", "PracticeExam"}

class SetCreate(BaseModel):
    title: str
    studyMethod: str
    content: list


@router.get("/sets")
def sets(auth: str = Depends(verify_auth)):
    try:

        supabase, user = auth
        flashcards, practiceExams = get_sets(supabase, user.user.id)

        return {"flashcards": flashcards, "practiceExams": practiceExams}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Internal Server Error"))


@router.post("/sets")
def new_set(body: SetCreate, auth: str = Depends(verify_auth)):
    try:
        supabase, user = auth

        if body.studyMethod not in validStudyMethods or len(body.title) <= 0:
            raise HTTPException(status_code=400, detail=str("Invalid Input"))
        print("Content: ", body.content) 
        content = create_set(
            supabase, user.user.id, body.title, body.studyMethod, body.content
        )

        return {"set_content": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Internal Server Error"))


@router.get("/sets/{setId}/{studyMethod}")
def set_id_content(setId: str, studyMethod: str, auth: str = Depends(verify_auth)):
    try:
        supabase, user = auth

        if studyMethod not in validStudyMethods:
            raise HTTPException(status_code=400, detail=str("Invalid Input"))

        content, title = get_set_content_by_id(supabase, setId, studyMethod)

        return {"set_content": content, "title": title}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
