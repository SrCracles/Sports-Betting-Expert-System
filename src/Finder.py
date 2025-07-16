import pandas as pd
import os

class Finder:
    def __init__(self):
        # Usar ruta absoluta basada en la ubicación del script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'data', 'teams_stats.csv')
        self.teams_df = pd.read_csv(csv_path)
        self.teams = self.teams_df['team'].tolist()
    
    def get_all_teams(self):
        return "\n".join(self.teams)
    
    def find_similar_teams(self, team_name):
        team_name = team_name.lower()
        similar_teams_list = []
        
        for team in self.teams:
            team_lower = team.lower()
            if team_name in team_lower or team_lower in team_name:
                similar_teams_list.append(team)
                    
        return "\n".join(similar_teams_list)
    
    def find_exact_team(self, team_name):
        team_name_lower = team_name.lower()
        
        for team in self.teams:
            if team.lower() == team_name_lower:
                return True
                
        return False