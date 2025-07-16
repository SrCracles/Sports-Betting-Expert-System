import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandas.api.types import is_string_dtype # <-- ¡Importa esto!

# Determine the winner of a match based on scores
def generate_winner(row): 
    # There are two columns in each row.
    # We assign draw or the value that is the column home or away
    if row['home_score'] == row['away_score']:
        return 'draw'
    elif row['home_score'] > row['away_score']:
        return row['home_team']
    else:
        return row['away_team']
    
def generate_winner_2(row):
    #Writes in a row
    if row['home_score'] == row['away_score']:
        return 'draw'
    elif row['home_score'] > row['away_score']:
        return "home_team"
    else:
        return "away_team"
def sort_neutral(row):
    if row['neutral']==False:
 
        return row
    print("BEFORE")
    print(row)
    team_1=row['home_team']
    team_2=row['away_team']
    if (team_1.lower()>team_2.lower()):
        row['away_team']=team_1
        row['home_team']=team_2
    print("after ")
    print(row)
    return row

def lowercasing(row):
    for column_name,column_series in row.items():
        if column_series.dtype =='string':
            column_series=column_series.lower()
    return row




def generate_month(row):
    #Day of the week
    date = pd.to_datetime(row['date'], format="%Y-%m-%d")
    return date.month_name()

# Categorize team strength based on their statistics
def categorize_team_strength(team_stats):
    if team_stats['avg_goals_for'] >= 1.5 and team_stats['win_percentage'] >= 50:
        return 'strong'
    elif team_stats['avg_goals_for'] >= 1.1 and team_stats['win_percentage'] >= 40:
        return 'medium'
    else:
        return 'weak'

# Categorize match risk based on teams strengths
def categorize_match_risk(row):
    if row['home_strength'] == 'strong' and row['away_strength'] == 'weak':
        return 'low_risk'
    elif row['home_strength'] == 'weak' and row['away_strength'] == 'strong':
        return 'high_risk'
    elif row['home_strength'] == row['away_strength']:
        return 'medium_risk'
    else:
        return 'medium_risk'


def load_and_process_data():
  
    
    results = pd.read_csv('./data/results.csv')
    
    # Filter only World Cup matches (including qualifications)
    world_cup_data = results[
        (results['tournament'].str.contains('FIFA World Cup', case=False, na=False)) |
        (results['tournament'] == 'FIFA World Cup')
    ]
    
    # Create a copy for the raw World Cup data
    world_cup_raw = world_cup_data.copy()
    
    # Add derived columns
    world_cup_data['winner'] = world_cup_data.apply(generate_winner, axis=1)
    
    
    # Calculate team statistics
    team_stats = {}
    
    # Get unique teams
    all_teams = set(world_cup_data['home_team'].unique()) | set(world_cup_data['away_team'].unique())
    
    for team in all_teams:
        # Home matches
        home_matches = world_cup_data[ (world_cup_data['home_team'] == team) ]
        # Away matches
        away_matches = world_cup_data[(world_cup_data['away_team'] == team) ]

        
        
        
        # Total matches
        total_matches = len(home_matches) + len(away_matches) 
        
        if total_matches == 0:
            continue
        
        # Calculate wins, losses, draws
        home_wins = len(home_matches[home_matches['winner'] == team])
        away_wins = len(away_matches[away_matches['winner'] == team])
        

        total_wins = home_wins + away_wins 
        
        # Calculate goals
        home_goals_for = home_matches['home_score'].sum()
        away_goals_for = away_matches['away_score'].sum()
        total_goals_for = home_goals_for + away_goals_for
        
        home_goals_against = home_matches['away_score'].sum()
        away_goals_against = away_matches['home_score'].sum()
        total_goals_against = home_goals_against + away_goals_against
        
        # Store team statistics
        team_stats[team] = {
            'matches': total_matches,
            'wins': total_wins,
            'win_percentage': (total_wins / total_matches) * 100 if total_matches > 0 else 0,
            'avg_goals_for': total_goals_for / total_matches if total_matches > 0 else 0,
            'avg_goals_against': total_goals_against / total_matches if total_matches > 0 else 0,
            'home_win_percentage': (home_wins / len(home_matches)) * 100 if len(home_matches) > 0 else 0,
            'away_win_percentage': (away_wins / len(away_matches)) * 100 if len(away_matches) > 0 else 0,
        }
        
        # Categorize team strength
        team_stats[team]['strength'] = categorize_team_strength(team_stats[team])
    
    print(f"Processed {len(world_cup_data)} World Cup matches for {len(team_stats)} teams")
    
    return world_cup_data, team_stats

