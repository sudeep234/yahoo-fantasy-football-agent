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


def print_team_owners(teams: list):
    """Print a clean table of team names and their owners."""
    print("\n" + "=" * 60)
    print("👥 TEAM OWNERS")
    print("=" * 60 + "\n")
    
    if not teams:
        print("   No team data available.")
        return
    
    # Calculate column widths
    max_team_len = max(len(t['name']) for t in teams) if teams else 20
    max_team_len = max(max_team_len, 15)
    max_owner_len = max(len(t['manager'] or 'N/A') for t in teams) if teams else 15
    max_owner_len = max(max_owner_len, 10)
    
    # Header
    header = f"   {'#':<4} | {'Team Name':<{max_team_len}} | {'Owner/Manager':<{max_owner_len}}"
    print(header)
    print(f"   {'-' * (len(header) - 3)}")
    
    # Rows
    for i, team in enumerate(teams, 1):
        owner = team['manager'] or 'N/A'
        print(f"   {i:<4} | {team['name']:<{max_team_len}} | {owner:<{max_owner_len}}")
    
    print()


async def multi_year_treasurer(agent, all_leagues: list):
    """Calculate prize money earnings by owner across multiple years."""
    print("\n" + "=" * 70)
    print("📅 MULTI-YEAR TREASURER")
    print("=" * 70)
    print("\nThis feature calculates total earnings by OWNER across multiple seasons.\n")
    
    # Get available years from leagues
    available_years = sorted(set(l['season'] for l in all_leagues))
    print(f"Available seasons: {available_years}")
    
    # Get start year
    while True:
        try:
            start_year = int(input("\nEnter start year: ").strip())
            if start_year in available_years:
                break
            else:
                print(f"❌ Year {start_year} not available. Choose from: {available_years}")
        except ValueError:
            print("❌ Please enter a valid year.")
    
    # Get end year
    while True:
        try:
            end_year = int(input("Enter end year: ").strip())
            if end_year in available_years and end_year >= start_year:
                break
            elif end_year < start_year:
                print(f"❌ End year must be >= start year ({start_year}).")
            else:
                print(f"❌ Year {end_year} not available. Choose from: {available_years}")
        except ValueError:
            print("❌ Please enter a valid year.")
    
    # Get unique league names
    unique_names = sorted(set(l['name'] for l in all_leagues))
    print(f"\nAvailable leagues: {unique_names}")
    
    league_name = input("\nEnter league name to search for: ").strip()
    
    # Find matching leagues in the year range
    matching_leagues = [
        l for l in all_leagues 
        if league_name.lower() in l['name'].lower() 
        and start_year <= l['season'] <= end_year
    ]
    
    if not matching_leagues:
        print(f"\n❌ No leagues matching '{league_name}' found between {start_year}-{end_year}.")
        return
    
    matching_leagues = sorted(matching_leagues, key=lambda x: x['season'])
    print(f"\n✅ Found {len(matching_leagues)} matching league(s):")
    for l in matching_leagues:
        print(f"   📅 {l['season']}: {l['name']} (ID: {l['league_id']})")
    
    # Get prize inputs (once for all years)
    print("\n💰 Prize Money Configuration (applies to all years)")
    print("-" * 50)
    
    while True:
        try:
            pos1_prize = float(input("Enter prize for 1st place each week ($): ").strip())
            if pos1_prize >= 0:
                break
            print("❌ Please enter a positive number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    while True:
        try:
            pos2_prize = float(input("Enter prize for 2nd place each week ($): ").strip())
            if pos2_prize >= 0:
                break
            print("❌ Please enter a positive number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    while True:
        try:
            pos3_prize = float(input("Enter prize for 3rd place each week ($): ").strip())
            if pos3_prize >= 0:
                break
            print("❌ Please enter a positive number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    while True:
        try:
            num_weeks = int(input("Enter number of weeks to analyze per season: ").strip())
            if num_weeks >= 1:
                break
            print("❌ Please enter at least 1 week.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    # Process each year
    owner_totals = {}  # owner_name -> {total: float, years: {year: amount}}
    year_summaries = {}  # year -> {team_name: amount}
    team_to_owner_global = {}  # Keep track of team->owner mapping across years
    
    print(f"\n📊 Processing {len(matching_leagues)} season(s)...")
    print("=" * 70)
    
    for league in matching_leagues:
        year = league['season']
        print(f"\n📅 {year}: {league['name']}")
        print("-" * 50)
        
        # Get team info to map team names to owners
        await asyncio.sleep(0.5)  # Rate limiting
        teams = await agent.get_all_teams_info(league['league_key'])
        team_to_owner = {}
        print(f"   Teams found: {len(teams)}")
        for team in teams:
            owner = team['manager'] if team['manager'] else team['name']
            team_to_owner[team['name']] = owner
            team_to_owner_global[team['name']] = owner  # Store globally
            # Debug: show team->owner mapping
            # print(f"      {team['name']} -> {owner}")
        
        # Get weekly scores with rate limiting
        weekly_rankings = {}
        for week in range(1, num_weeks + 1):
            await asyncio.sleep(0.3)  # Rate limiting between API calls
            scores = await agent.get_weekly_scores(league['league_key'], week)
            if scores:
                sorted_scores = sorted(scores, key=lambda x: x.points, reverse=True)
                weekly_rankings[week] = [s.team_name for s in sorted_scores[:3]]
                print(f"   Week {week}: ✅")
            else:
                weekly_rankings[week] = []
                print(f"   Week {week}: ⚠️ No data")
        
        # Calculate team earnings for this year
        team_earnings = {}
        for week, rankings in weekly_rankings.items():
            for rank, team_name in enumerate(rankings, 1):
                if team_name not in team_earnings:
                    team_earnings[team_name] = 0
                if rank == 1:
                    team_earnings[team_name] += pos1_prize
                elif rank == 2:
                    team_earnings[team_name] += pos2_prize
                elif rank == 3:
                    team_earnings[team_name] += pos3_prize
        
        year_summaries[year] = team_earnings
        
        # Aggregate by owner
        for team_name, amount in team_earnings.items():
            owner = team_to_owner.get(team_name, team_name)
            if owner not in owner_totals:
                owner_totals[owner] = {'total': 0, 'years': {}}
            owner_totals[owner]['total'] += amount
            owner_totals[owner]['years'][year] = owner_totals[owner]['years'].get(year, 0) + amount
    
    # Print results
    print("\n" + "=" * 70)
    print(f"📊 MULTI-YEAR EARNINGS SUMMARY ({start_year}-{end_year})")
    print("=" * 70)
    print(f"\n   League: {league_name}")
    print(f"   Seasons: {start_year} - {end_year} ({len(matching_leagues)} seasons)")
    print(f"   Weeks per season: {num_weeks}")
    print(f"   Prizes: 1st=${pos1_prize:.2f}, 2nd=${pos2_prize:.2f}, 3rd=${pos3_prize:.2f}")
    
    # Print team to owner mapping
    print("\n" + "-" * 70)
    print("👥 TEAM TO OWNER MAPPING")
    print("-" * 70)
    for team_name, owner_name in sorted(team_to_owner_global.items()):
        print(f"   {team_name} -> {owner_name}")
    
    # Print yearly breakdown
    print("\n" + "-" * 70)
    print("📅 EARNINGS BY YEAR (by Team)")
    print("-" * 70)
    
    years = sorted(year_summaries.keys())
    for year in years:
        print(f"\n   {year}:")
        year_data = year_summaries[year]
        sorted_teams = sorted(year_data.items(), key=lambda x: x[1], reverse=True)
        for team, amount in sorted_teams:
            if amount > 0:
                print(f"      {team}: ${amount:.2f}")
    
    # Print owner leaderboard
    print("\n" + "=" * 70)
    print("🏆 TOTAL EARNINGS BY OWNER")
    print("=" * 70 + "\n")
    
    sorted_owners = sorted(owner_totals.items(), key=lambda x: x[1]['total'], reverse=True)
    
    max_owner_len = max(len(o) for o, _ in sorted_owners) if sorted_owners else 15
    
    # Header with years
    header = f"   {'Rank':<6} | {'Owner':<{max_owner_len}}"
    for year in years:
        header += f" | {year:>10}"
    header += f" | {'TOTAL':>12}"
    print(header)
    print(f"   {'-' * (len(header) - 3)}")
    
    for rank, (owner, data) in enumerate(sorted_owners, 1):
        if data['total'] > 0:
            medal = ["🥇", "🥈", "🥉"][rank - 1] if rank <= 3 else f"{rank}."
            row = f"   {medal:<6} | {owner:<{max_owner_len}}"
            for year in years:
                year_amount = data['years'].get(year, 0)
                if year_amount > 0:
                    row += f" | ${year_amount:>9.2f}"
                else:
                    row += f" | {'-':>10}"
            row += f" | ${data['total']:>11.2f}"
            print(row)
    
    # Grand total
    grand_total = sum(d['total'] for d in owner_totals.values())
    print(f"\n   {'─' * 50}")
    print(f"   💰 GRAND TOTAL PAID OUT: ${grand_total:.2f}")
    print()


def show_main_menu():
    """Display the main menu and get user choice."""
    print("\n" + "=" * 60)
    print("📌 MAIN MENU")
    print("=" * 60)
    print("   1. 🏆 League Treasurer (Single Season)")
    print("   2. 📅 Multi-Year Treasurer (Earnings by Owner)")
    print("   3. 📊 View Team Statistics")
    print("   4. 🏈 View Player Rosters")
    print("   5. 🏅 View League Standings")
    print("   6. 🎯 View Weekly Matchups (Coming Soon)")
    print("   7. 📈 View Season Statistics (Coming Soon)")
    print("   8. 🔄 Switch League")
    print("   9. 👋 Exit")
    print("-" * 60)
    
    while True:
        try:
            choice = input("Enter your choice (1-9): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return int(choice)
            else:
                print("Invalid choice. Please enter 1-9.")
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
            # Multi-Year Treasurer
            await multi_year_treasurer(agent, all_leagues)
        
        elif menu_choice == 3:
            # Team Statistics
            print(f"\n📊 Fetching team statistics for {selected_league['name']}...")
            teams = await agent.get_all_teams_info(selected_league['league_key'])
            standings = await agent.get_league_standings(selected_league['league_key'])
            print_team_stats(teams, standings)
        
        elif menu_choice == 4:
            # Player Rosters
            print(f"\n🏈 Fetching team rosters for {selected_league['name']}...")
            teams = await agent.get_all_teams_info(selected_league['league_key'])
            await print_player_stats(agent, teams)
        
        elif menu_choice == 5:
            # League Standings
            print(f"\n🏅 Fetching league standings for {selected_league['name']}...")
            standings = await agent.get_league_standings(selected_league['league_key'])
            print_standings(standings)
        
        elif menu_choice == 6:
            # Weekly Matchups - Coming Soon
            print("\n🎯 Weekly Matchups feature is coming soon!")
            print("   This feature will show head-to-head matchups for any week.")
        
        elif menu_choice == 7:
            # Season Statistics - Coming Soon
            print("\n📈 Season Statistics feature is coming soon!")
            print("   This feature will show aggregated stats across the entire season.")
        
        elif menu_choice == 8:
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
        
        elif menu_choice == 9:
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