from othello_simulator.core.placement import Placement
from othello_simulator.core.state import BLACK_PLAYER, GAME_ENDED_MARKER, BoardState
from othello_simulator.core.utils import get_opponent_player


class GameManager:
    """Handles game execution and flow control.

    Attributes
    ----------
    _current_player : int
        The currently active player (1 for black, 2 for white, 0 for game ended)
    _placement : Placement
        Reference to the placement validation handler
    _state : BoardState
        Reference to the board state object
    """

    def __init__(
        self,
        placement: Placement,
        state: BoardState,
    ) -> None:
        """Initialize the game manager."""
        # The black player goes first
        self._current_player: int = BLACK_PLAYER
        self._placement = placement
        self._state = state

    def _flip_stones_in_direction(  # noqa: PLR0913
        self,
        start_row: int,
        start_col: int,
        row_direction: int,
        col_direction: int,
        current_player: int,
        opponent_player: int,
    ) -> None:
        """Flip all opponent stones in the specified direction.

        Starting from the placed stone, moves in the given direction
        and flips all consecutive opponent stones until reaching
        a stone of the current player.

        Parameters
        ----------
        start_row : int
            The row of the newly placed stone
        start_col : int
            The column of the newly placed stone
        row_direction : int
            The row direction to move (-1, 0, or 1)
        col_direction : int
            The column direction to move (-1, 0, or 1)
        current_player : int
            The player who placed the stone
        opponent_player : int
            The opponent player whose stones will be flipped
        """
        check_row: int = start_row + row_direction
        check_col: int = start_col + col_direction

        # Flip opponent stones until reaching current player's stone
        while self._state.is_within_board(check_row, check_col):
            cell_value: int = self._state.get_cell_value(check_row, check_col)
            if cell_value == opponent_player:
                self._state.set_cell_value(check_row, check_col, current_player)
                check_row += row_direction
                check_col += col_direction
            elif cell_value == current_player:
                # Reached current player's stone, stop flipping
                break
            else:
                # Empty cell (should not occur if can_flip_in_direction returned True)
                break

    def _switch_to_next_player(self, previous_player: int) -> None:
        """Switch to the next player and handle pass/game end logic.

        Attempts to switch to the opponent. If the opponent has no valid moves,
        the turn passes back to the previous player. If neither player can move,
        the game ends.

        Parameters
        ----------
        previous_player : int
            The player who just completed their turn
        """
        next_player: int = get_opponent_player(previous_player)
        self._current_player = next_player

        if not self._placement.get_valid_placements(next_player):
            self._current_player = previous_player
            if not self._placement.get_valid_placements(previous_player):
                self._current_player = GAME_ENDED_MARKER

    @property
    def current_player(self) -> int:
        """Get the current player."""
        return self._current_player

    def is_game_ended(self) -> bool:
        """Check if the game has ended.

        Returns
        -------
        bool
            True if neither player can make a valid move, False otherwise
        """
        return self._current_player == GAME_ENDED_MARKER

    def set_current_player(self, player: int) -> None:
        """Set the current player.

        Parameters
        ----------
        player : int
            The player to set as current (1 for black, 2 for white, 0 for game ended)
        """
        self._current_player = player

    def place_and_flip(
        self,
        target_row: int,
        target_col: int,
        current_player: int | None = None,
    ) -> bool:
        """Place a stone at the specified position and flip captured stones.

        Validates the move, places the stone, flips all captured opponent
        stones in all valid directions, and advances to the next player.

        Parameters
        ----------
        target_row : int
            The row where the stone will be placed (0-based)
        target_col : int
            The column where the stone will be placed (0-based)
        current_player : int, optional
            The player making the move. If None, uses the current active player

        Returns
        -------
        bool
            True if the move was successfully executed, False if invalid

        Notes
        -----
        This method handles the complete move execution including:
        - Move validation
        - Stone placement
        - Stone flipping in all valid directions
        - Turn advancement with pass/game end handling
        """
        if current_player is None:
            current_player = self._current_player

        if not self._placement.is_valid_placement(target_row, target_col, current_player):
            return False

        # Place the stone
        self._state.set_cell_value(target_row, target_col, current_player)
        opponent_player: int = get_opponent_player(current_player)

        # Flip stones in all valid directions
        directions: list[tuple[int, int]] = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for row_direction, col_direction in directions:
            if self._placement.can_flip_in_direction(
                target_row,
                target_col,
                row_direction,
                col_direction,
                current_player,
                opponent_player,
            ):
                self._flip_stones_in_direction(
                    target_row,
                    target_col,
                    row_direction,
                    col_direction,
                    current_player,
                    opponent_player,
                )

        # Switch to next player
        self._switch_to_next_player(current_player)

        return True
