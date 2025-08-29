from othello_simulator.core.state import EMPTY_CELL, BoardState
from othello_simulator.core.utils import get_opponent_player


class Placement:
    """Handles validation logic for Othello piece placements.

    Attributes
    ----------
    _state : BoardState
        Reference to the board state for position checking.
    """

    def __init__(self, state: BoardState) -> None:
        """Initialize the placement validator."""
        self._state = state

    def can_flip_in_direction(  # noqa: PLR0913
        self,
        start_row: int,
        start_col: int,
        row_direction: int,
        col_direction: int,
        current_player: int,
        opponent_player: int,
    ) -> bool:
        """Check if opponent stones can be flipped in the specified direction.

        Starting from the target position, checks if there is a line of
        opponent stones followed by a current player stone in the given
        direction, which would allow capturing.

        Parameters
        ----------
        start_row : int
            The row of the potential placement
        start_col : int
            The column of the potential placement
        row_direction : int
            The row direction to check (-1, 0, or 1)
        col_direction : int
            The column direction to check (-1, 0, or 1)
        current_player : int
            The player making the placement
        opponent_player : int
            The opponent player whose stones might be captured

        Returns
        -------
        bool
            True if stones can be flipped in this direction, False otherwise

        Notes
        -----
        For a valid capture, the pattern must be:
            [empty cell] → [opponent stone]+ → [own stone]
        where + means one or more opponent stones.
        """
        check_row: int = start_row + row_direction
        check_col: int = start_col + col_direction

        # Check if the adjacent cell contains an opponent stone
        if not self._state.is_within_board(check_row, check_col):
            return False
        if self._state.get_cell_value(check_row, check_col) != opponent_player:
            return False

        # Look for a current player stone that would close the line
        check_row += row_direction
        check_col += col_direction

        while self._state.is_within_board(check_row, check_col):
            cell_value: int = self._state.get_cell_value(check_row, check_col)
            if cell_value == EMPTY_CELL:
                return False
            if cell_value == current_player:  # Found closing stone
                return True
            # Continue through opponent stones
            check_row += row_direction
            check_col += col_direction

        return False

    def get_valid_placements(self, player: int) -> list[tuple[int, int]]:
        """Get all valid placements for the specified player.

        Parameters
        ----------
        player : int
            The player to find valid moves for

        Returns
        -------
        list[tuple[int, int]]
            A list of (row, col) tuples representing all valid placement
            positions for the player. Empty list if no valid moves exist.
        """
        return [
            (i, j)
            for i in range(self._state.size)
            for j in range(self._state.size)
            if self.is_valid_placement(i, j, player)
        ]

    def is_valid_placement(
        self,
        target_row: int,
        target_col: int,
        current_player: int,
    ) -> bool:
        """
        Check if placing a piece at the specified position is a valid placement.

        A placement is valid if:
        1. The target position is within board boundaries
        2. The target position is empty
        3. The placement would capture at least one opponent stone
           in at least one direction

        Parameters
        ----------
        target_row : int
            The row where the piece would be placed (0-based)
        target_col : int
            The column where the piece would be placed (0-based)
        current_player : int
            The player making the placement

        Returns
        -------
        bool
            True if the placement is valid according to Othello rules,
            False otherwise
        """
        if not self._state.is_within_board(target_row, target_col):
            return False

        # Placement is invalid if target cell is not empty
        if self._state.get_cell_value(target_row, target_col) != EMPTY_CELL:
            return False

        opponent_player: int = get_opponent_player(current_player)

        # Check all 8 directions
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
            if self.can_flip_in_direction(
                target_row,
                target_col,
                row_direction,
                col_direction,
                current_player,
                opponent_player,
            ):
                return True

        return False
