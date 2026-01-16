from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def sha256_file(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    file_path = Path(path)
    if not file_path.exists():
        return None
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def current_commit_ref() -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def ensure_dir(path: str) -> Path:
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)


def utc_now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def env_override(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(key, default)

