from __future__ import annotations

from pathlib import Path
import os
import sys
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"

COLORS = {
    "navy": (10, 18, 32),
    "navy2": (14, 24, 43),
    "slate": (30, 41, 59),
    "slate2": (51, 65, 85),
    "muted": (148, 163, 184),
    "line": (71, 85, 105),
    "white": (248, 250, 252),
    "card": (15, 23, 42),
    "card2": (22, 33, 53),
    "cyan": (34, 211, 238),
    "blue": (96, 165, 250),
    "green": (74, 222, 128),
    "amber": (251, 191, 36),
    "red": (248, 113, 113),
    "purple": (168, 85, 247),
}

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REGULAR)
    return ImageFont.truetype(path, size=size)


def gradient_background(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), COLORS["navy"])
    px = img.load()
    for y in range(height):
        for x in range(width):
            rx = x / max(width - 1, 1)
            ry = y / max(height - 1, 1)
            r = int(10 + 18 * rx + 8 * ry)
            g = int(18 + 23 * rx + 11 * ry)
            b = int(32 + 46 * rx + 18 * ry)
            # soft cyan/purple glows
            dx1 = (x - width * 0.12) / width
            dy1 = (y - height * 0.18) / height
            glow1 = max(0, 1 - (dx1 * dx1 + dy1 * dy1) * 18)
            dx2 = (x - width * 0.84) / width
            dy2 = (y - height * 0.72) / height
            glow2 = max(0, 1 - (dx2 * dx2 + dy2 * dy2) * 14)
            r = min(255, int(r + 22 * glow2))
            g = min(255, int(g + 40 * glow1 + 10 * glow2))
            b = min(255, int(b + 45 * glow1 + 30 * glow2))
            px[x, y] = (r, g, b)
    return img


def rounded(draw: ImageDraw.ImageDraw, xy, radius: int, fill, outline=None, width: int = 1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text(draw: ImageDraw.ImageDraw, xy, s: str, size: int, fill=COLORS["white"], bold=False, mono=False, anchor=None, align="left"):
    draw.text(xy, s, font=font(size, bold=bold, mono=mono), fill=fill, anchor=anchor, align=align)


def wrap_text(draw: ImageDraw.ImageDraw, s: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = s.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font_obj)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw: ImageDraw.ImageDraw, xy, s: str, size: int, max_width: int, fill=COLORS["muted"], bold=False, line_gap=8):
    f = font(size, bold=bold)
    x, y = xy
    for line in wrap_text(draw, s, f, max_width):
        draw.text((x, y), line, font=f, fill=fill)
        y += size + line_gap
    return y


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill, width: int = 5):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=fill, width=width)
    # arrow head
    import math

    angle = math.atan2(y2 - y1, x2 - x1)
    length = 18
    spread = 0.55
    p1 = (x2 - length * math.cos(angle - spread), y2 - length * math.sin(angle - spread))
    p2 = (x2 - length * math.cos(angle + spread), y2 - length * math.sin(angle + spread))
    draw.polygon([end, p1, p2], fill=fill)


def chip(draw, xy, label: str, fill, outline=None, text_fill=COLORS["white"], pad_x=18, pad_y=9, size=24):
    f = font(size, bold=True)
    x, y = xy
    bbox = draw.textbbox((0, 0), label, font=f)
    w = bbox[2] - bbox[0] + pad_x * 2
    h = bbox[3] - bbox[1] + pad_y * 2
    rounded(draw, (x, y, x + w, y + h), 999, fill=fill, outline=outline or fill, width=1)
    draw.text((x + pad_x, y + pad_y - 2), label, font=f, fill=text_fill)
    return w, h


