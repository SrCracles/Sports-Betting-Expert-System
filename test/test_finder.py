import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Finder import Finder

@pytest.fixture
def finder_instance():
    return Finder()

def test_exact_team_find(finder_instance):
    assert finder_instance.find_exact_team("colombia") is True
    assert finder_instance.find_exact_team("brazil") is True
    assert finder_instance.find_exact_team("spain") is True
    
    assert finder_instance.find_exact_team("COLOMBIA") is True
    assert finder_instance.find_exact_team("Brazil") is True
    
    assert finder_instance.find_exact_team("not_a_team") is False

def test_similar_teams(finder_instance):
    similar_teams = finder_instance.find_similar_teams("co")
    assert "colombia" in similar_teams
    
    similar_to_bra = finder_instance.find_similar_teams("bra")
    assert "brazil" in similar_to_bra
    
    land_teams = finder_instance.find_similar_teams("land")
    assert len(land_teams) > 0
    
    empty_search = finder_instance.find_similar_teams("")
    assert len(empty_search) > 0

def test_get_all_teams(finder_instance):
    all_teams = finder_instance.get_all_teams()
    
    assert isinstance(all_teams, list)
    assert len(all_teams) > 0
    
    assert "brazil" in all_teams
    assert "germany" in all_teams
    assert "argentina" in all_teams