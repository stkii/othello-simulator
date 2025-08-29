from othello_simulator.core.state import BLACK_PLAYER, EMPTY_CELL, WHITE_PLAYER, BoardState


class ScoreCalculator:
    """Handles score calculation and winner determination.

    Attributes
    ----------
    _state : BoardState
        Reference to the board state for stone counting.
    """

    def __init__(self, state: BoardState) -> None:
        """Initialize the score calculator."""
        self._state = state

    def get_score(self) -> tuple[int, int]:
        """Get the current score of each player.

        Returns
        -------
        tuple[int, int]
            A tuple containing (black_stones_count, white_stones_count)
            representing the current score for each player.
        """
        black_stones_count: int = self._state.count_stones(BLACK_PLAYER)
        white_stones_count: int = self._state.count_stones(WHITE_PLAYER)
        return (black_stones_count, white_stones_count)

    def get_winner(self) -> int:
        """Get the winner of the game.

        Returns
        -------
        int
            The winner identifier:
            - 1 (BLACK_PLAYER) if black has more stones
            - 2 (WHITE_PLAYER) if white has more stones
            - 0 (EMPTY_CELL) if the game is a tie
        """
        black_stones_count, white_stones_count = self.get_score()

        if black_stones_count > white_stones_count:
            return BLACK_PLAYER
        # Using `elif` here improves clarity by making mutual exclusivity explicit.
        elif white_stones_count > black_stones_count:  # noqa: RET505
            return WHITE_PLAYER
        else:
            return EMPTY_CELL  # Tie game
