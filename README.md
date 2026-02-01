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

### 🏆 League Treasurer (Prize Money Calculator)

The main feature of this application is the **League Treasurer** - a tool that calculates weekly prize money earnings for all teams in your fantasy football league.

**Inputs Required:**
| Input | Description |
|-------|-------------|
| 1st Place Prize | Dollar amount awarded to the highest scorer each week |
| 2nd Place Prize | Dollar amount awarded to the second highest scorer each week |
| 3rd Place Prize | Dollar amount awarded to the third highest scorer each week |
| Number of Weeks | How many weeks of the season to analyze |

**Output Generated:**

The application generates a comprehensive **Weekly Prize Money Table** showing:

```
Team Name           | Wk 1    | Wk 2    | ... | Wk N    | TOTAL
-----------------------------------------------------------------
Team A              | $20.00  |    -    | ... | $15.00  | $35.00
Team B              |    -    | $10.00  | ... | $20.00  | $30.00
...
-----------------------------------------------------------------
TOTAL PAID OUT      | $45.00  | $45.00  | ... | $45.00  | $630.00
```

Plus an **Earnings Leaderboard** ranking teams by total prize money:
```
🥇 Team A: $100.00
🥈 Team B: $95.00
🥉 Team C: $90.00
...
```

### Other Features

- Retrieve league information
- Access team statistics
- Get player statistics
- View league standings
- Check matchups
- Obtain season statistics

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.