"""Render the README animation from the synthetic demo claim values."""

from __future__ import annotations

from itertools import pairwise
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "bioverity-loop.gif"
SIZE = (1080, 500)
SCALE = 2

BG = "#0b1519"
PANEL = "#112229"
LINE = "#294047"
MUTED = "#8ca4a8"
WHITE = "#eaf2ed"
GREEN = "#67d6a3"
AMBER = "#f0b96b"
BLUE = "#78b9d9"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            index = (0 if bold else 7) if candidate.endswith("Avenir Next.ttc") else 0
            return ImageFont.truetype(candidate, size * SCALE, index=index)
    return ImageFont.load_default()


FONTS = {size: font(size) for size in (13, 14, 16, 19, 22, 30, 39)}
BOLD = {size: font(size, True) for size in (13, 14, 16, 19, 22, 30, 39)}


def render(frame: int) -> Image.Image:
    t = frame / 35
    phase = min(3, frame // 9)
    canvas = Image.new("RGB", (SIZE[0] * SCALE, SIZE[1] * SCALE), BG)
    draw = ImageDraw.Draw(canvas)

    def box(x0, y0, x1, y1, fill, outline=None, radius=0, width=1):
        draw.rounded_rectangle(
            (x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE),
            radius=radius * SCALE,
            fill=fill,
            outline=outline,
            width=width * SCALE,
        )

    def txt(x, y, value, size, color=WHITE, bold=False):
        draw.text((x * SCALE, y * SCALE), value, font=(BOLD if bold else FONTS)[size], fill=color)

    box(0, 0, 1080, 500, BG)
    box(30, 27, 39, 44, GREEN, radius=2)
    box(44, 27, 53, 44, BLUE, radius=2)
    txt(67, 23, "BIOVERITY", 19, bold=True)
    txt(796, 28, "CLAIMS AS CODE  /  LIVE TRACE", 13, MUTED)
    draw.line((30 * SCALE, 65 * SCALE, 1050 * SCALE, 65 * SCALE), fill=LINE, width=SCALE)

    txt(31, 82, "When evidence changes, the claim changes.", 30, bold=True)
    txt(
        32, 125, "A reproducible ecological regression, from observation to human review", 16, MUTED
    )

    steps = [
        ("01", "OBSERVATION", "New field record", GREEN),
        ("02", "EVIDENCE", "Snapshot EVS-000021", BLUE),
        ("03", "CLAIM CI", "Support recalculated", AMBER),
        ("04", "NEXT ACTION", "Researcher review", GREEN),
    ]
    for i, (number, title, detail, accent) in enumerate(steps):
        x = 30 + i * 258
        active = i <= phase
        box(x, 173, x + 240, 247, PANEL if active else BG, accent if active else LINE, 5)
        box(x + 13, 185, x + 44, 216, accent if active else LINE, radius=3)
        txt(x + 19, 191, number, 13, BG if active else MUTED, bold=True)
        txt(x + 53, 184, title, 14, WHITE if active else MUTED, bold=True)
        txt(x + 53, 207, detail, 13, MUTED)
        if i < 3:
            draw.line(
                ((x + 241) * SCALE, 209 * SCALE, (x + 256) * SCALE, 209 * SCALE),
                fill=accent if i < phase else LINE,
                width=2 * SCALE,
            )

    box(30, 269, 688, 427, PANEL, LINE, 5)
    txt(48, 284, "ECR-000018", 13, MUTED, bold=True)
    txt(48, 307, "Spotted lanternfly interaction", 22, WHITE, bold=True)
    txt(48, 341, "CLAIM SUPPORT", 13, MUTED, bold=True)
    draw.line((48 * SCALE, 393 * SCALE, 658 * SCALE, 393 * SCALE), fill=LINE, width=SCALE)
    points = [
        (48, 377),
        (135, 370),
        (220, 367),
        (305, 355),
        (390, 343),
        (475, 360),
        (560, 383),
        (653, 389),
    ]
    visible = min(len(points), max(2, 2 + int(t * 8)))
    for a, b in pairwise(points[:visible]):
        draw.line(
            (a[0] * SCALE, a[1] * SCALE, b[0] * SCALE, b[1] * SCALE),
            fill=GREEN if b[0] < 390 else AMBER,
            width=3 * SCALE,
        )
    px, py = points[visible - 1]
    draw.ellipse(
        ((px - 5) * SCALE, (py - 5) * SCALE, (px + 5) * SCALE, (py + 5) * SCALE),
        fill=AMBER if phase >= 2 else GREEN,
    )
    txt(565, 301, "0.82", 19, GREEN, bold=True)
    txt(568, 329, "to", 13, MUTED)
    txt(600, 326, "0.50", 19, AMBER, bold=True)

    box(705, 269, 1050, 427, PANEL, LINE, 5)
    txt(723, 284, "VERITYDECISION", 13, MUTED, bold=True)
    txt(723, 311, "Field survey", 22, WHITE if phase >= 3 else MUTED, bold=True)
    txt(723, 345, "Policy: researcher review", 16, GREEN if phase >= 3 else MUTED)
    box(723, 385, 1031, 392, LINE, radius=2)
    fill_width = int((0.18 + 0.76 * min(1, max(0, (frame - 25) / 10))) * 308)
    box(723, 385, 723 + fill_width, 392, GREEN if phase >= 3 else BLUE, radius=2)

    stages = ["INGEST", "VALIDATE", "DETECT", "REVIEW"]
    for i, stage in enumerate(stages):
        x = 31 + i * 165
        box(x, 453, x + 7, 460, [GREEN, BLUE, AMBER, GREEN][i] if i <= phase else LINE, radius=2)
        txt(x + 14, 447, stage, 13, WHITE if i == phase else MUTED, bold=i == phase)
    txt(851, 447, "SYNTHETIC DEMO DATA", 13, MUTED)
    return canvas.resize(SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    frames = [render(i) for i in range(36)]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=[100] * 35 + [1200],
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
