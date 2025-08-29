import importlib.util
from pathlib import Path

from flask import Flask, Response, current_app, jsonify, render_template, request

from examples.base import StrategyBase
from othello_simulator.core.board import Board
from othello_simulator.service.controller import GameController

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

GAME_STATE_FILE = UPLOAD_FOLDER / "game-state.json"


game_controller = GameController(str(GAME_STATE_FILE))


class PlayerStrategy(StrategyBase):
    """A dummy strategy that simply waits for human input."""

    def choose_move(self, _board: Board) -> tuple[int, int] | None:
        # This should never be called for human players in normal operation
        return None


def _load_strategy(file_path: str, player: int) -> StrategyBase | None:
    try:
        # Load module dynamically
        spec = importlib.util.spec_from_file_location("strategy_module", file_path)
        if spec is None:
            msg = f"Failed to create spec for {file_path}"
            current_app.logger.error(msg)
            return None

        strategy_module = importlib.util.module_from_spec(spec)
        if strategy_module is None:
            msg = f"Failed to create module from spec for {file_path}"
            current_app.logger.error(msg)
            return None

        # Execute module
        if spec.loader is None:
            msg = f"No loader found for {file_path}"
            current_app.logger.error(msg)
            return None
        spec.loader.exec_module(strategy_module)

        if hasattr(strategy_module, "MyStrategy"):
            # Type ignore for dynamic loading
            return strategy_module.MyStrategy(player)  # type: ignore[no-any-return]
        msg = f"MyStrategyクラスが見つかりません: {file_path}"
        current_app.logger.error(msg)
        return None

    except Exception as e:
        msg = f"戦略読み込みエラー: {e}"
        current_app.logger.exception(msg)
        return None


@app.route("/")
def index() -> str:
    """Render the HTML page after attempting to restore a previous state."""
    # When the server starts, attempt to restore the previous game state.
    game_controller.load_state()
    return render_template("index.html")


@app.route("/get-state")
def get_state() -> Response:
    if game_controller.board is None:
        game_controller.load_state()
    state = game_controller.get_current_state()
    return jsonify(
        {"success": True, "state": state}
        if state
        else {"success": False, "message": "ゲームが開始されていません"},
    )


@app.route("/upload-strategies", methods=["POST"])
def upload_strategies() -> Response:
    black_player_file = request.files["blackPlayer"]
    white_player_file = request.files["whitePlayer"]

    if black_player_file.filename == "" or white_player_file.filename == "":
        return jsonify({"success": False, "error": "ファイルが選択されていません"})

    # Temporary save the files to the upload folder.
    black_player_path = UPLOAD_FOLDER / f"black_{black_player_file.filename}"
    white_player_path = UPLOAD_FOLDER / f"white_{white_player_file.filename}"

    black_player_file.save(black_player_path)
    white_player_file.save(white_player_path)

    # Load strategies via the singleton manager.
    strategy_1 = _load_strategy(str(black_player_path), 1)
    strategy_2 = _load_strategy(str(white_player_path), 2)

    if strategy_1 is None or strategy_2 is None:
        return jsonify({"success": False, "error": "Failed to load strategies"})

    name_1 = (black_player_file.filename or "unknown").replace(".py", "")
    name_2 = (white_player_file.filename or "unknown").replace(".py", "")

    game_controller.start_game(
        strategy_1,
        strategy_2,
        name_1,
        name_2,
        strategy1_file=str(black_player_path),
        strategy2_file=str(white_player_path),
    )

    state = game_controller.get_current_state()

    return jsonify(
        {
            "success": True,
            "black_player_name": name_1,
            "white_player_name": name_2,
            "state": state,
        },
    )


