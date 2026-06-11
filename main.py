import uvicorn
import subprocess
import os
import sys
import threading
from fastapi import FastAPI
from core.config import settings
from api.routes import router as chat_router

# Initialize FastAPI app
app = FastAPI(title=settings.PROJECT_NAME)

# Include the router
app.include_router(chat_router)

def run_streamlit():
    """Run the Streamlit frontend in a separate process."""
    streamlit_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", streamlit_path, "--server.port", str(settings.STREAMLIT_PORT), "--server.headless", "true"],
        env=os.environ.copy()
    )

if __name__ == "__main__":
    print(f"Starting {settings.PROJECT_NAME} Backend on port {settings.API_PORT}...")
    print(f"Starting Streamlit Frontend on port {settings.STREAMLIT_PORT}...")
    
    # Start streamlit in a background thread so it launches alongside uvicorn
    threading.Thread(target=run_streamlit, daemon=True).start()
    
    # Start Uvicorn for FastAPI
    uvicorn.run("main:app", host="0.0.0.0", port=settings.API_PORT, reload=True)
