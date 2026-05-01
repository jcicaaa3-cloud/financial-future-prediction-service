from __future__ import annotations

from pathlib import Path
import time

from src.data.generate_mock_data import generate_mock_financial_data
from src.data.build_panel_dataset import build_panel_dataset
from src.models.train_model import train_all_models
from src.models.predict_company import predict_company
from src.explain.report_generator import generate_company_report
from src.service.decision_packet import build_decision_packet
from src.service.scenario_stress_test import run_stress_test
from src.llm.report_prompt_builder import build_llm_report_prompt

ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data" / "raw" / "financial_panel_mock.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "feature_panel.csv"
MODELS_DIR = ROOT / "outputs" / "models"
PRED_DIR = ROOT / "outputs" / "predictions"
REPORT_DIR = ROOT / "outputs" / "reports"
PACKET_DIR = ROOT / "outputs" / "decision_packets"
STRESS_DIR = ROOT / "outputs" / "stress_tests"
LLM_INPUT_DIR = ROOT / "outputs" / "llm_inputs"


def _step(title: str) -> float:
    print(title, flush=True)
    return time.perf_counter()


def _done(start: float) -> None:
    print(f"      done in {time.perf_counter() - start:.2f}s", flush=True)


def main() -> None:
    print("Financial Future Prediction MVP v0.4 input/LLM-ready", flush=True)

    start = _step("[1/8] Generating synthetic company-quarter financial panel...")
    generate_mock_financial_data(output_path=RAW_PATH, n_companies=40, n_quarters=16, seed=42)
    _done(start)

    start = _step("[2/8] Building financial ratio, latent proxy, and future label panel...")
    feature_df = build_panel_dataset(input_path=RAW_PATH, output_path=PROCESSED_PATH)
    print(f"      rows={len(feature_df):,}, columns={len(feature_df.columns):,}", flush=True)
    _done(start)

    start = _step("[3/8] Training baseline interpretable models...")
    metrics = train_all_models(feature_path=PROCESSED_PATH, model_dir=MODELS_DIR)
    print("      metrics:", flush=True)
    for k, v in metrics.items():
        print(f"      - {k}: {v}", flush=True)
    _done(start)

    company_id = "C003"

    start = _step("[4/8] Predicting one company as service-style JSON...")
    pred = predict_company(company_id=company_id, feature_path=PROCESSED_PATH, model_dir=MODELS_DIR, output_dir=PRED_DIR)
    print(f"      saved prediction: {PRED_DIR / (company_id + '_prediction.json')}", flush=True)
    _done(start)

    start = _step("[5/8] Generating human-readable diagnosis report...")
    report_path = generate_company_report(prediction=pred, output_dir=REPORT_DIR)
    print(f"      saved report: {report_path}", flush=True)
    _done(start)

    start = _step("[6/8] Creating API-style decision packet...")
    packet_path = build_decision_packet(pred, PACKET_DIR)
    print(f"      saved packet: {packet_path}", flush=True)
    _done(start)

    start = _step("[7/8] Running scenario stress test...")
    stress_path = run_stress_test(company_id=company_id, feature_path=PROCESSED_PATH, model_dir=MODELS_DIR, output_dir=STRESS_DIR)
    print(f"      saved stress test: {stress_path}", flush=True)
    _done(start)

    start = _step("[8/8] Building model-agnostic LLM report prompt...")
    prompt_path = build_llm_report_prompt(prediction=pred, output_dir=LLM_INPUT_DIR)
    print(f"      saved LLM input prompt: {prompt_path}", flush=True)
    _done(start)

    print("\nDone. Open outputs/reports/C003_report.md or outputs/llm_inputs/C003_llm_report_prompt.md", flush=True)


if __name__ == "__main__":
    main()
