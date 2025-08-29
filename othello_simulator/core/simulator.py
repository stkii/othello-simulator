from typing import Any

from othello_simulator.core.board import Board


class GameSimulator:
    """Provides simulation functionality for Othello game scenarios.

    This class allows simulating moves and game states without affecting
    the original board state. It's particularly useful for UI previews,
    AI strategy evaluation, and what-if analysis.

    The simulator creates isolated copies of game states to ensure that
    simulations do not interfere with the actual game progression.
    """

    @staticmethod
    def simulate_move_preview(
        original_board: Board,
        target_row: int,
        target_col: int,
        player: int,
    ) -> tuple[bool, list[tuple[int, int]]]:
        """Simulate a move and return the stones that would be flipped.

        Creates a copy of the board state and simulates the move to determine
        which stones would be flipped without affecting the original board.
        This is useful for UI previews and move validation.

        Parameters
        ----------
        original_board : Board
            The original board state to simulate from
        target_row : int
            The row where the stone would be placed (0-based)
        target_col : int
            The column where the stone would be placed (0-based)
        player : int
            The player making the move (1 for black, 2 for white)

        Returns
        -------
        tuple[bool, list[tuple[int, int]]]
            A tuple containing:
            - success: True if the move is valid and was simulated successfully
            - flipped_stones: List of (row, col) tuples representing stones
              that would be flipped by this move

        Notes
        -----
        This method does not modify the original board state. It creates
        an isolated simulation environment for safe move evaluation.
        """
        # Validate move before simulation
        if not original_board.is_valid_move(target_row, target_col, player):
            return False, []

        # Create a simulation board using the facade's copy method
        simulation_board = Board.create_copy(original_board)

        # Record the state before the move
        original_state = simulation_board.board  # This returns a copy

        # Execute the move in the simulation
        move_success = simulation_board.make_move(target_row, target_col, player)
        if not move_success:
            return False, []

        # Identify which stones were flipped
        flipped_stones: list[tuple[int, int]] = []
        new_state = simulation_board.board  # This returns a copy

        for row in range(simulation_board.size):
            for col in range(simulation_board.size):
                # Skip the placed stone itself
                if (row, col) == (target_row, target_col):
                    continue
                # Check if this stone was flipped
                if original_state[row][col] != new_state[row][col]:
                    flipped_stones.append((row, col))

        return True, flipped_stones

    @staticmethod
    def simulate_game_state_after_move(
        original_board: Board,
        target_row: int,
        target_col: int,
        player: int,
    ) -> Board | None:
        """Simulate a move and return the resulting board state.

        Creates a complete simulation of the board state after executing
        the specified move. Useful for AI strategy evaluation and
        game analysis scenarios.

        Parameters
        ----------
        original_board : Board
            The original board state to simulate from
        target_row : int
            The row where the stone would be placed (0-based)
        target_col : int
            The column where the stone would be placed (0-based)
        player : int
            The player making the move (1 for black, 2 for white)

        Returns
        -------
        Optional[Board]
            The board state after the move is executed, or None if the move
            is invalid. The returned board is independent of the original.

        Notes
        -----
        This method creates a completely independent board instance,
        allowing for complex simulation scenarios without affecting
        the original game state.
        """
        # Validate move before simulation
        if not original_board.is_valid_move(target_row, target_col, player):
            return None

        # Create a simulation board using the facade's copy method
        simulation_board = Board.create_copy(original_board)

        # Execute the move in the simulation
        move_success = simulation_board.make_move(target_row, target_col, player)
        if not move_success:
            return None

        return simulation_board

    @staticmethod
    def create_temporary_simulation(original_board: Board) -> tuple[Board, dict[str, Any]]:
        """Create a temporary simulation environment that can be easily restored.

        This method creates a board copy and a snapshot of the original state
        for scenarios where you might want to run multiple simulations and
        restore the original state quickly.

        Parameters
        ----------
        original_board : Board
            The original board state to simulate from

        Returns
        -------
        tuple[Board, dict[str, Any]]
            A tuple containing:
            - simulation_board: An independent copy for simulation
            - snapshot: Original state data for restoration

        Notes
        -----
        This is useful for complex simulation scenarios where you need
        to try multiple moves and restore the original state efficiently.
        """
        simulation_board = Board.create_copy(original_board)
        snapshot = original_board.create_snapshot()
        return simulation_board, snapshot
