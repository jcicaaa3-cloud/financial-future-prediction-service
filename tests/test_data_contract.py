from __future__ import annotations

from financial_risk_scoring.data.generate_sample import generate_sample_input
from financial_risk_scoring.data.io import build_company_quarter_panel, load_input_directory


def test_sample_data_satisfies_contract(tmp_path):
    input_dir = generate_sample_input(tmp_path / "sample", n_companies=6, start_year=2022, end_year=2025)
    frames = load_input_directory(input_dir)
    assert set(frames) == {"company_master", "financial", "market", "macro", "disclosure"}
    panel = build_company_quarter_panel(input_dir)
    assert panel["company_id"].nunique() == 6
    assert "quarter_index" in panel.columns
