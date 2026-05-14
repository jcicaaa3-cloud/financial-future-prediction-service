from __future__ import annotations

from pathlib import Path

ASSET_DIR = Path(__file__).resolve().parents[1] / "docs" / "assets"
ASSET_DIR.mkdir(parents=True, exist_ok=True)


def write(name: str, body: str) -> None:
    (ASSET_DIR / name).write_text(body.strip() + "\n", encoding="utf-8")


def svg_shell(width: int, height: int, content: str, *, bg: str = "#0B1220") -> str:
    return f"""
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Quarterly Financial Risk Scoring visual">
  <defs>
    <linearGradient id="hero" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0B1220"/>
      <stop offset="0.55" stop-color="#111827"/>
      <stop offset="1" stop-color="#1E3A8A"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#38BDF8"/>
      <stop offset="0.5" stop-color="#A78BFA"/>
      <stop offset="1" stop-color="#34D399"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#020617" flood-opacity="0.35"/>
    </filter>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.18"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#34D399"/>
    </marker>
    <style>
      .title {{ font: 800 48px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #F8FAFC; letter-spacing: -0.04em; }}
      .subtitle {{ font: 500 20px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #CBD5E1; }}
      .tiny {{ font: 600 13px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #94A3B8; letter-spacing: .08em; text-transform: uppercase; }}
      .label {{ font: 800 18px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #E2E8F0; }}
      .body {{ font: 500 14px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #CBD5E1; }}
      .darkLabel {{ font: 800 17px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #0F172A; }}
      .darkBody {{ font: 500 13px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #475569; }}
      .metric {{ font: 900 36px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #F8FAFC; }}
      .metricDark {{ font: 900 32px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #0F172A; }}
      .badgeText {{ font: 800 13px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #E0F2FE; }}
      .small {{ font: 500 12px -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; fill: #64748B; }}
    </style>
  </defs>
  <rect width="{width}" height="{height}" fill="{bg}"/>
  {content}
</svg>
"""


