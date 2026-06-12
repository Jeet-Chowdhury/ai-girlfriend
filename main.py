import os
import subprocess
import sys

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.routes import router as chat_router
from core.config import settings
from core.llm import get_llm_info
from core.shutdown import cleanup_resources, register_streamlit_process, setup_shutdown_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    cleanup_resources()


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(chat_router)


def start_streamlit() -> subprocess.Popen:
    streamlit_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    popen_kwargs: dict = {"env": os.environ.copy()}

    if sys.platform == "win32":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            streamlit_path,
            "--server.port",
            str(settings.STREAMLIT_PORT),
            "--server.headless",
            "true",
        ],
        **popen_kwargs,
    )
    register_streamlit_process(process)
    return process


if __name__ == "__main__":
    setup_shutdown_handlers()

    llm = get_llm_info()
    print(f"Starting {settings.PROJECT_NAME} Backend on port {settings.API_PORT}...")
    print(f"LLM: {llm['provider']} ({llm['model']})")
    print(f"Starting Streamlit Frontend on port {settings.STREAMLIT_PORT}...")
    print("Press Ctrl+C to stop (cleans up Streamlit + Ollama GPU memory).")

    start_streamlit()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )
