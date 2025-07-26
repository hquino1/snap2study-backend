from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ENV: str = "local"

    class Config():
        env_file = ".env"


def get_settings():
    return Settings()