from __future__ import annotations

from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import run_demo  # noqa: E402


def main() -> None:
    run_demo.main()
    required = [
        Path("data/raw/financial_panel_mock.csv"),
        Path("data/processed/feature_panel.csv"),
        Path("outputs/models/metadata.json"),
        Path("outputs/predictions/C003_prediction.json"),
        Path("outputs/reports/C003_report.md"),
        Path("outputs/decision_packets/C003_decision_packet.json"),
        Path("outputs/stress_tests/C003_stress_test.json"),
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError(f"Missing expected outputs: {missing}")

    prediction = json.loads(Path("outputs/predictions/C003_prediction.json").read_text(encoding="utf-8"))
    for key in ["growth_possibility_score", "risk_signal_score", "financial_health_score"]:
        value = prediction["scores"][key]
        if not (0 <= value <= 100):
            raise RuntimeError(f"Score out of range: {key}={value}")

    print("SMOKE_TEST_OK")


if __name__ == "__main__":
    main()
