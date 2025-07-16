from telegram import Update
from telegram.ext import ContextTypes
from UserSession import UserSession
from State import State
from Bayesian_Network import Bayesian_Network
from expert_system import ExpertSystemManager

class FinalState(State):
    def __init__(self):
        self.user_session: UserSession | None = None

    def set_user_session(self, user_session: UserSession):
        self.user_session = user_session
        self.bayesian_network= Bayesian_Network()
        self.expert_system = ExpertSystemManager()

    async def manage_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        session_data = self.user_session.get_session_data()
        print("-----USER DATA------- ")
        print(session_data)
        print("-----USER DATA------- ")

        evidence = {
        'home_team': session_data['home_team'],
        'away_team': session_data['away_team']
        }
        prob=self.bayesian_network.calculate_probabilities(evidence)
        print("----bayesian--------")
        print("HOME")
        print(prob['home'])
        print("AWAY")
        print(prob['away'])
        print("DRAW")
        print(prob['draw'])
        print("----bayesian--------")
        print("----bayesian--------")
        
        analysis_result = self.expert_system.analyze_match(
            home_prob=prob['home'],
            away_prob=prob['away'],
            draw_prob=prob['draw'],
            session_data=session_data
        )
        
        print("\n--- Final Match Data Collected ---")
        for key, value in session_data.items():
            print(f"{key}: {value}")
        print("----------------------------------\n")
        
        response = "Thank you! All match details have been collected. You can start over with /start. These are the results"


        await update.message.reply_text(analysis_result, parse_mode='Markdown')
        self.user_session.go_to_next_state()
        return