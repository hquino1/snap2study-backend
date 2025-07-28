from crypt import methods
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import images

settings = get_settings()

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENV == "local" else [settings.ENV],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(images.router)

@app.get('/')
def test():
    return {"message": "Hello world!"}