from dataclasses import dataclass
from typing import Optional


@dataclass
class WeeklyScore:
    """Represents a team's score for a single week."""
    team_name: str
    week: int
    points: float
    opponent_name: Optional[str] = None
    opponent_points: Optional[float] = None


@dataclass
class TopScorer:
    """Represents a top scorer summary."""
    team_name: str
    total_points: float
    weeks_played: int
    average_points: float


@dataclass
class TeamStats:
    """Comprehensive team statistics."""
    team_name: str
    team_key: str
    wins: int = 0
    losses: int = 0
    ties: int = 0
    points_for: float = 0.0
    points_against: float = 0.0
    
    @property
    def win_percentage(self) -> float:
        total_games = self.wins + self.losses + self.ties
        if total_games == 0:
            return 0.0
        return self.wins / total_games