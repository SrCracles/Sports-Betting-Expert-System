from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class KeyPlayersInjuredState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text.lower()
        session_data = self.user_session.get_session_data()
        
        valid_options = ['home', 'away', 'both', 'no']

        if user_input not in valid_options:
            response = "Please specify 'home', 'away', 'both', or 'no' if there are no key players injured."
            await update.message.reply_text(response)
            return 

        session_data['key_players_injured'] = user_input 
        
        response = f"Key players injured status set to: '{user_input}'. Now, on a scale of 1 to 10, how would you rate the importance of this match? (1 being low importance, 10 being very high importance):"
        await update.message.reply_text(response)
        self.user_session.go_to_next_state() 
        return