#from pgmpy.models import DiscreteBayesianNetwork
#from pgmpy.factors.discrete import TabularCPD

#soccer_match_model = DiscreteBayesianNetwork()

#soccer_match_model.add_nodes_from([])
#soccer_match_model.add_edge()

#cpd_ = TabularCPD("", variable_card=?, values=[[?], [?], [?]])

#from pgmpy.inference import VariableElimination

"""
inference = VariableElimination(soccer_match_model)
posterior_p = inference.query([""], evidence={"?": 0, "?": 2})
print (posterior_p)
"""

import pandas as pd
import numpy as np
import os # Import the os module for path manipulation
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class Bayesian_Network:
    def __init__(self): 
        self.data_path = self._get_fixed_data_path() # Call new method to get fixed path
        self.data = self._load_data()
        self.model = self._define_model_structure()
        self._estimate_and_add_cpds()
        self.inference_engine = VariableElimination(self.model)
        

    def _get_fixed_data_path(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fixed_path = os.path.join(script_dir, 'data', 'final_dataset.csv')
        return fixed_path

    def _load_data(self):
        try:
            return pd.read_csv(self.data_path)
        except FileNotFoundError:
            print(f"Error: Dataset not found at {self.data_path}. Please ensure 'data/final_dataset.csv' exists relative to your script.")
            return None

    def _define_model_structure(self):
        return DiscreteBayesianNetwork([
            ('home_team', 'winner'),
            ('away_team', 'winner')
        ])

    def _estimate_and_add_cpds(self):
        if self.data is None:
            return

        mle = MaximumLikelihoodEstimator(self.model, self.data)

        for node in self.model.nodes():
            try:
                cpd = mle.estimate_cpd(node)
                self.model.add_cpds(cpd)
            except Exception as e:
                # Provide more context for common estimation issues
                if "Data is too sparse" in str(e) or "doesn't have enough data" in str(e):
                    print(f"Warning: Could not estimate CPD for node '{node}' due to sparse data or insufficient unique values in the dataset. Error: {e}")
                else:
                    print(f"Warning: Could not estimate CPD for node '{node}'. Error: {e}")

        if not self.model.check_model():
            print("Warning: The Bayesian Network model is not valid after adding CPDs. This might indicate missing CPDs or structural issues.")

    def calculate_probabilities(self, evidence: dict):
        
        result = self.inference_engine.query(variables=['winner'], evidence=evidence)
        probabilities = {
            'home': float(result.values[result.state_names['winner'].index('home_team')]),
            'away': float(result.values[result.state_names['winner'].index('away_team')]),
            'draw': float(result.values[result.state_names['winner'].index('draw')])
        }
        
        return probabilities
