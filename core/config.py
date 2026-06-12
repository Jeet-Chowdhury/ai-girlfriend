from typing import Literal

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Girlfriend Chat"
    API_PORT: int = 8000
    STREAMLIT_PORT: int = 8501
    API_RELOAD: bool = False
    LLM_PROVIDER: Literal["local", "groq"] = "local"
    OLLAMA_MODEL: str = "fluffy/l3-8b-stheno-v3.2"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_UNLOAD_ON_EXIT: bool = True
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "qwen/qwen3-32b"
    GF_NAME: str = "Stheno"
    GF_AGE: int = 21
    GF_PROFESSION: str = "College Student"
    APP_TIMEZONE: str = "Asia/Kolkata"
    WORK_START: str = "09:00"
    WORK_END: str = "17:00"
    SLEEP_START: str = "23:00"
    SLEEP_END: str = "07:00"

    class Config:
        env_file = ".env"

settings = Settings()
