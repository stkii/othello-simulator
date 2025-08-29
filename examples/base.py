from __future__ import annotations

from flask import current_app

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
            current_app.logger.debug("打てる場所がありません。パスします。")
            return None

        # ===========================================
        # ここから下を編集してください
        # ===========================================

        # 最終的な戻り値は石を置く場所の座標です
        # テンプレートなので最初の有効手を返す
        return valid_moves[0] if valid_moves else None
