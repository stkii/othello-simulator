from __future__ import annotations

from othello_simulator.core.board import Board


class StrategyBase:
    """Base class for Othello strategies."""

    def __init__(self, player: int) -> None:
        self.player = player  # 1: black, 2: white

    def choose_move(self, board: Board) -> tuple[int, int] | None:
        """Choose a move based on the board state."""
        # Subclasses must implement this method
        msg = "Subclass must implement this method"
        raise NotImplementedError(msg)


class MyStrategy(StrategyBase):
    """Your original strategy class."""

    def choose_move(self, board: Board) -> tuple[int, int] | None:
        """
        Choose a move based on the board state.

        Parameters
        ----------
        board: Board
            現在の盤面情報

        Returns
        -------
        tuple[int, int] | None:
            石を置く場所の座標 (row, col)
            置ける場所がない場合は None

        Notes
        -----
        利用可能なBoardクラスのメソッド:
            board.board: 盤面の状態を取得
            board.size: 盤面のサイズを取得
            board.current_player: 現在のプレイヤーを取得
                Returns: 1(黒), 2(白), 0(ゲーム終了)
            board.get_valid_moves(player): 指定プレイヤーの合法手を取得
                Returns: [(row, col), ...] のリスト
            board.is_valid_move(row, col, player): 指定位置が合法手かチェック
                Returns: True/False
            board.get_score(): 現在のスコアを取得
                Returns: (黒の石数, 白の石数)
            board.get_winner(): 勝者を取得
                Returns: 1(黒), 2(白), 0(引き分け)
            board.is_game_ended(): ゲームが終了したかチェック
                Returns: True/False
            Board.create_copy(board): 盤面のコピーを作成 (元の盤面に影響しない)
                Returns: 新しいBoardオブジェクト

        利用可能なGameSimulatorクラスのメソッド (クラスのインポートが必要):
            GameSimulator.simulate_move_preview(board, row, col, player):
                手を置いた場合にひっくり返される石を事前計算
                Returns: (成功判定, ひっくり返される石の位置リスト)
            GameSimulator.simulate_game_state_after_move(board, row, col, player):
                手を置いた後の盤面状態を取得 (元の盤面に影響しない)
                Returns: 新しいBoardオブジェクト (無効な手の場合はNone)
            GameSimulator.create_temporary_simulation(board):
                一時的なシミュレーション環境を作成
                Returns: (シミュレーション用Board, 元の状態のスナップショット)
        """
        # First, simulate the board by creating a copy for analysis
        board_copy = Board.create_copy(board)

        # Get valid moves from the simulated board
        valid_moves: list[tuple[int, int]] = board_copy.get_valid_moves(self.player)
        if not valid_moves:
            return None

        # ===========================================
        # ここから下を編集してください
        # ===========================================

        position_values = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100],
        ]

        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for move in valid_moves:
            if move in corners:
                return move

        dangerous_positions = [
            (0, 1),
            (1, 0),
            (1, 1),  # 左上角の隣接
            (0, 6),
            (1, 6),
            (1, 7),  # 右上角の隣接
            (6, 0),
            (6, 1),
            (7, 1),  # 左下角の隣接
            (6, 6),
            (6, 7),
            (7, 6),
        ]  # 右下角の隣接

        safe_moves = []
        for move in valid_moves:
            if move not in dangerous_positions:
                safe_moves.append(move)  # noqa: PERF401

        moves_to_consider = safe_moves if safe_moves else valid_moves

        best_move = None
        best_score = -float("inf")

        for move in moves_to_consider:
            row, col = move

            flipped_count = self._count_flipped_stones(board, row, col)

            position_score = position_values[row][col]
            flip_score = flipped_count * 2

            if (row in {0, 7} or col in {0, 7}) and (row, col) not in corners:
                edge_penalty = -5
            else:
                edge_penalty = 0

            total_score = position_score + flip_score + edge_penalty

            if total_score > best_score:
                best_score = total_score
                best_move = move

        return best_move

    def _count_flipped_stones(self, board: Board, row: int, col: int) -> int:
        """
        指定した位置に石を置いた場合にひっくり返せる石の数を計算

        引数:
            board: Board オブジェクト
            row, col: 石を置く位置

        戻り値:
            int: ひっくり返せる石の数
        """

        # 盤面をコピーして試行
        board_copy = Board.create_copy(board)
        board_copy.current_player = self.player

        # 石を置く前の自分の石の数
        initial_count = sum(row.count(self.player) for row in board_copy.board)

        # 実際に石を置いてみる
        board_copy.make_move(row, col, self.player)

        # 石を置いた後の自分の石の数
        new_count = sum(row.count(self.player) for row in board_copy.board)

        return new_count - initial_count - 1
