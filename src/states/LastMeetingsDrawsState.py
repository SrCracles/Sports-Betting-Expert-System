from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State
from datetime import datetime, timedelta

class LastMeetingsDrawsState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text.strip()
        session_data = self.user_session.get_session_data()
        
        try:
            last_meetings_draws = int(user_input)
            
            if last_meetings_draws < 0:
                response = "The number of draws cannot be negative. Please enter a positive number or zero:"
                await update.message.reply_text(response)
                return 

        except ValueError:
            response = "That doesn't look like a valid number. Please enter a whole number for the draws in the last 3 meetings:"
            await update.message.reply_text(response)
            return
        
        session_data['last_meetings_draws'] = last_meetings_draws
        
        response = f"Draws in last 3 meetings set to: {last_meetings_draws}. Now, what's the date of the match? Please use YYYY-MM-DD format, or type 'today' or 'tomorrow'."
        await update.message.reply_text(response)
        self.user_session.go_to_next_state() 
        return