from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class HomeCrowdSizeState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        session_data = self.user_session.get_session_data()
        
        home_team = session_data['home_team']

        try:
            home_crowd_size = int(user_input)
            
            if home_crowd_size <= 0:
                response = "The crowd size must be a positive number. Please enter a number greater than zero:"
                await update.message.reply_text(response)
                return 

            session_data['home_crowd_size'] = home_crowd_size 
            
            response = f"Home crowd size set to: {home_crowd_size}. Now, what's the home crowd's support level as a percentage (0-100)?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state() 
            return

        except ValueError:
            response = f"That doesn't look like a valid number. Please enter the home crowd size as a whole number:"
            await update.message.reply_text(response)
            return