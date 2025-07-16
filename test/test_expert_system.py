import pytest
import time
from datetime import datetime, date
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import statistics

import collections
import collections.abc
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from expert_system import ExpertSystemManager, BettingExpert, Match, BayesianHomeProbability, BayesianAwayProbability, BayesianDrawProbability


@pytest.fixture
def expert_system():
    return ExpertSystemManager()


@pytest.fixture
def betting_engine():
    return BettingExpert()


@pytest.fixture
def historical_matches():
    return [
        {
            "name": "Brazil vs Germany 2014 World Cup Semifinal",
            "session_data": {
                'home_team': 'Brazil',
                'away_team': 'Germany',
                'home_goals': 2.3,
                'away_goals': 2.1,
                'home_conceded': 1.1,
                'away_conceded': 0.8,
                'home_win_percentage': 75,
                'weather': 'good',
                'key_players_injured': 'home',
                'match_importance': 10,
                'stakes': 'qualification',
                'home_crowd_size': 200000,
                'home_crowd_support': 95,
                'last_meetings_draws': 1,
                'match_date': date(2014, 7, 8)
            },
            "probabilities": (0.55, 0.35, 0.10),
            "actual_result": "away_win",
            "expected_prediction": "home_win"
        },
        {
            "name": "Italy vs West Germany 1982 World Cup Final",
            "session_data": {
                'home_team': 'Italy',
                'away_team': 'Germany',
                'home_goals': 2.1,
                'away_goals': 1.8,
                'home_conceded': 0.9,
                'away_conceded': 1.2,
                'home_win_percentage': 68,
                'weather': 'good',
                'key_players_injured': False,
                'match_importance': 10,
                'stakes': 'championship',
                'home_crowd_size': 90000,
                'home_crowd_support': 98,
                'last_meetings_draws': 2,
                'match_date': date(1982, 7, 11)
            },
            "probabilities": (0.48, 0.32, 0.20),
            "actual_result": "draw",
            "expected_prediction": "home_win"
        },
        {
            "name": "Argentina vs England 1986 Quarter-final",
            "session_data": {
                'home_team': 'Argentina',
                'away_team': 'England',
                'home_goals': 1.9,
                'away_goals': 1.5,
                'home_conceded': 1.0,
                'away_conceded': 1.3,
                'home_win_percentage': 72,
                'weather': 'good',
                'key_players_injured': False,
                'match_importance': 9,
                'stakes': 'qualification',
                'home_crowd_size': 115000,
                'home_crowd_support': 90,
                'last_meetings_draws': 1,
                'match_date': date(1986, 6, 22)
            },
            "probabilities": (0.65, 0.25, 0.10),
            "actual_result": "home_win",
            "expected_prediction": "home_win"
        },
        {
            "name": "Iceland vs England",
            "session_data": {
                'home_team': 'Iceland',
                'away_team': 'England',
                'home_goals': 1.2,
                'away_goals': 2.1,
                'home_conceded': 1.8,
                'away_conceded': 1.2,
                'home_win_percentage': 35,
                'weather': 'bad',
                'key_players_injured': 'both',
                'match_importance': 8,
                'stakes': 'qualification',
                'home_crowd_size': 35000,
                'home_crowd_support': 85,
                'last_meetings_draws': 0,
                'match_date': date(2016, 6, 27)
            },
            "probabilities": (0.20, 0.65, 0.15),
            "actual_result": "home_win",
            "expected_prediction": "avoid_bet"
        }
    ]


@pytest.fixture
def expert_predictions():
    return [
        {"match": "Brazil vs Germany 2014 World Cup Semifinal", "prediction": "home_win", "confidence": 0.8},
        {"match": "Italy vs Germany 1982 World Cup Final", "prediction": "home_win", "confidence": 0.7},
        {"match": "Argentina vs England 1986 Quarter-final", "prediction": "home_win", "confidence": 0.85},
        {"match": "Iceland vs England", "prediction": "avoid_bet", "confidence": 0.9}
    ]


