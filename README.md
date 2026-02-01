# Fantasy Football Treasurer

This project is a Python application (Fantasy Football Treasurer) that interacts with the Yahoo Fantasy Football API to retrieve and display statistics for the season. It allows users to access various data points related to their fantasy football league, teams, and players.

## Project Structure

```
yahoo-fantasy-football-agent
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── agent
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── tools
│   │       ├── __init__.py
│   │       ├── league_info.py
│   │       ├── team_stats.py
│   │       ├── player_stats.py
│   │       ├── standings.py
│   │       ├── matchups.py
│   │       └── season_stats.py
│   ├── auth
│   │   ├── __init__.py
│   │   ├── oauth.py
│   │   └── prompt_credentials.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── yahoo_client.py
│   │   └── endpoints.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── league.py
│   │   ├── team.py
│   │   ├── player.py
│   │   └── stats.py
│   └── utils
│       ├── __init__.py
│       └── formatters.py
├── tests
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_api.py
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fantasy-football-treasurer.git
   cd fantasy-football-treasurer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Yahoo App Setup (Required for Authentication)

Before using this application, you need to create a Yahoo Developer App to obtain API credentials.

### Step 1: Create a Yahoo Developer App

1. Go to [Yahoo Developer Apps](https://developer.yahoo.com/apps/)
2. Sign in with your Yahoo account
3. Click **"Create an App"**
4. Fill in the application details:
   - **Application Name**: `Fantasy Football Treasurer` (or any name you prefer)
   - **Application Type**: Select **"Installed Application"**
   - **Description**: Optional description of your app
   - **Home Page URL**: `https://localhost`
   - **Redirect URI(s)**: `https://localhost/callback`
   - **API Permissions**: Check **"Fantasy Sports"** (Read/Write)

5. Click **"Create App"**
6. You will receive:
   - **Client ID (Consumer Key)**: A long alphanumeric string
   - **Client Secret (Consumer Secret)**: Keep this secure!

### Step 2: Save Your Credentials

Copy your **Client ID** and **Client Secret** - you'll need to enter them when running the application.

> ⚠️ **Security Note**: Your credentials are only used for the current session and are never stored by the application.

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Enter your credentials when prompted:
   - Yahoo email address
   - Client ID (Consumer Key)
   - Client Secret (Consumer Secret)

