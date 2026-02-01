def format_team_stats(team_stats):
    formatted_stats = []
    for stat in team_stats:
        formatted_stats.append(f"Team: {stat['team_name']}, Wins: {stat['wins']}, Losses: {stat['losses']}")
    return "\n".join(formatted_stats)

def format_player_stats(player_stats):
    formatted_stats = []
    for stat in player_stats:
        formatted_stats.append(f"Player: {stat['player_name']}, Points: {stat['points']}, Rebounds: {stat['rebounds']}, Assists: {stat['assists']}")
    return "\n".join(formatted_stats)

def format_league_standings(standings):
    formatted_standings = []
    for standing in standings:
        formatted_standings.append(f"Team: {standing['team_name']}, Rank: {standing['rank']}, Wins: {standing['wins']}, Losses: {standing['losses']}")
    return "\n".join(formatted_standings)

def format_season_stats(season_stats):
    formatted_stats = []
    for stat in season_stats:
        formatted_stats.append(f"Week: {stat['week']}, Total Points: {stat['total_points']}")
    return "\n".join(formatted_stats)