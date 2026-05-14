from __future__ import annotations

from financial_risk_scoring.data.generate_sample import generate_sample_input
from financial_risk_scoring.data.io import build_company_quarter_panel
from financial_risk_scoring.features.engineering import TARGET_COLUMNS, assert_no_future_label_leakage, make_feature_panel


def test_feature_engineering_has_targets_and_no_future_columns(tmp_path):
    input_dir = generate_sample_input(tmp_path / "sample", n_companies=6, start_year=2022, end_year=2025)
    panel = build_company_quarter_panel(input_dir)
    result = make_feature_panel(panel)
    assert set(TARGET_COLUMNS).issubset(result.frame.columns)
    assert result.feature_columns
    assert_no_future_label_leakage(result.feature_columns)
    assert all(not col.startswith("target_") for col in result.feature_columns)
