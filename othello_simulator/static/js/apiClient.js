class ApiClient {
  constructor() {
    this.baseUrl = '';
  }

  // CPU vs CPU game
  async uploadCpuVsCpu(strategyFiles) {
    try {
      const response = await fetch(`${this.baseUrl}/upload-strategies`, {
        method: 'POST',
        body: strategyFiles,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error uploading CPU strategies:', error);
      throw error;
    }
  }

  // Player vs CPU game
  async uploadPlayerVsCpu(strategyFile) {
    try {
      const response = await fetch(`${this.baseUrl}/upload-player-vs-cpu`, {
        method: 'POST',
        body: strategyFile,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error uploading player strategy:', error);
      throw error;
    }
  }

  // Execute next move
  async nextMove(playerMove = null) {
    try {
      const requestBody = playerMove ? { player_move: playerMove } : {};

      const response = await fetch('/next-move', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const moveResult = await response.json();
      return moveResult;
    } catch (error) {
      console.error('Next move error:', error);
      throw new Error(`Failed to get next move: ${error.message}`);
    }
  }

  // Reset game
  async resetGame() {
    try {
      const response = await fetch('/reset-game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const resetResult = await response.json();
      return resetResult;
    } catch (error) {
      console.error('Reset game error:', error);
      throw new Error(`Failed to reset game: ${error.message}`);
    }
  }
}

export default ApiClient;
