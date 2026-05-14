from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from financial_risk_scoring.data.generate_sample import generate_sample_input
from financial_risk_scoring.service.pipeline import run_prediction_pipeline
from financial_risk_scoring.utils import write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a small recruiter-friendly demo snapshot.")
    parser.add_argument("--company-id", default="C003")
    parser.add_argument("--input-dir", default="data/input/sample")
    parser.add_argument("--work-artifact-dir", default="artifacts/portfolio_snapshot_work")
    parser.add_argument("--output-dir", default="examples/portfolio_snapshot")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    generate_sample_input(input_dir)
    packet = run_prediction_pipeline(
        input_dir=input_dir,
        company_id=args.company_id,
        artifact_dir=args.work_artifact_dir,
        request_id="portfolio-snapshot",
    )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "decision_packet.json", packet)

    for key, filename in [
        ("report_path", "risk_report.md"),
        ("llm_prompt_path", "llm_prompt.md"),
        ("dashboard_path", "portfolio_dashboard.html"),
        ("metrics_path", "time_split_metrics.json"),
        ("walk_forward_metrics_path", "walk_forward_metrics.json"),
        ("data_quality_path", "data_quality_report.json"),
        ("drift_report_path", "quarter_drift_report.json"),
    ]:
        src = Path(packet[key])
        if src.exists():
            shutil.copy2(src, out_dir / filename)

    summary = f"""
# Portfolio snapshot

This folder contains generated outputs from the V4 pipeline for `{packet['company_id']}`.

Open `portfolio_dashboard.html` in a browser to see the recruiter-friendly static dashboard.

## Key result

- Company: {packet['company_name']} ({packet['company_id']})
- Quarter: {packet['quarter']}
- Risk level: {packet['risk_level']}
- Report: `risk_report.md`
- Decision packet: `decision_packet.json`

## Caveat

The bundled sample data is synthetic and exists to demonstrate engineering flow, not real financial accuracy.
""".strip()
    (out_dir / "README.md").write_text(summary, encoding="utf-8")
    print(f"portfolio_snapshot={out_dir}")


if __name__ == "__main__":
    main()
