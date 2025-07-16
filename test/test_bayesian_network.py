import pytest
import pandas as pd
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.Bayesian_Network import Bayesian_Network


@pytest.fixture(scope="session")
def bayesian_network_instance():
    network = Bayesian_Network()
    return network

@pytest.fixture(scope="session")
def final_dataset():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'final_dataset.csv')
    df = pd.read_csv(data_path)
    print(f"Loaded final_dataset.csv with {len(df)} rows and {len(df.columns)} columns")
    return df

def test_1(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'peru', 'colombia')

def test_2(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'colombia', 'germany')

def test_3(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'colombia', 'brazil')

def test_4(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'argentina', 'colombia')

def test_5(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'colombia', 'spain')

def test_6(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'uruguay', 'brazil')

def test_7(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'argentina', 'uruguay')

def test_8(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'uruguay', 'spain')

def test_9(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'england', 'uruguay')

def test_10(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'uruguay', 'mexico')
def test_11(bayesian_network_instance, final_dataset):
    check_prediction_against_history(bayesian_network_instance, final_dataset, 'uruguay', 'mexico')



def check_prediction_against_history(bayesian_network, dataset, home_team, away_team):
    
    evidence = {
        'home_team': home_team,
        'away_team': away_team
    }
    
    winner_probabilities = bayesian_network.calculate_probabilities(evidence)
    
    
    assert winner_probabilities['home'] >= 0
    assert winner_probabilities['away'] >= 0
    assert winner_probabilities['draw'] >= 0
    
    max_prob_result = max(winner_probabilities, key=winner_probabilities.get)
    
    historical_matches = dataset[
        (dataset['home_team'] == home_team) & 
        (dataset['away_team'] == away_team)
    ]
    
    if len(historical_matches) > 0:
        home_wins = sum(historical_matches['winner'] == 'home_team')
        away_wins = sum(historical_matches['winner'] == 'away_team')
        draws = sum(historical_matches['winner'] == 'draw')
        
        results_count = {'home': home_wins, 'away': away_wins, 'draw': draws}
        most_common_result = max(results_count, key=results_count.get)
        assert max_prob_result == most_common_result
        return True
    else:
        return False