def rounded_rect(x, y, w, h, fill, stroke="#334155", rx=22, opacity=1, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" opacity="{opacity}" {extra}/>'


def text(x, y, value, cls="body", anchor="start"):
    value = value.replace("&", "&amp;")
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{value}</text>'


def hero():
    cards = []
    labels = [
        (82, 282, "Data Contract"),
        (274, 282, "Leakage Guard"),
        (466, 282, "Leaderboard"),
        (658, 282, "FastAPI"),
        (850, 282, "Dashboard"),
    ]
    for x, y, label in labels:
        cards.append(rounded_rect(x, y, 150, 54, "rgba(15,23,42,.72)", "#334155", 18, extra='filter="url(#soft)"'))
        cards.append(text(x+75, y+33, label, "badgeText", "middle"))
    arrows = []
    for x1 in [232, 424, 616, 808]:
        arrows.append(f'<path d="M{x1} 309 C{x1+34} 309 {x1+28} 309 {x1+66} 309" stroke="#38BDF8" stroke-width="4" marker-end="url(#arrow)" stroke-linecap="round"/>')
        arrows.append(f'<circle cx="{x1+32}" cy="309" r="3" fill="#A78BFA"/>')
    content = f"""
      <rect width="1200" height="420" fill="url(#hero)"/>
      <circle cx="1080" cy="-20" r="240" fill="#2563EB" opacity="0.20"/>
      <circle cx="980" cy="360" r="180" fill="#22C55E" opacity="0.12"/>
      <path d="M0 360 C220 315 390 400 620 350 C850 300 945 265 1200 300" stroke="url(#accent)" stroke-width="3" opacity=".55"/>
      {text(72, 86, 'PORTFOLIO-GRADE ML BACKEND', 'tiny')}
      {text(72, 145, 'Quarterly Financial', 'title')}
      {text(72, 198, 'Risk Scoring Service', 'title')}
      {text(72, 238, 'Leakage-aware tabular ML → FastAPI inference → monitoring → recruiter-friendly dashboard', 'subtitle')}
      {''.join(cards)}
      {''.join(arrows)}
      <g transform="translate(910 70)" filter="url(#shadow)">
        {rounded_rect(0, 0, 250, 180, '#F8FAFC', '#E2E8F0', 24)}
        {text(28, 44, 'Decision Packet', 'darkLabel')}
        {text(28, 74, 'risk_level', 'darkBody')}
        {text(168, 74, 'medium', 'darkBody')}
        <rect x="28" y="98" width="196" height="12" rx="6" fill="#E2E8F0"/>
        <rect x="28" y="98" width="132" height="12" rx="6" fill="#38BDF8"/>
        <rect x="28" y="126" width="196" height="12" rx="6" fill="#E2E8F0"/>
        <rect x="28" y="126" width="92" height="12" rx="6" fill="#A78BFA"/>
        <rect x="28" y="154" width="196" height="12" rx="6" fill="#E2E8F0"/>
        <rect x="28" y="154" width="162" height="12" rx="6" fill="#34D399"/>
      </g>
    """
    write("readme_hero.svg", svg_shell(1200, 420, content))


def architecture():
    nodes = [
        (54, 96, 190, 92, "OpenDART / KRX", "real-data adapters\nCSV templates"),
        (302, 96, 190, 92, "Schema Gate", "column contract\nquality checks"),
        (550, 96, 190, 92, "Feature Layer", "ratios · rolling\nproxy signals"),
        (798, 96, 190, 92, "Validation", "time split\nwalk-forward"),
        (302, 340, 190, 92, "Model Registry", "dummy · logistic\nrandom forest"),
        (550, 340, 190, 92, "FastAPI Service", "single + batch\nrequest artifacts"),
        (798, 340, 190, 92, "Outputs", "decision packet\nreport · LLM prompt"),
        (1010, 220, 150, 112, "Monitoring", "quality gates\ndrift smoke\ndashboard"),
    ]
    content = """
      <rect width="1200" height="620" fill="#F8FAFC"/>
      <text x="54" y="56" class="metricDark">System architecture</text>
      <text x="54" y="82" class="darkBody">A reviewer can trace the project from data contract to API artifacts without opening a notebook.</text>
    """
    for x, y, w, h, label, body in nodes:
        content += rounded_rect(x, y, w, h, "#FFFFFF", "#CBD5E1", 20, extra='filter="url(#soft)"')
        content += text(x + 22, y + 34, label, "darkLabel")
        for i, line in enumerate(body.split("\\n")):
            content += text(x + 22, y + 60 + i * 19, line, "darkBody")
    # arrows
    paths = [
        (244, 142, 302, 142, "#38BDF8"),
        (492, 142, 550, 142, "#38BDF8"),
        (740, 142, 798, 142, "#38BDF8"),
        (895, 188, 895, 340, "#A78BFA"),
        (492, 386, 550, 386, "#34D399"),
        (740, 386, 798, 386, "#34D399"),
        (988, 386, 1040, 332, "#34D399"),
        (645, 188, 397, 340, "#A78BFA"),
    ]
    for x1, y1, x2, y2, color in paths:
        content += f'<path d="M{x1} {y1} C{(x1+x2)//2} {y1} {(x1+x2)//2} {y2} {x2} {y2}" stroke="{color}" stroke-width="4" marker-end="url(#arrow)" fill="none" stroke-linecap="round"/>'
    content += """
      <rect x="54" y="506" width="1090" height="62" rx="18" fill="#EFF6FF" stroke="#BFDBFE"/>
      <text x="84" y="542" class="darkLabel">Portfolio signal:</text>
      <text x="245" y="542" class="darkBody">not just a model file — it shows API boundaries, validation hygiene, monitoring artifacts, and reviewer-ready outputs.</text>
    """
    write("architecture_flow.svg", svg_shell(1200, 620, content, bg="#F8FAFC"))


def reviewer_flow():
    steps = [
        (70, 150, "1", "Clone", "install requirements"),
        (295, 150, "2", "Run demo", "build artifacts"),
        (520, 150, "3", "Open dashboard", "visual review"),
        (745, 150, "4", "Check API", "FastAPI docs"),
        (970, 150, "5", "Discuss tradeoffs", "leakage · data · limits"),
    ]
    content = """
      <rect width="1200" height="380" fill="#0B1220"/>
      <text x="60" y="64" class="metric">Three-minute reviewer path</text>
      <text x="60" y="96" class="subtitle">The README now guides a hiring manager through the exact artifacts worth checking.</text>
    """
    for x, y, n, title, desc in steps:
        content += f'<circle cx="{x+55}" cy="{y-52}" r="26" fill="#38BDF8" opacity=".95"/>'
        content += f'<text x="{x+55}" y="{y-43}" text-anchor="middle" style="font:900 24px -apple-system,BlinkMacSystemFont,Segoe UI,Arial; fill:#0F172A">{n}</text>'
        content += rounded_rect(x, y, 150, 92, "#111827", "#334155", 22, extra='filter="url(#soft)"')
        content += text(x+22, y+38, title, "label")
        content += text(x+22, y+66, desc, "body")
    for x1 in [220, 445, 670, 895]:
        content += f'<path d="M{x1} 196 C{x1+35} 178 {x1+70} 178 {x1+100} 196" stroke="#A78BFA" stroke-width="5" fill="none" marker-end="url(#arrow)" stroke-linecap="round"/>'
        content += f'<path d="M{x1+34} 217 L{x1+50} 230 L{x1+66} 217" stroke="#34D399" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity=".8"/>'
    write("reviewer_flow.svg", svg_shell(1200, 380, content))


def validation_monitoring():
    content = """
      <rect width="1200" height="500" fill="#F8FAFC"/>
      <text x="60" y="58" class="metricDark">Validation + monitoring story</text>
      <text x="60" y="86" class="darkBody">The project does not claim investment accuracy; it shows engineering controls around risk scoring.</text>
      <g transform="translate(70 135)">
        <rect x="0" y="0" width="1060" height="88" rx="20" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#soft)"/>
        <text x="28" y="36" class="darkLabel">Walk-forward validation</text>
        <text x="28" y="62" class="darkBody">Train on older quarters → test on the next quarter → repeat. Avoids the random-split trap.</text>
        <line x1="430" y1="44" x2="985" y2="44" stroke="#CBD5E1" stroke-width="6" stroke-linecap="round"/>
        <circle cx="460" cy="44" r="15" fill="#38BDF8"/><circle cx="560" cy="44" r="15" fill="#38BDF8"/><circle cx="660" cy="44" r="15" fill="#A78BFA"/><circle cx="760" cy="44" r="15" fill="#34D399"/><circle cx="860" cy="44" r="15" fill="#34D399"/><circle cx="960" cy="44" r="15" fill="#34D399"/>
        <text x="440" y="78" class="small">Q1</text><text x="540" y="78" class="small">Q2</text><text x="640" y="78" class="small">Q3</text><text x="740" y="78" class="small">Q4</text><text x="840" y="78" class="small">Q5</text><text x="940" y="78" class="small">Q6</text>
      </g>
      <g transform="translate(70 270)">
        <rect x="0" y="0" width="330" height="128" rx="22" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#soft)"/>
        <text x="24" y="40" class="darkLabel">Data quality gates</text>
        <text x="24" y="68" class="darkBody">required columns · null checks</text>
        <text x="24" y="92" class="darkBody">company / quarter coverage</text>
        <circle cx="288" cy="40" r="20" fill="#DCFCE7"/><path d="M278 40 L286 48 L300 31" stroke="#16A34A" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
      <g transform="translate(450 270)">
        <rect x="0" y="0" width="330" height="128" rx="22" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#soft)"/>
        <text x="24" y="40" class="darkLabel">Drift smoke check</text>
        <text x="24" y="68" class="darkBody">latest quarter vs history</text>
        <text x="24" y="92" class="darkBody">standardized deltas</text>
        <path d="M245 88 C265 28 285 88 306 38" stroke="#A78BFA" stroke-width="5" fill="none" stroke-linecap="round"/>
      </g>
      <g transform="translate(830 270)">
        <rect x="0" y="0" width="330" height="128" rx="22" fill="#FFFFFF" stroke="#CBD5E1" filter="url(#soft)"/>
        <text x="24" y="40" class="darkLabel">Feature explanations</text>
        <text x="24" y="68" class="darkBody">global importance packet</text>
        <text x="24" y="92" class="darkBody">decision snapshot factors</text>
        <rect x="244" y="34" width="18" height="66" rx="6" fill="#38BDF8"/><rect x="272" y="54" width="18" height="46" rx="6" fill="#A78BFA"/><rect x="300" y="22" width="18" height="78" rx="6" fill="#34D399"/>
      </g>
    """
    write("validation_monitoring.svg", svg_shell(1200, 500, content, bg="#F8FAFC"))


def dashboard_preview():
    content = """
      <rect width="1200" height="700" fill="#E2E8F0"/>
      <rect x="70" y="48" width="1060" height="604" rx="30" fill="#F8FAFC" stroke="#CBD5E1" filter="url(#shadow)"/>
      <rect x="70" y="48" width="1060" height="118" rx="30" fill="#111827"/>
      <text x="110" y="96" class="subtitle">Portfolio artifact · static HTML dashboard</text>
      <text x="110" y="136" class="metric">Quarterly Financial Risk Scoring</text>
      <rect x="890" y="92" width="170" height="42" rx="21" fill="#FEF3C7"/>
      <text x="975" y="119" text-anchor="middle" style="font:800 15px -apple-system,BlinkMacSystemFont,Segoe UI,Arial; fill:#92400E">Risk: medium</text>
      <g transform="translate(110 205)">
        <rect x="0" y="0" width="220" height="112" rx="20" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="22" y="36" class="darkBody">Margin risk</text><text x="22" y="82" class="metricDark">0.62</text>
        <rect x="250" y="0" width="220" height="112" rx="20" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="272" y="36" class="darkBody">Drawdown proxy</text><text x="272" y="82" class="metricDark">0.48</text>
        <rect x="500" y="0" width="220" height="112" rx="20" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="522" y="36" class="darkBody">Liquidity stress</text><text x="522" y="82" class="metricDark">0.31</text>
        <rect x="750" y="0" width="220" height="112" rx="20" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="772" y="36" class="darkBody">Selected model</text><text x="772" y="82" style="font:900 24px -apple-system,BlinkMacSystemFont,Segoe UI,Arial; fill:#0F172A">RandomForest</text>
      </g>
      <g transform="translate(110 355)">
        <rect x="0" y="0" width="470" height="220" rx="22" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="24" y="42" class="darkLabel">Leaderboard</text>
        <rect x="24" y="74" width="390" height="18" rx="9" fill="#E2E8F0"/><rect x="24" y="74" width="285" height="18" rx="9" fill="#38BDF8"/>
        <rect x="24" y="114" width="390" height="18" rx="9" fill="#E2E8F0"/><rect x="24" y="114" width="245" height="18" rx="9" fill="#A78BFA"/>
        <rect x="24" y="154" width="390" height="18" rx="9" fill="#E2E8F0"/><rect x="24" y="154" width="160" height="18" rx="9" fill="#94A3B8"/>
        <text x="330" y="91" class="darkBody">RF</text><text x="330" y="131" class="darkBody">LogReg</text><text x="330" y="171" class="darkBody">Dummy</text>
      </g>
      <g transform="translate(620 355)">
        <rect x="0" y="0" width="440" height="220" rx="22" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="24" y="42" class="darkLabel">Monitoring packet</text>
        <circle cx="70" cy="100" r="34" fill="#DCFCE7"/><path d="M54 98 L66 111 L90 82" stroke="#16A34A" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <text x="118" y="92" class="darkLabel">Quality gates pass</text>
        <text x="118" y="120" class="darkBody">schema · nulls · coverage</text>
        <path d="M62 176 C112 102 170 190 226 132 C282 76 326 152 386 106" stroke="#A78BFA" stroke-width="5" fill="none" stroke-linecap="round"/>
      </g>
    """
    write("dashboard_preview.svg", svg_shell(1200, 700, content, bg="#E2E8F0"))


if __name__ == "__main__":
    hero()
    architecture()
    reviewer_flow()
    validation_monitoring()
    dashboard_preview()
    print(f"assets={ASSET_DIR}")
