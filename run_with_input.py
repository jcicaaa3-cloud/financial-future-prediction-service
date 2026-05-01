from __future__ import annotations

from pathlib import Path
import argparse
import time

from src.data.build_real_panel_from_input import build_real_panel_from_input
from src.data.build_panel_dataset import build_panel_dataset
from src.models.train_model import train_all_models
from src.models.predict_company import predict_company
from src.explain.report_generator import generate_company_report
from src.service.decision_packet import build_decision_packet
from src.service.scenario_stress_test import run_stress_test
from src.llm.report_prompt_builder import build_llm_report_prompt

ROOT = Path(__file__).resolve().parent


def _step(title: str) -> float:
    print(title, flush=True)
    return time.perf_counter()


def _done(start: float) -> None:
    print(f"      done in {time.perf_counter() - start:.2f}s", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the pipeline using CSV files from data/input/* instead of mock generator.")
    parser.add_argument("--input-dir", default=str(ROOT / "data" / "input" / "sample"))
    parser.add_argument("--company-id", default="C003")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    company_id = args.company_id

    raw_path = ROOT / "data" / "raw" / "financial_panel_from_input.csv"
    processed_path = ROOT / "data" / "processed" / "feature_panel_from_input.csv"
    model_dir = ROOT / "outputs" / "models_input"
    pred_dir = ROOT / "outputs" / "predictions_input"
    report_dir = ROOT / "outputs" / "reports_input"
    packet_dir = ROOT / "outputs" / "decision_packets_input"
    stress_dir = ROOT / "outputs" / "stress_tests_input"
    llm_input_dir = ROOT / "outputs" / "llm_inputs"

    print("Financial Future Prediction MVP v0.4 input/LLM-ready", flush=True)

    start = _step("[1/8] Validating and merging CSV files from data/input...")
    raw_df = build_real_panel_from_input(input_dir=input_dir, output_path=raw_path)
    print(f"      raw panel rows={len(raw_df):,}, columns={len(raw_df.columns):,}", flush=True)
    _done(start)

    start = _step("[2/8] Building feature and future-label panel...")
    feature_df = build_panel_dataset(input_path=raw_path, output_path=processed_path)
    print(f"      feature panel rows={len(feature_df):,}, columns={len(feature_df.columns):,}", flush=True)
    _done(start)

    start = _step("[3/8] Training baseline tabular models...")
    metrics = train_all_models(feature_path=processed_path, model_dir=model_dir)
    for k, v in metrics.items():
        print(f"      - {k}: {v}", flush=True)
    _done(start)

    start = _step("[4/8] Predicting selected company...")
    pred = predict_company(company_id=company_id, feature_path=processed_path, model_dir=model_dir, output_dir=pred_dir)
    print(f"      saved prediction: {pred_dir / (company_id + '_prediction.json')}", flush=True)
    _done(start)

    start = _step("[5/8] Generating deterministic markdown report...")
    report_path = generate_company_report(prediction=pred, output_dir=report_dir)
    print(f"      saved report: {report_path}", flush=True)
    _done(start)

    start = _step("[6/8] Creating API-style decision packet...")
    packet_path = build_decision_packet(pred, packet_dir)
    print(f"      saved packet: {packet_path}", flush=True)
    _done(start)

    start = _step("[7/8] Running scenario stress test...")
    stress_path = run_stress_test(company_id=company_id, feature_path=processed_path, model_dir=model_dir, output_dir=stress_dir)
    print(f"      saved stress test: {stress_path}", flush=True)
    _done(start)

    start = _step("[8/8] Building model-agnostic LLM report prompt...")
    prompt_path = build_llm_report_prompt(prediction=pred, output_dir=llm_input_dir)
    print(f"      saved LLM input prompt: {prompt_path}", flush=True)
    _done(start)

    print("\nDone. For real data, replace data/input/*.csv using the template columns.", flush=True)


if __name__ == "__main__":
    main()
