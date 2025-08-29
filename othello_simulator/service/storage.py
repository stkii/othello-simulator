import json
from pathlib import Path
from typing import Any


class JSONStorage:
    """Simple JSON persistence class."""

    def __init__(self, file_path: str) -> None:
        """
        Initialize JSONStorage.

        Parameters
        ----------
        file_path : str
            File path for saving data
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, data: dict[str, Any]) -> bool:
        """
        Save game state to JSON file.

        Parameters
        ----------
        data : dict[str, Any]
            Game state data to save

        Returns
        -------
        bool
            True if save successful, False if failed
        """
        try:
            # Save in JSON format with human-readable formatting
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True

        except Exception:
            return False

    def load(self) -> dict[str, Any] | None:
        """Load game state from JSON file.

        Returns
        -------
        dict[str, Any] | None
            Loaded game state data, None if failed
        """
        try:
            if not self.file_path.exists():
                return None

            with self.file_path.open("r", encoding="utf-8") as f:
                return json.load(f)  # type: ignore[no-any-return]

        except Exception:
            return None

    def clear(self) -> bool:
        """Delete saved game state file.

        Returns
        -------
        bool
            True if deletion successful, False if failed
        """
        try:
            if self.file_path.exists():
                self.file_path.unlink()
            return True

        except Exception:
            return False

    def exists(self) -> bool:
        """Check if game state file exists.

        Returns
        -------
        bool
            True if file exists
        """
        return self.file_path.exists()

    def get_file_path(self) -> Path:
        """Get save file path.

        Returns
        -------
        Path
            Path to the save file
        """
        return self.file_path

    def backup(self, backup_suffix: str = ".backup") -> bool:
        """Backup current game state file.

        Parameters
        ----------
        backup_suffix : str
            Suffix for backup file

        Returns
        -------
        bool
            True if backup successful, False if failed
        """
        try:
            if not self.file_path.exists():
                return True

            backup_path = self.file_path.with_suffix(self.file_path.suffix + backup_suffix)
            backup_path.write_bytes(self.file_path.read_bytes())

            return True

        except Exception:
            return False
