class FileManager {
  constructor(apiClient, uiManager) {
    this.apiClient = apiClient;
    this.uiManager = uiManager;
  }

  /**
   * Upload CPU vs CPU strategies
   */
  async uploadCpuStrategies() {
    if (!this.#validateCpuVsCpuForm()) {
      this.uiManager.showStatus('error', '両方のプレイヤーのファイルを選択してください');
      return null;
    }

    const formData = this.#createUploadFormData();
    this.uiManager.showStatus('loading', '戦略ファイル読み込み中...');

    try {
      const result = await this.apiClient.uploadCpuVsCpu(formData);
      if (result.success) {
        this.uiManager.showStatus(
          'success',
          `戦略読み込み完了: ${result.black_player_name} vs ${result.white_player_name}`
        );
      }
      return result;
    } catch (error) {
      this.uiManager.showStatus('error', `通信エラー: ${error.message}`);
      return null;
    }
  }

  #validateCpuVsCpuForm() {
    const blackPlayerFile = document.getElementById('blackPlayerFile');
    const whitePlayerFile = document.getElementById('whitePlayerFile');
    return blackPlayerFile?.files?.length > 0 && whitePlayerFile?.files?.length > 0;
  }

  #createUploadFormData() {
    const formData = new FormData();
    const blackPlayerFile = document.getElementById('blackPlayerFile');
    const whitePlayerFile = document.getElementById('whitePlayerFile');

    if (blackPlayerFile?.files[0]) {
      formData.append('blackPlayer', blackPlayerFile.files[0]);
    }
    if (whitePlayerFile?.files[0]) {
      formData.append('whitePlayer', whitePlayerFile.files[0]);
    }

    return formData;
  }

  /**
   * Upload Player vs CPU strategy
   */
  async uploadPlayerVsCpu() {
    if (!this.#validatePlayerVsCpuForm()) {
      this.uiManager.showStatus('error', 'CPU戦略ファイルを選択してください');
      return null;
    }

    const formData = this.#createPlayerVsCpuFormData();
    this.uiManager.showStatus('loading', 'CPU戦略ファイル読み込み中...');

    try {
      const result = await this.apiClient.uploadPlayerVsCpu(formData);
      if (result.success) {
        this.uiManager.showStatus('success', `プレイヤーvsCPU戦開始: ${result.cpu_strategy}`);
      }
      return result;
    } catch (error) {
      this.uiManager.showStatus('error', `通信エラー: ${error.message}`);
      return null;
    }
  }

  #validatePlayerVsCpuForm() {
    const cpuStrategyFile = document.getElementById('cpuStrategyFile');
    return cpuStrategyFile?.files?.length > 0;
  }

  #createPlayerVsCpuFormData() {
    const formData = new FormData();
    const cpuStrategyFile = document.getElementById('cpuStrategyFile');
    const playerColor = document.querySelector('input[name="playerColor"]:checked')?.value || 'black';

    if (cpuStrategyFile?.files[0]) {
      formData.append('cpuStrategy', cpuStrategyFile.files[0]);
    }
    formData.append('playerColor', playerColor);

    return formData;
  }
}

export default FileManager;
