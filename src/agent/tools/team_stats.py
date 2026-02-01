def get_team_stats(league_id, team_id, client):
    """
    Retrieve and format team statistics for a given team in a specific league.
    
    Parameters:
    league_id (str): The ID of the fantasy league.
    team_id (str): The ID of the team.
    client (YahooClient): An instance of the YahooClient to make API requests.
    
    Returns:
    dict: A dictionary containing formatted team statistics.
    """
    response = client.get_team_stats(league_id, team_id)
    if response and 'team_stats' in response:
        stats = response['team_stats']
        formatted_stats = {
            'team_id': stats['team_id'],
            'wins': stats['wins'],
            'losses': stats['losses'],
            'points_for': stats['points_for'],
            'points_against': stats['points_against'],
            'rank': stats['rank'],
        }
        return formatted_stats
    return None

def display_team_stats(stats):
    """
    Display the formatted team statistics.
    
    Parameters:
    stats (dict): A dictionary containing team statistics.
    """
    if stats:
        print(f"Team ID: {stats['team_id']}")
        print(f"Wins: {stats['wins']}")
        print(f"Losses: {stats['losses']}")
        print(f"Points For: {stats['points_for']}")
        print(f"Points Against: {stats['points_against']}")
        print(f"Rank: {stats['rank']}")
    else:
        print("No statistics available for this team.")