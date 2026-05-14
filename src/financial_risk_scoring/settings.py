from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Common project paths used by scripts and API handlers."""

    root: Path = Path(__file__).resolve().parents[2]

    @property
    def data_input_sample(self) -> Path:
        return self.root / "data" / "input" / "sample"

    @property
    def artifacts(self) -> Path:
        return self.root / "artifacts"


PATHS = ProjectPaths()
