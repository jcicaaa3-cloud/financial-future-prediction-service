from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from financial_risk_scoring.data.generate_sample import generate_sample_input


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="data/input/sample")
    parser.add_argument("--n-companies", type=int, default=40)
    args = parser.parse_args()
    path = generate_sample_input(args.output_dir, n_companies=args.n_companies)
    print(f"Generated sample input files under {path}")


if __name__ == "__main__":
    main()
