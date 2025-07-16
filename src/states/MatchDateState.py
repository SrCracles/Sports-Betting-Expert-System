from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State
from datetime import datetime, timedelta

class MatchDateState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text.strip().lower()
        session_data = self.user_session.get_session_data()
        
        match_date = datetime.now().date() 
        
        if user_input:
            if user_input == 'today':
                match_date = datetime.now().date()
            elif user_input == 'tomorrow':
                match_date = datetime.now().date() + timedelta(days=1)
            else:
                try:
                    match_date = datetime.strptime(user_input, '%Y-%m-%d').date()
                except ValueError:
                    response = "That's not a valid date format. Please use **YYYY-MM-DD**, or type 'today' or 'tomorrow'."
                    await update.message.reply_text(response)
                    return
        
        if match_date < datetime.now().date():
            response = "The match date cannot be in the past. Please enter a date from today onwards:"
            await update.message.reply_text(response)
            return

        session_data['match_date'] = match_date
        
        response = f"Match date set to: {match_date.strftime('%Y-%m-%d')}. Now lets see how are the bets... Type OK to continue"
        await update.message.reply_text(response)
        self.user_session.go_to_next_state() 
        return