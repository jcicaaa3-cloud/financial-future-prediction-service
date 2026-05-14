from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from financial_risk_scoring.data.generate_sample import generate_sample_input
from financial_risk_scoring.service.pipeline import run_prediction_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sample data and run the V4 showcase risk-scoring pipeline.")
    parser.add_argument("--company-id", default="C003")
    parser.add_argument("--input-dir", default="data/input/sample")
    parser.add_argument("--artifact-dir", default="artifacts")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    generate_sample_input(input_dir)
    packet = run_prediction_pipeline(
        input_dir=input_dir,
        company_id=args.company_id,
        artifact_dir=args.artifact_dir,
    )
    print("Prediction completed")
    print(f"request_id={packet['request_id']}")
    print(f"risk_level={packet['risk_level']}")
    print(f"decision_packet={packet['decision_packet_path']}")
    print(f"report={packet['report_path']}")
    print(f"dashboard={packet['dashboard_path']}")


if __name__ == "__main__":
    main()
