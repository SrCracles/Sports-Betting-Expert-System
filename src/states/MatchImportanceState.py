from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class MatchImportanceState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        session_data = self.user_session.get_session_data()
        
        try:
            match_importance = int(user_input)
            
            if not (1 <= match_importance <= 10):
                response = "Match importance must be a number between 1 and 10. Please try again:"
                await update.message.reply_text(response)
                return 

            session_data['match_importance'] = match_importance 
            
            response = f"Match importance set to: {match_importance}. Now, what's the estimated size of the home crowd (e.g., 50000)?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state() 
            return

        except ValueError:
            response = "That doesn't look like a valid number. Please enter the match importance as a whole number between 1 and 10:"
            await update.message.reply_text(response)
            return