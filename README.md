# AI Girlfriend Chat Application

A complete chat application using FastAPI for the backend and Streamlit for the frontend. It features an uncensored, human-like AI companion using the `fluffy/l3-8b-stheno-v3.2` model via Ollama. Context and memory are handled seamlessly with Langchain and Langgraph.

## Prerequisites
1. **Python 3.8+**
2. **Ollama**: Installed and running on your system.

## Setup Instructions

### 1. Download the Ollama Model
Make sure Ollama is running, then pull and run the required model:
```bash
ollama run fluffy/l3-8b-stheno-v3.2
```

### 2. Activate Virtual Environment
If you haven't already, ensure you are using the virtual environment:
```bash
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
The application is fully configurable via the `.env` file. You can copy the provided example to get started:
```bash
cp .env.example .env
```
Inside `.env`, you can customize:
- `GF_NAME`: Her name.
- `GF_AGE`: Her age.
- `GF_PROFESSION`: Her profession.
- `API_PORT`: Port for the FastAPI backend (default `8000`).
- `STREAMLIT_PORT`: Port for the Streamlit UI (default `8501`).

### 5. Run the Application
You can start the entire project (both the FastAPI backend and Streamlit frontend) with a single command:
```bash
python main.py
```

### 6. Access the App
- **Chat Interface (Streamlit)**: [http://localhost:8501](http://localhost:8501)
- **API Documentation (FastAPI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
