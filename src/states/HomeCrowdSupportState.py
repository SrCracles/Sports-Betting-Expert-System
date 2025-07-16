from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State

class HomeCrowdSupportState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text.strip()
        session_data = self.user_session.get_session_data()
        
        home_team = session_data['home_team']
        
        try:
            home_crowd_support = int(user_input)
            
            if not (0 <= home_crowd_support <= 100):
                response = f"Crowd support percentage must be between 0 and 100. Please try again for {home_team}:"
                await update.message.reply_text(response)
                return
        
        except ValueError:
            response = f"That doesn't look like a valid percentage. Please enter a whole number between 0 and 100 for {home_team}:"
            await update.message.reply_text(response)
            return

        session_data['home_crowd_support'] = home_crowd_support 
        
        response = f"Home crowd support for {home_team} is set to: {home_crowd_support}%. Now, how many draws have there been in the last 3 meetings between these teams? (Enter a number):"
        await update.message.reply_text(response)
        self.user_session.go_to_next_state() 
        return