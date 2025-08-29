from typing import Any

from othello_simulator.core.manager import GameManager
from othello_simulator.core.placement import Placement
from othello_simulator.core.score import ScoreCalculator
from othello_simulator.core.state import BoardState


class Board:
    """Facade for the Othello game service.

    This class provides a simplified interface to the Othello game system,
    encapsulating all core game functionality including board state management,
    move validation, scoring, and game flow control.

    Attributes
    ----------
    _state : BoardState
        The internal board state representation
    _placement : Placement
        Handler for move validation and placement logic
    _score_calculator : ScoreCalculator
        Calculator for game scores and winner determination
    _game_manager : GameManager
        Manager for game flow and turn control
    """

    def __init__(self) -> None:
        """Initialize the Othello board with default starting configuration."""
        self._state = BoardState()
        self._placement = Placement(self._state)
        self._score_calculator = ScoreCalculator(self._state)
        self._game_manager = GameManager(self._placement, self._state)

    @classmethod
    def create_copy(cls, original: "Board") -> "Board":
        """Create an independent copy of the board for simulation purposes.

        This method creates a new Board instance with the same state as the original
        but completely independent memory allocation to prevent any interference
        between simulation and actual game state.

        Parameters
        ----------
        original : Board
            The board to copy

        Returns
        -------
        Board
            A new Board instance with identical state to the original

        Notes
        -----
        This method preserves the facade pattern by providing a public interface
        for creating board copies without exposing internal implementation details.
        """
        # Create new instance with default initialization
        copy_board = cls()

        # Copy board state using public interface
        original_board_data = original.board
        for row in range(copy_board.size):
            for col in range(copy_board.size):
                copy_board._state.set_cell_value(row, col, original_board_data[row][col])

        # Copy the current player state directly
        copy_board._game_manager.set_current_player(original.current_player)

        return copy_board

    @property
    def board(self) -> list[list[int]]:
        """Get a copy of the board state to prevent direct modification."""
        return self._state.board

    @property
    def size(self) -> int:
        """Get the board size."""
        return self._state.size

    @property
    def current_player(self) -> int:
        """Get the current player."""
        return self._game_manager.current_player

    @current_player.setter
    def current_player(self, player: int) -> None:
        """Set the current player."""
        self._game_manager.set_current_player(player)

    def create_snapshot(self) -> dict[str, Any]:
        """Create a snapshot of the current board state for restoration.

        Returns
        -------
        dict[str, Any]
            A dictionary containing all necessary state information
        """
        return {
            "board": self.board,
            "current_player": self.current_player,
        }

    def is_game_ended(self) -> bool:
        """Check if the game has ended.

        Returns
        -------
        bool
            True if neither player can make a valid move, False otherwise
        """
        return self._game_manager.is_game_ended()

    def is_valid_move(
        self,
        target_row: int,
        target_col: int,
        current_player: int | None = None,
    ) -> bool:
        """Check if placing a stone at the specified position is a valid move.

        Parameters
        ----------
        target_row : int
            The row index where the stone would be placed (0-based)
        target_col : int
            The column index where the stone would be placed (0-based)
        current_player : int, optional
            The player making the move. If None, uses the current active player

        Returns
        -------
        bool
            True if the move is valid and would capture at least one opponent stone,
            False otherwise
        """
        if self._game_manager.is_game_ended():
            return False

        if current_player is None:
            current_player = self._game_manager.current_player

        return self._placement.is_valid_placement(target_row, target_col, current_player)

    def get_score(self) -> tuple[int, int]:
        """Get the current score as (black_count, white_count).

        Returns
        -------
        tuple[int, int]
            A tuple containing (black_stones_count, white_stones_count)
        """
        return self._score_calculator.get_score()

    def get_valid_moves(self, player: int | None = None) -> list[tuple[int, int]]:
        """Get all valid moves for the specified player.

        Parameters
        ----------
        player : int, optional
            The player to get valid moves for. If None, uses the current active player

        Returns
        -------
        list[tuple[int, int]]
            A list of (row, col) tuples representing all valid move positions
            for the specified player
        """
        if player is None:
            player = self._game_manager.current_player
        return self._placement.get_valid_placements(player)

    def get_winner(self) -> int:
        """Get the winner of the game.

        Determines the winner based on who has more stones on the board.
        Should typically be called when the game has ended.

        Returns
        -------
        int
            The winner identifier:
            - 1 if black player has more stones
            - 2 if white player has more stones
            - 0 if the game is tied
        """
        return self._score_calculator.get_winner()

    def make_move(
        self,
        target_row: int,
        target_col: int,
        current_player: int | None = None,
    ) -> bool:
        """Place a stone at the specified position and flip captured stones.

        Parameters
        ----------
        target_row : int
            The row index where the stone will be placed (0-based)
        target_col : int
            The column index where the stone will be placed (0-based)
        current_player : int, optional
            The player making the move. If None, uses the current active player

        Returns
        -------
        bool
            True if the move was successfully executed, False if invalid

        Notes
        -----
        This method automatically flips all captured opponent stones and advances
        the turn to the next player. If the next player has no valid moves,
        the turn will pass back. If neither player can move, the game ends.
        """
        if self._game_manager.is_game_ended():
            return False

        return self._game_manager.place_and_flip(target_row, target_col, current_player)

    def restore_from_snapshot(self, snapshot: dict[str, Any]) -> None:
        """Restore the board state from a snapshot.

        Parameters
        ----------
        snapshot : dict[str, Any]
            The snapshot data to restore from
        """
        board_data = snapshot["board"]
        for row in range(self.size):
            for col in range(self.size):
                self._state.set_cell_value(row, col, board_data[row][col])
        self._game_manager.set_current_player(snapshot["current_player"])
