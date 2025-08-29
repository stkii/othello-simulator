from typing import Any

from othello_simulator.core.board import Board
from othello_simulator.core.simulator import GameSimulator

from .state import GameState
from .storage import JSONStorage


class GameController:
    """Unified game controller class."""

    def __init__(self, storage_path: str) -> None:
        """Initialize GameController.

        Parameters
        ----------
        storage_path : str
            File path for game state storage
        """
        self.board: Board | None = None
        self.game_state = GameState()
        self.storage = JSONStorage(storage_path)

    def start_game(  # noqa: PLR0913
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
        """Start new game.

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
        # Create new board
        self.board = Board()

        # Set up game state
        self.game_state.setup_game(
            strategy1=strategy1,
            strategy2=strategy2,
            name1=name1,
            name2=name2,
            player_vs_cpu=player_vs_cpu,
            player=player,
            strategy1_file=strategy1_file,
            strategy2_file=strategy2_file,
        )

        # Save state
        self.save_state()

    def save_state(self) -> bool:
        """Save current game state.

        Returns
        -------
        bool
            True if save successful
        """
        try:
            # Create game state data
            state_data = self.game_state.to_dict()

            # Add board state
            if self.board:
                state_data.update(
                    {
                        "board_state": [row[:] for row in self.board.board],  # Board copy
                        "current_player": self.board.current_player,
                    },
                )

            # Execute save
            return self.storage.save(state_data)

        except Exception:
            return False

    def load_state(self) -> bool:
        """Restore saved game state.

        Returns
        -------
        bool
            True if restoration successful
        """
        try:
            # Load state data
            state_data = self.storage.load()
            if not state_data:
                return False

            # Restore game state
            self.game_state.from_dict(state_data)

            # Restore board state
            if state_data.get("board_state"):
                self.board = Board()
                snapshot = {
                    "board": state_data["board_state"],
                    "current_player": state_data.get("current_player", 1),
                }
                self.board.restore_from_snapshot(snapshot)

            return True

        except Exception:
            return False

    def make_move_with_tracking(self, row: int, col: int, player: int) -> bool:
        """Execute move and update highlight information.

        Parameters
        ----------
        row : int
            Row coordinate
        col : int
            Column coordinate
        player : int
            Player number

        Returns
        -------
        bool
            True if move execution successful
        """
        if not self.board or not self.board.is_valid_move(row, col, player):
            return False

        # Simulate move result (for highlighting)
        success, flipped_stones_tuples = GameSimulator.simulate_move_preview(
            self.board,
            row,
            col,
            player,
        )

        if not success:
            return False

        # Update highlight information
        self.game_state.update_highlights([row, col], flipped_stones_tuples)

        # Execute actual move
        return self.board.make_move(row, col, player)

    def get_current_state(self) -> dict[str, Any] | None:
        """Get current game state.

        Returns
        -------
        dict[str, Any] | None
            Game state dictionary, None if board doesn't exist
        """
        if not self.board:
            return None

        # Calculate scores
        black_score, white_score = self.board.get_score()

        # Get valid moves list
        valid_moves = []
        if self.board.current_player > 0:
            valid_moves_tuples = self.board.get_valid_moves(self.board.current_player)
            valid_moves = [[row, col] for row, col in valid_moves_tuples]

        # Check game end
        is_game_over = self.board.is_game_ended()
        winner = None
        if is_game_over:
            winner = self.board.get_winner()

        # Build state dictionary
        return {
            "board": [row[:] for row in self.board.board],  # Board copy
            "current_player": self.board.current_player,
            "black_score": black_score,
            "white_score": white_score,
            "valid_moves": valid_moves,
            "is_game_over": is_game_over,
            "winner": winner,
            "black_player_name": self.game_state.black_player_name,
            "white_player_name": self.game_state.white_player_name,
            "move_count": self.game_state.move_count,
            **self.game_state.get_highlight_data(),
            **self.game_state.get_player_mode_data(),
        }

    def make_next_move(  # noqa: PLR0911
        self,
        player_move: list[int] | None = None,
    ) -> dict[str, Any] | None:
        """Execute next move.

        Parameters
        ----------
        player_move : list[int] | None
            Player move [row, col], None for CPU move

        Returns
        -------
        dict[str, Any] | None
            Game state after move execution, None if unable to execute
        """
        if not self.board or self.board.is_game_ended():
            return None

        current_player = self.board.current_player

        # Check and process player turn
        if self.game_state.is_player_turn(current_player):
            if player_move is None:
                # Waiting for player input
                self.game_state.set_waiting_for_player(waiting=True)
                self.save_state()
                return self.get_current_state()

            # Execute player move
            row, col = player_move
            if self.make_move_with_tracking(row, col, current_player):
                self.game_state.move_count += 1
                self.game_state.set_waiting_for_player(waiting=False)
                self.save_state()
                return self.get_current_state()
            return None

        # Execute CPU move
        strategy = self.game_state.get_current_strategy(current_player)

        try:
            # Check if strategy is available
            if strategy is None:
                # Strategy not loaded, cannot proceed with CPU move
                return None

            # Check valid moves
            valid_moves_tuples = self.board.get_valid_moves(current_player)
            valid_moves = [[row, col] for row, col in valid_moves_tuples]

            if not valid_moves:
                # Pass processing (core/GameManager handles automatically)
                self.game_state.clear_highlights()
                self.save_state()
                return self.get_current_state()

            # Get move from strategy
            move = strategy.choose_move(self.board)

            if move and len(move) >= 2:  # noqa: PLR2004
                row, col = move[0], move[1]

                if self.make_move_with_tracking(row, col, current_player):
                    self.game_state.move_count += 1
                    self.save_state()
                    return self.get_current_state()
                return None
            # Strategy chose to pass
            self.game_state.clear_highlights()
            self.save_state()
            return self.get_current_state()

        except Exception:
            return None

    def reset_game(self) -> None:
        """Reset game."""
        self.board = None
        self.game_state.reset()
        self.storage.clear()

    def set_strategies(
        self,
        strategy1: Any,  # noqa: ANN401
        strategy2: Any,  # noqa: ANN401
    ) -> None:
        """Set strategy objects (used during state restoration).

        Parameters
        ----------
        strategy1 : Any
            Player 1 strategy
        strategy2 : Any
            Player 2 strategy
        """
        self.game_state.strategy1 = strategy1
        self.game_state.strategy2 = strategy2
