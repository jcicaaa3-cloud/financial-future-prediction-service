from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from financial_risk_scoring.data.io import build_company_quarter_panel
from financial_risk_scoring.evaluation.walk_forward import walk_forward_evaluate
from financial_risk_scoring.features.engineering import make_feature_panel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/input/sample")
    parser.add_argument("--artifact-dir", default="artifacts/evaluation")
    args = parser.parse_args()

    panel = build_company_quarter_panel(args.input_dir)
    feature_result = make_feature_panel(panel)
    result = walk_forward_evaluate(feature_result.frame, feature_result.feature_columns, artifact_dir=args.artifact_dir)
    print(f"fold_count={result['fold_count']}")


if __name__ == "__main__":
    main()
