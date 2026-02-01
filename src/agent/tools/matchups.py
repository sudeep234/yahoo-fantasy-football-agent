def get_matchups(yahoo_client, league_id):
    matchups = yahoo_client.get_matchups(league_id)
    formatted_matchups = format_matchups(matchups)
    return formatted_matchups

def format_matchups(matchups):
    formatted = []
    for matchup in matchups:
        formatted.append({
            'team1': matchup['team1'],
            'team2': matchup['team2'],
            'score1': matchup['score1'],
            'score2': matchup['score2'],
            'date': matchup['date'],
        })
    return formatted