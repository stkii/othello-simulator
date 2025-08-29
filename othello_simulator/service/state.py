from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class GameState:
    """Centralized game state management class."""

    # Basic game information
    player1_name: str = ""
    player2_name: str = ""
    black_player_name: str = ""
    white_player_name: str = ""
    move_count: int = 0
    strategy1_file: str | None = None
    strategy2_file: str | None = None

    # Player mode control
    is_player_vs_cpu: bool = False
    player: int = 1  # Player number (1: black, 2: white)
    waiting_for_player: bool = False

    # Highlight information
    last_move: list[int] | None = None
    flipped_stones: list[list[int]] = field(default_factory=list)

    # Strategy objects (runtime only, not for persistence)
    strategy1: Any = field(default=None, init=False, repr=False)
    strategy2: Any = field(default=None, init=False, repr=False)

    def setup_game(  # noqa: PLR0913
        self,
        strategy1: Any,  # noqa: ANN401
        strategy2: Any,  # noqa: ANN401
        name1: str,
        name2: str,
        *,
        player_vs_cpu: bool = False,
        player: int = 1,
        strategy1_file: str | None = None,
        strategy2_file: str | None = None,
    ) -> None:
        """Set up game state at start.

        Parameters
        ----------
        strategy1 : Any
            Player 1 strategy
        strategy2 : Any
            Player 2 strategy
        name1 : str
            Player 1 name
        name2 : str
            Player 2 name
        player_vs_cpu : bool
            Whether this is player vs CPU mode
        player : int
            Player number (for player vs CPU mode)
        strategy1_file : str | None
            Player 1 strategy file path
        strategy2_file : str | None
            Player 2 strategy file path
        """
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.player1_name = name1
        self.player2_name = name2
        self.black_player_name = name1
        self.white_player_name = name2
        self.move_count = 0
        self.strategy1_file = strategy1_file
        self.strategy2_file = strategy2_file

        # Set player mode
        self.is_player_vs_cpu = player_vs_cpu
        self.player = player
        self.waiting_for_player = False

        # Clear highlight information
        self.clear_highlights()

    def is_player_turn(self, current_player: int) -> bool:
        """Check if current turn is the player's turn.

        Parameters
        ----------
        current_player : int
            Current player number

        Returns
        -------
        bool
            True if it's the player's turn
        """
        return self.is_player_vs_cpu and current_player == self.player

    def get_current_strategy(self, current_player: int) -> Any:  # noqa: ANN401
        """Get strategy for current player.

        Parameters
        ----------
        current_player : int
            Current player number

        Returns
        -------
        Any
            Player's strategy object
        """
        return self.strategy1 if current_player == 1 else self.strategy2

    def update_highlights(self, move: list[int], flipped_stones: list[tuple[int, int]]) -> None:
        """Update highlight information.

        Parameters
        ----------
        move : list[int]
            Last move coordinates [row, col]
        flipped_stones : list[tuple[int, int]]
            List of flipped stone coordinates
        """
        self.last_move = move
        self.flipped_stones = [[row, col] for row, col in flipped_stones] if flipped_stones else []

    def clear_highlights(self) -> None:
        """Clear highlight information."""
        self.last_move = None
        self.flipped_stones = []

    def set_waiting_for_player(self, *, waiting: bool) -> None:
        """Set player input waiting state.

        Parameters
        ----------
        waiting : bool
            Input waiting state
        """
        self.waiting_for_player = waiting

    def reset(self) -> None:
        """Reset game state."""
        self.player1_name = ""
        self.player2_name = ""
        self.black_player_name = ""
        self.white_player_name = ""
        self.move_count = 0
        self.strategy1_file = None
        self.strategy2_file = None
        self.is_player_vs_cpu = False
        self.player = 1
        self.waiting_for_player = False
        self.clear_highlights()
        self.strategy1 = None
        self.strategy2 = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for persistence.

        Returns
        -------
        dict[str, Any]
            State dictionary for persistence
        """
        data = asdict(self)
        # Don't persist strategy objects
        data.pop("strategy1", None)
        data.pop("strategy2", None)
        return data

    def from_dict(self, data: dict[str, Any]) -> None:
        """Restore state from dictionary.

        Parameters
        ----------
        data : dict[str, Any]
            State dictionary for restoration
        """
        # Basic information
        self.player1_name = data.get("player1_name", "")
        self.player2_name = data.get("player2_name", "")
        self.black_player_name = data.get("black_player_name", "")
        self.white_player_name = data.get("white_player_name", "")
        self.move_count = data.get("move_count", 0)
        self.strategy1_file = data.get("strategy1_file")
        self.strategy2_file = data.get("strategy2_file")

        # Player mode
        self.is_player_vs_cpu = data.get("is_player_vs_cpu", False)
        self.player = data.get("player", 1)
        self.waiting_for_player = data.get("waiting_for_player", False)

        # Highlight information
        self.last_move = data.get("last_move")
        self.flipped_stones = data.get("flipped_stones", [])

        # Strategy objects set separately during restoration
        self.strategy1 = None
        self.strategy2 = None

    def get_highlight_data(self) -> dict[str, Any]:
        """Get highlight information (for API compatibility).

        Returns
        -------
        dict[str, Any]
            Highlight information dictionary
        """
        return {
            "last_move": self.last_move,
            "flipped_stones": self.flipped_stones,
        }

    def get_player_mode_data(self) -> dict[str, Any]:
        """Get player mode information (for API compatibility).

        Returns
        -------
        dict[str, Any]
            Player mode information dictionary
        """
        return {
            "is_player_vs_cpu": self.is_player_vs_cpu,
            "player": self.player,
            "waiting_for_player": self.waiting_for_player,
        }
