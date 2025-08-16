from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.utils.auth import verify_auth
from app.routers import images
from app.routers import sets

settings = get_settings()

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(images.router)
app.include_router(sets.router)

@app.get('/')
def test():
    return {"message": "Hello world!"}