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

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. Follow the prompts to enter your Yahoo credentials. The application will not store your credentials.

## Features

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