class Team:
    def __init__(self, team_id, team_name, manager, roster):
        self.team_id = team_id
        self.team_name = team_name
        self.manager = manager
        self.roster = roster

    def get_team_info(self):
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "manager": self.manager,
            "roster": self.roster
        }

    def add_player(self, player):
        self.roster.append(player)

    def remove_player(self, player):
        if player in self.roster:
            self.roster.remove(player)

    def get_roster(self):
        return self.roster

    def __str__(self):
        return f"{self.team_name} managed by {self.manager}"