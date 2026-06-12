from fastapi import APIRouter
from pydantic import BaseModel
from agent.memory_agent import agent_instance
from core.llm import get_llm_info
from core.schedule import get_status

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

from fastapi.responses import StreamingResponse

@router.get("/status")
async def status_endpoint():
    return {**get_status(), **get_llm_info()}

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Process the message through the Langgraph agent
    # The agent instance maintains the state using the user_id as the thread_id
    response_text = agent_instance.chat(user_id=request.user_id, message=request.message)
    return ChatResponse(response=response_text)

@router.post("/chat_stream")
async def chat_stream_endpoint(request: ChatRequest):
    def event_stream():
        for chunk in agent_instance.stream_chat(user_id=request.user_id, message=request.message):
            yield chunk
            
    return StreamingResponse(event_stream(), media_type="text/plain")