if __name__ == "__main__":
    world_cup_data, team_stats = load_and_process_data()
    
    # Save raw World Cup data to CSV
    world_cup_raw = pd.read_csv('./data/results.csv')
    world_cup_raw = world_cup_raw[
        (world_cup_raw['tournament'].str.contains('FIFA World Cup', case=False, na=False)) |
        (world_cup_raw['tournament'] == 'FIFA World Cup')
    ]
    world_cup_raw['winner'] = world_cup_data.apply(generate_winner_2, axis=1)
    world_cup_raw['month'] = world_cup_data.apply(generate_month, axis=1)
    world_cup_raw = world_cup_raw.apply(sort_neutral,axis=1)

    # lower case string attributes
    for col in world_cup_raw.columns:
        if is_string_dtype(world_cup_raw[col]):
            world_cup_raw[col] = world_cup_raw[col].str.lower()


    world_cup_raw.to_csv('./data/results_worldcup.csv', index=False)
    print(f"\nCSV file './data/results_worldcup.csv' created successfully with {len(world_cup_raw)} World Cup matches")
    
    # Create a DataFrame from team_stats dictionary
    teams_list = []
    for team_name, stats in team_stats.items():
        team_row = {
            'team': team_name,
            'strength': stats['strength'],
            'win_percentage': stats['win_percentage'],
            'avg_goals_for': stats['avg_goals_for'],
            'avg_goals_against': stats['avg_goals_against'],
            'matches': stats['matches'],
            'wins': stats['wins'],
            'home_win_percentage': stats['home_win_percentage'],
            'away_win_percentage':stats['away_win_percentage'],
            
        }
        teams_list.append(team_row)
    

    
    
    # Convert to DataFrame
    teams_df = pd.DataFrame(teams_list)
    
    # Sort by team name for better organization
    teams_df = teams_df.sort_values('team').reset_index(drop=True)


    # lower case string attributes
    for col in teams_df.columns:
        if is_string_dtype(teams_df[col]):
            teams_df[col] = teams_df[col].str.lower()
    
    # Save to CSV
    teams_df.to_csv('./data/teams_stats.csv', index=False)

    
    
    print(f"\nCSV file 'teams_stats.csv' created successfully with {len(teams_df)} teams")
    print("\nColumn names in the CSV:")
    print(list(teams_df.columns))
    
    print("\nPreview of the first 5 rows:")
    print(teams_df.head())


    # Merge data sets
    final_dataset = pd.merge(world_cup_raw, teams_df, left_on='home_team', right_on='team', how='left')
    final_dataset = final_dataset.rename(columns={
        'strength': 'home_strength',
        'win_percentage': 'home_win_percentage_overall',
        'avg_goals_for': 'home_avg_goals_for',
        'avg_goals_against': 'home_avg_goals_against',
        'matches': 'home_matches',
        'wins': 'home_wins',
        'home_win_percentage': 'home_home_win_percentage',
        'away_win_percentage': 'home_away_win_percentage',
        
    }).drop(columns=['team'])


    final_dataset = pd.merge(final_dataset, teams_df, left_on='away_team', right_on='team', how='left', suffixes=('_home_meta', '_away_meta')) # Added suffixes to avoid any potential lingering conflicts if not all columns are renamed
    final_dataset = final_dataset.rename(columns={
        'strength': 'away_strength',
        'win_percentage': 'away_win_percentage',
        'avg_goals_for': 'away_avg_goals_for',
        'avg_goals_against': 'away_avg_goals_against',
        'matches': 'away_matches',
        'wins': 'away_wins',
        'home_win_percentage': 'away_home_win_percentage',
        'away_win_percentage': 'away_away_win_percentage',
    }).drop(columns=['team'])
    

    
    final_dataset['date'] = pd.to_datetime(final_dataset['date'], format="%Y-%m-%d")

    # 2. Filter the DataFrame for dates after 1990.
    final_dataset = final_dataset[final_dataset['date'].dt.year > 1980]

    
    final_dataset.to_csv('./data/final_dataset.csv', index=False)