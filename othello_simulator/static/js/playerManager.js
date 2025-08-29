class PlayerManager {
  /**
   * Constructors
   * @param {import('./gameState.js').default} gameState - Game state object
   * @param {import('./uiManager.js').default} uiControls - UI controls object
   */
  constructor(gameState, uiManager) {
    this.gameState = gameState;
    this.uiManager = uiManager;
    this.waitingForInput = false;
    this.inputCallback = null;
  }

  /**
   * プレイヤー入力待ち開始
   */
  startWaitingForInput(callback) {
    this.waitingForInput = true;
    this.inputCallback = callback;
    this.uiManager.showPlayerPrompt(true);
  }

  /**
   * 入力待ち終了
   */
  #stopWaitingForInput() {
    this.waitingForInput = false;
    this.inputCallback = null;
    this.uiManager.showPlayerPrompt(false);
  }

  /**
   * プレイヤーの手を処理
   */
  handlePlayerMove(row, col) {
    if (!this.waitingForInput || !this.inputCallback) return false;

    this.uiManager.addMoveLog(`👤 プレイヤーが (${row}, ${col}) に配置`);
    this.inputCallback([row, col]);
    this.#stopWaitingForInput();
    return true;
  }

  /**
   * プレイヤーターン開始
   */
  onPlayerTurn(callback) {
    if (!this.gameState.isCurrentPlayerHuman()) {
      return;
    }
    this.startWaitingForInput(callback);
  }

  /**
   * プレイヤーターン終了
   */
  onPlayerTurnEnd() {
    this.#stopWaitingForInput();
  }

  /**
   * 入力待ちかどうか判定
   */
  isWaiting() {
    return this.waitingForInput;
  }

  /**
   * プレイヤーの手を実行
   */
  makeMove(row, col) {
    if (!this.waitingForInput) {
      return false;
    }

    if (!this.gameState.isValidMove(row, col)) {
      return false;
    }

    return this.handlePlayerMove(row, col);
  }

  /**
   * ボードクリックハンドラーを作成
   */
  createBoardClickHandler() {
    return (row, col) => {
      if (this.waitingForInput && this.gameState.isCurrentPlayerHuman()) {
        this.makeMove(row, col);
      }
    };
  }

  /**
   * プレイヤーターンをチェックし適切に処理
   */
  checkAndHandlePlayerTurn(callback) {
    if (!this.gameState.isPlayerVsCpuMode() || this.gameState.isGameFinished()) {
      return false;
    }

    if (this.gameState.isCurrentPlayerHuman()) {
      this.onPlayerTurn(callback);
      return true;
    } else {
      this.onPlayerTurnEnd();
      return false;
    }
  }
}

export default PlayerManager;
