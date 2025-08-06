from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from app.utils.image_text_extraction import image_text_extraction
from app.utils.ai import llm_generate
from app.utils.auth import verify_auth

router = APIRouter()

class ImageAnalyze(BaseModel):
    input: str
    studyMethod: str
    model: str
    type: str


prompts = {
    "Flashcards":
    '''
    You are an assistant that generates effective study flashcards from course review notes.
        Extract key concepts, definitions, or questions and present them in a Q&A flashcard format.
        Return the flashcards as a JSON array with "question" and "answer" fields.

        Output a JSON array. Each object must have:
        - "question": a clear question relevant to the course review.
        - "answer": answer or answers to the question.

        Only include content relevant to studying. Respond only with a JSON array of flashcards. 
        Do NOT include any explanations or text before or after the JSON.
    ''',

    "PracticeExam":
    '''
    You are an assistant that generates realistic college-level exams from course review notes.
        Your task is to extract key concepts, definitions, and potential test questions from the input and generate multiple-choice questions (MCQs).

        Output a JSON array. Each object must have:
        - "question": a clear question relevant to the course review.
        - "answers": an array of 4 answer choices, where exactly one is correct.
        - "correct": the index (0-3) of the correct answer in the "answers" array.

        Requirements:
        - Focus strictly on academic and study-relevant content.
        - Do NOT include any explanations or text before or after the JSON output.

        Respond ONLY with the JSON array.
    '''
}


@router.post("/analyze-image")
async def analyze_image(body: ImageAnalyze, auth: str = Depends(verify_auth)):
    try:
        if body.type == 'image':
            text = image_text_extraction(body.input)
        else:
            text = body.input
        
        print("Text Extraction: ", text)
        response = llm_generate(body.model, text, prompts[body.studyMethod])
        print("LLM Response: ", response)

        return {"content": response}

    except Exception as e:
        return {"error": "Analyze Image internal server error"}
