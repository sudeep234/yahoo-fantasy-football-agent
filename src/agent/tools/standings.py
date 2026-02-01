def get_standings(yahoo_client):
    """
    Retrieve and format league standings from Yahoo Fantasy Football API.
    
    Parameters:
    yahoo_client (YahooClient): An instance of YahooClient to make API requests.

    Returns:
    list: A list of formatted standings for the league.
    """
    standings_data = yahoo_client.get_standings()
    formatted_standings = []

    for team in standings_data['teams']:
        formatted_standings.append({
            'team_name': team['name'],
            'wins': team['wins'],
            'losses': team['losses'],
            'ties': team['ties'],
            'points_for': team['pointsFor'],
            'points_against': team['pointsAgainst'],
        })

    return formatted_standings