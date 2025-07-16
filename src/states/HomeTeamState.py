from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State
from Finder import Finder

class HomeTeamState(State):
    def __init__(self):
        self.user_session: UserSession | None = None
        self.finder=Finder()

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg=update.message.text
        if (self.finder.find_exact_team(msg)):
            self.user_session.get_session_data()['home_team']=msg.lower()
            response="Ok. What is the away team?"
            await update.message.reply_text(response)
            self.user_session.go_to_next_state()
            return
        
        similars=self.finder.find_similar_teams(msg)
        if similars!="":
            response="Uhmmm. I don't have that team in my list. Is one of these?"
            response+=similars
            await update.message.reply_text(response)
            return


        response="I have no idea what is that team. These are the available teams "
        response+=self.finder.get_all_teams()
        await update.message.reply_text(response)
        return





        
        