def card(draw, xy, wh, title: str, body: str, accent, icon: str | None = None):
    x, y = xy
    w, h = wh
    rounded(draw, (x + 6, y + 8, x + w + 6, y + h + 8), 24, fill=(4, 8, 15))
    rounded(draw, (x, y, x + w, y + h), 24, fill=COLORS["card2"], outline=(51, 65, 85), width=2)
    draw.line((x + 24, y + 1, x + w - 24, y + 1), fill=accent, width=3)
    if icon:
        rounded(draw, (x + 22, y + 24, x + 70, y + 72), 14, fill=accent)
        text(draw, (x + 46, y + 46), icon, 23, fill=COLORS["navy"], bold=True, anchor="mm")
        title_x = x + 86
    else:
        title_x = x + 24
    text(draw, (title_x, y + 25), title, 24, fill=COLORS["white"], bold=True)
    draw_wrapped(draw, (x + 24, y + 84), body, 20, w - 48, fill=COLORS["muted"], line_gap=8)


def hero() -> None:
    W, H = 1600, 760
    img = gradient_background(W, H)
    d = ImageDraw.Draw(img)

    # grid dots
    for x in range(60, W, 80):
        for y in range(58, H, 80):
            if (x + y) % 3 == 0:
                d.ellipse((x, y, x + 3, y + 3), fill=(45, 67, 93))

    chip(d, (80, 72), "PORTFOLIO-GRADE ML BACKEND", fill=(8, 47, 73), outline=(34, 211, 238), size=22)
    text(d, (80, 145), "Quarterly Financial", 72, bold=True)
    text(d, (80, 232), "Risk Scoring Service", 70, bold=True, fill=(220, 252, 231))
    draw_wrapped(
        d,
        (82, 338),
        "Leakage-aware company-quarter pipeline with FastAPI inference, chronological validation, model leaderboard, monitoring artifacts, and reviewer-ready dashboard.",
        28,
        860,
        fill=(203, 213, 225),
        line_gap=10,
    )

    # right mock result panel
    x0, y0, w0, h0 = 1080, 94, 430, 420
    rounded(d, (x0 + 10, y0 + 12, x0 + w0 + 10, y0 + h0 + 12), 28, fill=(3, 7, 18))
    rounded(d, (x0, y0, x0 + w0, y0 + h0), 28, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    text(d, (x0 + 34, y0 + 38), "Decision packet", 29, bold=True)
    chip(d, (x0 + 306, y0 + 34), "MEDIUM", fill=(113, 63, 18), outline=(251, 191, 36), size=17)
    metrics = [("margin_deterioration", "0.631", COLORS["amber"]), ("drawdown_proxy", "0.482", COLORS["blue"]), ("liquidity_stress", "0.287", COLORS["green"])]
    yy = y0 + 105
    for name, value, color in metrics:
        rounded(d, (x0 + 34, yy, x0 + w0 - 34, yy + 78), 18, fill=(22, 33, 53), outline=(51, 65, 85), width=1)
        text(d, (x0 + 56, yy + 21), name, 21, fill=(203, 213, 225))
        text(d, (x0 + w0 - 92, yy + 20), value, 32, bold=True, fill=color, anchor=None)
        d.rectangle((x0 + 56, yy + 58, x0 + 320, yy + 65), fill=(51, 65, 85))
        d.rectangle((x0 + 56, yy + 58, x0 + 56 + int(float(value) * 264), yy + 65), fill=color)
        yy += 96
    text(d, (x0 + 34, y0 + h0 - 50), "JSON · Markdown · LLM packet · Dashboard", 17, fill=COLORS["muted"], mono=True)

    # flow rail
    steps = [
        ("CSV contract", "schema gates", COLORS["cyan"], "1"),
        ("Feature factory", "leakage guard", COLORS["blue"], "2"),
        ("Leaderboard", "baseline comparison", COLORS["purple"], "3"),
        ("FastAPI", "sync + batch", COLORS["green"], "4"),
        ("Dashboard", "reviewer artifact", COLORS["amber"], "5"),
    ]
    sx, sy = 82, 582
    cw, ch, gap = 246, 104, 32
    for i, (title, body, color, icon) in enumerate(steps):
        x = sx + i * (cw + gap)
        rounded(d, (x, sy, x + cw, sy + ch), 22, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        rounded(d, (x + 18, sy + 24, x + 54, sy + 60), 12, fill=color)
        text(d, (x + 36, sy + 42), icon, 17, fill=COLORS["navy"], bold=True, anchor="mm")
        text(d, (x + 70, sy + 22), title, 22, bold=True)
        text(d, (x + 70, sy + 57), body, 18, fill=COLORS["muted"])
        if i < len(steps) - 1:
            arrow(d, (x + cw + 6, sy + ch // 2), (x + cw + gap - 6, sy + ch // 2), fill=(34, 211, 238), width=4)

    img.save(ASSET_DIR / "github_hero.png", quality=95)


def architecture() -> None:
    W, H = 1600, 1020
    img = gradient_background(W, H)
    d = ImageDraw.Draw(img)
    text(d, (80, 62), "System Architecture", 58, bold=True)
    text(d, (82, 132), "A service-shaped ML project: contracts, validation, API boundary, and review artifacts.", 28, fill=(203, 213, 225))

    columns = [
        ("Input layer", [("Company master", "sector, identifiers"), ("Financials", "quarterly statements"), ("Market / macro", "price + macro context"), ("Disclosure fields", "risk signal proxies")], COLORS["cyan"]),
        ("Feature factory", [("Schema validation", "required files + dtypes"), ("Panel builder", "company-quarter grain"), ("Leakage guard", "available-at-time fields"), ("Target builder", "next-quarter labels")], COLORS["blue"]),
        ("Model layer", [("Baseline suite", "dummy / logistic / RF"), ("Chronological split", "no random-only validation"), ("Walk-forward eval", "quarter-by-quarter test"), ("Feature importance", "reviewable signals")], COLORS["purple"]),
        ("Service layer", [("FastAPI", "single + batch scoring"), ("Decision packet", "risk score + metadata"), ("Monitoring", "quality + drift reports"), ("Artifacts", "report + LLM prompt")], COLORS["green"]),
        ("Reviewer layer", [("Dashboard HTML", "open in browser"), ("GitHub README", "visual narrative"), ("Model card", "caveats + scope"), ("Case study", "interview talking points")], COLORS["amber"]),
    ]
    top = 205
    col_w = 270
    gap = 25
    left = 70
    for idx, (title, rows, accent) in enumerate(columns):
        x = left + idx * (col_w + gap)
        rounded(d, (x + 8, top + 10, x + col_w + 8, top + 710), 28, fill=(4, 8, 15))
        rounded(d, (x, top, x + col_w, top + 710), 28, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        rounded(d, (x + 22, top + 24, x + col_w - 22, top + 80), 18, fill=accent)
        text(d, (x + col_w // 2, top + 52), title, 24, bold=True, fill=COLORS["navy"], anchor="mm")
        yy = top + 120
        for name, body in rows:
            rounded(d, (x + 22, yy, x + col_w - 22, yy + 118), 18, fill=(22, 33, 53), outline=(51, 65, 85), width=1)
            text(d, (x + 42, yy + 22), name, 21, bold=True)
            draw_wrapped(d, (x + 42, yy + 54), body, 18, col_w - 86, fill=COLORS["muted"], line_gap=4)
            yy += 142
        if idx < len(columns) - 1:
            y_mid = top + 360
            arrow(d, (x + col_w + 6, y_mid), (x + col_w + gap - 7, y_mid), fill=(34, 211, 238), width=5)

    # bottom governance rail
    rounded(d, (100, 915, W - 100, 974), 20, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    rail = "Synthetic sample only · not investment advice · not credit screening · leakage-aware validation · reproducible artifacts"
    text(d, (W // 2, 945), rail, 24, fill=(203, 213, 225), anchor="mm")
    img.save(ASSET_DIR / "architecture_diagram.png", quality=95)


def dashboard_preview() -> None:
    W, H = 1600, 920
    bg = Image.new("RGB", (W, H), (241, 245, 249))
    d = ImageDraw.Draw(bg)
    rounded(d, (90, 60, W - 90, H - 60), 30, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    rounded(d, (90, 60, W - 90, 145), 30, fill=(15, 23, 42))
    d.rectangle((90, 106, W - 90, 145), fill=(15, 23, 42))
    for i, color in enumerate([(248, 113, 113), (251, 191, 36), (74, 222, 128)]):
        d.ellipse((128 + i * 34, 92, 146 + i * 34, 110), fill=color)
    text(d, (228, 90), "portfolio_dashboard.html", 22, fill=(203, 213, 225), mono=True)

    # header
    rounded(d, (120, 175, W - 120, 330), 24, fill=(15, 23, 42))
    text(d, (155, 205), "Quarterly Financial Risk Scoring Dashboard", 40, bold=True)
    text(d, (157, 260), "Synthetic reviewer snapshot · C003 · Manufacturing · 2024Q4", 24, fill=(203, 213, 225))
    chip(d, (1230, 216), "RISK: MEDIUM", fill=(113, 63, 18), outline=(251, 191, 36), size=22)

    # kpi cards
    kpis = [("Margin deterioration", "0.631", COLORS["amber"]), ("Drawdown proxy", "0.482", COLORS["blue"]), ("Liquidity stress", "0.287", COLORS["green"])]
    x = 120
    for name, val, color in kpis:
        rounded(d, (x, 360, x + 430, 500), 22, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        text(d, (x + 28, 390), name, 23, fill=(71, 85, 105), bold=True)
        text(d, (x + 28, 425), val, 52, fill=color, bold=True)
        d.rectangle((x + 210, 452, x + 390, 464), fill=(226, 232, 240))
        d.rectangle((x + 210, 452, x + 210 + int(float(val) * 180), 464), fill=color)
        x += 460

    # panels
    rounded(d, (120, 535, 765, 830), 22, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    text(d, (150, 565), "Risk factors", 30, fill=(15, 23, 42), bold=True)
    factors = ["Operating margin pressure", "Elevated leverage proxy", "Disclosure risk flag"]
    for i, item in enumerate(factors):
        yy = 625 + i * 58
        rounded(d, (150, yy, 720, yy + 40), 12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        text(d, (170, yy + 10), f"→ {item}", 20, fill=(51, 65, 85))

    rounded(d, (795, 535, W - 120, 830), 22, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    text(d, (825, 565), "Validation leaderboard", 30, fill=(15, 23, 42), bold=True)
    headers = ["Target", "Model", "ROC-AUC", "PR-AUC"]
    xs = [825, 1090, 1240, 1370]
    for xx, h in zip(xs, headers):
        text(d, (xx, 620), h, 18, fill=(71, 85, 105), bold=True)
    rows = [("margin", "random_forest", "0.71", "0.68"), ("drawdown", "logistic", "0.64", "0.59"), ("liquidity", "random_forest", "0.76", "0.72")]
    for i, row in enumerate(rows):
        yy = 660 + i * 54
        d.line((825, yy - 13, W - 160, yy - 13), fill=(226, 232, 240), width=1)
        for xx, value in zip(xs, row):
            text(d, (xx, yy), value, 19, fill=(30, 41, 59), mono=(xx != 825))

    bg.save(ASSET_DIR / "dashboard_preview.png", quality=95)



def api_contract_preview() -> None:
    W, H = 1600, 760
    img = Image.new("RGB", (W, H), (248, 250, 252))
    d = ImageDraw.Draw(img)
    text(d, (70, 58), "API contract preview", 46, fill=(15, 23, 42), bold=True)
    text(d, (72, 112), "The repository exposes model output like a backend service, with inspectable artifacts for review.", 27, fill=(71, 85, 105))

    # client request panel
    rounded(d, (90, 210, 470, 595), 22, fill=(255, 255, 255), outline=(37, 99, 235), width=3)
    text(d, (125, 246), "Client request", 36, fill=(15, 23, 42), bold=True)
    code = [
        "POST /v1/predictions",
        "{",
        '  "company_id": "C003",',
        '  "input_dir": "data/input/sample"',
        "}",
    ]
    yy = 320
    for line in code:
        text(d, (125, yy), line, 21, fill=(51, 65, 85), mono=True)
        yy += 31

    arrow(d, (485, 405), (600, 405), fill=(37, 99, 235), width=6)

    # service panel
    rounded(d, (615, 210, 995, 595), 22, fill=(239, 246, 255), outline=(14, 165, 233), width=3)
    text(d, (645, 246), "FastAPI service", 36, fill=(15, 23, 42), bold=True)
    steps = ["schema validation", "train / load baselines", "score company", "write request artifacts", "return decision packet"]
    yy = 315
    for item in steps:
        rounded(d, (650, yy, 945, yy + 36), 12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        text(d, (670, yy + 8), item, 20, fill=(51, 65, 85))
        yy += 48

    arrow(d, (1010, 405), (1125, 405), fill=(34, 197, 94), width=6)

    # response panel
    rounded(d, (1140, 210, 1510, 595), 22, fill=(255, 255, 255), outline=(22, 163, 74), width=3)
    text(d, (1170, 246), "Response packet", 36, fill=(15, 23, 42), bold=True)
    response = [
        "{",
        '  "risk_level": "low",',
        '  "scores": {...},',
        '  "dashboard_path": "...",',
        '  "metrics_preview": {...}',
        "}",
    ]
    yy = 320
    for line in response:
        text(d, (1170, yy), line, 21, fill=(51, 65, 85), mono=True)
        yy += 31

    rounded(d, (130, 650, 1470, 718), 18, fill=(15, 23, 42))
    text(d, (165, 674), "GET /health · POST /v1/batch-predictions · GET /v1/models/latest/leaderboard · GET /v1/monitoring/latest/drift", 23, fill=(248, 250, 252), mono=True)
    img.save(ASSET_DIR / "api_contract_preview.png", quality=95)


def social_preview() -> None:
    W, H = 1280, 640
    img = gradient_background(W, H)
    d = ImageDraw.Draw(img)
    chip(d, (70, 62), "FASTAPI · ML · MLOPS · FINANCIAL RISK", fill=(8, 47, 73), outline=(34, 211, 238), size=20)
    text(d, (70, 142), "Quarterly Financial", 62, bold=True)
    text(d, (70, 220), "Risk Scoring Service", 68, bold=True, fill=(220, 252, 231))
    draw_wrapped(d, (74, 320), "Leakage-aware validation, baseline leaderboard, monitoring artifacts, and reviewer-ready dashboard for a portfolio-grade ML backend project.", 27, 760, fill=(203, 213, 225), line_gap=10)
    # mini architecture stack right
    labels = [("CSV", COLORS["cyan"]), ("Features", COLORS["blue"]), ("Models", COLORS["purple"]), ("API", COLORS["green"]), ("Dashboard", COLORS["amber"])]
    x0, y0 = 900, 135
    for i, (label, color) in enumerate(labels):
        y = y0 + i * 82
        rounded(d, (x0, y, x0 + 230, y + 55), 16, fill=(15, 23, 42), outline=color, width=2)
        text(d, (x0 + 115, y + 28), label, 22, bold=True, anchor="mm")
        if i < len(labels) - 1:
            arrow(d, (x0 + 115, y + 58), (x0 + 115, y + 77), fill=(34, 211, 238), width=4)
    img.save(ASSET_DIR / "github_social_preview.png", quality=95)


def flow_frame(active: int) -> Image.Image:
    W, H = 1200, 420
    img = gradient_background(W, H)
    d = ImageDraw.Draw(img)
    text(d, (54, 42), "End-to-end scoring flow", 42, bold=True)
    text(d, (56, 96), "The README animation intentionally shows the service boundary, not just a model call.", 22, fill=(203, 213, 225))
    steps = [
        ("Data contract", "5 CSV files"),
        ("Feature factory", "ratios + guardrails"),
        ("Model leaderboard", "dummy / LR / RF"),
        ("FastAPI service", "single + batch"),
        ("Artifacts", "dashboard + reports"),
    ]
    colors = [COLORS["cyan"], COLORS["blue"], COLORS["purple"], COLORS["green"], COLORS["amber"]]
    sx, sy, cw, ch, gap = 48, 176, 190, 118, 42
    for i, (title, subtitle) in enumerate(steps):
        x = sx + i * (cw + gap)
        active_fill = (22, 33, 53) if i != active else (30, 64, 89)
        outline = colors[i] if i == active else (51, 65, 85)
        width = 4 if i == active else 2
        rounded(d, (x, sy, x + cw, sy + ch), 22, fill=active_fill, outline=outline, width=width)
        rounded(d, (x + 17, sy + 20, x + 48, sy + 51), 9, fill=colors[i])
        text(d, (x + 32, sy + 35), str(i + 1), 16, fill=COLORS["navy"], bold=True, anchor="mm")
        text(d, (x + 20, sy + 62), title, 19, bold=True)
        text(d, (x + 20, sy + 91), subtitle, 16, fill=COLORS["muted"])
        if i < len(steps) - 1:
            a_color = colors[i] if i == active else (71, 85, 105)
            arrow(d, (x + cw + 6, sy + ch // 2), (x + cw + gap - 8, sy + ch // 2), fill=a_color, width=5)
            if i == active:
                # small "popping" dot on arrow
                d.ellipse((x + cw + 15, sy + ch // 2 - 10, x + cw + 35, sy + ch // 2 + 10), fill=colors[i])
    return img


def animated_flow() -> None:
    frames: list[Image.Image] = []
    for active in [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]:
        frames.append(flow_frame(active))
    frames[0].save(
        ASSET_DIR / "pipeline_flow.gif",
        save_all=True,
        append_images=frames[1:],
        duration=520,
        loop=0,
        optimize=True,
    )


def asset_readme() -> None:
    (ASSET_DIR / "README.md").write_text(
        """
# README visual assets

These assets are intentionally committed because the repository is being used as a portfolio project.
They make the GitHub landing page reviewable without requiring a reviewer to run the app first.

- `github_hero.png`: README hero image.
- `pipeline_flow.gif`: animated service flow with highlighted arrows.
- `architecture_diagram.png`: full architecture overview.
- `dashboard_preview.png`: reviewer-facing dashboard mock preview.
- `api_contract_preview.png`: API request/response preview.
- `github_social_preview.png`: image to upload in GitHub repository settings as the social preview.

Regenerate them with:

```bash
python scripts/render_github_assets.py
```
""".strip()
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    hero()
    architecture()
    dashboard_preview()
    api_contract_preview()
    social_preview()
    animated_flow()
    asset_readme()
    print(f"rendered assets to {ASSET_DIR}")


if __name__ == "__main__":
    required_assets = [
        ASSET_DIR / "github_hero.png",
        ASSET_DIR / "dashboard_preview.png",
        ASSET_DIR / "pipeline_flow.gif",
        ASSET_DIR / "architecture_diagram.png",
        ASSET_DIR / "github_social_preview.png",
    ]
    if "--force" not in sys.argv and all(path.exists() and path.stat().st_size > 1024 for path in required_assets):
        print(f"README visual assets already exist in {ASSET_DIR}. Use --force to regenerate.")
    else:
        main()
