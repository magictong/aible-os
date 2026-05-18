import uuid
from typing import Optional
from datetime import datetime

class ChatSession:
    """AI App 对话会话"""
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.messages: list[dict] = []
        self.created_at = datetime.now().isoformat()
    
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def get_history(self, limit: int = 20) -> list[dict]:
        """获取最近 N 条历史消息"""
        return self.messages[-limit:]

class SessionManager:
    """会话管理器"""
    
    def __init__(self):
        self._sessions: dict[str, dict[str, ChatSession]] = {}  # {app_id: {session_id: ChatSession}}
    
    def get_or_create(self, app_id: str, session_id: str = None) -> ChatSession:
        if app_id not in self._sessions:
            self._sessions[app_id] = {}
        
        if session_id and session_id in self._sessions[app_id]:
            return self._sessions[app_id][session_id]
        
        session = ChatSession(session_id)
        self._sessions[app_id][session.session_id] = session
        return session
    
    def list_sessions(self, app_id: str) -> list[ChatSession]:
        return list(self._sessions.get(app_id, {}).values())
    
    def clear_sessions(self, app_id: str):
        if app_id in self._sessions:
            self._sessions[app_id] = {}

session_manager = SessionManager()
