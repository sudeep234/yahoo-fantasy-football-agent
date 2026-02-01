class League:
    def __init__(self, league_id, name, season, teams):
        self.league_id = league_id
        self.name = name
        self.season = season
        self.teams = teams

    def get_league_info(self):
        return {
            "league_id": self.league_id,
            "name": self.name,
            "season": self.season,
            "teams": [team.get_team_info() for team in self.teams]
        }

    def add_team(self, team):
        self.teams.append(team)

    def remove_team(self, team_id):
        self.teams = [team for team in self.teams if team.team_id != team_id]