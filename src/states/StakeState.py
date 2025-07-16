from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State
from Finder import Finder

class StakeState(State):
    def __init__(self):
        self.user_session: UserSession | None = None
        self.finder = Finder() 

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = update.message.text.lower()
        
        # Keywords for Qualifying Stage
        qualifier_keywords = [
            "qualifier", "qualifiers", "qualifying", "qualification", 
            "preliminary", "play-in", "play in", "road to", 
            "pre-tournament", "first one", "first"
        ]

        # Keywords for Group Stage
        group_keywords = [
            "group", "group stage", "group phase", "second one", 
            "first round", "initial stage", "second"
        ]

        # Keywords for Knockout Stage
        knockout_keywords = [
            "knockout", "knockout stage", "elimination", "eliminations", "eliminatory", 
            "round of 16", "quarter-final", "quarter final", "quarterfinals", 
            "semi-final", "semi final", "semifinals", "final", 
            "last 16", "last eight", "last four", "championship", 
            "playoffs", "single elimination", "do or die", "third one","third"
        ]

        # 1. Check for Qualifying Stage (Eliminatories)
        if any(keyword in msg for keyword in qualifier_keywords):
            self.user_session.get_session_data()['match_stage'] = 'qualifier'
            response = "Okay, a match from the Qualifying Stage. Now what is the average goals for the home team?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state()
            return
        
        # 2. Then check for Group Stage (Fase de Grupos)
        elif any(keyword in msg for keyword in group_keywords):
            self.user_session.get_session_data()['match_stage'] = 'group'
            response = "Understood! A match from the Group Stage. Now what is the average goals for the home team?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state()
            return
        
        # 3. Finally, check for Knockout Stage
        elif any(keyword in msg for keyword in knockout_keywords):
            self.user_session.get_session_data()['match_stage'] = 'knockout'
            response = "Got it! So, a match from the Knockout Stage. Now what is the average goals for the home team?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state()
            return
        
        
        else:
            response = "I'm sorry, I didn't understand. Are you referring to a match from the Qualifying Stage, the Group Stage, or the Knockout Stage?"
            await update.message.reply_text(response)
            return