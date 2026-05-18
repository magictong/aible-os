from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from typing import Optional
import json

from core.engine import AppEngine, engine as app_engine
from core.session import session_manager
from core.app_loader import AppLoader
from config import APPS_DIR, get_public_settings

router = APIRouter(prefix="/api/chat", tags=["chat"])
loader = AppLoader(APPS_DIR)

class ChatRequest(BaseModel):
    app_id: str
    message: str
    session_id: Optional[str] = None

@router.post("/send")
async def send_message(req: ChatRequest):
    """发送消息给 AI App，返回流式 SSE 响应"""
    app_info = loader.get_app(req.app_id)
    if not app_info:
        raise HTTPException(status_code=404, detail="App not found")

    # Refresh LLM config from settings file each time
    app_engine.refresh()

    session = session_manager.get_or_create(req.app_id, req.session_id)
    session.add_message("user", req.message)
    
    async def event_generator():
        full_response = ""
        async for chunk in app_engine.run_app(
            app_id=req.app_id,
            app_entry="",
            app_dir=app_info.app_dir,
            message=req.message,
            history=session.get_history(limit=10)
        ):
            full_response += chunk
            yield {"event": "chunk", "data": json.dumps({"text": chunk, "session_id": session.session_id})}
        
        session.add_message("assistant", full_response)
        yield {"event": "done", "data": json.dumps({"session_id": session.session_id})}
    
    return EventSourceResponse(event_generator())

@router.get("/sessions/{app_id}")
async def list_sessions(app_id: str):
    """列出 App 的对话会话"""
    sessions = session_manager.list_sessions(app_id)
    return [
        {
            "session_id": s.session_id,
            "created_at": s.created_at,
            "message_count": len(s.messages),
            "preview": s.messages[0]["content"][:50] if s.messages else ""
        }
        for s in sessions
    ]

@router.get("/history/{app_id}/{session_id}")
async def get_history(app_id: str, session_id: str):
    """获取会话历史"""
    session = session_manager.get_or_create(app_id, session_id)
    return {"messages": session.get_history()}
