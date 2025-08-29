class GameState {
  constructor() {
    this.state = null;
    this.isGameEnd = false;
    this.gameMode = 'cpu_vs_cpu'; // 'cpu_vs_cpu' | 'player_vs_cpu'
    this.playerNumber = 1;
    this.waitingForPlayer = false;
    this.autoInterval = null;
  }

  setState(newState) {
    this.state = newState;
    this.isGameEnd = newState?.is_game_over || false;
  }

  // Get game state
  getState() {
    return this.state;
  }

  // Set game end state
  setGameEnd(isEnd) {
    this.isGameEnd = isEnd;
  }

  // Check if game is finished
  isGameFinished() {
    return this.isGameEnd;
  }

  /**
   * プレイヤー vs CPUモードを設定
   */
  setPlayerVsCpuMode(playerNumber = 1) {
    this.gameMode = 'player_vs_cpu';
    this.playerNumber = playerNumber;
  }

  /**
   * CPU vs CPUモードを設定
   */
  setCpuVsCpuMode() {
    this.gameMode = 'cpu_vs_cpu';
    this.playerNumber = 1;
  }

  /**
   * プレイヤー vs CPUモードかどうか判定
   */
  isPlayerVsCpuMode() {
    return this.gameMode === 'player_vs_cpu';
  }

  // Get player number
  getPlayerNumber() {
    return this.playerNumber;
  }

  // Set waiting for player flag
  setWaitingForPlayer(waiting) {
    this.waitingForPlayer = waiting;
  }

  // Check if waiting for player
  isWaitingForPlayer() {
    return this.waitingForPlayer;
  }

  /**
   * 有効な手の位置かどうか判定
   */
  isValidPosition(row, col) {
    if (!this.state?.valid_moves) return false;
    return this.state.valid_moves.some(([r, c]) => r === row && c === col);
  }

  // Set auto interval
  setAutoInterval(interval) {
    this.autoInterval = interval;
  }

  // Get auto interval
  getAutoInterval() {
    return this.autoInterval;
  }

  // Clear auto interval
  clearAutoInterval() {
    if (this.autoInterval) {
      clearInterval(this.autoInterval);
      this.autoInterval = null;
    }
  }

  /**
   * 現在のプレイヤーが人間かどうか判定
   */
  isCurrentPlayerHuman() {
    return this.gameMode === 'player_vs_cpu' && this.state?.current_player === this.playerNumber;
  }

  /**
   * ゲーム状態をリセット
   */
  reset() {
    this.state = null;
    this.isGameEnd = false;
    this.waitingForPlayer = false;
    this.clearAutoInterval();
  }
}

export default GameState;
