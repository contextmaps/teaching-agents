"""
Scaffold-only generator. Produces 5 placeholder PNGs for tutorial anchor
screenshots. Each is an 800x500 gray rectangle with the platform name centered.

Onur replaces these with real screenshots after the skeleton ships.

Requires Pillow (PIL). Pillow is NOT a runtime dependency — it's only needed
to regenerate placeholders. Faculty don't need it.

Usage:
    python tools/generate_placeholder_pngs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow is not installed. Run: pip install pillow", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS = REPO_ROOT / "assets" / "tutorials"

TARGETS = [
    ("copilot",    "entry-point.png",        "Microsoft Copilot"),
    ("chatgpt",    "entry-point.png",        "ChatGPT"),
    ("claude",     "entry-point.png",        "Claude"),
    ("gemini",     "entry-point.png",        "Google Gemini"),
    ("notebooklm", "notebook-overview.png",  "NotebookLM"),
]

WIDTH, HEIGHT = 800, 500
BG = (224, 222, 216)
FG = (90, 90, 85)
BORDER = (180, 178, 170)
SUBTITLE_FG = (130, 128, 120)


def find_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def draw_one(out_path: Path, label: str) -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    # Inner border
    draw.rectangle([(20, 20), (WIDTH - 21, HEIGHT - 21)], outline=BORDER, width=2)

    title_font = find_font(40)
    subtitle_font = find_font(18)

    # Center the platform label
    bbox = draw.textbbox((0, 0), label, font=title_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (WIDTH - tw) // 2
    y = (HEIGHT - th) // 2 - 20
    draw.text((x, y), label, fill=FG, font=title_font)

    subtitle = "Placeholder — replace with real screenshot"
    sb = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sw = sb[2] - sb[0]
    draw.text(((WIDTH - sw) // 2, y + th + 16), subtitle, fill=SUBTITLE_FG, font=subtitle_font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)


def main() -> int:
    for platform_id, filename, label in TARGETS:
        out = ASSETS / platform_id / filename
        draw_one(out, label)
        print(f"  wrote {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
