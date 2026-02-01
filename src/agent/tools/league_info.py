def get_league_info(api_client, league_id):
    response = api_client.get_league(league_id)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to retrieve league information")

def format_league_info(league_info):
    formatted_info = {
        "league_id": league_info.get("league_id"),
        "name": league_info.get("name"),
        "status": league_info.get("status"),
        "season": league_info.get("season"),
        "teams": [team["name"] for team in league_info.get("teams", [])]
    }
    return formatted_info

def display_league_info(formatted_info):
    print("League Information:")
    print(f"ID: {formatted_info['league_id']}")
    print(f"Name: {formatted_info['name']}")
    print(f"Status: {formatted_info['status']}")
    print(f"Season: {formatted_info['season']}")
    print("Teams:")
    for team in formatted_info['teams']:
        print(f"- {team}")