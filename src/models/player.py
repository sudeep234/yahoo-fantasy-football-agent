class Player:
    def __init__(self, player_id, name, position, team, stats=None):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.team = team
        self.stats = stats if stats is not None else {}

    def update_stats(self, new_stats):
        self.stats.update(new_stats)

    def get_stat(self, stat_name):
        return self.stats.get(stat_name, None)

    def __repr__(self):
        return f"Player(id={self.player_id}, name={self.name}, position={self.position}, team={self.team}, stats={self.stats})"