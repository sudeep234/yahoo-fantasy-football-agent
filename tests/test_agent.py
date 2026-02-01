import unittest
from src.agent.agent import FantasyFootballTreasurer

class TestFantasyFootballTreasurer(unittest.TestCase):

    def setUp(self):
        self.agent = FantasyFootballTreasurer()

    def test_get_league_info(self):
        # Test to retrieve league information
        league_info = self.agent.get_league_info()
        self.assertIsNotNone(league_info)

    def test_get_team_stats(self):
        # Test to retrieve team statistics
        team_stats = self.agent.get_team_stats()
        self.assertIsNotNone(team_stats)

    def test_get_player_stats(self):
        # Test to retrieve player statistics
        player_stats = self.agent.get_player_stats()
        self.assertIsNotNone(player_stats)

    def test_get_standings(self):
        # Test to retrieve league standings
        standings = self.agent.get_standings()
        self.assertIsNotNone(standings)

    def test_get_season_stats(self):
        # Test to retrieve season statistics
        season_stats = self.agent.get_season_stats()
        self.assertIsNotNone(season_stats)

if __name__ == '__main__':
    unittest.main()