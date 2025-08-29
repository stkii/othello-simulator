class MoveValidator {
  constructor(gameState) {
    this.gameState = gameState;
  }

  /**
   * 手の妥当性を検証
   */
  isValidMove(row, col) {
    if (!this.#isValidCoordinates(row, col)) return false;
    if (this.gameState.isGameEnd) return false;
    return this.gameState.isValidPosition(row, col);
  }

  /**
   * 座標の基本検証
   */
  #isValidCoordinates(row, col) {
    return row >= 0 && row < 8 && col >= 0 && col < 8;
  }

  /**
   * 有効な手のリストを取得
   */
  getValidMoves() {
    return this.gameState.state?.valid_moves || [];
  }

  /**
   * 指定位置が盤面上の有効な座標かどうか判定
   */
  isWithinBoard(row, col) {
    return this.#isValidCoordinates(row, col);
  }

  /**
   * ゲーム終了状態での手の検証
   */
  canMakeMove() {
    if (this.gameState.isGameEnd) return false;
    if (!this.gameState.state) return false;
    return this.getValidMoves().length > 0;
  }

  /**
   * プレイヤーが手を打てる状態かどうか判定
   */
  isPlayerTurnValid() {
    return this.canMakeMove() && !this.gameState.isGameEnd;
  }
}

export default MoveValidator;
