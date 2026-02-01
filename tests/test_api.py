import unittest
from src.api.yahoo_client import YahooClient

class TestYahooClient(unittest.TestCase):

    def setUp(self):
        self.client = YahooClient()

    def test_authentication(self):
        # Test that the client can authenticate with valid credentials
        credentials = {'username': 'test_user', 'password': 'test_pass'}
        self.client.authenticate(credentials)
        self.assertTrue(self.client.is_authenticated)

    def test_get_league_info(self):
        # Test retrieving league information
        league_info = self.client.get_league_info(12345)  # Replace with a valid league ID
        self.assertIsNotNone(league_info)
        self.assertIn('league_id', league_info)

    def test_get_team_stats(self):
        # Test retrieving team statistics
        team_stats = self.client.get_team_stats(12345)  # Replace with a valid team ID
        self.assertIsNotNone(team_stats)
        self.assertIn('team_id', team_stats)

    def test_get_player_stats(self):
        # Test retrieving player statistics
        player_stats = self.client.get_player_stats(67890)  # Replace with a valid player ID
        self.assertIsNotNone(player_stats)
        self.assertIn('player_id', player_stats)

if __name__ == '__main__':
    unittest.main()