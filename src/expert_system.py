from experta import *
from datetime import datetime, timedelta

class Match(Fact):
    """Information about a football match"""
    pass

class BayesianHomeProbability(Fact):
    """Bayesian probability of home victory"""
    pass

class BayesianAwayProbability(Fact):
    """Bayesian probability of away victory"""
    pass

class BayesianDrawProbability(Fact):
    """Bayesian probability of draw"""
    pass

class BettingExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []
        self.analysis_results = []

    @DefFacts()
    def initial_knowledge(self):
        """Initial configuration"""
        yield Fact(system_ready=True)

    # 1. HIGH RISK RULE (Maximum priority)
    @Rule(
    AS.match << Match(
        weather='bad',
        key_players_injured=P(lambda x: x == "both" or x == "home" or x == "away")
    ), salience=20)
    def avoid_high_risk(self, match):
        recommendation = {
            'type': 'avoid_bet',
            'confidence': 0.9,
            'reason': 'High risk: Bad weather and key injuries'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append("RULE 1: HIGH RISK - Avoid betting")

    # 2. HIGH BAYESIAN PROBABILITY (Second priority)
    @Rule(
        AS.home_prob << BayesianHomeProbability(probability=P(lambda x: x >= 0.75)),
        salience=15
    )
    def bayesian_home_strong(self, home_prob):
        recommendation = {
            'type': 'home_win',
            'confidence': home_prob['probability'],
            'reason': f'Bayesian: Home victory very likely ({home_prob["probability"]:.1%})'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append(f"RULE 2A: Bayesian home victory - {home_prob['probability']:.1%}")

    @Rule(
        AS.away_prob << BayesianAwayProbability(probability=P(lambda x: x >= 0.75)),
        salience=15
    )
    def bayesian_away_strong(self, away_prob):
        recommendation = {
            'type': 'away_win',
            'confidence': away_prob['probability'],
            'reason': f'Bayesian: Away victory very likely ({away_prob["probability"]:.1%})'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append(f"RULE 2B: Bayesian away victory - {away_prob['probability']:.1%}")

    @Rule(
        AS.draw_prob << BayesianDrawProbability(probability=P(lambda x: x >= 0.6)),
        salience=15
    )
    def bayesian_draw_likely(self, draw_prob):
        recommendation = {
            'type': 'draw',
            'confidence': draw_prob['probability'],
            'reason': f'Bayesian: Draw likely ({draw_prob["probability"]:.1%})'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append(f"RULE 2C: Bayesian draw - {draw_prob['probability']:.1%}")

    # 3. PROBABLE BLOWOUT
    @Rule(
        AS.match << Match(
            home_goals=P(lambda x: x >= 3.0),
            away_conceded=P(lambda x: x <= 1.5)
        ),
        salience=12
    )
    def probable_blowout(self, match):
        recommendation = {
            'type': 'home_blowout',
            'confidence': 0.85,
            'reason': 'Extreme performance difference - Home blowout'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append("RULE 3: PROBABLE BLOWOUT - Decisive home victory")

    # 4. STRONG HOME TEAM
    @Rule(
        AS.match << Match(
            home_goals=P(lambda x: x >= 2.0),
            away_conceded=P(lambda x: x <= 1.0),
            home_win_percentage=P(lambda x: x >= 70)
        ),
        salience=10
    )
    def strong_home_team(self, match):
        recommendation = {
            'type': 'home_win',
            'confidence': 0.8,
            'reason': 'Strong home team: Good goals, low conceded, high win percentage'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append("RULE 4: STRONG HOME TEAM")

    # 5. STRONG AWAY TEAM
    @Rule(
        AS.match << Match(
            away_goals=P(lambda x: x >= 1.8),
            away_conceded=P(lambda x: x <= 1.2),
            home_win_percentage=P(lambda x: x <= 40)
        ),
        salience=10
    )
    def strong_away_team(self, match):
        recommendation = {
            'type': 'away_win',
            'confidence': 0.78,
            'reason': 'Strong away team vs weak home team'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append("RULE 5: STRONG AWAY TEAM")

    # 6. MASSIVE CROWD ADVANTAGE
    @Rule(
        AS.match << Match(
            home_crowd_size=P(lambda x: x >= 30000),
            home_crowd_support=P(lambda x: x >= 60)
        ),
        salience=8
    )
    def massive_crowd_advantage(self, match):
        recommendation = {
            'type': 'home_win',
            'confidence': 0.75,
            'reason': 'Massive home crowd - Important psychological factor'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append("RULE 6: MASSIVE CROWD ADVANTAGE")

    # 7. PROBABLE DRAW
    @Rule(
        AS.match << Match(
            home_goals=P(lambda x: 1.5 <= x <= 2.2),
            away_goals=P(lambda x: 1.5 <= x <= 2.2),
            last_meetings_draws=P(lambda x: x >= 3)
        ),
        salience=7
    )
    def likely_draw(self, match):
        recommendation = {
            'type': 'draw',
            'confidence': 0.7,
            'reason': 'Balanced teams with history of draws'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append("RULE 7: PROBABLE DRAW")

    # 8. UNCERTAIN BAYESIAN ANALYSIS
    @Rule(
        AS.home_prob << BayesianHomeProbability(probability=P(lambda x: x < 0.3)),
        AS.away_prob << BayesianAwayProbability(probability=P(lambda x: x < 0.3)),
        AS.draw_prob << BayesianDrawProbability(probability=P(lambda x: x < 0.3)),
        salience=5
    )
    def uncertain_bayesian(self, home_prob, away_prob, draw_prob):
        recommendation = {
            'type': 'no_clear_bet',
            'confidence': 0.3,
            'reason': 'Bayesian analysis shows no clear trend'
        }
        self.recommendations.append(recommendation)
        self.analysis_results.append("RULE 8: UNCERTAIN BAYESIAN ANALYSIS")

    # 9. DEFAULT RULE
    @Rule(
        Fact(system_ready=True),
        salience=1
    )
    def default_recommendation(self):
        if not self.recommendations:
            recommendation = {
                'type': 'insufficient_data',
                'confidence': 0.2,
                'reason': 'Insufficient data for reliable analysis'
            }
            self.recommendations.append(recommendation)
            self.analysis_results.append("RULE 9: INSUFFICIENT DATA")

    def get_final_recommendation(self):
        """Returns the recommendation with highest confidence"""
        if not self.recommendations:
            return None
        best_rec = max(self.recommendations, key=lambda x: x['confidence'])
        return best_rec

    def get_analysis_results(self):
        """Returns all analysis results"""
        return self.analysis_results

    def reset_recommendations(self):
        self.recommendations = []
        self.analysis_results = []


class ExpertSystemManager:
    """Main class to manage the expert system from the Telegram bot"""
    
    def __init__(self):
        self.engine = BettingExpert()
    
    def analyze_match(self, home_prob, away_prob, draw_prob, session_data):
        """
        Main method that receives probabilities and session data
        and returns a complete analysis as string
        
        Args:
            home_prob (float): Home victory probability (0-1)
            away_prob (float): Away victory probability (0-1)
            draw_prob (float): Draw probability (0-1)
            session_data (dict): User session data
        
        Returns:
            str: Complete analysis formatted for the user
        """
        try:
      
            self.engine.reset()
            self.engine.reset_recommendations()
            
            total_prob = home_prob + away_prob + draw_prob
            if abs(total_prob - 1.0) > 0.01:
                home_prob = home_prob / total_prob
                away_prob = away_prob / total_prob
                draw_prob = draw_prob / total_prob
            
            match_data = self._prepare_match_data(session_data)
            
            self.engine.declare(Match(**match_data))
            
            bayesian_facts = [
                BayesianHomeProbability(probability=home_prob),
                BayesianAwayProbability(probability=away_prob),
                BayesianDrawProbability(probability=draw_prob)
            ]
            
            for fact in bayesian_facts:
                self.engine.declare(fact)
            
            self.engine.run()
            
            recommendation = self.engine.get_final_recommendation()
            analysis_results = self.engine.get_analysis_results()
            
            return self._format_analysis_response(
                recommendation, 
                match_data, 
                home_prob, 
                away_prob, 
                draw_prob,
                analysis_results
            )
            
        except Exception as e:
            return f"Error in analysis: {str(e)}\n\nPlease try again."
    
    def _prepare_match_data(self, session_data):
        """Prepares match data with default values"""
        return {
            'home_team': session_data.get('home_team', 'Home'),
            'away_team': session_data.get('away_team', 'Away'),
            'home_goals': session_data.get('home_goals', 1.5),
            'away_goals': session_data.get('away_goals', 1.5),
            'home_conceded': session_data.get('home_conceded', 1.5),
            'away_conceded': session_data.get('away_conceded', 1.5),
            'home_win_percentage': session_data.get('home_win_percentage', 50),
            'weather': session_data.get('weather', 'good'),
            'key_players_injured': session_data.get('key_players_injured', True),
            'match_importance': session_data.get('match_importance', 5),
            'stakes': session_data.get('stakes', 'regular'),
            'home_crowd_size': session_data.get('home_crowd_size', 30000),
            'home_crowd_support': session_data.get('home_crowd_support', 75),
            'last_meetings_draws': session_data.get('last_meetings_draws', 1),
            'match_date': session_data.get('match_date', datetime.now().date())
        }
    
    def _format_analysis_response(self, recommendation, match_data, home_prob, away_prob, draw_prob, analysis_results):
        """Formats the analysis response for the user"""
        
        recommendation_map = {
            'home_win': f'BET ON {match_data["home_team"].upper()} VICTORY',
            'away_win': f'BET ON {match_data["away_team"].upper()} VICTORY',
            'draw': 'BET ON DRAW',
            'home_blowout': f'BET ON {match_data["home_team"].upper()} BLOWOUT',
            'avoid_bet': 'DO NOT BET - AVOID THIS MATCH',
            'cautious_bet': 'BET WITH GREAT CAUTION',
            'no_clear_bet': 'NO CLEAR TREND',
            'insufficient_data': 'INSUFFICIENT DATA'
        }
        
        response = f"""
**COMPLETE EXPERT SYSTEM ANALYSIS**
═══════════════════════════════════════════

**MATCH:** {match_data['home_team']} vs {match_data['away_team']}

**BAYESIAN PROBABILITIES:**
{match_data['home_team']} Victory: {home_prob:.1%}
{match_data['away_team']} Victory: {away_prob:.1%}
Draw: {draw_prob:.1%}

**INFERENCE ENGINE ANALYSIS:**
"""
        
        if analysis_results:
            for result in analysis_results:
                response += f"   {result}\n"
        else:
            response += "    No specific rules were activated\n"
        
        response += "\n" + "═" * 43 + "\n"
        
        if recommendation:
            recommendation_text = recommendation_map.get(
                recommendation['type'],
                f"{recommendation['type'].upper()}"
            )
            
            response += f"**FINAL RECOMMENDATION:**\n{recommendation_text}\n\n"
            response += f"**Reason:** {recommendation['reason']}\n"
            response += f"**Confidence:** {recommendation['confidence']:.1%}\n\n"
            
            confidence = recommendation['confidence']
            if confidence >= 0.8:
                confidence_level = "VERY HIGH"
                advice = "This is a bet with high probability of success."
            elif confidence >= 0.6:
                confidence_level = "HIGH"
                advice = "Recommended bet with moderate caution."
            elif confidence >= 0.4:
                confidence_level = "MEDIUM"
                advice = "Consider betting only small amounts."
            else:
                confidence_level = "LOW"
                advice = "We recommend avoiding betting on this match."
            
            response += f"**Confidence Level:** {confidence_level}\n\n"
            response += f"**Betting Advice:** {advice}\n"
        else:
            response += "**Could not generate a recommendation**\n"
        
        response += "\n" + "═" * 43 + "\n"
        response += "**Good luck with your bets!**\n"
        response += "Use /start to analyze another match"
        
        return response