from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama

from core.config import settings


def create_chat_model() -> BaseChatModel:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "groq":
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is required when LLM_PROVIDER=groq. "
                "Get a free key at https://console.groq.com/keys"
            )
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.85,
        )

    if provider == "local":
        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.85,
            top_p=0.9,
        )

    raise ValueError(
        f'Invalid LLM_PROVIDER "{settings.LLM_PROVIDER}". Use "local" or "groq".'
    )


def get_llm_info() -> dict:
    provider = settings.LLM_PROVIDER.lower()
    if provider == "groq":
        return {"provider": "groq", "model": settings.GROQ_MODEL}
    return {"provider": "local", "model": settings.OLLAMA_MODEL}


def unload_ollama_model() -> bool:
    """Tell Ollama to unload the model from GPU/RAM (keep_alive=0)."""
    try:
        import requests

        response = requests.post(
            f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate",
            json={"model": settings.OLLAMA_MODEL, "keep_alive": 0},
            timeout=10,
        )
        return response.ok
    except Exception:
        return False