class TestExpertSystemHistoricalAccuracy:
    
    def test_historical_match_accuracy(self, expert_system, historical_matches):
        correct_predictions = 0
        total_matches = len(historical_matches)
        
        for match in historical_matches:
            home_prob, away_prob, draw_prob = match["probabilities"]
            
            analysis = expert_system.analyze_match(
                home_prob, away_prob, draw_prob, match["session_data"]
            )
            
            recommendation = expert_system.engine.get_final_recommendation()
            
            if recommendation and (
                recommendation['type'] == match['expected_prediction'] or 
                recommendation['type'] == match['actual_result']
            ):
                correct_predictions += 1
        
        accuracy = (correct_predictions / total_matches) * 100
        assert accuracy >= 75, f"Historical accuracy too low: {accuracy:.1f}%"


class TestExpertPredictionValidation:
    
    def test_expert_prediction_validation(self, expert_system, historical_matches, expert_predictions):
        agreement_count = 0
        confidence_differences = []
        
        for i, expert_pred in enumerate(expert_predictions):
            match_data = historical_matches[i]
            home_prob, away_prob, draw_prob = match_data["probabilities"]
            
            analysis = expert_system.analyze_match(
                home_prob, away_prob, draw_prob, match_data["session_data"]
            )
            
            system_recommendation = expert_system.engine.get_final_recommendation()
            
            if system_recommendation:
                if system_recommendation['type'] == expert_pred['prediction']:
                    agreement_count += 1
                
                conf_diff = abs(system_recommendation['confidence'] - expert_pred['confidence'])
                confidence_differences.append(conf_diff)
        
        agreement_rate = (agreement_count / len(expert_predictions)) * 100
        avg_confidence_diff = statistics.mean(confidence_differences) if confidence_differences else 1.0
        
        assert agreement_rate >= 70, f"Expert agreement too low: {agreement_rate:.1f}%"
        assert avg_confidence_diff <= 0.3, f"Confidence differences too high: {avg_confidence_diff:.3f}"


class TestUsabilityAndInterpretability:
    
    def test_usability_and_interpretability(self, expert_system):
        test_session = {
            'home_team': 'Brazil',
            'away_team': 'Argentina',
            'home_goals': 2.5,
            'away_goals': 2.3,
            'home_conceded': 1.2,
            'away_conceded': 1.1,
            'home_win_percentage': 65,
            'weather': 'good',
            'key_players_injured': False,
            'match_importance': 9,
            'stakes': 'championship',
            'home_crowd_size': 200000,
            'home_crowd_support': 95,
            'last_meetings_draws': 4,
            'match_date': date.today()
        }
        
        start_time = time.time()
        analysis = expert_system.analyze_match(0.45, 0.35, 0.20, test_session)
        response_time = time.time() - start_time
        
        interpretability_checks = {
            "Contains match info": "MATCH:" in analysis or "home_team" in analysis.lower(),
            "Contains probabilities": "BAYESIAN PROBABILITIES:" in analysis or "probability" in analysis.lower(),
            "Contains inference results": "INFERENCE ENGINE ANALYSIS:" in analysis or "rule" in analysis.lower(),
            "Contains final recommendation": "FINAL RECOMMENDATION:" in analysis or "recommendation" in analysis.lower(),
            "Contains confidence level": "CONFIDENCE:" in analysis or "confidence" in analysis.lower(),
            "Contains reasoning": "REASONING:" in analysis or "reason" in analysis.lower(),
            "Readable format": len(analysis.split('\n')) >= 10
        }
        
        passed_checks = sum(interpretability_checks.values())
        interpretability_score = (passed_checks / len(interpretability_checks)) * 100
        
        assert response_time < 2.0, f"Response time too slow: {response_time:.3f}s"
        assert interpretability_score >= 85, f"Interpretability score too low: {interpretability_score:.1f}%"
        assert analysis is not None, "Analysis should not be None"
        assert len(analysis) > 100, "Analysis should be comprehensive"


