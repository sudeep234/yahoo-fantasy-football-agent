import asyncio
from auth.prompt_credentials import prompt_for_credentials
from auth.oauth import YahooOAuth
from api.yahoo_client import YahooFantasyClient
from agent.agent import FantasyFootballTreasurer


def get_prize_inputs() -> dict:
    """Get prize money inputs from user."""
    print("\n💰 Prize Money Configuration")
    print("-" * 40)
    
    while True:
        try:
            pos1 = float(input("Enter prize for 1st place each week ($): ").strip())
            if pos1 < 0:
                print("❌ Please enter a positive number.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    while True:
        try:
            pos2 = float(input("Enter prize for 2nd place each week ($): ").strip())
            if pos2 < 0:
                print("❌ Please enter a positive number.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    while True:
        try:
            pos3 = float(input("Enter prize for 3rd place each week ($): ").strip())
            if pos3 < 0:
                print("❌ Please enter a positive number.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    while True:
        try:
            num_weeks = int(input("Enter number of weeks to analyze: ").strip())
            if num_weeks < 1:
                print("❌ Please enter at least 1 week.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid number.")
    
    return {
        'pos1_prize': pos1,
        'pos2_prize': pos2,
        'pos3_prize': pos3,
        'num_weeks': num_weeks
    }


def print_prize_table(weekly_rankings: dict, prizes: dict):
    """Print a table showing prize money earned by each team per week."""
    pos1_prize = prizes['pos1_prize']
    pos2_prize = prizes['pos2_prize']
    pos3_prize = prizes['pos3_prize']
    num_weeks = prizes['num_weeks']
    
    # Collect all team names
    all_teams = set()
    for week_data in weekly_rankings.values():
        for team in week_data:
            all_teams.add(team)
    
    all_teams = sorted(all_teams)
    
    # Build prize data: team -> {week: prize}
    prize_data = {team: {} for team in all_teams}
    
    for week, rankings in weekly_rankings.items():
        if week > num_weeks:
            continue
        for rank, team in enumerate(rankings, 1):
            if rank == 1:
                prize_data[team][week] = pos1_prize
            elif rank == 2:
                prize_data[team][week] = pos2_prize
            elif rank == 3:
                prize_data[team][week] = pos3_prize
    
    # Calculate column widths
    max_name_len = max(len(team) for team in all_teams) if all_teams else 10
    max_name_len = max(max_name_len, 10)  # Minimum width
    col_width = 8  # Width for week columns
    
    # Print header
    print("\n" + "=" * 70)
    print("💰 WEEKLY PRIZE MONEY TABLE")
    print("=" * 70)
    print(f"\n   1st Place: ${pos1_prize:.2f} | 2nd Place: ${pos2_prize:.2f} | 3rd Place: ${pos3_prize:.2f}")
    print(f"   Weeks analyzed: 1-{num_weeks}\n")
    
    # Table header
    header = f"{'Team Name':<{max_name_len}}"
    for week in range(1, num_weeks + 1):
        header += f" | {'Wk ' + str(week):>{col_width}}"
    header += f" | {'TOTAL':>{col_width}}"
    
    print(header)
    print("-" * len(header))
    
    # Table rows
    grand_total = 0
    team_totals = []
    
    for team in all_teams:
        row = f"{team:<{max_name_len}}"
        total = 0
        
        for week in range(1, num_weeks + 1):
            prize = prize_data[team].get(week, 0)
            total += prize
            if prize > 0:
                row += f" | ${prize:>{col_width-1}.2f}"
            else:
                row += f" | {'-':>{col_width}}"
        
        row += f" | ${total:>{col_width-1}.2f}"
        print(row)
        
        grand_total += total
        team_totals.append((team, total))
    
    # Print footer
    print("-" * len(header))
    footer = f"{'TOTAL PAID OUT':<{max_name_len}}"
    for week in range(1, num_weeks + 1):
        week_total = pos1_prize + pos2_prize + pos3_prize
        footer += f" | ${week_total:>{col_width-1}.2f}"
    footer += f" | ${grand_total:>{col_width-1}.2f}"
    print(footer)
    
    # Print leaderboard
    print("\n" + "=" * 70)
    print("🏆 EARNINGS LEADERBOARD")
    print("=" * 70 + "\n")
    
    sorted_totals = sorted(team_totals, key=lambda x: x[1], reverse=True)
    
    for rank, (team, total) in enumerate(sorted_totals, 1):
        if total > 0:
            medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"{rank}."
            print(f"   {medal} {team}: ${total:.2f}")


async def run():
    print("=" * 60)
    print("Yahoo Fantasy Football Agent")
    print("=" * 60)
    print("\n⚠️  Your credentials will NOT be stored anywhere.")
    print("They are only used for this session.\n")
    
    # Prompt for credentials (not stored)
    credentials = prompt_for_credentials()
    
    print(f"\n👤 Authenticating as: {credentials['email']}")
    
    # Initialize OAuth (credentials held in memory only)
    oauth = YahooOAuth(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        user_email=credentials['email']
    )
    
    # Authenticate
    print("\n🔐 Authenticating with Yahoo...")
    access_token = await oauth.authenticate()
    
    if not access_token:
        print("❌ Authentication failed. Exiting.")
        return
    
    print("✅ Authentication successful!\n")
    
    # Initialize the Yahoo client
    client = YahooFantasyClient(access_token)
    
    # Initialize the agent with the client
    agent = FantasyFootballTreasurer(client)
    
    # List all leagues from last 5 years
    print("📋 Fetching all your Fantasy Football leagues (2021-2025)...")
    print("=" * 60)
    
    leagues_by_year = await agent.list_all_leagues_all_years()
    
    if not leagues_by_year:
        print("❌ No leagues found for 2021-2025.")
        print("\n   This could mean:")
        print("   - You're not in any Fantasy Football leagues")
        print("   - The API permissions are not set correctly")
        print("   - Try checking your Yahoo Developer App settings")
        return
    
    total_leagues = sum(len(leagues) for leagues in leagues_by_year.values())
    print(f"\n✅ Found {total_leagues} league(s) across {len(leagues_by_year)} season(s):\n")
    
    for year in sorted(leagues_by_year.keys(), reverse=True):
        leagues = leagues_by_year[year]
        print(f"🏈 {year} SEASON ({len(leagues)} league(s))")
        print("-" * 40)
        for i, league in enumerate(leagues, 1):
            print(f"   {i}. {league['name']} (ID: {league['league_id']})")
            print(f"      League Key: {league['league_key']}")
            print(f"      Teams: {league['num_teams']}")
            if league.get('current_week'):
                print(f"      Current Week: {league['current_week']}")
        print()
    
    # Find all x-lte leagues across all years
    print("=" * 60)
    print("🔍 Searching for 'x-lte' leagues across all seasons...")
    print("-" * 60)
    
    xlte_leagues = await agent.find_all_leagues_by_name("x-lte")
    
    if not xlte_leagues:
        print("❌ Could not find any 'x-lte' leagues.")
        print("   Available leagues are listed above.")
    else:
        print(f"\n✅ Found {len(xlte_leagues)} 'x-lte' league(s):\n")
        for league in xlte_leagues:
            print(f"   📅 {league['season']}: {league['name']} (ID: {league['league_id']})")
            print(f"      League Key: {league['league_key']}")
            print(f"      Teams: {league['num_teams']}")
            print()
        
        # Ask user which league to analyze
        print("-" * 60)
        if len(xlte_leagues) == 1:
            selected_league = xlte_leagues[0]
        else:
            print("Select a league to analyze (enter number):")
            for i, league in enumerate(xlte_leagues, 1):
                print(f"   {i}. {league['season']} - {league['name']} (ID: {league['league_id']})")
            
            while True:
                try:
                    choice = input("\nEnter choice (1-{}): ".format(len(xlte_leagues))).strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(xlte_leagues):
                        selected_league = xlte_leagues[idx]
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a number.")
        
        print(f"\n📊 Selected: {selected_league['name']} (ID: {selected_league['league_id']}) - {selected_league['season']}")
        
        # Get prize inputs
        prizes = get_prize_inputs()
        
        print(f"\n📊 Fetching weekly scores for weeks 1-{prizes['num_weeks']}...")
        print("=" * 60)
        
        # Get weekly rankings (top 3 teams per week)
        weekly_rankings = {}  # week -> [team1, team2, team3] in order of points
        
        for week in range(1, prizes['num_weeks'] + 1):
            scores = await agent.get_weekly_scores(selected_league['league_key'], week)
            
            if scores:
                sorted_scores = sorted(scores, key=lambda x: x.points, reverse=True)
                # Get top 3 team names for this week
                weekly_rankings[week] = [s.team_name for s in sorted_scores[:3]]
                print(f"   Week {week}: ✅ {len(scores)} teams")
            else:
                weekly_rankings[week] = []
                print(f"   Week {week}: ⚠️ No scores available")
        
        # Print the prize table
        print_prize_table(weekly_rankings, prizes)
    
    # Clear credentials from memory
    credentials.clear()
    print("\n🔒 Credentials cleared from memory.")
    print("👋 Session ended.")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()