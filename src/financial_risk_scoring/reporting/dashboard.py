from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from financial_risk_scoring.utils import ensure_dir


def _esc(value: Any) -> str:
    return html.escape(str(value))


def _round_or_na(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        return f"{float(value):.3f}"
    except (TypeError, ValueError):
        return str(value)


def _score_cards(scores: dict[str, Any]) -> str:
    cards: list[str] = []
    for key, value in scores.items():
        try:
            numeric = max(0.0, min(1.0, float(value)))
        except (TypeError, ValueError):
            numeric = 0.0
        pct = int(round(numeric * 100))
        label = key.replace("_", " ").title()
        cards.append(
            f"""
            <div class="metric-card">
              <div class="metric-label">{_esc(label)}</div>
              <div class="metric-value">{numeric:.3f}</div>
              <div class="meter"><span style="width:{pct}%"></span></div>
            </div>
            """
        )
    return "\n".join(cards)


def _list(items: list[Any]) -> str:
    if not items:
        return "<li>No signal generated</li>"
    return "\n".join(f"<li>{_esc(item)}</li>" for item in items)


def _feature_snapshot_table(snapshot: dict[str, Any]) -> str:
    if not snapshot:
        return "<p class='muted'>No feature snapshot available.</p>"
    rows = "\n".join(
        f"<tr><td>{_esc(key)}</td><td>{_esc(value)}</td></tr>" for key, value in snapshot.items()
    )
    return f"<table><thead><tr><th>Feature</th><th>Current value</th></tr></thead><tbody>{rows}</tbody></table>"


def _metrics_table(metrics: dict[str, Any]) -> str:
    rows = []
    for target, detail in metrics.get("targets", {}).items():
        selected = detail.get("selected_model")
        selected_metric = detail.get("selected_metric", {}) or {}
        rows.append(
            "<tr>"
            f"<td>{_esc(target)}</td>"
            f"<td><span class='pill'>{_esc(selected)}</span></td>"
            f"<td>{_esc(_round_or_na(selected_metric.get('roc_auc')))}</td>"
            f"<td>{_esc(_round_or_na(selected_metric.get('average_precision')))}</td>"
            f"<td>{_esc(_round_or_na(selected_metric.get('f1_at_0_5')))}</td>"
            "</tr>"
        )
    if not rows:
        rows.append("<tr><td colspan='5'>No metrics found</td></tr>")
    return """
    <table>
      <thead><tr><th>Target</th><th>Selected model</th><th>ROC-AUC</th><th>PR-AUC</th><th>F1@0.5</th></tr></thead>
      <tbody>{}</tbody>
    </table>
    """.format("\n".join(rows))


def _importance_section(metrics: dict[str, Any]) -> str:
    blocks = []
    for target, detail in metrics.get("targets", {}).items():
        rows = []
        for item in detail.get("top_features", [])[:8]:
            rows.append(
                "<tr>"
                f"<td>{_esc(item.get('feature'))}</td>"
                f"<td>{_esc(item.get('importance'))}</td>"
                f"<td>{_esc(item.get('interpretation_hint'))}</td>"
                "</tr>"
            )
        if not rows:
            rows.append("<tr><td colspan='3'>Selected model does not expose simple feature importance.</td></tr>")
        blocks.append(
            f"""
            <div class="mini-section">
              <h3>{_esc(target)}</h3>
              <table>
                <thead><tr><th>Feature</th><th>Importance</th><th>Hint</th></tr></thead>
                <tbody>{''.join(rows)}</tbody>
              </table>
            </div>
            """
        )
    return "\n".join(blocks)


def _quality_table(data_quality: dict[str, Any]) -> str:
    if not data_quality:
        return "<p class='muted'>No data quality report available.</p>"
    gates = data_quality.get("quality_gates", {})
    gate_rows = "\n".join(
        f"<tr><td>{_esc(key)}</td><td><span class='status {'pass' if value else 'check'}'>{'PASS' if value else 'CHECK'}</span></td></tr>"
        for key, value in gates.items()
    )
    return f"""
    <p class="muted big-number">{data_quality.get('row_count')} rows · {data_quality.get('company_count')} companies · {data_quality.get('quarter_count')} quarters · {data_quality.get('feature_count')} features</p>
    <table><thead><tr><th>Gate</th><th>Status</th></tr></thead><tbody>{gate_rows}</tbody></table>
    """


def _drift_table(drift_report: dict[str, Any]) -> str:
    if not drift_report:
        return "<p class='muted'>No drift report available.</p>"
    rows = []
    for item in drift_report.get("features", [])[:8]:
        severity = str(item.get("severity", "low")).lower()
        rows.append(
            "<tr>"
            f"<td>{_esc(item.get('feature'))}</td>"
            f"<td>{_esc(item.get('standardized_delta'))}</td>"
            f"<td><span class='status {severity}'>{_esc(item.get('severity'))}</span></td>"
            "</tr>"
        )
    return f"""
    <p class="muted">Latest quarter compared with earlier quarters: <strong>{_esc(drift_report.get('latest_quarter'))}</strong></p>
    <table><thead><tr><th>Feature</th><th>Std. delta</th><th>Severity</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
    """


def render_portfolio_dashboard(
    packet: dict[str, Any],
    *,
    metrics: dict[str, Any],
    data_quality: dict[str, Any] | None = None,
    drift_report: dict[str, Any] | None = None,
    output_path: str | Path,
) -> Path:
    """Render a dependency-free static HTML dashboard for portfolio review."""
    out = Path(output_path)
    ensure_dir(out.parent)
    data_quality = data_quality or {}
    drift_report = drift_report or {}
    risk_level = str(packet.get("risk_level", "unknown")).lower()

    document = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Financial Risk Scoring Portfolio Dashboard</title>
  <style>
    :root {{
      --ink: #0f172a;
      --muted: #64748b;
      --line: #e2e8f0;
      --panel: #ffffff;
      --soft: #f8fafc;
      --blue: #2563eb;
      --green: #16a34a;
      --purple: #7c3aed;
      --orange: #d97706;
      --pink: #db2777;
    }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%); color: var(--ink); }}
    header {{ position: relative; overflow: hidden; color: white; padding: 42px 48px 34px; background: radial-gradient(circle at 85% 10%, rgba(99,102,241,0.55), transparent 32%), linear-gradient(135deg, #0f172a 0%, #172554 62%, #0e7490 100%); }}
    header::after {{ content: ""; position: absolute; inset: 0; background-image: linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px); background-size: 72px 72px; opacity: .42; }}
    header > * {{ position: relative; z-index: 1; }}
    main {{ padding: 28px 40px 46px; max-width: 1220px; margin: auto; }}
    h1 {{ font-size: clamp(34px, 5vw, 58px); line-height: 1.02; margin: 10px 0 10px; letter-spacing: -0.04em; }}
    h2 {{ margin: 0 0 12px; font-size: 22px; }}
    h3 {{ margin: 24px 0 8px; font-size: 17px; color: #334155; }}
    .eyebrow {{ color: #cbd5e1; text-transform: uppercase; letter-spacing: .14em; font-size: 13px; font-weight: 800; }}
    .subhead {{ color: #dbeafe; max-width: 880px; font-size: 18px; }}
    .risk-badge {{ display: inline-flex; align-items: center; gap: 8px; margin-top: 16px; padding: 9px 14px; border-radius: 999px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em; background: rgba(255,255,255,.13); border: 1px solid rgba(255,255,255,.22); }}
    .risk-badge.low {{ color: #bbf7d0; }}
    .risk-badge.medium {{ color: #fde68a; }}
    .risk-badge.high {{ color: #fecaca; }}
    .flow {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-top: 28px; max-width: 1080px; }}
    .flow span {{ position: relative; padding: 11px 10px; border-radius: 14px; background: rgba(255,255,255,.10); border: 1px solid rgba(255,255,255,.18); text-align: center; font-weight: 800; font-size: 13px; }}
    .flow span:not(:last-child)::after {{ content: "→"; position: absolute; right: -15px; top: 50%; transform: translateY(-50%); color: #7dd3fc; font-size: 22px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; }}
    .two-col {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
    .card, .metric-card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 20px; box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06); }}
    .metric-label {{ color: var(--muted); font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: .05em; }}
    .metric-value {{ font-size: 42px; font-weight: 900; letter-spacing: -0.04em; margin: 8px 0 12px; }}
    .meter {{ height: 10px; background: #e2e8f0; border-radius: 999px; overflow: hidden; }}
    .meter span {{ display: block; height: 100%; background: linear-gradient(90deg, var(--blue), var(--purple)); border-radius: 999px; }}
    .muted {{ color: var(--muted); font-size: 14px; }}
    .big-number {{ font-weight: 700; color: #334155; }}
    .pill {{ display: inline-block; padding: 5px 9px; border-radius: 999px; background: #eff6ff; color: #1d4ed8; font-weight: 800; font-size: 12px; }}
    .status {{ display: inline-block; padding: 5px 9px; border-radius: 999px; font-size: 12px; font-weight: 800; text-transform: uppercase; }}
    .status.pass, .status.low {{ background: #dcfce7; color: #166534; }}
    .status.medium, .status.check {{ background: #fef3c7; color: #92400e; }}
    .status.high {{ background: #fee2e2; color: #991b1b; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 14px; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 11px 10px; text-align: left; vertical-align: top; }}
    th {{ color: #334155; background: #f8fafc; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
    section {{ margin: 18px 0; }}
    code {{ background: #f1f5f9; padding: 3px 5px; border-radius: 5px; }}
    ul {{ padding-left: 22px; }}
    li {{ margin: 7px 0; }}
    .mini-section + .mini-section {{ margin-top: 22px; }}
    .footer-note {{ border-left: 4px solid var(--blue); }}
    @media (max-width: 760px) {{
      header {{ padding: 30px 22px; }}
      main {{ padding: 20px 16px 36px; }}
      .flow {{ grid-template-columns: 1fr 1fr; }}
      .flow span:not(:last-child)::after {{ display: none; }}
    }}
  </style>
</head>
<body>
<header>
  <div class="eyebrow">Portfolio artifact · static HTML · generated by pipeline</div>
  <h1>Quarterly Financial Risk Scoring Dashboard</h1>
  <p class="subhead">{_esc(packet.get('company_name'))} ({_esc(packet.get('company_id'))}) · {_esc(packet.get('sector'))} · {_esc(packet.get('quarter'))}</p>
  <span class="risk-badge {risk_level}">Risk level: {_esc(packet.get('risk_level'))}</span>
  <div class="flow">
    <span>CSV contract</span><span>Feature pipeline</span><span>Validation</span><span>FastAPI</span><span>Monitoring</span><span>LLM packet</span>
  </div>
</header>
<main>
  <section class="grid">{_score_cards(packet.get('scores', {}))}</section>

  <section class="two-col">
    <div class="card"><h2>Risk factors</h2><ul>{_list(packet.get('top_risk_factors', []))}</ul></div>
    <div class="card"><h2>Positive factors</h2><ul>{_list(packet.get('positive_factors', []))}</ul></div>
  </section>

  <section class="card">
    <h2>Feature snapshot</h2>
    <p class="muted">Latest company-quarter values used by the service packet.</p>
    {_feature_snapshot_table(packet.get('feature_snapshot', {}))}
  </section>

  <section class="card">
    <h2>Validation leaderboard</h2>
    <p class="muted">Chronological split; baseline model comparison. Synthetic sample metrics are engineering evidence only.</p>
    {_metrics_table(metrics)}
  </section>

  <section class="card">
    <h2>Model-used feature importance</h2>
    <p class="muted">Global baseline importance. This is not causal evidence.</p>
    {_importance_section(metrics)}
  </section>

  <section class="two-col">
    <div class="card"><h2>Data quality gates</h2>{_quality_table(data_quality)}</div>
    <div class="card"><h2>Quarter drift smoke check</h2>{_drift_table(drift_report)}</div>
  </section>

  <section class="card footer-note">
    <h2>Why this exists</h2>
    <p>This artifact is meant to show ML engineering, API design, validation hygiene, monitoring awareness, and portfolio storytelling. It is not investment, lending, credit, trading, or corporate-rating advice.</p>
    <p class="muted">Request ID: <code>{_esc(packet.get('request_id'))}</code></p>
  </section>
</main>
</body>
</html>
""".strip()
    out.write_text(document, encoding="utf-8")
    return out
