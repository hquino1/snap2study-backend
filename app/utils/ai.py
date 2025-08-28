import ollama
import json
from app.config import get_settings

settings = get_settings()


def llm_generate(model, userPrompt, systemPrompt):
    try:
        LLM = ollama.Client(host=settings.OLLAMA_URL)

        response = LLM.generate(model=model, prompt=userPrompt, system=systemPrompt)
        print("Response: ", response["response"])
        parsed_response = json.loads(response["response"])

        return parsed_response

    except Exception as e:
        print("Exception in LLM_generate: ", e)
