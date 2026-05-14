from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"


def _write(name: str, svg: str) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    out = ASSET_DIR / name
    out.write_text(svg.strip() + "\n", encoding="utf-8")
    return out


def _arrow_defs() -> str:
    return """
    <defs>
      <linearGradient id="heroGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0f172a"/>
        <stop offset="52%" stop-color="#1e3a8a"/>
        <stop offset="100%" stop-color="#0f766e"/>
      </linearGradient>
      <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#ffffff" stop-opacity="0.98"/>
        <stop offset="100%" stop-color="#f8fafc" stop-opacity="0.98"/>
      </linearGradient>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#020617" flood-opacity="0.18"/>
      </filter>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#2563eb" />
      </marker>
      <marker id="arrowDark" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#334155" />
      </marker>
    </defs>
    """


def _text(x: int, y: int, value: str, *, size: int = 24, weight: int = 500, color: str = "#0f172a", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>'


def _pill(x: int, y: int, w: int, label: str, *, fill: str = "#eff6ff", color: str = "#1d4ed8") -> str:
    return f'''
    <rect x="{x}" y="{y}" width="{w}" height="34" rx="17" fill="{fill}"/>
    {_text(x + w // 2, y + 23, label, size=15, weight=700, color=color, anchor="middle")}
    '''


def _card(x: int, y: int, w: int, h: int, title: str, body: str, *, accent: str = "#2563eb", number: str | None = None) -> str:
    icon = "" if number is None else f'<circle cx="{x+28}" cy="{y+32}" r="18" fill="{accent}"/><text x="{x+28}" y="{y+38}" text-anchor="middle" font-family="Inter, ui-sans-serif, system-ui" font-size="16" font-weight="800" fill="#ffffff">{escape(number)}</text>'
    title_x = x + 24 if number is None else x + 54
    return f'''
    <g filter="url(#shadow)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="url(#panelGrad)" stroke="#e2e8f0"/>
    </g>
    {icon}
    {_text(title_x, y + 38, title, size=20, weight=800, color="#0f172a")}
    {_text(x + 24, y + 76, body, size=15, weight=500, color="#475569")}
    <rect x="{x}" y="{y + h - 6}" width="{w}" height="6" rx="3" fill="{accent}" opacity="0.72"/>
    '''


def build_hero() -> str:
    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1400" height="620" viewBox="0 0 1400 620" role="img" aria-label="Quarterly Financial Risk Scoring Service overview">
      {_arrow_defs()}
      <rect width="1400" height="620" rx="0" fill="url(#heroGrad)"/>
      <circle cx="1250" cy="80" r="190" fill="#38bdf8" opacity="0.12"/>
      <circle cx="170" cy="560" r="210" fill="#22c55e" opacity="0.10"/>
      {_text(70, 96, "Quarterly Financial Risk Scoring Service", size=46, weight=900, color="#ffffff")}
      {_text(72, 138, "Leakage-aware ML backend · FastAPI · time-based validation · portfolio dashboard", size=22, weight=600, color="#dbeafe")}
      {_pill(72, 172, 144, "FastAPI", fill="#dbeafe", color="#1e40af")}
      {_pill(232, 172, 210, "Chronological CV", fill="#dcfce7", color="#166534")}
      {_pill(458, 172, 178, "Monitoring", fill="#fef3c7", color="#92400e")}
      {_pill(652, 172, 190, "LLM-ready report", fill="#ede9fe", color="#5b21b6")}

      <g transform="translate(70,245)">
        <rect x="0" y="0" width="1260" height="282" rx="26" fill="#ffffff" opacity="0.96" filter="url(#shadow)"/>
        <rect x="0" y="0" width="1260" height="46" rx="26" fill="#f8fafc"/>
        <circle cx="28" cy="23" r="7" fill="#ef4444"/><circle cx="52" cy="23" r="7" fill="#f59e0b"/><circle cx="76" cy="23" r="7" fill="#22c55e"/>
        {_text(110, 31, "github.com/…/financial-future-prediction-service", size=16, weight=700, color="#64748b")}

        <g transform="translate(40,80)">
          {_card(0, 0, 250, 146, "Data contract", "5 CSV inputs · schema gates", accent="#0ea5e9", number="1")}
          <path d="M268,74 C292,74 300,74 326,74" stroke="#2563eb" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          {_card(340, 0, 250, 146, "Feature pipeline", "ratios · rolling signals · labels", accent="#22c55e", number="2")}
          <path d="M608,74 C632,74 640,74 666,74" stroke="#2563eb" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          {_card(680, 0, 250, 146, "Validation", "walk-forward · baselines", accent="#f59e0b", number="3")}
          <path d="M948,74 C972,74 980,74 1006,74" stroke="#2563eb" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
          {_card(1020, 0, 180, 146, "Service", "API · dashboard", accent="#8b5cf6", number="4")}
        </g>
      </g>
      {_text(70, 585, "Portfolio framing: engineering evidence, not investment advice or production credit scoring.", size=18, weight=600, color="#cbd5e1")}
    </svg>
    '''


def build_architecture() -> str:
    rows = [
        ("Input layer", "company_master · financial_statement · market · macro · disclosures", "#e0f2fe", "#0369a1"),
        ("Data quality", "schema validation · missingness · quarter coverage · sample gates", "#dcfce7", "#166534"),
        ("Feature layer", "financial ratios · trend deltas · rolling means · available-at-time guards", "#fef3c7", "#92400e"),
        ("Model layer", "dummy baseline · logistic regression · random forest · leaderboard", "#ede9fe", "#5b21b6"),
        ("Service layer", "FastAPI single prediction · batch scoring · model metrics endpoints", "#ffe4e6", "#9f1239"),
        ("Portfolio artifacts", "decision packet · markdown report · LLM prompt · dashboard · drift report", "#f1f5f9", "#334155"),
    ]
    cards = []
    x, y, w, h = 90, 100, 1020, 72
    for i, (title, desc, fill, color) in enumerate(rows):
        yy = y + i * 92
        cards.append(f'''
          <rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="18" fill="{fill}" stroke="#cbd5e1"/>
          <circle cx="{x+34}" cy="{yy+36}" r="20" fill="{color}"/>
          <text x="{x+34}" y="{yy+43}" text-anchor="middle" font-family="Inter, ui-sans-serif, system-ui" font-size="18" font-weight="900" fill="#ffffff">{i+1}</text>
          {_text(x+70, yy+31, title, size=20, weight=850, color="#0f172a")}
          {_text(x+70, yy+55, desc, size=15, weight=550, color="#475569")}
        ''')
        if i < len(rows) - 1:
            cards.append(f'<path d="M{600},{yy+h+8} L{600},{yy+92-8}" stroke="#334155" stroke-width="3" fill="none" marker-end="url(#arrowDark)"/>')
    side = f'''
      <rect x="1160" y="120" width="250" height="454" rx="22" fill="#ffffff" stroke="#e2e8f0" filter="url(#shadow)"/>
      {_text(1185, 158, "Review signals", size=22, weight=900, color="#0f172a")}
      {_text(1185, 202, "✓ clear service boundary", size=16, weight=700, color="#166534")}
      {_text(1185, 238, "✓ leakage-aware framing", size=16, weight=700, color="#166534")}
      {_text(1185, 274, "✓ time-based validation", size=16, weight=700, color="#166534")}
      {_text(1185, 310, "✓ API + Docker + CI", size=16, weight=700, color="#166534")}
      {_text(1185, 346, "✓ dashboard artifact", size=16, weight=700, color="#166534")}
      <line x1="1185" y1="378" x2="1385" y2="378" stroke="#e2e8f0"/>
      {_text(1185, 414, "Caveat", size=18, weight=900, color="#9f1239")}
      {_text(1185, 448, "Synthetic sample data", size=15, weight=700, color="#475569")}
      {_text(1185, 474, "No investment advice", size=15, weight=700, color="#475569")}
      {_text(1185, 500, "Baseline model only", size=15, weight=700, color="#475569")}
    '''
    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1480" height="720" viewBox="0 0 1480 720" role="img" aria-label="System architecture overview">
      {_arrow_defs()}
      <rect width="1480" height="720" fill="#f8fafc"/>
      {_text(70, 60, "System architecture", size=36, weight=900, color="#0f172a")}
      {_text(72, 90, "From company-quarter CSVs to validated API responses and portfolio artifacts", size=17, weight=600, color="#64748b")}
      {''.join(cards)}
      {side}
    </svg>
    '''


def build_dashboard_preview() -> str:
    # Designed as a static mock preview for README, not a substitute for generated HTML dashboard.
    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1480" height="860" viewBox="0 0 1480 860" role="img" aria-label="Portfolio dashboard preview">
      {_arrow_defs()}
      <rect width="1480" height="860" fill="#eef2f7"/>
      <rect x="70" y="60" width="1340" height="760" rx="28" fill="#ffffff" filter="url(#shadow)"/>
      <rect x="70" y="60" width="1340" height="110" rx="28" fill="#111827"/>
      <circle cx="112" cy="94" r="8" fill="#ef4444"/><circle cx="140" cy="94" r="8" fill="#f59e0b"/><circle cx="168" cy="94" r="8" fill="#22c55e"/>
      {_text(110, 132, "Quarterly Financial Risk Scoring Dashboard", size=31, weight=900, color="#ffffff")}
      {_text(110, 158, "Synthetic reviewer snapshot · C003 · 2025Q4 · generated by pipeline", size=16, weight=600, color="#cbd5e1")}
      <rect x="1190" y="104" width="160" height="42" rx="21" fill="#fef3c7"/>
      {_text(1270, 132, "MEDIUM RISK", size=15, weight=900, color="#92400e", anchor="middle")}

      <g transform="translate(110,205)">
        <rect x="0" y="0" width="270" height="122" rx="20" fill="#eff6ff" stroke="#bfdbfe"/>
        {_text(24, 42, "Margin risk", size=17, weight=800, color="#1e40af")}
        {_text(24, 91, "0.438", size=42, weight=900, color="#0f172a")}
        <rect x="310" y="0" width="270" height="122" rx="20" fill="#fef3c7" stroke="#fde68a"/>
        {_text(334, 42, "Drawdown proxy", size=17, weight=800, color="#92400e")}
        {_text(334, 91, "0.512", size=42, weight=900, color="#0f172a")}
        <rect x="620" y="0" width="270" height="122" rx="20" fill="#dcfce7" stroke="#bbf7d0"/>
        {_text(644, 42, "Liquidity stress", size=17, weight=800, color="#166534")}
        {_text(644, 91, "0.289", size=42, weight=900, color="#0f172a")}
        <rect x="930" y="0" width="270" height="122" rx="20" fill="#ede9fe" stroke="#ddd6fe"/>
        {_text(954, 42, "Data quality", size=17, weight=800, color="#5b21b6")}
        {_text(954, 91, "PASS", size=40, weight=900, color="#0f172a")}
      </g>

      <g transform="translate(110,365)">
        <rect x="0" y="0" width="590" height="255" rx="22" fill="#ffffff" stroke="#e5e7eb"/>
        {_text(28, 42, "Top explanation factors", size=22, weight=900, color="#0f172a")}
        <rect x="28" y="72" width="530" height="34" rx="10" fill="#f8fafc"/>
        {_text(44, 95, "operating_margin_delta_1q", size=15, weight=700, color="#334155")}
        <rect x="28" y="118" width="486" height="34" rx="10" fill="#f8fafc"/>
        {_text(44, 141, "debt_ratio", size=15, weight=700, color="#334155")}
        <rect x="28" y="164" width="450" height="34" rx="10" fill="#f8fafc"/>
        {_text(44, 187, "disclosure_risk_count", size=15, weight=700, color="#334155")}
        <rect x="28" y="210" width="408" height="34" rx="10" fill="#f8fafc"/>
        {_text(44, 233, "cash_ratio_trend", size=15, weight=700, color="#334155")}

        <rect x="630" y="0" width="590" height="255" rx="22" fill="#ffffff" stroke="#e5e7eb"/>
        {_text(658, 42, "Validation leaderboard", size=22, weight=900, color="#0f172a")}
        <rect x="658" y="68" width="534" height="40" rx="12" fill="#f1f5f9"/>
        {_text(678, 94, "target", size=14, weight=800, color="#475569")}
        {_text(850, 94, "selected", size=14, weight=800, color="#475569")}
        {_text(1020, 94, "ROC-AUC", size=14, weight=800, color="#475569")}
        {_text(678, 142, "margin deterioration", size=14, weight=700, color="#0f172a")}
        {_text(850, 142, "random forest", size=14, weight=700, color="#0f172a")}
        {_text(1020, 142, "0.71", size=14, weight=700, color="#0f172a")}
        {_text(678, 182, "drawdown proxy", size=14, weight=700, color="#0f172a")}
        {_text(850, 182, "logistic", size=14, weight=700, color="#0f172a")}
        {_text(1020, 182, "0.64", size=14, weight=700, color="#0f172a")}
        {_text(678, 222, "liquidity stress", size=14, weight=700, color="#0f172a")}
        {_text(850, 222, "random forest", size=14, weight=700, color="#0f172a")}
        {_text(1020, 222, "0.69", size=14, weight=700, color="#0f172a")}
      </g>

      <g transform="translate(110,650)">
        <rect x="0" y="0" width="590" height="130" rx="22" fill="#f8fafc" stroke="#e5e7eb"/>
        {_text(28, 42, "Artifacts", size=22, weight=900, color="#0f172a")}
        {_text(28, 76, "decision_packet.json · risk_report.md · llm_prompt.md · monitoring reports", size=16, weight=650, color="#475569")}
        <rect x="630" y="0" width="590" height="130" rx="22" fill="#f8fafc" stroke="#e5e7eb"/>
        {_text(658, 42, "Service surface", size=22, weight=900, color="#0f172a")}
        {_text(658, 76, "POST /v1/predictions · POST /v1/batch-predictions · GET /metrics", size=16, weight=650, color="#475569")}
      </g>
    </svg>
    '''


def build_api_surface() -> str:
    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1400" height="560" viewBox="0 0 1400 560" role="img" aria-label="API surface and artifacts">
      {_arrow_defs()}
      <rect width="1400" height="560" fill="#f8fafc"/>
      {_text(70, 70, "API and artifact surface", size=36, weight=900, color="#0f172a")}
      {_text(72, 102, "The project is framed as a small service, not just a notebook experiment.", size=18, weight=600, color="#64748b")}
      <rect x="80" y="150" width="360" height="300" rx="24" fill="#ffffff" stroke="#e2e8f0" filter="url(#shadow)"/>
      {_text(112, 195, "Reviewer request", size=23, weight=900, color="#0f172a")}
      {_text(112, 238, "POST /v1/predictions", size=17, weight=800, color="#2563eb")}
      {_text(112, 272, "POST /v1/batch-predictions", size=17, weight=800, color="#2563eb")}
      {_text(112, 306, "GET /v1/models/latest/metrics", size=17, weight=800, color="#2563eb")}
      {_text(112, 340, "GET /v1/monitoring/latest/drift", size=17, weight=800, color="#2563eb")}
      <path d="M462,300 C510,300 530,300 585,300" stroke="#2563eb" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
      <rect x="600" y="150" width="360" height="300" rx="24" fill="#ffffff" stroke="#e2e8f0" filter="url(#shadow)"/>
      {_text(632, 195, "Pipeline execution", size=23, weight=900, color="#0f172a")}
      {_text(632, 238, "validate CSV contract", size=17, weight=700, color="#475569")}
      {_text(632, 272, "merge company-quarter panel", size=17, weight=700, color="#475569")}
      {_text(632, 306, "train/score baselines", size=17, weight=700, color="#475569")}
      {_text(632, 340, "build explanations + monitors", size=17, weight=700, color="#475569")}
      <path d="M982,300 C1030,300 1050,300 1105,300" stroke="#2563eb" stroke-width="4" fill="none" marker-end="url(#arrow)"/>
      <rect x="1120" y="150" width="300" height="300" rx="24" fill="#ffffff" stroke="#e2e8f0" filter="url(#shadow)"/>
      {_text(1152, 195, "Returned artifacts", size=23, weight=900, color="#0f172a")}
      {_text(1152, 238, "decision packet JSON", size=17, weight=700, color="#475569")}
      {_text(1152, 272, "static dashboard HTML", size=17, weight=700, color="#475569")}
      {_text(1152, 306, "markdown risk report", size=17, weight=700, color="#475569")}
      {_text(1152, 340, "LLM prompt packet", size=17, weight=700, color="#475569")}
      {_text(1152, 374, "quality / drift report", size=17, weight=700, color="#475569")}
    </svg>
    '''


def build_reviewer_journey() -> str:
    steps = [
        ("01", "Open README", "visual overview + one-command demo"),
        ("02", "Run snapshot", "generated dashboard and decision packet"),
        ("03", "Inspect API", "FastAPI docs and request contracts"),
        ("04", "Check validation", "time split, walk-forward, leaderboard"),
        ("05", "Discuss tradeoffs", "synthetic data caveat + real-data plan"),
    ]
    blocks = []
    start_x, y = 80, 180
    for idx, (num, title, desc) in enumerate(steps):
        x = start_x + idx * 260
        blocks.append(f'''
          <circle cx="{x+70}" cy="{y}" r="54" fill="#1d4ed8"/>
          {_text(x+70, y+12, num, size=31, weight=900, color="#ffffff", anchor="middle")}
          {_text(x, y+95, title, size=21, weight=900, color="#0f172a")}
          {_text(x, y+124, desc, size=15, weight=600, color="#64748b")}
        ''')
        if idx < len(steps) - 1:
            blocks.append(f'<path d="M{x+126},{y} C{x+160},{y} {x+188},{y} {x+214},{y}" stroke="#94a3b8" stroke-width="4" stroke-dasharray="8 8" fill="none" marker-end="url(#arrowDark)"/>')
    return f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="1420" height="420" viewBox="0 0 1420 420" role="img" aria-label="Reviewer journey">
      {_arrow_defs()}
      <rect width="1420" height="420" rx="0" fill="#ffffff"/>
      <rect x="40" y="40" width="1340" height="340" rx="30" fill="#f8fafc" stroke="#e2e8f0"/>
      {_text(80, 95, "Reviewer journey", size=34, weight=900, color="#0f172a")}
      {_text(82, 126, "A hiring manager can understand the project without reading every source file.", size=17, weight=600, color="#64748b")}
      {''.join(blocks)}
    </svg>
    '''


def main() -> None:
    paths = [
        _write("readme_hero.svg", build_hero()),
        _write("architecture_overview.svg", build_architecture()),
        _write("portfolio_dashboard_preview.svg", build_dashboard_preview()),
        _write("api_surface.svg", build_api_surface()),
        _write("reviewer_journey.svg", build_reviewer_journey()),
    ]
    (ASSET_DIR / "README.md").write_text(
        "# README visual assets\n\nThese SVG files are generated by `python scripts/generate_readme_assets.py` and are used by the repository README.\n",
        encoding="utf-8",
    )
    for path in paths:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
