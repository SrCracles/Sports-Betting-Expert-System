from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State
from Finder import Finder

class InitialState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        response="Let me ask you some questions... What is the home team?"
        await update.message.reply_text(response)
        self.user_session.go_to_next_state()
        