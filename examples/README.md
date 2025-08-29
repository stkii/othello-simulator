# Strategy Examples

このディレクトリには、CPU戦略を実装するための参考となるコードをまとめています。

---

## ファイル構成

- `base.py`:
  戦略の基底クラス（抽象クラス）と枠組みを定義しています。

- `sample_strategy.py`:
  `base.py` の基底クラスを継承し、具体的な戦略の実装例を示しています。
  実装の参考にしてください。

---

### Step 1: 戦略ファイルの準備

```bash
# base.pyをコピーして新しい戦略ファイルを作成
cp base.py my_strategy.py
```

### Step 2: 戦略の実装

`my_strategy.py` ファイルを開き、`MyStrategy` クラスの `choose_move` メソッドを編集します。

> [!IMPORTANT]
> **クラス名** `MyStrategy` **は変更しないでください。** システムがこの名前を期待しているため、変更すると動作しません。

#### 実装する場所

```python
class MyStrategy(StrategyBase):
    def choose_move(self, board: Board) -> tuple[int, int] | None:
        # ===========================================
        # ここから下を編集してください
        # ===========================================

        # Example: ランダムに手を選ぶ
        import random
        return random.choice(valid_moves)
```

#### 簡単な実装例

```python
# Example_1: 角を優先する戦略
corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
for corner in corners:
    if corner in valid_moves:
        return corner

# Example_2: 最も多くの石をひっくり返せる手を選ぶ
from othello_simulator.core.simulator import GameSimulator

best_move = None
max_flips = 0

for move in valid_moves:
    success, flipped_positions = GameSimulator.simulate_move_preview(
        board, move[0], move[1], self.player
    )
    if success and len(flipped_positions) > max_flips:
        max_flips = len(flipped_positions)
        best_move = move

return best_move
```

### Step 3: 戦略のテスト

1. アプリケーションを起動:

   ```bash
   flask --app othello_simulator run
   ```

2. ブラウザで `http://127.0.0.1:5000` にアクセス

3. 「ファイルを選択」ボタンで作成した戦略ファイル（例: `my_strategy.py`）をアップロード

> [!WARNING]
> 本アプリケーションはアップロードされたPythonファイルを検証なしで直接実行します。ローカル使用を前提とした設計です。信頼できるファイルのみをアップロードし、本番環境での使用は避けてください。

4. 「プレイヤー vs CPU」または「CPU vs CPU」モードで対戦開始
