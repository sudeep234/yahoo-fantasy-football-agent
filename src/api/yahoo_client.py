import aiohttp
from typing import Optional, List, Dict, Any


class YahooFantasyClient:
    """Client for Yahoo Fantasy Sports API."""
    
    BASE_URL = "https://fantasysports.yahooapis.com/fantasy/v2"
    
    def __init__(self, access_token: str):
        self._access_token = access_token
        self._headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
    
    async def _request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make authenticated request to Yahoo API."""
        url = f"{self.BASE_URL}/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error = await response.text()
                    print(f"API Error ({response.status}): {error}")
                    return None
    
    async def get_user_leagues(self, game_key: str = "nfl") -> Optional[List[Dict]]:
        """Get all leagues for the authenticated user."""
        endpoint = f"users;use_login=1/games;game_keys={game_key}/leagues?format=json"
        return await self._request(endpoint)
    
    async def get_leagues_by_season(self, season: int) -> Optional[List[Dict]]:
        """Get leagues for a specific season."""
        game_key = self._get_game_key(season)
        endpoint = f"users;use_login=1/games;game_keys={game_key}/leagues?format=json"
        return await self._request(endpoint)
    
    async def get_league_info(self, league_key: str) -> Optional[Dict]:
        """Get league information."""
        endpoint = f"league/{league_key}?format=json"
        return await self._request(endpoint)
    
    async def get_league_standings(self, league_key: str) -> Optional[Dict]:
        """Get league standings."""
        endpoint = f"league/{league_key}/standings?format=json"
        return await self._request(endpoint)
    
    async def get_league_scoreboard(self, league_key: str, week: int) -> Optional[Dict]:
        """Get scoreboard for a specific week."""
        endpoint = f"league/{league_key}/scoreboard;week={week}?format=json"
        return await self._request(endpoint)
    
    async def get_all_teams(self, league_key: str) -> Optional[Dict]:
        """Get all teams in a league."""
        endpoint = f"league/{league_key}/teams?format=json"
        return await self._request(endpoint)
    
    async def get_team_stats(self, team_key: str, week: int) -> Optional[Dict]:
        """Get team stats for a specific week."""
        endpoint = f"team/{team_key}/stats;type=week;week={week}?format=json"
        return await self._request(endpoint)
    
    async def get_matchups(self, league_key: str, week: int) -> Optional[Dict]:
        """Get matchups for a specific week."""
        endpoint = f"league/{league_key}/scoreboard;week={week}?format=json"
        return await self._request(endpoint)
    
    async def get_team_roster(self, team_key: str) -> Optional[Dict]:
        """Get roster for a specific team."""
        endpoint = f"team/{team_key}/roster?format=json"
        return await self._request(endpoint)
    
    def _get_game_key(self, season: int) -> str:
        """Get Yahoo game key for NFL season."""
        game_keys = {
            2023: "423",
            2024: "449",
            2025: "453"
        }
        return game_keys.get(season, "nfl")