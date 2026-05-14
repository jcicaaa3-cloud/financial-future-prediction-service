from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
SNAPSHOT_DIR = ROOT / "examples" / "portfolio_snapshot"

COLORS = {
    "bg": "#08111f",
    "bg2": "#0f172a",
    "card": "#111827",
    "card2": "#162033",
    "line": "#3b82f6",
    "line2": "#22c55e",
    "hot": "#f97316",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "cyan": "#38bdf8",
    "purple": "#a78bfa",
    "green": "#34d399",
    "yellow": "#facc15",
    "red": "#fb7185",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def rounded_rect(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str | None = None, width: int = 2, radius: int = 18) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str, fnt: ImageFont.ImageFont, fill: str) -> None:
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=4, align="center")
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = xy[0] + (xy[2] - xy[0] - w) / 2
    y = xy[1] + (xy[3] - xy[1] - h) / 2
    draw.multiline_text((x, y), text, font=fnt, fill=fill, align="center", spacing=4)


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str, width: int = 6) -> None:
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 16
    p1 = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    p2 = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=color)


def add_subtle_grid(draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
    for x in range(0, width, 48):
        draw.line([(x, 0), (x, height)], fill="#0b2036", width=1)
    for y in range(0, height, 48):
        draw.line([(0, y), (width, y)], fill="#0b2036", width=1)


def build_pipeline_motion_gif() -> None:
    width, height = 1200, 360
    stages = [
        "CSV\nContract",
        "Feature\nEngineering",
        "Leakage\nGuard",
        "Model\nLeaderboard",
        "FastAPI\nScoring",
        "Dashboard\n+ LLM Packet",
    ]
    box_w, box_h = 158, 92
    top = 168
    gap = (width - 80 - box_w * len(stages)) // (len(stages) - 1)
    boxes = []
    for i in range(len(stages)):
        x = 40 + i * (box_w + gap)
        boxes.append((x, top, x + box_w, top + box_h))

    frames = []
    for frame in range(30):
        active = frame % (len(stages) - 1)
        pulse = 0.5 + 0.5 * math.sin(frame / 30 * math.pi * 2)
        img = Image.new("RGB", (width, height), COLORS["bg"])
        draw = ImageDraw.Draw(img)
        add_subtle_grid(draw, width, height)

        draw.text((40, 34), "Quarterly Financial Risk Scoring Service", font=font(36, True), fill=COLORS["text"])
        draw.text((42, 84), "A portfolio-grade ML backend: data contract → leakage guard → model evidence → API → reviewer dashboard", font=font(21), fill=COLORS["muted"])
        draw.text((42, 120), "Not an investment-advice toy. A service-oriented ML engineering case study.", font=font(18, True), fill=COLORS["green"])

        # arrows behind boxes
        for i in range(len(boxes) - 1):
            s = (boxes[i][2] + 8, boxes[i][1] + box_h // 2)
            e = (boxes[i + 1][0] - 8, boxes[i + 1][1] + box_h // 2)
            c = COLORS["hot"] if i == active else "#1d4ed8"
            w = 9 if i == active else 5
            draw_arrow(draw, s, e, c, w)
            if i == active:
                # moving dot / spark
                t = pulse
                dot = (int(s[0] + (e[0] - s[0]) * t), int(s[1] + (e[1] - s[1]) * t))
                draw.ellipse((dot[0]-9, dot[1]-9, dot[0]+9, dot[1]+9), fill=COLORS["yellow"], outline="#fff7ed", width=2)

        for i, (x1, y1, x2, y2) in enumerate(boxes):
            if i == active or i == active + 1:
                outline = COLORS["yellow"]
                fill = "#15223a"
                w = 4
            else:
                outline = "#334155"
                fill = COLORS["card"]
                w = 2
            rounded_rect(draw, (x1, y1, x2, y2), fill=fill, outline=outline, width=w, radius=18)
            text_center(draw, (x1 + 8, y1 + 5, x2 - 8, y2 - 5), stages[i], font(18, True), COLORS["text"])

        # bottom proof chips
        chips = ["FastAPI", "Docker", "CI", "pytest", "walk-forward", "monitoring", "LLM-ready"]
        x = 42
        for chip in chips:
            tw = draw.textlength(chip, font=font(15, True))
            rounded_rect(draw, (int(x), 300, int(x + tw + 28), 330), fill="#0b2542", outline="#2563eb", width=1, radius=14)
            draw.text((x + 14, 306), chip, font=font(15, True), fill="#bfdbfe")
            x += tw + 42
        frames.append(img)

    frames[0].save(
        ASSET_DIR / "pipeline_motion.gif",
        save_all=True,
        append_images=frames[1:],
        duration=110,
        loop=0,
        optimize=True,
    )


def svg_box(x: int, y: int, w: int, h: int, title: str, subtitle: str, color: str) -> str:
    title_esc = title.replace("&", "&amp;")
    subtitle_esc = subtitle.replace("&", "&amp;")
    return f'''
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#111827" stroke="{color}" stroke-width="2"/>
      <text x="{x+18}" y="{y+34}" fill="#f8fafc" font-size="20" font-weight="700">{title_esc}</text>
      <text x="{x+18}" y="{y+62}" fill="#94a3b8" font-size="14">{subtitle_esc}</text>
    </g>'''


def svg_arrow(x1: int, y1: int, x2: int, y2: int, color: str = "#38bdf8") -> str:
    return f'''
      <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="4" stroke-linecap="round" marker-end="url(#arrow)"/>'''


def build_system_architecture_svg() -> None:
    svg = f'''<svg width="1280" height="760" viewBox="0 0 1280 760" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="760" gradientUnits="userSpaceOnUse">
      <stop stop-color="#07111f"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#38bdf8" />
    </marker>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1280" height="760" fill="url(#bg)"/>
  <g opacity="0.25">
    {''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="760" stroke="#1e293b"/>' for x in range(0,1280,64))}
    {''.join(f'<line x1="0" y1="{y}" x2="1280" y2="{y}" stroke="#1e293b"/>' for y in range(0,760,64))}
  </g>
  <text x="52" y="68" fill="#f8fafc" font-size="34" font-weight="800">System Architecture</text>
  <text x="52" y="104" fill="#94a3b8" font-size="18">Reviewer sees a service boundary, not a loose notebook: validated inputs → leakage-aware ML → API/reporting/monitoring outputs.</text>

  <text x="54" y="164" fill="#38bdf8" font-size="18" font-weight="800">1. Inputs</text>
  {svg_box(54, 185, 210, 88, "Company master", "company_id, sector", "#38bdf8")}
  {svg_box(54, 296, 210, 88, "Financials", "quarterly statements", "#38bdf8")}
  {svg_box(54, 407, 210, 88, "Market + macro", "returns, rates, FX", "#38bdf8")}
  {svg_box(54, 518, 210, 88, "Disclosures", "risk text proxies", "#38bdf8")}

  <text x="384" y="164" fill="#a78bfa" font-size="18" font-weight="800">2. ML Pipeline</text>
  {svg_box(384, 185, 244, 86, "Schema validation", "fail fast on bad CSV", "#a78bfa")}
  {svg_box(384, 304, 244, 86, "Panel builder", "company-quarter table", "#a78bfa")}
  {svg_box(384, 423, 244, 86, "Feature factory", "ratios + rolling windows", "#a78bfa")}
  {svg_box(384, 542, 244, 86, "Leakage guard", "available-at-time split", "#facc15")}

  {svg_box(730, 185, 244, 86, "Target builder", "next-quarter labels", "#22c55e")}
  {svg_box(730, 304, 244, 86, "Walk-forward eval", "chronological evidence", "#22c55e")}
  {svg_box(730, 423, 244, 86, "Model leaderboard", "dummy/logit/RF", "#22c55e")}
  {svg_box(730, 542, 244, 86, "Decision packet", "scores + explanations", "#22c55e")}

  <text x="1060" y="164" fill="#fb7185" font-size="18" font-weight="800">3. Interfaces</text>
  {svg_box(1040, 185, 216, 72, "FastAPI", "/v1/predictions", "#fb7185")}
  {svg_box(1040, 286, 216, 72, "Batch scoring", "train once, score many", "#fb7185")}
  {svg_box(1040, 387, 216, 72, "Monitoring", "quality + drift reports", "#fb7185")}
  {svg_box(1040, 488, 216, 72, "Dashboard", "static reviewer artifact", "#fb7185")}
  {svg_box(1040, 589, 216, 72, "LLM packet", "memo-ready context", "#fb7185")}

  {svg_arrow(278, 230, 368, 230)} {svg_arrow(278, 341, 368, 341)} {svg_arrow(278, 452, 368, 452)} {svg_arrow(278, 563, 368, 563)}
  {svg_arrow(628, 229, 716, 229)} {svg_arrow(628, 348, 716, 348)} {svg_arrow(628, 467, 716, 467)} {svg_arrow(628, 586, 716, 586)}
  {svg_arrow(974, 229, 1026, 221)} {svg_arrow(974, 467, 1026, 322)} {svg_arrow(974, 467, 1026, 423)} {svg_arrow(974, 586, 1026, 524)} {svg_arrow(974, 586, 1026, 625)}

  <rect x="52" y="688" width="1172" height="44" rx="16" fill="#0b2542" stroke="#2563eb"/>
  <text x="76" y="717" fill="#bfdbfe" font-size="16" font-weight="700">Portfolio proof:</text>
  <text x="220" y="717" fill="#f8fafc" font-size="16">pytest · Docker · GitHub Actions · model card · API contract · dashboard snapshot · no real-money recommendation claim</text>
</svg>'''
    (ASSET_DIR / "system_architecture.svg").write_text(svg, encoding="utf-8")


def read_snapshot() -> dict[str, Any]:
    p = SNAPSHOT_DIR / "decision_packet.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def draw_dashboard_preview() -> None:
    packet = read_snapshot()
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), "#f8fafc")
    draw = ImageDraw.Draw(img)
    # left dark sidebar
    draw.rectangle((0, 0, width, height), fill="#f1f5f9")
    draw.rectangle((0, 0, width, 124), fill="#0f172a")
    draw.text((48, 32), "Portfolio Dashboard Preview", font=font(36, True), fill="#f8fafc")
    draw.text((50, 82), "Generated artifact: decision packet · risk report · metrics · monitoring · LLM prompt", font=font(20), fill="#cbd5e1")

    company = packet.get("company_name", "Sample Company")
    company_id = packet.get("company_id", "C003")
    quarter = packet.get("quarter", "2025Q4")
    risk_level = packet.get("risk_level", "MODERATE")
    scores = packet.get("scores", {}) or {}

    # hero card
    rounded_rect(draw, (48, 156, 1232, 306), fill="#ffffff", outline="#cbd5e1", width=2, radius=24)
    draw.text((82, 188), f"{company} ({company_id})", font=font(30, True), fill="#0f172a")
    draw.text((82, 232), f"Quarter: {quarter} · Risk level: {risk_level}", font=font(22, True), fill="#dc2626" if risk_level.upper() == "HIGH" else "#f97316")
    draw.text((720, 190), "Reviewer signal", font=font(18, True), fill="#475569")
    draw.text((720, 225), "Service-shaped ML project, not a notebook demo", font=font(24, True), fill="#0f172a")
    draw.text((720, 263), "FastAPI · baseline leaderboard · leakage-aware validation · monitoring", font=font(18), fill="#64748b")

    # scores
    labels = list(scores.keys())[:3]
    if not labels:
        labels = ["margin_deterioration_risk", "drawdown_proxy_risk", "liquidity_stress_risk"]
        scores = {labels[0]: 0.42, labels[1]: 0.61, labels[2]: 0.35}
    card_y = 338
    for idx, key in enumerate(labels):
        x = 48 + idx * 405
        rounded_rect(draw, (x, card_y, x + 370, card_y + 138), fill="#ffffff", outline="#cbd5e1", width=2, radius=20)
        label = key.replace("_", " ").title()
        value = float(scores.get(key, 0.0))
        draw.text((x + 26, card_y + 24), label, font=font(18, True), fill="#475569")
        draw.text((x + 26, card_y + 62), f"{value:.3f}", font=font(42, True), fill="#0f172a")
        # bar
        draw.rounded_rectangle((x + 178, card_y + 80, x + 340, card_y + 96), radius=8, fill="#e2e8f0")
        draw.rounded_rectangle((x + 178, card_y + 80, x + 178 + int(162 * max(0, min(1, value))), card_y + 96), radius=8, fill="#2563eb")

    # bottom panels
    rounded_rect(draw, (48, 512, 610, 674), fill="#ffffff", outline="#cbd5e1", width=2, radius=20)
    draw.text((76, 536), "Evidence artifacts", font=font(22, True), fill="#0f172a")
    artifacts = ["decision_packet.json", "portfolio_dashboard.html", "walk_forward_metrics.json", "data_quality_report.json", "risk_report.md"]
    for i, item in enumerate(artifacts):
        draw.text((82, 576 + i * 24), f"✓ {item}", font=font(17), fill="#334155")

    rounded_rect(draw, (650, 512, 1232, 674), fill="#ffffff", outline="#cbd5e1", width=2, radius=20)
    draw.text((678, 536), "API surface", font=font(22, True), fill="#0f172a")
    endpoints = ["GET /health", "POST /v1/predictions", "POST /v1/batch-predictions", "GET /v1/models/latest/leaderboard", "GET /v1/monitoring/latest/drift"]
    for i, item in enumerate(endpoints):
        draw.text((684, 576 + i * 24), f"→ {item}", font=font(17), fill="#334155")

    img.save(ASSET_DIR / "dashboard_preview.png")


def draw_social_preview() -> None:
    width, height = 1280, 640
    img = Image.new("RGB", (width, height), COLORS["bg"])
    draw = ImageDraw.Draw(img)
    add_subtle_grid(draw, width, height)
    # decorative arrows
    for i, color in enumerate([COLORS["cyan"], COLORS["purple"], COLORS["green"], COLORS["hot"]]):
        y = 130 + i * 74
        draw_arrow(draw, (760, y), (1110, y + 36), color, width=10)
    draw.text((70, 78), "Quarterly Financial", font=font(58, True), fill=COLORS["text"])
    draw.text((70, 146), "Risk Scoring Service", font=font(58, True), fill=COLORS["text"])
    draw.text((74, 238), "Portfolio-grade ML backend for financial risk signals", font=font(28, True), fill=COLORS["cyan"])
    draw.text((74, 292), "FastAPI · Docker · CI · walk-forward validation · monitoring · dashboard", font=font(24), fill=COLORS["muted"])
    # chips
    chips = ["Data contract", "Leakage guard", "Model leaderboard", "LLM packet"]
    x = 74
    for chip in chips:
        tw = draw.textlength(chip, font=font(20, True))
        rounded_rect(draw, (int(x), 408, int(x + tw + 34), 456), fill="#0b2542", outline="#2563eb", width=2, radius=22)
        draw.text((x + 17, 419), chip, font=font(20, True), fill="#bfdbfe")
        x += tw + 50
    draw.text((74, 548), "Not investment advice. Built to demonstrate ML service engineering.", font=font(21, True), fill=COLORS["yellow"])
    img.save(ASSET_DIR / "github_social_preview.png")


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    build_pipeline_motion_gif()
    build_system_architecture_svg()
    draw_dashboard_preview()
    draw_social_preview()
    (ASSET_DIR / "README.md").write_text(
        """# README visual assets

These files are generated by `python scripts/export_readme_assets.py` and are embedded in the repository README.

- `pipeline_motion.gif`: animated hero image for the README top section.
- `system_architecture.svg`: static architecture diagram.
- `dashboard_preview.png`: static dashboard preview for GitHub README.
- `github_social_preview.png`: optional repository social preview image for GitHub settings.
""".strip()
        + "\n",
        encoding="utf-8",
    )
    print(f"generated={ASSET_DIR}")


if __name__ == "__main__":
    main()