3. **Authentication Flow**:
   - The application will open your browser to Yahoo's login page
   - Sign in and authorize the application
   - After authorization, your browser will redirect to `https://localhost/callback?code=XXXXXXXX`
   - **The page will NOT load** (this is expected - localhost isn't running a server)
   - Look at your browser's **URL/address bar**
   - Copy the **code** value from the URL (everything after `code=`)
   - Paste this authorization code into the application prompt

4. Once authenticated, select your league and configure prize money settings.

## Features

## Features

After authenticating and selecting a league, you'll see the main menu:

```
============================================================
📌 MAIN MENU
============================================================
   1. 🏆 Single Season Treasurer (Prize Money Calculator)
   2. 📅 Multi-Year Treasurer (Aggregate by Owner)
   3. 📊 View Team Statistics
   4. 🏈 View Player Rosters
   5. 🏅 View League Standings
   6. 🎯 View Weekly Matchups (Coming Soon)
   7. 📈 View Season Statistics (Coming Soon)
   8. 🔄 Switch League
   9. 👋 Exit
------------------------------------------------------------
```

---

### 1. 🏆 Single Season Treasurer (Prize Money Calculator)

Calculates weekly prize money earnings for all teams in your fantasy football league for a single season.

**How to Use:**
1. Select option `1` from the main menu
2. Enter prize amounts for 1st, 2nd, and 3rd place
3. Enter the number of weeks to analyze
4. View the generated prize money table

**Inputs Required:**
| Input | Description |
|-------|-------------|
| 1st Place Prize | Dollar amount awarded to the highest scorer each week |
| 2nd Place Prize | Dollar amount awarded to the second highest scorer each week |
| 3rd Place Prize | Dollar amount awarded to the third highest scorer each week |
| Number of Weeks | How many weeks of the season to analyze |

**Output Generated:**

```
Team Name           | Wk 1    | Wk 2    | ... | Wk N    | TOTAL
-----------------------------------------------------------------
Team A              | $20.00  |    -    | ... | $15.00  | $35.00
Team B              |    -    | $10.00  | ... | $20.00  | $30.00
...
-----------------------------------------------------------------
TOTAL PAID OUT      | $45.00  | $45.00  | ... | $45.00  | $630.00
```

Plus an **Earnings Leaderboard**:
```
🥇 Team A: $100.00
🥈 Team B: $95.00
🥉 Team C: $90.00
...
```

---

### 2. 📅 Multi-Year Treasurer (Aggregate by Owner)

**The flagship feature!** Aggregates prize money earnings across multiple seasons, grouped by owner name. This is perfect for leagues that have run for multiple years and want to see total historical earnings.

**How to Use:**
1. Select option `2` from the main menu
2. Enter the year range (e.g., 2021-2025)
3. Enter prize amounts for 1st, 2nd, and 3rd place
4. Enter the number of weeks per season to analyze
5. Wait while the application fetches data from each season (rate-limited to avoid API throttling)

**Inputs Required:**
| Input | Description |
|-------|-------------|
| Start Year | First year to include (e.g., 2021) |
| End Year | Last year to include (e.g., 2025) |
| 1st Place Prize | Dollar amount for highest scorer each week |
| 2nd Place Prize | Dollar amount for second highest scorer |
| 3rd Place Prize | Dollar amount for third highest scorer |
| Number of Weeks | Weeks per season to analyze |

**Output Generated:**

```
================================================================================
📊 MULTI-YEAR EARNINGS SUMMARY (2021-2025)
================================================================================

Owner Name                                          | Total Earnings
--------------------------------------------------------------------------------
John Smith                                          |        $485.00
Sarah Johnson                                       |        $420.00
Mike Williams                                       |        $380.00
...
--------------------------------------------------------------------------------
GRAND TOTAL                                         |      $2,250.00
================================================================================
```

**Features:**
- Automatically discovers game keys for each NFL season
- Handles owner changes (same owner across different team names)
- Rate-limited API calls to prevent throttling
- Shows team-to-owner mapping for verification

---

### 3. 📊 View Team Statistics

View detailed statistics for each team in your league.

**How to Use:**
1. Select option `3` from the main menu
2. Statistics for all teams are displayed automatically

**Output Example:**
```
──────────────────────────────────────────────────────
📋 Team #1: Thunderbolts
──────────────────────────────────────────────────────
   Manager: John D.
   Team Key: 449.l.530952.t.1
   Record: 10-4
   Points For: 1,847.52
   Points Against: 1,623.18
   Streak: W3
   Waiver Priority: 5
   Moves: 23
   Trades: 2
```

---

### 3. 🏈 View Player Rosters

View the roster (players) for any team in your league.

**How to Use:**
1. Select option `4` from the main menu
2. Choose a specific team or view all teams
3. View the roster with player positions and status

**Output Example:**
```
📋 Thunderbolts - Roster
────────────────────────────────────────────────────────────
   Pos   | Player Name                    | Team  | Status
   -------------------------------------------------------
   QB    | Josh Allen                     | BUF   | Active
   WR    | Ja'Marr Chase                  | CIN   | Active
   WR    | Amon-Ra St. Brown              | DET   | Active
   RB    | Derrick Henry                  | BAL   | Active
   RB    | Saquon Barkley                 | PHI   | Active
   TE    | Travis Kelce                   | KC    | Active
   K     | Justin Tucker                  | BAL   | Active
   DEF   | San Francisco 49ers            | SF    | Active
   BN    | Jayden Daniels                 | WAS   | Active
   ...
```

---

### 4. 🏅 View League Standings

View current rankings with records and point totals.

**How to Use:**
1. Select option `5` from the main menu
2. Standings are displayed automatically

**Output Example:**
```
================================================================================
🏅 LEAGUE STANDINGS
================================================================================

Rank   | Team Name        | Record     |   Points For |   Points Against | Streak
----------------------------------------------------------------------------------
1      | Thunderbolts     | 10-4       |      1847.52 |          1623.18 |     W3
2      | Power Rangers    | 9-5        |      1789.34 |          1654.22 |     W1
3      | Trojans          | 8-6        |      1756.89 |          1701.45 |     L2
...
```

---

### 6. 🎯 View Weekly Matchups *(Coming Soon)*

Check head-to-head matchups for any week.

**Planned Output:**
```
Week 14 Matchups:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Thunderbolts (142.56) vs Power Rangers (128.34)  ✓ Thunderbolts WIN
Trojans (135.22) vs DaBears (119.87)             ✓ Trojans WIN
Bulldawgs (127.45) vs Sith Happens (131.20)      ✓ Sith Happens WIN
...
```

---

### 7. 📈 View Season Statistics *(Coming Soon)*

Obtain aggregated stats across the entire season.

**Planned Output:**
```
Season Summary (2025):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Highest Single Week Score: 186.42 (Thunderbolts, Week 8)
Lowest Single Week Score: 78.56 (DaBears, Week 3)
Average Weekly Score: 124.67
Most Consistent Team: Power Rangers (Std Dev: 12.3)
Total Points Scored: 20,943.56
```

---

### 8. 🔄 Switch League

Switch to a different league without restarting the application.

**How to Use:**
1. Select option `8` from the main menu
2. Choose from the list of your available leagues (current league marked with 👈)
3. Continue using other features with the new league

---

### 9. 👋 Exit

Exit the application. Your credentials are automatically cleared from memory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.