from typing import Optional, List, Dict
from api.yahoo_client import YahooFantasyClient
from models.stats import WeeklyScore, TopScorer
import json


class FantasyFootballTreasurer:
    """Fantasy Football Treasurer - Agent to interact with Yahoo Fantasy Football."""
    
    def __init__(self, client: YahooFantasyClient):
        self.client = client
    
    async def get_league_standings(self, league_key: str) -> List[Dict]:
        """Get league standings with team records and points."""
        standings_data = await self.client.get_league_standings(league_key)
        standings = []
        
        if not standings_data:
            return standings
        
        try:
            fantasy_content = standings_data.get('fantasy_content', {})
            league_data = fantasy_content.get('league', [])
            
            if isinstance(league_data, list):
                for item in league_data:
                    if isinstance(item, dict) and 'standings' in item:
                        standings_obj = item['standings']
                        teams_obj = standings_obj.get('0', {}).get('teams', {})
                        
                        if isinstance(teams_obj, dict):
                            teams_list = [v for k, v in teams_obj.items() if k != 'count']
                        else:
                            teams_list = teams_obj if isinstance(teams_obj, list) else []
                        
                        for team_data in teams_list:
                            if not isinstance(team_data, dict):
                                continue
                            
                            team_info = team_data.get('team', [])
                            if isinstance(team_info, dict):
                                team_info = [team_info]
                            
                            team = {
                                'name': '',
                                'team_key': '',
                                'rank': 0,
                                'wins': 0,
                                'losses': 0,
                                'ties': 0,
                                'points_for': 0.0,
                                'points_against': 0.0,
                                'streak': '',
                                'manager': ''
                            }
                            
                            for info in team_info:
                                if isinstance(info, list):
                                    for detail in info:
                                        if isinstance(detail, dict):
                                            if 'name' in detail:
                                                team['name'] = detail['name']
                                            if 'team_key' in detail:
                                                team['team_key'] = detail['team_key']
                                            if 'managers' in detail:
                                                managers = detail['managers']
                                                if isinstance(managers, list) and managers:
                                                    mgr = managers[0].get('manager', {})
                                                    team['manager'] = mgr.get('nickname', '')
                                                elif isinstance(managers, dict):
                                                    mgr = managers.get('0', {}).get('manager', {})
                                                    team['manager'] = mgr.get('nickname', '')
                                elif isinstance(info, dict):
                                    if 'team_standings' in info:
                                        ts = info['team_standings']
                                        team['rank'] = int(ts.get('rank', 0))
                                        team['points_for'] = float(ts.get('points_for', 0))
                                        team['points_against'] = float(ts.get('points_against', 0))
                                        
                                        streak = ts.get('streak', {})
                                        if streak:
                                            team['streak'] = f"{streak.get('type', '')[0].upper()}{streak.get('value', '')}"
                                        
                                        outcome = ts.get('outcome_totals', {})
                                        team['wins'] = int(outcome.get('wins', 0))
                                        team['losses'] = int(outcome.get('losses', 0))
                                        team['ties'] = int(outcome.get('ties', 0))
                            
                            if team['name']:
                                standings.append(team)
        except (KeyError, TypeError, IndexError, ValueError) as e:
            print(f"Error parsing standings: {e}")
        
        return sorted(standings, key=lambda x: x['rank'])
    
    async def get_all_teams_info(self, league_key: str) -> List[Dict]:
        """Get information about all teams in the league."""
        teams_data = await self.client.get_all_teams(league_key)
        teams = []
        
        if not teams_data:
            return teams
        
        try:
            fantasy_content = teams_data.get('fantasy_content', {})
            league_data = fantasy_content.get('league', [])
            
            if isinstance(league_data, list):
                for item in league_data:
                    if isinstance(item, dict) and 'teams' in item:
                        teams_obj = item['teams']
                        
                        if isinstance(teams_obj, dict):
                            teams_list = [v for k, v in teams_obj.items() if k != 'count']
                        else:
                            teams_list = teams_obj if isinstance(teams_obj, list) else []
                        
                        for team_data in teams_list:
                            if not isinstance(team_data, dict):
                                continue
                            
                            team_info = team_data.get('team', [])
                            if isinstance(team_info, dict):
                                team_info = [team_info]
                            
                            team = {
                                'name': '',
                                'team_key': '',
                                'team_id': '',
                                'manager': '',
                                'logo_url': '',
                                'waiver_priority': 0,
                                'moves': 0,
                                'trades': 0
                            }
                            
                            for info in team_info:
                                if isinstance(info, list):
                                    for detail in info:
                                        if isinstance(detail, dict):
                                            if 'name' in detail:
                                                team['name'] = detail['name']
                                            if 'team_key' in detail:
                                                team['team_key'] = detail['team_key']
                                            if 'team_id' in detail:
                                                team['team_id'] = detail['team_id']
                                            if 'team_logos' in detail:
                                                logos = detail['team_logos']
                                                if isinstance(logos, list) and logos:
                                                    team['logo_url'] = logos[0].get('team_logo', {}).get('url', '')
                                            if 'managers' in detail:
                                                managers = detail['managers']
                                                if isinstance(managers, list) and managers:
                                                    mgr = managers[0].get('manager', {})
                                                    team['manager'] = mgr.get('nickname', '')
                                                elif isinstance(managers, dict):
                                                    mgr = managers.get('0', {}).get('manager', {})
                                                    team['manager'] = mgr.get('nickname', '')
                                            if 'waiver_priority' in detail:
                                                team['waiver_priority'] = int(detail['waiver_priority'])
                                            if 'number_of_moves' in detail:
                                                team['moves'] = int(detail['number_of_moves'])
                                            if 'number_of_trades' in detail:
                                                team['trades'] = int(detail['number_of_trades'])
                                elif isinstance(info, dict):
                                    if 'name' in info:
                                        team['name'] = info['name']
                                    if 'waiver_priority' in info:
                                        team['waiver_priority'] = int(info['waiver_priority'])
                                    if 'number_of_moves' in info:
                                        team['moves'] = int(info['number_of_moves'])
                                    if 'number_of_trades' in info:
                                        team['trades'] = int(info['number_of_trades'])
                            
                            if team['name']:
                                teams.append(team)
        except (KeyError, TypeError, IndexError, ValueError) as e:
            print(f"Error parsing teams: {e}")
        
        return teams
    
    async def get_team_roster(self, team_key: str) -> List[Dict]:
        """Get roster (players) for a specific team."""
        roster_data = await self.client.get_team_roster(team_key)
        players = []
        
        if not roster_data:
            return players
        
        try:
            fantasy_content = roster_data.get('fantasy_content', {})
            team_data = fantasy_content.get('team', [])
            
            if isinstance(team_data, list):
                for item in team_data:
                    if isinstance(item, dict) and 'roster' in item:
                        roster_obj = item['roster']
                        players_obj = roster_obj.get('0', {}).get('players', {})
                        
                        if isinstance(players_obj, dict):
                            players_list = [v for k, v in players_obj.items() if k != 'count']
                        else:
                            players_list = players_obj if isinstance(players_obj, list) else []
                        
                        for player_data in players_list:
                            if not isinstance(player_data, dict):
                                continue
                            
                            player_info = player_data.get('player', [])
                            if isinstance(player_info, dict):
                                player_info = [player_info]
                            
                            player = {
                                'name': '',
                                'player_key': '',
                                'position': '',
                                'team': '',
                                'status': '',
                                'selected_position': ''
                            }
                            
                            for info in player_info:
                                if isinstance(info, list):
                                    for detail in info:
                                        if isinstance(detail, dict):
                                            if 'name' in detail:
                                                player['name'] = detail['name'].get('full', '')
                                            if 'player_key' in detail:
                                                player['player_key'] = detail['player_key']
                                            if 'editorial_team_abbr' in detail:
                                                player['team'] = detail['editorial_team_abbr'].upper()
                                            if 'display_position' in detail:
                                                player['position'] = detail['display_position']
                                            if 'status' in detail:
                                                player['status'] = detail['status']
                                elif isinstance(info, dict):
                                    if 'selected_position' in info:
                                        sel_pos = info['selected_position']
                                        if isinstance(sel_pos, list) and sel_pos:
                                            player['selected_position'] = sel_pos[0].get('position', '')
                                        elif isinstance(sel_pos, dict):
                                            player['selected_position'] = sel_pos.get('position', '')
                            
                            if player['name']:
                                players.append(player)
        except (KeyError, TypeError, IndexError, ValueError) as e:
            print(f"Error parsing roster: {e}")
        
        return players

    async def list_all_leagues(self, season: int = None) -> List[Dict]:
        """List all leagues for a given season or all seasons if None."""
        if season:
            return await self._get_leagues_for_season(season)
        else:
            # Get leagues for last 5 years
            all_leagues = []
            for year in range(2021, 2026):
                leagues = await self._get_leagues_for_season(year)
                all_leagues.extend(leagues)
            return all_leagues
    
    async def list_all_leagues_all_years(self) -> Dict[int, List[Dict]]:
        """List all leagues grouped by year for last 5 years."""
        leagues_by_year = {}
        for year in range(2021, 2026):
            leagues = await self._get_leagues_for_season(year)
            if leagues:
                leagues_by_year[year] = leagues
        return leagues_by_year
    
    async def _get_leagues_for_season(self, season: int) -> List[Dict]:
        """Get leagues for a specific season."""
        leagues_data = await self.client.get_leagues_by_season(season)
        
        leagues = []
        
        if not leagues_data:
            return leagues
        
        try:
            fantasy_content = leagues_data.get('fantasy_content', {})
            users = fantasy_content.get('users', {})
            
            # Handle both dict and list formats
            if isinstance(users, dict):
                user = users.get('0', {}).get('user', [])
            elif isinstance(users, list):
                user = users[0] if users else []
            else:
                user = []
            
            for item in user:
                if isinstance(item, dict) and 'games' in item:
                    games = item['games']
                    
                    # Handle games as dict or list
                    if isinstance(games, dict):
                        games_list = [v for k, v in games.items() if k != 'count']
                    elif isinstance(games, list):
                        games_list = games
                    else:
                        continue
                    
                    for game_value in games_list:
                        if not isinstance(game_value, dict):
                            continue
                        
                        game_data = game_value.get('game', [])
                        if isinstance(game_data, dict):
                            game_data = [game_data]
                        
                        for game_item in game_data:
                            if not isinstance(game_item, dict):
                                continue
                            
                            if 'leagues' not in game_item:
                                continue
                            
                            leagues_obj = game_item['leagues']
                            
                            # Handle leagues as dict or list
                            if isinstance(leagues_obj, dict):
                                leagues_list = [v for k, v in leagues_obj.items() if k != 'count']
                            elif isinstance(leagues_obj, list):
                                leagues_list = leagues_obj
                            else:
                                continue
                            
                            for league_value in leagues_list:
                                if not isinstance(league_value, dict):
                                    continue
                                
                                league_info = league_value.get('league', [])
                                if isinstance(league_info, dict):
                                    league_info = [league_info]
                                
                                if league_info and isinstance(league_info[0], dict):
                                    league = {
                                        'name': league_info[0].get('name', 'Unknown'),
                                        'league_id': league_info[0].get('league_id'),
                                        'league_key': league_info[0].get('league_key'),
                                        'num_teams': league_info[0].get('num_teams'),
                                        'current_week': league_info[0].get('current_week'),
                                        'season': season
                                    }
                                    leagues.append(league)
        except (KeyError, TypeError, IndexError) as e:
            print(f"Error parsing leagues for {season}: {e}")
        
        return leagues
    
    async def find_league_by_name(self, name: str, season: int = None) -> Optional[Dict]:
        """Find a league by name. If season is None, search all years."""
        if season:
            leagues = await self.list_all_leagues(season)
        else:
            leagues = await self.list_all_leagues()
        
        for league in leagues:
            if name.lower() in league['name'].lower():
                return league
        
        return None
    
    async def find_all_leagues_by_name(self, name: str) -> List[Dict]:
        """Find all leagues matching a name across all years."""
        all_leagues = await self.list_all_leagues()
        matching = []
        
        for league in all_leagues:
            if name.lower() in league['name'].lower():
                matching.append(league)
        
        return matching
    
    async def get_weekly_scores(self, league_key: str, week: int) -> List[WeeklyScore]:
        """Get all team scores for a specific week."""
        scores = []
        scoreboard = await self.client.get_matchups(league_key, week)
        
        if not scoreboard:
            return scores
        
        try:
            fantasy_content = scoreboard.get('fantasy_content', {})
            league_data = fantasy_content.get('league', [])
            
            if isinstance(league_data, dict):
                league_data = [league_data]
            
            for item in league_data:
                if not isinstance(item, dict) or 'scoreboard' not in item:
                    continue
                
                scoreboard_data = item['scoreboard']
                
                # Handle matchups as dict or list
                if isinstance(scoreboard_data, dict):
                    matchups = scoreboard_data.get('0', {}).get('matchups', {})
                    if isinstance(matchups, dict):
                        matchups_list = [v for k, v in matchups.items() if k != 'count']
                    else:
                        matchups_list = matchups if isinstance(matchups, list) else []
                else:
                    continue
                
                for matchup_data in matchups_list:
                    if not isinstance(matchup_data, dict):
                        continue
                    
                    matchup = matchup_data.get('matchup', {})
                    
                    # Handle teams
                    teams_obj = matchup.get('0', {}).get('teams', {})
                    if isinstance(teams_obj, dict):
                        teams_list = [v for k, v in teams_obj.items() if k != 'count']
                    elif isinstance(teams_obj, list):
                        teams_list = teams_obj
                    else:
                        continue
                    
                    for team_data in teams_list:
                        if not isinstance(team_data, dict):
                            continue
                        
                        team_info = team_data.get('team', [])
                        if isinstance(team_info, dict):
                            team_info = [team_info]
                        
                        team_name = ""
                        team_points = 0.0
                        
                        for info in team_info:
                            if isinstance(info, list):
                                for detail in info:
                                    if isinstance(detail, dict) and 'name' in detail:
                                        team_name = detail['name']
                            elif isinstance(info, dict):
                                if 'name' in info:
                                    team_name = info['name']
                                if 'team_points' in info:
                                    points_data = info['team_points']
                                    if isinstance(points_data, dict):
                                        team_points = float(points_data.get('total', 0))
                                    else:
                                        team_points = float(points_data)
                        
                        if team_name:
                            scores.append(WeeklyScore(
                                team_name=team_name,
                                week=week,
                                points=team_points
                            ))
                            
        except (KeyError, TypeError, IndexError, ValueError) as e:
            print(f"Error parsing week {week} scores: {e}")
        
        return scores
    
    async def get_weekly_top_scorers(self, league_key: str, top_n: int = 3) -> None:
        """Get top N scorers for each completed week."""
        league_info = await self.client.get_league_info(league_key)
        
        current_week = 17
        
        if league_info:
            try:
                fantasy_content = league_info.get('fantasy_content', {})
                league_data = fantasy_content.get('league', [])
                if isinstance(league_data, dict):
                    current_week = int(league_data.get('current_week', 17))
                elif isinstance(league_data, list) and league_data and isinstance(league_data[0], dict):
                    current_week = int(league_data[0].get('current_week', 17))
            except (KeyError, TypeError, ValueError):
                pass
        
        print(f"{'='*60}")
        print(f"TOP {top_n} SCORERS BY WEEK")
        print(f"{'='*60}\n")
        
        all_scores: Dict[str, List[float]] = {}
        
        for week in range(1, current_week + 1):
            print(f"📅 WEEK {week}")
            print("-" * 40)
            
            scores = await self.get_weekly_scores(league_key, week)
            
            if not scores:
                print("   No scores available for this week.\n")
                continue
            
            sorted_scores = sorted(scores, key=lambda x: x.points, reverse=True)
            
            for rank, score in enumerate(sorted_scores[:top_n], 1):
                medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"{rank}."
                print(f"   {medal} {score.team_name}: {score.points:.2f} pts")
                
                if score.team_name not in all_scores:
                    all_scores[score.team_name] = []
                all_scores[score.team_name].append(score.points)
            
            print()
        
        print(f"{'='*60}")
        print(f"SEASON SUMMARY - TOP {top_n} OVERALL SCORERS")
        print(f"{'='*60}\n")
        
        team_totals = [
            TopScorer(
                team_name=team,
                total_points=sum(points),
                weeks_played=len(points),
                average_points=sum(points) / len(points) if points else 0
            )
            for team, points in all_scores.items()
        ]
        
        sorted_totals = sorted(team_totals, key=lambda x: x.total_points, reverse=True)
        
        for rank, scorer in enumerate(sorted_totals[:top_n], 1):
            medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"{rank}."
            print(f"{medal} {scorer.team_name}")
            print(f"   Total Points: {scorer.total_points:.2f}")
            print(f"   Weeks Played: {scorer.weeks_played}")
            print(f"   Avg Points/Week: {scorer.average_points:.2f}")
            print()