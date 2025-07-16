from __future__ import annotations

from typing import Dict, Any
from telegram import Update
from telegram.ext import ContextTypes


from State import State

class UserSession:
    def __init__(self, user_id: int):
        self.user_id = user_id
        from states.InitialState import InitialState
        from states.HomeTeamState import HomeTeamState
        from states.AwayTeamState import AwayTeamState
        from states.StakeState import StakeState
        from HomeGoalsState import HomeGoalsState
        from AwayGoalsState import AwayGoalsState
        from states.HomeConcededState import HomeConcededState
        from states.AwayConcededState import AwayConcededState
        from states.HomeWinPercentageState import HomeWinPercentageState
        from states.WeatherState import WeatherState
        from states.KeyPlayersInjuredState import KeyPlayersInjuredState
        from states.MatchImportanceState import MatchImportanceState
        from states.HomeCrowdSizeState import HomeCrowdSizeState
        from states.HomeCrowdSupportState import HomeCrowdSupportState
        from states.LastMeetingsDrawsState import LastMeetingsDrawsState
        from states.MatchDateState import MatchDateState
        from states.FinalState import FinalState
        
        self.states: list[State] = [
            InitialState(),          
            HomeTeamState(),         
            AwayTeamState(),         
            StakeState(),            
            HomeGoalsState(),        
            AwayGoalsState(),        
            HomeConcededState(),     
            AwayConcededState(),     
            HomeWinPercentageState(),
            WeatherState(),          
            KeyPlayersInjuredState(),
            MatchImportanceState(),  
            HomeCrowdSizeState(),    
            HomeCrowdSupportState(), 
            LastMeetingsDrawsState(),
            MatchDateState(),        
            FinalState()             
        ]
        self.current_index = 0
        self.session_data: Dict[str, Any] = {}

        self._current_state: State = self.states[self.current_index]
        self._current_state.set_user_session(self)

    def get_session_data(self) -> Dict[str, Any]:
        return self.session_data

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self._current_state.manage_message(update, context)

    def go_to_next_state(self):
        self.current_index = (self.current_index + 1) % len(self.states)
        self._current_state = self.states[self.current_index]
        self._current_state.set_user_session(self)