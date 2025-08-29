# Constants
BOARD_SIZE: int = 8
EMPTY_CELL: int = 0
BLACK_PLAYER: int = 1
WHITE_PLAYER: int = 2
GAME_ENDED_MARKER: int = 0


class BoardState:
    """Represents the state of an Othello board.

    Attributes
    ----------
    _board : list[list[int]]
        A 2D list representing the board state, where:
        - 0 represents an empty cell
        - 1 represents a black stone
        - 2 represents a white stone
    _size : int
        The size (width and height) of the square board.
    """

    def __init__(self) -> None:
        """Initialize the board state with the standard Othello starting position."""
        self._size: int = BOARD_SIZE
        self._board: list[list[int]] = self._initialize_board()

    def _initialize_board(self) -> list[list[int]]:
        """Create the initial board state.

        Sets up a standard Othello starting position with four stones
        placed in the center of the board in a diagonal pattern.

        Returns
        -------
        list[list[int]]
            A 2D list representing the initial board configuration.
        """
        board: list[list[int]] = [
            [EMPTY_CELL for _ in range(self._size)] for _ in range(self._size)
        ]

        # Initial stone placement
        center: int = self._size // 2
        board[center - 1][center - 1] = WHITE_PLAYER
        board[center - 1][center] = BLACK_PLAYER
        board[center][center - 1] = BLACK_PLAYER
        board[center][center] = WHITE_PLAYER

        return board

    @property
    def board(self) -> list[list[int]]:
        """Get a copy of the board state.

        Returns a defensive copy to prevent external modification
        of the internal board state.

        Returns
        -------
        list[list[int]]
            A deep copy in effect (sufficient for immutable elements)
            where each cell contains:
            - 0 represents an empty cell
            - 1 represents a black stone
            - 2 represents a white stone
        """
        # Defensive copy: row lists are cloned, and ints are immutable,
        # so this is effectively a deep copy and sufficient to protect internal state.
        return [row[:] for row in self._board]

    @property
    def size(self) -> int:
        """Get the board size."""
        return self._size

    def count_stones(self, player: int) -> int:
        """Count the number of stones for a specific player.

        Parameters
        ----------
        player : int
            The player to count stones for (1 for black, 2 for white).

        Returns
        -------
        int
            The total number of stones the player has on the board.
        """
        return sum(row.count(player) for row in self._board)

    def get_cell_value(self, row: int, col: int) -> int:
        """Get the value of a specific cell.

        Parameters
        ----------
        row : int
            The row index (0-based)
        col : int
            The column index (0-based)

        Returns
        -------
        int
            The value at the specified position:
            - 0 represents an empty cell
            - 1 represents a black stone
            - 2 represents a white stone

        Notes
        -----
        No bounds checking is performed.
        Please use is_within_board() beforehand to ensure the coordinates are valid.
        """
        return self._board[row][col]

    def is_within_board(self, row: int, col: int) -> bool:
        """Check if the given position is within board boundaries.

        Parameters
        ----------
        row : int
            The row index (0-based) to check
        col : int
            The column index (0-based) to check

        Returns
        -------
        bool
            True if the position is within the board boundaries,
            False otherwise.
        """
        return 0 <= row < self._size and 0 <= col < self._size

    def set_cell_value(self, row: int, col: int, value: int) -> None:
        """Set the value of a specific cell.

        Parameters
        ----------
        row : int
            The row index (0-based)
        col : int
            The column index (0-based)
        value : int
            The value to set:
            - 0 represents an empty cell
            - 1 represents a black stone
            - 2 represents a white stone

        Notes
        -----
        No bounds checking is performed.
        Please use is_within_board() beforehand to ensure the coordinates are valid.
        """
        self._board[row][col] = value
