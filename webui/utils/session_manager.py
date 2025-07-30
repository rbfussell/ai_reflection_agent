"""Session state management for the WebUI."""

import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Session:
    """Represents a user session."""
    id: str
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    
    def touch(self):
        """Update last accessed time."""
        self.last_accessed = datetime.now()
        
    def is_expired(self, timeout_minutes: int = 60) -> bool:
        """Check if session has expired."""
        return datetime.now() - self.last_accessed > timedelta(minutes=timeout_minutes)


class SessionManager:
    """Manages user sessions for the WebUI."""
    
    def __init__(self):
        self._sessions: Dict[str, Session] = {}
        
    def create_session(self) -> str:
        """Create a new session and return its ID."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = Session(id=session_id)
        return session_id
        
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID, None if not found or expired."""
        if session_id not in self._sessions:
            return None
            
        session = self._sessions[session_id]
        if session.is_expired():
            del self._sessions[session_id]
            return None
            
        session.touch()
        return session
        
    def get_or_create_session(self, session_id: Optional[str] = None) -> tuple[str, Session]:
        """Get existing session or create new one."""
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session_id, session
                
        # Create new session
        new_id = self.create_session()
        return new_id, self._sessions[new_id]
        
    def cleanup_expired_sessions(self):
        """Remove expired sessions."""
        expired_ids = [
            sid for sid, session in self._sessions.items()
            if session.is_expired()
        ]
        for sid in expired_ids:
            del self._sessions[sid]
            
    def get_session_count(self) -> int:
        """Get number of active sessions."""
        self.cleanup_expired_sessions()
        return len(self._sessions)


# Global session manager instance
session_manager = SessionManager()