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


def print_standings(standings: list):
    """Print league standings in a formatted table."""
    print("\n" + "=" * 80)
    print("🏅 LEAGUE STANDINGS")
    print("=" * 80 + "\n")
    
    if not standings:
        print("   No standings data available.")
        return
    
    # Calculate column widths
    max_name_len = max(len(s['name']) for s in standings) if standings else 15
    max_name_len = max(max_name_len, 15)
    
    # Header
    header = f"{'Rank':<6} | {'Team Name':<{max_name_len}} | {'Record':<10} | {'Points For':>12} | {'Points Against':>14} | {'Streak':>6}"
    print(header)
    print("-" * len(header))
    
    for team in standings:
        record = f"{team['wins']}-{team['losses']}"
        if team['ties'] > 0:
            record += f"-{team['ties']}"
        
        row = f"{team['rank']:<6} | {team['name']:<{max_name_len}} | {record:<10} | {team['points_for']:>12.2f} | {team['points_against']:>14.2f} | {team['streak']:>6}"
        print(row)
    
    print()


def print_team_stats(teams: list, standings: list):
    """Print detailed team statistics."""
    print("\n" + "=" * 80)
    print("📊 TEAM STATISTICS")
    print("=" * 80 + "\n")
    
    if not teams:
        print("   No team data available.")
        return
    
    # Create a lookup for standings info
    standings_lookup = {s['name']: s for s in standings} if standings else {}
    
    for i, team in enumerate(teams, 1):
        print(f"{'─' * 50}")
        print(f"📋 Team #{i}: {team['name']}")
        print(f"{'─' * 50}")
        print(f"   Manager: {team['manager'] or 'N/A'}")
        print(f"   Team Key: {team['team_key']}")
        
        # Add standings info if available
        if team['name'] in standings_lookup:
            s = standings_lookup[team['name']]
            record = f"{s['wins']}-{s['losses']}"
            if s['ties'] > 0:
                record += f"-{s['ties']}"
            print(f"   Record: {record}")
            print(f"   Points For: {s['points_for']:.2f}")
            print(f"   Points Against: {s['points_against']:.2f}")
            print(f"   Streak: {s['streak']}")
        
        print(f"   Waiver Priority: {team['waiver_priority']}")
        print(f"   Moves: {team['moves']}")
        print(f"   Trades: {team['trades']}")
        print()


async def print_player_stats(agent, teams: list):
    """Print player/roster information for each team."""
    print("\n" + "=" * 80)
    print("🏈 PLAYER ROSTERS")
    print("=" * 80 + "\n")
    
    if not teams:
        print("   No team data available.")
        return
    
    # Ask user which team's roster to view
    print("Select a team to view roster:")
    for i, team in enumerate(teams, 1):
        print(f"   {i}. {team['name']}")
    print(f"   {len(teams) + 1}. View all teams")
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(teams) + 1}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx <= len(teams):
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")
    
    if idx == len(teams):
        # View all teams
        selected_teams = teams
    else:
        selected_teams = [teams[idx]]
    
    for team in selected_teams:
        print(f"\n{'─' * 60}")
        print(f"📋 {team['name']} - Roster")
        print(f"{'─' * 60}")
        
        roster = await agent.get_team_roster(team['team_key'])
        
        if not roster:
            print("   No roster data available.")
            continue
        
        # Group by position
        positions_order = ['QB', 'WR', 'RB', 'TE', 'K', 'DEF', 'BN', 'IR']
        
        # Header
        print(f"   {'Pos':<5} | {'Player Name':<30} | {'Team':<5} | {'Status':<10}")
        print(f"   {'-' * 55}")
        
        for player in roster:
            pos = player['selected_position'] or player['position']
            status = player['status'] if player['status'] else 'Active'
            print(f"   {pos:<5} | {player['name']:<30} | {player['team']:<5} | {status:<10}")
        
        print()


