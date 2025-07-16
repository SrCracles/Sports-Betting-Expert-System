from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class WeatherState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text.lower()
        session_data = self.user_session.get_session_data()
        
        if user_input not in ['good', 'bad']:
            response = "Weather can only be 'good' or 'bad'. Please enter one of these options:"
            await update.message.reply_text(response)
            return 

        session_data['weather'] = user_input 
        
        response = f"Weather conditions set to: '{user_input}'. Now, are there any key players injured? Please reply with 'home', 'away', 'both', or 'no'."
        await update.message.reply_text(response)
        self.user_session.go_to_next_state() 
        return