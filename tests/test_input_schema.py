from __future__ import annotations

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.validate_input_schema import validate_input_directory  # noqa: E402
from src.data.build_real_panel_from_input import build_real_panel_from_input  # noqa: E402


def test_sample_input_schema_ok() -> None:
    report = validate_input_directory(ROOT / "data" / "input" / "sample", write_report=False)
    assert report["ok"] is True


def test_build_real_panel_from_sample(tmp_path: Path) -> None:
    out = tmp_path / "panel.csv"
    df = build_real_panel_from_input(ROOT / "data" / "input" / "sample", out)
    assert out.exists()
    assert len(df) > 0
    assert "company_id" in df.columns
    assert "macro_rate" in df.columns


def main() -> None:
    test_sample_input_schema_ok()
    with tempfile.TemporaryDirectory() as tmpdir:
        test_build_real_panel_from_sample(Path(tmpdir))
    print("INPUT_SCHEMA_TEST_OK")


if __name__ == "__main__":
    main()
