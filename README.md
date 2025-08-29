# Othello-Simulator

![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg?logo=python&logoColor=white&style=flat&labelColor=24292e)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-3b808b.svg?logo=flask&logoColor=white&labelColor=24292e)](https://flask.palletsprojects.com/)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Othello-simulator**は、Pythonの学習者がオリジナルのオセロ戦略を実装してプログラミングスキルを向上させるためのWebアプリケーションです。

## Getting Started

### 事前準備

Python のバージョン管理とパッケージ管理を一元的に行えるツールとして、uv の利用を推奨します。詳しい情報や導入手順は[uv公式サイト](https://docs.astral.sh/uv/getting-started/installation/)を参照してください。

### インストールと環境設定

#### With `uv`

```bash
# Clone repository
git clone https://github.com/stkii/othello-simulator.git && cd othello-simulator/

# Creates `.venv` based on the dependencies in `uv.lock`.
uv sync
```

#### Without `uv`

3.10 以上 3.13 未満の Python バージョンを使っていることを確認してください。以下のコマンドで仮想環境を作成し、依存関係をインストールしてください。

```bash
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.lock
```

### アプリの起動

```bash
flask --app othello_simulator run
```

ブラウザで `http://127.0.0.1:5000` にアクセスしてください。

> [!WARNING]
> 本アプリケーションはアップロードされたPythonファイルを検証なしで直接実行します。ローカル使用を前提とした設計です。信頼できるファイルのみをアップロードし、本番環境での使用は避けてください。

## 戦略アルゴリズム実装

戦略アルゴリズムを実装する手順は [`examples/`](https://github.com/stkii/othello-simulator/tree/main/examples) を参照してください。
