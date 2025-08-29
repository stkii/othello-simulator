class BoardRenderer {
  constructor() {
    this.boardElement = null;
  }

  setBoardElement(element) {
    this.boardElement = element;
  }

  #applyStoneEffects(stone, gameState, row, col) {
    if (gameState.last_move && gameState.last_move[0] === row && gameState.last_move[1] === col) {
      stone.classList.add('new-stone', 'highlight-new');
      setTimeout(() => stone.classList.remove('highlight-new'), 3000);
    }

    if (
      gameState.flipped_stones &&
      gameState.flipped_stones.some(([flippedRow, flippedCol]) => flippedRow === row && flippedCol === col)
    ) {
      stone.classList.add('flipped-stone', 'highlight-flipped');
      setTimeout(() => stone.classList.remove('highlight-flipped'), 3000);
    }
  }

  #renderBlackStone(cell, gameState, row, col) {
    const stone = document.createElement('div');
    stone.className = 'stone black-stone';
    stone.textContent = '●';

    this.#applyStoneEffects(stone, gameState, row, col);
    cell.appendChild(stone);
  }

  #renderWhiteStone(cell, gameState, row, col) {
    const stone = document.createElement('div');
    stone.className = 'stone white-stone';
    stone.textContent = '○';

    this.#applyStoneEffects(stone, gameState, row, col);
    cell.appendChild(stone);
  }

  #renderValidMove(cell, row, col, onCellClick) {
    cell.classList.add('valid-move');
    cell.innerHTML = '<div style="color: white; font-size: 20px;">✓</div>';

    if (onCellClick) {
      cell.style.cursor = 'pointer';
      cell.onclick = () => onCellClick(row, col);
    }
  }

  renderBoard(gameState, gameStateInstance, onCellClick = null) {
    if (!this.boardElement || !gameState) return;
    this.boardElement.innerHTML = '';

    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const cell = document.createElement('div');
        cell.className = 'cell';

        if (gameState.last_move && gameState.last_move[0] === row && gameState.last_move[1] === col) {
          cell.classList.add('last-move');
        }

        if (gameState.board[row][col] === 1) {
          this.#renderBlackStone(cell, gameState, row, col);
        } else if (gameState.board[row][col] === 2) {
          this.#renderWhiteStone(cell, gameState, row, col);
        } else if (gameStateInstance && gameStateInstance.isValidPosition(row, col)) {
          this.#renderValidMove(cell, row, col, onCellClick);
        }

        this.boardElement.appendChild(cell);
      }
    }
  }

  updateScoreDisplay(gameState) {
    if (!gameState) return;

    const blackScoreElement = document.getElementById('blackScore');
    const whiteScoreElement = document.getElementById('whiteScore');
    const moveCountElement = document.getElementById('moveCount');
    const currentPlayerElement = document.getElementById('currentPlayer');

    if (blackScoreElement) blackScoreElement.textContent = gameState.black_score;
    if (whiteScoreElement) whiteScoreElement.textContent = gameState.white_score;
    if (moveCountElement) moveCountElement.textContent = gameState.move_count;

    if (currentPlayerElement) {
      const currentPlayerText =
        gameState.current_player === 1 ? '● 黒番' : gameState.current_player === 2 ? '○ 白番' : 'ゲーム終了';
      currentPlayerElement.textContent = currentPlayerText;
    }
  }

  updatePlayerNames(gameState) {
    if (!gameState) return;

    const currentMatchElement = document.getElementById('currentMatch');
    const blackPlayerNameElement = document.getElementById('blackPlayerName');
    const whitePlayerNameElement = document.getElementById('whitePlayerName');

    if (currentMatchElement) {
      currentMatchElement.textContent = `${gameState.black_player_name} (●) vs ${gameState.white_player_name} (○)`;
    }

    if (blackPlayerNameElement) blackPlayerNameElement.textContent = gameState.black_player_name;
    if (whitePlayerNameElement) whitePlayerNameElement.textContent = gameState.white_player_name;
  }

  displayGameEnd(gameState) {
    const gameEndElement = document.getElementById('gameEndStatus');
    if (!gameEndElement || !gameState) return;

    const winner = gameState.winner;
    let resultText = '';
    if (winner === 1) {
      resultText = `🎉 ${gameState.black_player_name} の勝利！`;
    } else if (winner === 2) {
      resultText = `🎉 ${gameState.white_player_name} の勝利！`;
    } else {
      resultText = '引き分け！';
    }

    const finalScore = `最終スコア: 黒 ${gameState.black_score} - 白 ${gameState.white_score}`;
    gameEndElement.innerHTML = `<div class="game-end">${resultText}<br>${finalScore}</div>`;
  }
}

export default BoardRenderer;
