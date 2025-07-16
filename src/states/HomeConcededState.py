from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class HomeConcededState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        session_data = self.user_session.get_session_data()
        
        home_team = session_data['home_team']
        away_team = session_data['away_team']

        try:
            home_conceded = float(user_input)
            
            if home_conceded < 0:
                response = f"Goals conceded can't be negative. Please enter a positive number or zero for {home_team}:"
                await update.message.reply_text(response)
                return 

            session_data['home_conceded'] = home_conceded 
            
            response = f"Okay! Average goals conceded by {home_team} are set to {home_conceded}. Now, what are the average goals conceded by {away_team}?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state() 
            return

        except ValueError:
            response = f"That doesn't look like a valid number. Please enter the average goals conceded by {home_team} (e.g., 1.5 or 0):"
            await update.message.reply_text(response)
            return