def show_main_menu():
    """Display the main menu and get user choice."""
    print("\n" + "=" * 60)
    print("📌 MAIN MENU")
    print("=" * 60)
    print("   1. 🏆 League Treasurer (Prize Money Calculator)")
    print("   2. 📊 View Team Statistics")
    print("   3. 🏈 View Player Rosters")
    print("   4. 🏅 View League Standings")
    print("   5. 🎯 View Weekly Matchups (Coming Soon)")
    print("   6. 📈 View Season Statistics (Coming Soon)")
    print("   7. 🔄 Switch League")
    print("   8. 👋 Exit")
    print("-" * 60)
    
    while True:
        try:
            choice = input("Enter your choice (1-8): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return int(choice)
            else:
                print("Invalid choice. Please enter 1-8.")
        except ValueError:
            print("Please enter a number.")


async def run():
    print("=" * 60)
    print("🏈 Fantasy Football Treasurer")
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
    
    # Discover available game keys
    print("🔍 Discovering available NFL seasons...")
    game_keys = await agent.discover_game_keys()
    if game_keys:
        print(f"   Found {len(game_keys)} season(s): {sorted(game_keys.keys(), reverse=True)}")
        for season in sorted(game_keys.keys(), reverse=True):
            print(f"      {season}: game_key={game_keys[season]}")
    print()
    
    # List all leagues from discovered seasons
    print("📋 Fetching all your Fantasy Football leagues...")
    print("=" * 60)
    
    leagues_by_year = await agent.list_all_leagues_all_years()
    
    if not leagues_by_year:
        print("❌ No leagues found.")
        print("\n   This could mean:")
        print("   - You're not in any Fantasy Football leagues")
        print("   - The API permissions are not set correctly")
        print("   - Try checking your Yahoo Developer App settings")
        return
    
    total_leagues = sum(len(leagues) for leagues in leagues_by_year.values())
    print(f"\n✅ Found {total_leagues} league(s) across {len(leagues_by_year)} season(s):\n")
    
    # Flatten all leagues for selection
    all_leagues = []
    for year in sorted(leagues_by_year.keys(), reverse=True):
        leagues = leagues_by_year[year]
        print(f"🏈 {year} SEASON ({len(leagues)} league(s))")
        print("-" * 40)
        for i, league in enumerate(leagues, 1):
            all_leagues.append(league)
            print(f"   {len(all_leagues)}. {league['name']} (ID: {league['league_id']})")
            print(f"      League Key: {league['league_key']}")
            print(f"      Teams: {league['num_teams']}")
            if league.get('current_week'):
                print(f"      Current Week: {league['current_week']}")
        print()
    
    # Let user select a league
    print("=" * 60)
    print("Select a league to work with:")
    print("-" * 60)
    for i, league in enumerate(all_leagues, 1):
        print(f"   {i}. {league['season']} - {league['name']}")
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(all_leagues)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(all_leagues):
                selected_league = all_leagues[idx]
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")
    
    print(f"\n✅ Selected: {selected_league['name']} ({selected_league['season']})")
    
    # Main menu loop
    while True:
        menu_choice = show_main_menu()
        
        if menu_choice == 1:
            # League Treasurer
            print(f"\n📊 League Treasurer - {selected_league['name']} ({selected_league['season']})")
            prizes = get_prize_inputs()
            
            print(f"\n📊 Fetching weekly scores for weeks 1-{prizes['num_weeks']}...")
            print("=" * 60)
            
            weekly_rankings = {}
            for week in range(1, prizes['num_weeks'] + 1):
                scores = await agent.get_weekly_scores(selected_league['league_key'], week)
                
                if scores:
                    sorted_scores = sorted(scores, key=lambda x: x.points, reverse=True)
                    weekly_rankings[week] = [s.team_name for s in sorted_scores[:3]]
                    print(f"   Week {week}: ✅ {len(scores)} teams")
                else:
                    weekly_rankings[week] = []
                    print(f"   Week {week}: ⚠️ No scores available")
            
            print_prize_table(weekly_rankings, prizes)
        
        elif menu_choice == 2:
            # Team Statistics
            print(f"\n📊 Fetching team statistics for {selected_league['name']}...")
            teams = await agent.get_all_teams_info(selected_league['league_key'])
            standings = await agent.get_league_standings(selected_league['league_key'])
            print_team_stats(teams, standings)
        
        elif menu_choice == 3:
            # Player Rosters
            print(f"\n🏈 Fetching team rosters for {selected_league['name']}...")
            teams = await agent.get_all_teams_info(selected_league['league_key'])
            await print_player_stats(agent, teams)
        
        elif menu_choice == 4:
            # League Standings
            print(f"\n🏅 Fetching league standings for {selected_league['name']}...")
            standings = await agent.get_league_standings(selected_league['league_key'])
            print_standings(standings)
        
        elif menu_choice == 5:
            # Weekly Matchups - Coming Soon
            print("\n🎯 Weekly Matchups feature is coming soon!")
            print("   This feature will show head-to-head matchups for any week.")
        
        elif menu_choice == 6:
            # Season Statistics - Coming Soon
            print("\n📈 Season Statistics feature is coming soon!")
            print("   This feature will show aggregated stats across the entire season.")
        
        elif menu_choice == 7:
            # Switch League
            print("\n🔄 Select a different league:")
            print("-" * 60)
            for i, league in enumerate(all_leagues, 1):
                marker = " 👈" if league == selected_league else ""
                print(f"   {i}. {league['season']} - {league['name']}{marker}")
            
            while True:
                try:
                    choice = input(f"\nEnter choice (1-{len(all_leagues)}): ").strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(all_leagues):
                        selected_league = all_leagues[idx]
                        print(f"\n✅ Switched to: {selected_league['name']} ({selected_league['season']})")
                        break
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a number.")
        
        elif menu_choice == 8:
            # Exit
            break
    
    # Clear credentials from memory
    credentials.clear()
    print("\n🔒 Credentials cleared from memory.")
    print("👋 Session ended.")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()