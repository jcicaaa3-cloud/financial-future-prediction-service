from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from financial_risk_scoring.data.io import build_company_quarter_panel
from financial_risk_scoring.features.engineering import make_feature_panel
from financial_risk_scoring.monitoring.data_quality import build_data_quality_report
from financial_risk_scoring.monitoring.drift import build_quarter_drift_report
from financial_risk_scoring.utils import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate lightweight data quality and drift reports.")
    parser.add_argument("--input-dir", default="data/input/sample")
    parser.add_argument("--output-dir", default="artifacts/monitoring")
    args = parser.parse_args()

    panel = build_company_quarter_panel(args.input_dir)
    features = make_feature_panel(panel)
    out_dir = Path(args.output_dir)
    quality = build_data_quality_report(features.frame, features.feature_columns)
    drift = build_quarter_drift_report(features.frame, features.feature_columns)
    write_json(out_dir / "data_quality_report.json", quality)
    write_json(out_dir / "quarter_drift_report.json", drift)
    print(f"data_quality_report={out_dir / 'data_quality_report.json'}")
    print(f"quarter_drift_report={out_dir / 'quarter_drift_report.json'}")


if __name__ == "__main__":
    main()
