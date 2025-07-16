from __future__ import annotations
from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes


class State(ABC):
    @abstractmethod
    def set_user_session(self, user_session): # No quotes needed here
        pass

    @abstractmethod
    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass