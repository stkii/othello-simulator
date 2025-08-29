import GameState from './gameState.js';
import MoveValidator from './moveValidator.js';
import UiManager from './uiManager.js';
import PlayerManager from './playerManager.js';
import BoardRenderer from './boardRenderer.js';
import ApiClient from './apiClient.js';
import FileManager from './fileManager.js';

class GameOrchestrator {
  constructor() {
    this.gameState = new GameState();
    this.moveValidator = new MoveValidator(this.gameState);
    this.uiManager = new UiManager();
    this.playerManager = new PlayerManager(this.gameState, this.uiManager);
    this.boardRenderer = new BoardRenderer();
    this.apiClient = new ApiClient();
    this.fileManager = new FileManager(this.apiClient, this.uiManager);
  }

  /**
   * アプリケーション初期化
   */
  initialize() {
    this.#setupEventHandlers();
    this.boardRenderer.setBoardElement(document.getElementById('board'));
    this.uiManager.init();
  }

  /**
   * イベントハンドラーの設定
   */
  #setupEventHandlers() {
    // ボタンイベントの設定
    this.#setupButtonEvents();
  }

  /**
   * ボタンイベントの設定
   */
  #setupButtonEvents() {
    // CPU vs CPU戦略アップロードボタン
    const loadStrategiesBtn = document.getElementById('loadStrategiesBtn');
    if (loadStrategiesBtn) {
      loadStrategiesBtn.addEventListener('click', () => this.uploadStrategies());
    }

    // 次の手ボタン
    const nextMoveBtn = document.getElementById('nextMoveBtn');
    if (nextMoveBtn) {
      nextMoveBtn.addEventListener('click', () => this.nextMove());
    }

    // 自動再生ボタン
    const autoPlayBtn = document.getElementById('autoPlayBtn');
    if (autoPlayBtn) {
      autoPlayBtn.addEventListener('click', () => this.toggleAutoPlay());
    }

    // ゲームリセットボタン
    const resetGameBtn = document.querySelector('.reset-button');
    if (resetGameBtn) {
      resetGameBtn.addEventListener('click', () => this.resetGame());
    }

    // プレイヤーvsCPUボタン
    const loadPlayerVsCpuBtn = document.getElementById('loadPlayerVsCpuBtn');
    if (loadPlayerVsCpuBtn) {
      loadPlayerVsCpuBtn.addEventListener('click', () => this.startPlayerVsCpu());
    }
  }

  /**
   * CPU vs CPU戦略ファイルアップロード
   */
  async uploadStrategies() {
    const result = await this.fileManager.uploadCpuStrategies();
    if (result?.success) {
      this.gameState.setState(result.state);
      this.gameState.setCpuVsCpuMode();
      this.#startGameDisplay();
    }
  }

  /**
   * プレイヤーvsCPU戦開始
   */
  async startPlayerVsCpu() {
    const result = await this.fileManager.uploadPlayerVsCpu();
    if (result?.success) {
      this.gameState.setState(result.state);
      // プレイヤーの色に応じてモードを設定
      const playerNumber = result.player_color === 'black' ? 1 : 2;
      this.gameState.setPlayerVsCpuMode(playerNumber);
      this.#startGameDisplay();
      this.#handlePlayerVsCpuTurn();
    }
  }

  /**
   * 次の手を実行
   */
  async nextMove(playerMove = null) {
    if (this.gameState.isGameEnd) return;

    try {
      this.uiManager.showStatus('loading', '手を実行中...');
      const result = await this.apiClient.nextMove(playerMove);

      if (result.success) {
        this.gameState.setState(result.state);
        this.#updateDisplay();

        if (result.state.is_game_over) {
          this.#handleGameEnd();
        } else if (this.gameState.gameMode === 'player_vs_cpu') {
          this.#handlePlayerVsCpuTurn();
        }
      } else {
        this.uiManager.showStatus('error', result.message || '手の実行に失敗しました');
      }
    } catch (error) {
      this.uiManager.showStatus('error', `手の実行エラー: ${error.message}`);
    }
  }

  /**
   * プレイヤーの手を処理
   */
  makePlayerMove(row, col) {
    if (!this.moveValidator.isValidMove(row, col)) {
      this.uiManager.showStatus('error', '無効な手です');
      return;
    }

    if (!this.gameState.isCurrentPlayerHuman()) {
      this.uiManager.showStatus('error', 'プレイヤーのターンではありません');
      return;
    }

    this.playerManager.handlePlayerMove(row, col);
  }

  /**
   * 自動再生の切り替え
   */
  toggleAutoPlay() {
    if (this.gameState.getAutoInterval()) {
      this.#stopAutoPlay();
    } else {
      this.#startAutoPlay();
    }
  }

  /**
   * 自動再生開始
   */
  #startAutoPlay() {
    if (this.gameState.isGameEnd) {
      this.uiManager.showStatus('info', 'ゲームが終了しています');
      return;
    }

    const interval = setInterval(async () => {
      if (this.gameState.isGameEnd) {
        this.#stopAutoPlay();
        return;
      }
      await this.nextMove();
    }, 1000); // 1秒間隔

    this.gameState.setAutoInterval(interval);
    this.uiManager.setAutoPlayButtonText('自動再生停止');
    this.uiManager.showStatus('info', '自動再生を開始しました');
  }

  /**
   * 自動再生停止
   */
  #stopAutoPlay() {
    this.gameState.clearAutoInterval();
    this.uiManager.setAutoPlayButtonText('自動再生');
    this.uiManager.showStatus('info', '自動再生を停止しました');
  }

  /**
   * ゲームリセット
   */
  async resetGame() {
    try {
      this.#stopAutoPlay();
      this.playerManager.onPlayerTurnEnd();

      const result = await this.apiClient.resetGame();
      if (result.success) {
        this.gameState.reset();
        this.uiManager.hideGameArea();
        this.uiManager.showStatus('success', 'ゲームをリセットしました');
      }
    } catch (error) {
      this.uiManager.showStatus('error', `リセットエラー: ${error.message}`);
    }
  }

  /**
   * ゲーム表示開始
   */
  #startGameDisplay() {
    this.uiManager.showGameArea();
    this.#updateDisplay();
    this.uiManager.addMoveLog('ゲーム開始！');

    // ボタンの有効化
    this.uiManager.enableButton('nextMoveBtn', true);
    this.uiManager.enableButton('autoPlayBtn', true);
  }

  /**
   * 表示更新
   */
  #updateDisplay() {
    const clickHandler = this.gameState.isCurrentPlayerHuman()
      ? (row, col) => this.makePlayerMove(row, col)
      : null;

    this.boardRenderer.renderBoard(this.gameState.state, this.gameState, clickHandler);
    this.boardRenderer.updateScoreDisplay(this.gameState.state);
    this.boardRenderer.updatePlayerNames(this.gameState.state);
    this.uiManager.updateScore(this.gameState.state);
    this.uiManager.updatePlayerNames(this.gameState.state);
  }

  /**
   * プレイヤーvsCPUターンの処理
   */
  #handlePlayerVsCpuTurn() {
    if (this.gameState.isCurrentPlayerHuman()) {
      // プレイヤーのターン - 入力待ち開始
      this.playerManager.startWaitingForInput((move) => {
        this.nextMove(move);
      });
      this.uiManager.showStatus('info', 'あなたのターンです。石を置いてください。');
    } else {
      // CPUのターン - 自動的に次の手を実行
      setTimeout(() => {
        this.nextMove();
      }, 1000);
      this.uiManager.showStatus('info', 'CPUが考えています...');
    }
  }

  /**
   * ゲーム終了処理
   */
  #handleGameEnd() {
    this.#stopAutoPlay();
    this.playerManager.onPlayerTurnEnd();
    this.boardRenderer.displayGameEnd(this.gameState.state);

    // ボタンの無効化
    this.uiManager.enableButton('nextMoveBtn', false);
    this.uiManager.enableButton('autoPlayBtn', false);

    this.uiManager.showStatus('success', 'ゲーム終了！');
    this.uiManager.addMoveLog('ゲーム終了');
  }

  /**
   * 現在のゲーム状態を取得
   */
  getGameState() {
    return this.gameState;
  }

  /**
   * 現在のUIマネージャーを取得
   */
  getUiManager() {
    return this.uiManager;
  }
}

export default GameOrchestrator;
