"""Session state persistence and checkpointing manager for multi-agent pipelines."""

import json
import os
from typing import Any, Dict, List, Optional
from pathlib import Path


class SessionStore:
    """Manages saving, loading, and listing agent pipeline session checkpoints."""

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            storage_dir = os.getenv("JAGUAR_STORAGE_DIR", ".jaguar_sessions")
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_path(self, session_id: str) -> Path:
        # Sanitize session_id to prevent directory traversal
        safe_id = "".join(c for c in session_id if c.isalnum() or c in ("_", "-"))
        return self.storage_dir / f"{safe_id}.json"

    def save_checkpoint(self, session_id: str, state: Dict[str, Any]) -> bool:
        """Save pipeline execution state to a JSON checkpoint file."""
        if not session_id:
            raise ValueError("Session ID cannot be empty")
        
        file_path = self._get_session_path(session_id)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise IOError(f"Failed to save session {session_id}: {e}")

    def load_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a pipeline execution state from checkpoint."""
        file_path = self._get_session_path(session_id)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise IOError(f"Failed to load session {session_id}: {e}")

    def list_sessions(self) -> List[str]:
        """List all available session IDs."""
        if not self.storage_dir.exists():
            return []
        return [p.stem for p in self.storage_dir.glob("*.json")]

    def delete_session(self, session_id: str) -> bool:
        """Delete a session checkpoint file."""
        file_path = self._get_session_path(session_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False
