from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_divide(numerator: Any, denominator: Any, default: float = 0.0):
    """Pandas/numpy friendly division with zero denominator handling."""
    import numpy as np

    denom = np.asarray(denominator, dtype=float)
    num = np.asarray(numerator, dtype=float)
    out = np.divide(num, denom, out=np.full_like(num, default, dtype=float), where=denom != 0)
    return out
