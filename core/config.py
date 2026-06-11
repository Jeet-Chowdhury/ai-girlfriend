from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Girlfriend Chat"
    API_PORT: int = 8000
    STREAMLIT_PORT: int = 8501
    OLLAMA_MODEL: str = "fluffy/l3-8b-stheno-v3.2"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    GF_NAME: str = "Stheno"
    GF_AGE: int = 21
    GF_PROFESSION: str = "College Student"

    class Config:
        env_file = ".env"

settings = Settings()
