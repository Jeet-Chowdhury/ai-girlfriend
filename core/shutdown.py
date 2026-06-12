import atexit
import os
import signal
import subprocess
import sys
from typing import Optional

_streamlit_process: Optional[subprocess.Popen] = None
_shutting_down = False


def register_streamlit_process(process: subprocess.Popen) -> None:
    global _streamlit_process
    _streamlit_process = process


def kill_process_tree(pid: int) -> None:
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return

    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
    except (ProcessLookupError, PermissionError, OSError):
        pass


def cleanup_resources() -> None:
    global _shutting_down
    if _shutting_down:
        return
    _shutting_down = True

    if _streamlit_process and _streamlit_process.poll() is None:
        print("Stopping Streamlit...")
        kill_process_tree(_streamlit_process.pid)
        try:
            _streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass

    from core.config import settings

    if settings.OLLAMA_UNLOAD_ON_EXIT:
        from core.llm import unload_ollama_model

        print("Unloading Ollama model from GPU...")
        unload_ollama_model()


def setup_shutdown_handlers() -> None:
    atexit.register(cleanup_resources)

    def handle_signal(signum, frame):
        cleanup_resources()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    if sys.platform == "win32" and hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, handle_signal)
