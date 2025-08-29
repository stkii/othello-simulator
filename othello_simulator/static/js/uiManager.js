class UiManager {
  constructor() {
    this.elements = this.#getUIElements();
  }

  #getUIElements() {
    return {
      blackScore: document.getElementById('blackScore'),
      whiteScore: document.getElementById('whiteScore'),
      moveCount: document.getElementById('moveCount'),
      currentPlayer: document.getElementById('currentPlayer'),
      gameEndStatus: document.getElementById('gameEndStatus'),
      gameArea: document.getElementById('gameArea'),
    };
  }

  init() {
    this.#setupEventListeners();
    this.#showInitialStatus();
  }

  #setupEventListeners() {
    this.#setupButtonEvents();
    this.#setupFileInput();
    this.#setupModeSelect();
  }

  #showInitialStatus() {
    this.showStatus('loading', '対戦モードを選択して戦略ファイルをアップロードしてください');
  }

  #setupButtonEvents() {
    // ボタンイベントはGameOrchestratorで管理されるため、ここでは基本的なUI設定のみ行う
    this.enableButton('nextMoveBtn', false);
    this.enableButton('autoPlayBtn', false);
  }

  #setupFileInput() {
    const blackPlayerFile = document.getElementById('blackPlayerFile');
    const whitePlayerFile = document.getElementById('whitePlayerFile');
    const cpuStrategyFile = document.getElementById('cpuStrategyFile');

    if (blackPlayerFile) {
      blackPlayerFile.addEventListener('change', (e) => {
        this.#updateFileStatus('blackPlayerStatus', e.target.files[0]);
      });
    }

    if (whitePlayerFile) {
      whitePlayerFile.addEventListener('change', (e) => {
        this.#updateFileStatus('whitePlayerStatus', e.target.files[0]);
      });
    }

    if (cpuStrategyFile) {
      cpuStrategyFile.addEventListener('change', (e) => {
        this.#updateFileStatus('cpuStrategyStatus', e.target.files[0]);
      });
    }
  }

  /**
   * ファイル選択状態の表示更新
   */
  #updateFileStatus(statusElementId, file) {
    const statusElement = document.getElementById(statusElementId);
    if (statusElement) {
      if (file) {
        statusElement.textContent = `選択済み: ${file.name}`;
        statusElement.className = 'file-status file-ready';
      } else {
        statusElement.textContent = 'ファイルが選択されていません';
        statusElement.className = 'file-status file-empty';
      }
    }
  }

  #setupModeSelect() {
    const cpuVsCpuRadio = document.getElementById('cpuVsCpuRadio');
    const playerVsCpuRadio = document.getElementById('playerVsCpuRadio');

    if (cpuVsCpuRadio) {
      cpuVsCpuRadio.addEventListener('change', () => {
        if (cpuVsCpuRadio.checked) {
          this.showCpuVsCpuMode();
        }
      });
    }

    if (playerVsCpuRadio) {
      playerVsCpuRadio.addEventListener('change', () => {
        if (playerVsCpuRadio.checked) {
          this.showPlayerVsCpuMode();
        }
      });
    }
  }

  /**
   * CPU vs CPUモードの表示
   * CPU vs CPUモード用のUIを表示し、プレイヤー vs CPUモード用のUIを非表示にする
   */
  showCpuVsCpuMode() {
    const cpuVsCpuMode = document.getElementById('cpuVsCpuMode');
    const playerVsCpuMode = document.getElementById('playerVsCpuMode');

    if (cpuVsCpuMode) cpuVsCpuMode.style.display = 'block';
    if (playerVsCpuMode) playerVsCpuMode.style.display = 'none';
  }

  /**
   * プレイヤー vs CPUモードの表示
   * プレイヤー vs CPUモード用のUIを表示し、CPU vs CPUモード用のUIを非表示にする
   */
  showPlayerVsCpuMode() {
    const cpuVsCpuMode = document.getElementById('cpuVsCpuMode');
    const playerVsCpuMode = document.getElementById('playerVsCpuMode');

    if (cpuVsCpuMode) cpuVsCpuMode.style.display = 'none';
    if (playerVsCpuMode) playerVsCpuMode.style.display = 'block';
  }

  /**
   * ゲームエリアの表示
   * スクロールで移動可能なゲーム盤と情報パネルを含むゲームエリアを表示
   */
  showGameArea() {
    const gameArea = document.getElementById('gameArea');
    if (gameArea) {
      gameArea.style.display = 'flex';

      setTimeout(() => {
        gameArea.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      }, 300);
    }
  }

  /**
   * ゲームエリアの非表示
   * ゲーム盤と情報パネルを含むゲームエリアを非表示にする
   */
  hideGameArea() {
    const gameArea = document.getElementById('gameArea');
    if (gameArea) {
      gameArea.style.display = 'none';
    }
  }

  /**
   * ボタンの有効/無効状態制御
   */
  enableButton(buttonId, enabled) {
    const button = document.getElementById(buttonId);
    if (button) {
      button.disabled = !enabled;
    }
  }

  /**
   * 自動再生ボタンのテキスト設定
   * 自動再生の開始/停止状態に応じてボタンテキストを変更する
   * @param {string} text - 設定するテキスト
   */
  setAutoPlayButtonText(text) {
    const button = document.getElementById('autoPlayBtn');
    if (button) {
      button.textContent = text;
    }
  }

  /**
   * スコア表示更新
   */
  updateScore(gameState) {
    if (this.elements.blackScore) {
      this.elements.blackScore.textContent = gameState.black_score;
    }
    if (this.elements.whiteScore) {
      this.elements.whiteScore.textContent = gameState.white_score;
    }
    if (this.elements.moveCount) {
      this.elements.moveCount.textContent = gameState.move_count;
    }
  }

  /**
   * プレイヤー名更新
   */
  updatePlayerNames(gameState) {
    const blackPlayerNameElement = document.getElementById('blackPlayerName');
    const whitePlayerNameElement = document.getElementById('whitePlayerName');

    if (blackPlayerNameElement) blackPlayerNameElement.textContent = gameState.black_player_name;
    if (whitePlayerNameElement) whitePlayerNameElement.textContent = gameState.white_player_name;
  }

  /**
   * 選択されたゲームモードの取得
   * ラジオボタンで選択されているゲームモード（cpu-vs-cpu または player-vs-cpu）を取得
   * @returns {string} 選択されたゲームモード
   */
  getSelectedGameMode() {
    const modeRadio = document.querySelector('input[name="gameMode"]:checked');
    return modeRadio ? modeRadio.value : 'cpu-vs-cpu';
  }

  /**
   * ステータス表示
   * @param {string} type - ステータスタイプ (loading, success, error, info)
   * @param {string} message - 表示メッセージ
   */
  showStatus(type, message) {
    const statusElement = document.getElementById('status');
    if (statusElement) {
      statusElement.textContent = message;
      statusElement.className = `status ${type}`;
    }
  }

  /**
   * 移動ログ追加
   * @param {string} message - ログメッセージ
   */
  addMoveLog(message) {
    const moveLogElement = document.getElementById('moveLog');
    if (moveLogElement) {
      const timestamp = new Date().toLocaleTimeString();
      const logEntry = document.createElement('div');
      logEntry.textContent = `[${timestamp}] ${message}`;
      moveLogElement.appendChild(logEntry);

      // 自動スクロール
      moveLogElement.scrollTop = moveLogElement.scrollHeight;
    }
  }

  /**
   * プレイヤープロンプト表示制御
   * @param {boolean} show - 表示するかどうか
   */
  showPlayerPrompt(show) {
    // プレイヤープロンプトは現在のUIでは明示的に表示しない
    // 代わりにステータスメッセージで対応
    if (show) {
      this.showStatus('info', 'あなたのターンです。石を置いてください。');
    }
  }
}

export default UiManager;
