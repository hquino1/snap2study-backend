from app.routers.images import analyze_image
from fastapi.testclient import TestClient
from app.utils.auth import verify_auth
from main import app

def mock_verify_auth():
        return ("fake-client", "fake-user")

studyExample = '''
    Question: What is the primary function of mitochondria?
    Answer: They produce ATP through cellular respiration.

    Question: Why are mitochondria called the "powerhouse of the cell"?
    Answer: Because they generate most of the cell’s usable energy.

    Question: What process mainly occurs in mitochondria?
    Answer: The Krebs cycle and oxidative phosphorylation.
'''

client = TestClient(app)
app.dependency_overrides[verify_auth] = mock_verify_auth

def test_empty_input(mocker):
    mock_llm = mocker.patch("app.routers.images.llm_generate")
    mock_llm.return_value = "Mock response"

    response = client.post("/analyze-image", json={"input": "", "studyMethod": "Flashcards", "model": "mistral:7b-instruct", "type": "text"})
    assert response.status_code == 422


def test_invalid_study_input():

    response = client.post("/analyze-image", json={"input": "Hello", "studyMethod": "Flashcards", "model": "mistral:7b-instruct", "type": "text"})
    assert response.status_code == 400

def test_valid_study_input():

    response = client.post("/analyze-image", json={"input": studyExample, "studyMethod": "Flashcards", "model": "mistral:7b-instruct", "type": "text"})
    assert response.status_code == 200