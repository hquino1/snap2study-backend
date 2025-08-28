from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    ENV: str = "local"
    SUPABASE_URL: str
    SUPABASE_KEY: str
    OLLAMA_URL: str

    class Config():
        env_file = ".env"


def get_settings():
    return Settings()
