# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Othello-Simulator is a Flask-based web application that allows users to implement and test custom Othello/Reversi game strategies. The application supports both CPU vs CPU and Player vs CPU game modes, with strategies implemented as Python classes that are dynamically loaded and executed.

## Development Commands

### Environment Setup
```bash
# Recommended: Using uv
uv sync

# Alternative: Using pip
python -m venv .venv
. .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.lock
```

### Running the Application
```bash
flask --app othello_simulator run
```

### Code Quality Tools
```bash
# Python linting and formatting
ruff check othello_simulator/
ruff format othello_simulator/

# Type checking
mypy othello_simulator/

# JavaScript linting and formatting
npm run lint     # eslint othello_simulator/static/js/
npm run format   # prettier --write othello_simulator/static/js/
```

### Development Dependencies
Python dev tools are managed via `uv` dependency groups:
```bash
uv sync --group dev  # Installs mypy and ruff
```

## Architecture Overview

### Core Game Logic (othello_simulator/core/)
The game logic follows a modular, facade-based architecture:

- **Board** (facade): Main interface providing simplified access to all game functionality
- **BoardState**: Manages the 8x8 board state and stone placement data
- **Placement**: Handles move validation and legal move calculation
- **ScoreCalculator**: Computes scores and determines winners
- **GameManager**: Controls game flow, turn switching, and stone flipping logic
- **GameSimulator**: Provides isolated simulation capabilities for move previewing

### Strategy System
- **Base Strategy**: `examples/base.py` contains `StrategyBase` and `MyStrategy` template
- **Dynamic Loading**: Strategies are loaded via `importlib.util` and must implement `MyStrategy` class
- **Security Note**: Uploaded Python files are executed without sandboxing - local use only

### Web Layer (othello_simulator/)
- **Flask App**: `app.py` handles HTTP endpoints and file uploads
- **GameController**: `service/controller.py` orchestrates game state and strategy execution
- **State Management**: `service/state.py` manages game session data with JSON persistence
- **Frontend**: Vanilla JavaScript with ES6 modules handling UI interactions

### Frontend Architecture (othello_simulator/static/js/)
Modular JavaScript architecture with clear separation of concerns:

- **GameOrchestrator**: Main coordinator managing all components
- **GameState**: Centralized state management
- **BoardRenderer**: Handles visual board updates and animations
- **PlayerManager**: Manages human player interactions
- **FileManager**: Handles strategy file uploads
- **ApiClient**: HTTP communication with Flask backend
- **UiManager**: UI updates and user feedback

### Game Flow
1. Strategy files uploaded and dynamically loaded as Python modules
2. Game state persisted to JSON file in `uploads/` directory  
3. Moves processed through core game logic with validation
4. Frontend polls for game state updates and renders board changes
5. Human moves handled via click events, CPU moves executed automatically

### File Storage
- **uploads/**: Temporary storage for uploaded strategy files and game state
- **game-state.json**: Persisted game session data for recovery after server restart

### Configuration
- **ruff.toml**: Python code style (line length 99, comprehensive rule set)
- **pyproject.toml**: Python dependencies and project metadata  
- **package.json**: JavaScript tooling (ESLint, Prettier)
- **requirements.lock**: Locked Python dependencies for pip users