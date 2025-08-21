from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from app.utils.auth import verify_auth
from app.utils.ai import llm_generate
from app.db.sets import get_sets, get_set_content_by_id, create_set

router = APIRouter()
validStudyMethods = {"Flashcards", "PracticeExam"}

studyActivityPrompts = {
    "explanation": '''
        You are an assistant that generates effective and concise explanations when given the question
        and answer unless the answer happens to be wrong. Return your answer in just sentences in 1 paragraph, no bullet points or other forms of text alteration.
        Return it in a json object ONLY no array or any other form.

        Output a JSON array. Each object must have:
        - "Explanation": a thorough explnation that clearly helps the user learn and adds context.

    ''',

    "questions": '''
     You are an assistant that generates similar college-level question when given a questions from the user when given a similar question.
        Create questions that would be asked on an exam or different kinds of scenarios that would be tricky. 
        Create around 4 - 5 objects.

        Output a JSON array. Each object must have:
        - "question": a clear question relevant to the subject and question that was given to the user.

        Requirements:
        - Focus strictly on academic and study-relevant content.
        - Do NOT include any explanations or text before or after the JSON output.

        Respond ONLY with the JSON array.  
    ''',

    "definitions": '''
     You are an assistant that generates helpful definitions of vocabular when given a question and answer.
        Only create defintions if they are helpful to what the user is provided.

        Output a JSON array. Each object must have:
        - "term": the term that is being defined.
        - "definition": a clear defnition relevant to the subject and question that was given by the user.

        Requirements:
        - Focus strictly on academic and study-relevant content.
        - Do NOT include any explanations or text before or after the JSON output.

        Respond ONLY with the JSON array. 
    ''',

    "visual": '''
     You are an assistant that generates helpful visual aids for course subjects given a question and answer.

    Create a Mermaid diagram to help the user learn. Make it visually appealing, easy to understand, and detailed.

    CRITICAL REQUIREMENTS:
    - Output ONLY a JSON object (not an array)
    - The "mermaid" field must contain ONLY the raw Mermaid code
    - NO markdown code blocks (no ```mermaid```)
    - NO additional formatting or text
    - Ensure there are no spaces in node labels (use underscores or camelCase)

    Example output format:
    {"mermaid": "graph TD; NodeA-->NodeB; NodeB-->NodeC"}

    Generate exactly one diagram in this format.

    '''
}

class SetCreate(BaseModel):
    title: str
    studyMethod: str
    content: list

class StudyActivityBody(BaseModel):
    model: str
    question: str
    answer: str

# Individual Set Operations
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

# Set Content Operations
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


@router.post("/sets/{studyActivity}")
def set_id_content(body: StudyActivityBody, studyActivity: str, auth: str = Depends(verify_auth)):
    try:
        supabase, user = auth

        response = llm_generate(body.model, f"Question: ${body.question}\nAnswer: ${body.answer}", studyActivityPrompts[studyActivity])
        print("Response: ", response)
        return {"activity_content": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))