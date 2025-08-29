import GameOrchestrator from './gameOrchestrator.js';

function initializeApp() {
  // GameOrchestratorのインスタンスを作成
  const gameOrchestrator = new GameOrchestrator();

  // アプリケーションを初期化
  gameOrchestrator.initialize();

  return gameOrchestrator;
}

/**
 * DOMContentLoadedイベントでアプリケーションを開始
 */
document.addEventListener('DOMContentLoaded', () => {
  try {
    initializeApp();
  } catch (error) {
    console.error('アプリケーションの初期化に失敗しました:', error);
  }
});

window.addEventListener('error', (event) => {
  console.error('アプリケーションエラー:', event.error);
});

/**
 * 未処理のPromise拒否のハンドリング
 */
window.addEventListener('unhandledrejection', (event) => {
  console.error('未処理のPromise拒否:', event.reason);
  event.preventDefault();
});