@app.route("/upload-player-vs-cpu", methods=["POST"])
def upload_player_vs_cpu() -> Response:
    """Upload one AI strategy file and start a Human-vs-AI match."""

    if "cpuStrategy" not in request.files:
        return jsonify({"success": False, "error": "CPU file not selected"})

    cpu_file = request.files["cpuStrategy"]
    human_color = request.form.get("playerColor", "black")

    if not cpu_file.filename:
        return jsonify({"success": False, "error": "No file selected"})

    cpu_path = UPLOAD_FOLDER / f"cpu_{cpu_file.filename}"
    cpu_file.save(cpu_path)

    # Load the AI strategy.
    human_player = 1 if human_color == "black" else 2
    cpu_player = 2 if human_color == "black" else 1

    cpu_strategy = _load_strategy(str(cpu_path), cpu_player)
    if cpu_strategy is None:
        return jsonify({"success": False, "error": "Failed to load AI strategy"})

    human_strategy = PlayerStrategy(human_player)

    if human_player == 1:
        strategy1: StrategyBase = human_strategy
        strategy2: StrategyBase = cpu_strategy
        name1, name2 = "Player", (cpu_file.filename or "unknown").replace(".py", "")
        strategy1_file, strategy2_file = None, str(cpu_path)
    else:
        strategy1 = cpu_strategy
        strategy2 = human_strategy
        name1, name2 = (cpu_file.filename or "unknown").replace(".py", ""), "Player"
        strategy1_file, strategy2_file = str(cpu_path), None

    game_controller.start_game(
        strategy1,
        strategy2,
        name1,
        name2,
        player_vs_cpu=True,
        player=human_player,
        strategy1_file=strategy1_file,
        strategy2_file=strategy2_file,
    )

    state = game_controller.get_current_state()

    return jsonify(
        {
            "success": True,
            "cpu_strategy": (cpu_file.filename or "unknown").replace(".py", ""),
            "player_color": human_color,
            "state": state,
        },
    )


@app.route("/next-move", methods=["POST"])
def next_move() -> Response:  # noqa: C901
    """Advance the game by one move."""

    data = request.get_json() or {}
    player_move = data.get("player_move")

    # If the board is missing, attempt to restore it from persisted state.
    if game_controller.board is None and not game_controller.load_state():
        return jsonify(
            {
                "success": False,
                "error": "Game state not found. Please upload the file again.",
            },
        )

    # Check if strategies need to be reloaded
    if game_controller.game_state.is_player_vs_cpu:
        try:
            strategy1 = game_controller.game_state.strategy1
            strategy2 = game_controller.game_state.strategy2

            # Reload strategies if they are None
            if strategy1 is None:
                if game_controller.game_state.strategy1_file:
                    strategy1 = _load_strategy(game_controller.game_state.strategy1_file, 1)
                    game_controller.game_state.strategy1 = strategy1
                elif game_controller.game_state.player == 1:
                    # Player 1 is human, create HumanStrategy
                    strategy1 = PlayerStrategy(1)
                    game_controller.game_state.strategy1 = strategy1

            if strategy2 is None:
                if game_controller.game_state.strategy2_file:
                    strategy2 = _load_strategy(game_controller.game_state.strategy2_file, 2)
                    game_controller.game_state.strategy2 = strategy2
                elif game_controller.game_state.player == 2:  # noqa: PLR2004
                    # Player 2 is human, create HumanStrategy
                    strategy2 = PlayerStrategy(2)
                    game_controller.game_state.strategy2 = strategy2
        except Exception as e:
            return jsonify({"success": False, "error": f"Strategy reload failed: {e}"})

    state = game_controller.make_next_move(player_move)
    if state is None:
        return jsonify({"success": False, "error": "Failed to execute move"})

    return jsonify({"success": True, "state": state})


@app.route("/reset-game", methods=["POST"])
def reset_game() -> Response:
    """Reset the game and clear persisted state."""

    game_controller.reset_game()
    return jsonify({"success": True})


@app.route("/health", methods=["GET"])
def health_check() -> Response:
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "othello-simulator-game-api"})


if __name__ == "__main__":
    app.run(use_reloader=False)
