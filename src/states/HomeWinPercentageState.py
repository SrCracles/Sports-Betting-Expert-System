from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class HomeWinPercentageState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        session_data = self.user_session.get_session_data()
        
        home_team = session_data['home_team'] 

        try:
            home_win_percentage = float(user_input)
            
            if not (0 <= home_win_percentage <= 100):
                response = f"Win percentage must be between 0 and 100 (e.g., 75 for 75%). Please enter the win percentage for {home_team}:"
                await update.message.reply_text(response)
                return 

            session_data['home_win_percentage'] = home_win_percentage 
            
            # Prompt for weather conditions
            response = f"Understood! Win percentage for {home_team} is set to {home_win_percentage}%. Now, please describe the weather conditions for the match (good or bad)"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state() 
            return

        except ValueError:
            response = f"That doesn't look like a valid number. Please enter the win percentage for {home_team} (e.g., 75 for 75%):"
            await update.message.reply_text(response)
            return