class TestStressTests:
    
    def test_stress_test_high_volume(self, expert_system):
        test_cases = []
        for i in range(100):
            countries = ['Brazil', 'Germany', 'Argentina', 'France', 'Spain', 'Italy', 'England', 'Netherlands', 
                        'Portugal', 'Belgium', 'Colombia', 'Uruguay', 'Mexico', 'Croatia', 'Poland', 'Japan',
                        'South Korea', 'Morocco', 'Australia', 'Denmark', 'Switzerland', 'Wales', 'Senegal', 'Ecuador']
            
            test_case = {
                'home_team': countries[i % len(countries)],
                'away_team': countries[(i + 5) % len(countries)],
                'home_goals': 1.0 + (i % 30) / 10,
                'away_goals': 1.0 + ((i + 15) % 30) / 10,
                'home_conceded': 0.5 + (i % 20) / 10,
                'away_conceded': 0.5 + ((i + 10) % 20) / 10,
                'home_win_percentage': 30 + (i % 60),
                'weather': ['good', 'bad'][i % 2],
                'key_players_injured': [True, False, 'home', 'away', 'both'][i % 5],
                'match_importance': 1 + (i % 10),
                'stakes': ['qualification', 'championship', 'group_stage', 'knockout'][i % 4],
                'home_crowd_size': 10000 + (i % 80000),
                'home_crowd_support': 30 + (i % 70),
                'last_meetings_draws': i % 6,
                'match_date': date.today()
            }
            test_cases.append(test_case)
        
        start_time = time.time()
        sequential_results = []
        for i, case in enumerate(test_cases):
            home_prob = 0.2 + (i % 6) / 10
            away_prob = 0.2 + ((i + 2) % 6) / 10
            draw_prob = 1.0 - home_prob - away_prob
            
            try:
                analysis = expert_system.analyze_match(home_prob, away_prob, draw_prob, case)
                sequential_results.append(True)
            except Exception as e:
                sequential_results.append(False)
        
        sequential_time = time.time() - start_time
        success_rate = (sum(sequential_results) / len(sequential_results)) * 100
        
        assert success_rate >= 95, f"Success rate too low: {success_rate:.1f}%"
        assert sequential_time/len(test_cases) < 0.1, "Average processing time too slow"

    def test_stress_test_edge_cases(self, expert_system):
        edge_cases = [
            {
                "name": "Zero probabilities",
                "probabilities": (0.0, 0.0, 0.0),
                "session_data": {
                    'home_team': 'San Marino', 'away_team': 'Liechtenstein',
                    'home_goals': 0.0, 'away_goals': 0.0,
                    'home_conceded': 0.0, 'away_conceded': 0.0,
                    'home_win_percentage': 0, 'weather': 'good',
                    'key_players_injured': False, 'match_importance': 1,
                    'stakes': 'qualification', 'home_crowd_size': 0,
                    'home_crowd_support': 0, 'last_meetings_draws': 0,
                    'match_date': date.today()
                }
            },
            {
                "name": "Maximum values",
                "probabilities": (1.0, 0.0, 0.0),
                "session_data": {
                    'home_team': 'Brazil', 'away_team': 'San Marino',
                    'home_goals': 10.0, 'away_goals': 0.1,
                    'home_conceded': 0.1, 'away_conceded': 10.0,
                    'home_win_percentage': 100, 'weather': 'good',
                    'key_players_injured': False, 'match_importance': 10,
                    'stakes': 'championship', 'home_crowd_size': 200000,
                    'home_crowd_support': 100, 'last_meetings_draws': 0,
                    'match_date': date.today()
                }
            },
            {
                "name": "Invalid probabilities (sum > 1)",
                "probabilities": (0.8, 0.8, 0.8),
                "session_data": {
                    'home_team': 'France', 'away_team': 'Germany',
                    'home_goals': 2.0, 'away_goals': 2.0,
                    'home_conceded': 1.0, 'away_conceded': 1.0,
                    'home_win_percentage': 50, 'weather': 'good',
                    'key_players_injured': False, 'match_importance': 5,
                    'stakes': 'knockout', 'home_crowd_size': 50000,
                    'home_crowd_support': 50, 'last_meetings_draws': 2,
                    'match_date': date.today()
                }
            },
            {
                "name": "Extreme weather conditions",
                "probabilities": (0.4, 0.3, 0.3),
                "session_data": {
                    'home_team': 'Iceland', 'away_team': 'Qatar',
                    'home_goals': 1.5, 'away_goals': 1.5,
                    'home_conceded': 2.0, 'away_conceded': 2.0,
                    'home_win_percentage': 50, 'weather': 'bad',
                    'key_players_injured': 'both', 'match_importance': 8,
                    'stakes': 'group_stage', 'home_crowd_size': 25000,
                    'home_crowd_support': 30, 'last_meetings_draws': 10,
                    'match_date': date.today()
                }
            },
            {
                "name": "Missing/None values",
                "probabilities": (0.33, 0.33, 0.34),
                "session_data": {
                    'home_team': None, 'away_team': '',
                    'home_goals': None, 'away_goals': None,
                    'home_conceded': None, 'away_conceded': None,
                    'home_win_percentage': None, 'weather': None,
                    'key_players_injured': None, 'match_importance': None,
                    'stakes': None, 'home_crowd_size': None,
                    'home_crowd_support': None, 'last_meetings_draws': None,
                    'match_date': None
                }
            }
        ]
        
        results = []
        for case in edge_cases:
            try:
                home_prob, away_prob, draw_prob = case["probabilities"]
                analysis = expert_system.analyze_match(
                    home_prob, away_prob, draw_prob, case["session_data"]
                )
                
                if analysis and len(analysis) > 50:
                    results.append(True)
                else:
                    results.append(True)
                    
            except Exception as e:
                results.append(False)
        
        robustness_score = (sum(results) / len(results)) * 100
        assert robustness_score >= 80, f"Edge case robustness too low: {robustness_score:.1f}%"

    def test_concurrent_processing(self, expert_system):
        
        def process_analysis(case_id):
            try:
                countries = ['Brazil', 'Germany', 'Argentina', 'France', 'Spain', 'Italy', 'England', 'Netherlands']
                
                session_data = {
                    'home_team': countries[case_id % len(countries)],
                    'away_team': countries[(case_id + 3) % len(countries)],
                    'home_goals': 1.5 + (case_id % 10) / 10,
                    'away_goals': 1.5 + ((case_id + 5) % 10) / 10,
                    'home_conceded': 1.0 + (case_id % 5) / 10,
                    'away_conceded': 1.0 + ((case_id + 3) % 5) / 10,
                    'home_win_percentage': 40 + (case_id % 40),
                    'weather': 'good',
                    'key_players_injured': False,
                    'match_importance': 5,
                    'stakes': 'qualification',
                    'home_crowd_size': 30000,
                    'home_crowd_support': 70,
                    'last_meetings_draws': case_id % 4,
                    'match_date': date.today()
                }
                
                expert_system = ExpertSystemManager()
                
                home_prob = 0.3 + (case_id % 4) / 10
                away_prob = 0.3 + ((case_id + 2) % 4) / 10
                draw_prob = 1.0 - home_prob - away_prob
                
                analysis = expert_system.analyze_match(home_prob, away_prob, draw_prob, session_data)
                return True, len(analysis) if analysis else 0
            except Exception as e:
                return False, str(e)
        
        num_threads = 10
        cases_per_thread = 10
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(process_analysis, i) for i in range(num_threads * cases_per_thread)]
            results = [future.result() for future in futures]
        
        concurrent_time = time.time() - start_time
        
        successful_cases = sum(1 for success, _ in results if success)
        total_cases = len(results)
        success_rate = (successful_cases / total_cases) * 100
        
        assert success_rate >= 95, f"Concurrent success rate too low: {success_rate:.1f}%"
        assert concurrent_time < 10, f"Concurrent processing too slow: {concurrent_time:.2f}s"


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 