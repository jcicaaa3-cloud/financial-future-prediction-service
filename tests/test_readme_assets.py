from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_references_existing_local_visual_assets() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    asset_paths = re.findall(r'src="(docs/assets/[^"]+)"', readme)
    assert asset_paths, "README should contain local visual assets for GitHub presentation"
    for asset in asset_paths:
        path = ROOT / asset
        assert path.exists(), f"Missing README asset: {asset}"
        assert path.stat().st_size > 1000, f"README asset looks empty: {asset}"


def test_architecture_doc_uses_committed_visual_asset_instead_of_ascii_only_flow() -> None:
    doc = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "assets/architecture_diagram.png" in doc
    assert "CSV input directory" not in doc
