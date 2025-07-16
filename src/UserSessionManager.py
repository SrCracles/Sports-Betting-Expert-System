from __future__ import annotations
from typing import Dict
from UserSession import UserSession

class UserSessionManager:
    def __init__(self):
        self.user_sessions: Dict[int, UserSession] = {}
    def get_user_session(self, user_id: int) -> UserSession:
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = UserSession(user_id)
        return self.user_sessions[user_id]