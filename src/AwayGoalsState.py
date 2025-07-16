from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class AwayGoalsState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        session_data = self.user_session.get_session_data()
        
        away_team = session_data['away_team']
        home_team = session_data['home_team'] # Need home_team for the next prompt

        try:
            away_goals = float(user_input)
            
            if away_goals < 0:
                response = f"Goals cannot be negative. Please enter a positive number or zero for {away_team}:"
                await update.message.reply_text(response)
                return 

            session_data['away_goals'] = away_goals 
            
            response = f"Alright! Average goals for {away_team} are set to {away_goals}. Now, what are the average goals conceded by {home_team}?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state() 
            return

        except ValueError:
            response = f"That doesn't look like a valid number. Please enter the average goals scored by {away_team} (e.g., 2.5 or 1):"
            await update.message.reply_text(response)
            return