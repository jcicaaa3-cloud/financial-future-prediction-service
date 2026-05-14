from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from financial_risk_scoring.service.pipeline import run_prediction_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the V4 showcase risk-scoring pipeline with provided CSV input files.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--company-id", required=True)
    parser.add_argument("--artifact-dir", default="artifacts")
    args = parser.parse_args()

    packet = run_prediction_pipeline(
        input_dir=args.input_dir,
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
