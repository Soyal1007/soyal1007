#!/usr/bin/env python3
"""
make_ascii_gif.py: Premium ASCII video GIF generator.
Converts source video into a silky-smooth animated ASCII terminal portrait.
Features: per-character brightness coloring, gradient scanline, noise reduction, smooth edges.
"""

import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageSequence

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config
except ImportError:
    import config

OUTPUT_GIF_PATH = ROOT_DIR / "avi-ascii.gif"

# Premium 12-shade ramp for maximum facial detail
ASCII_RAMP = "  ..,,::;;++==**##%%@@"

# Per-brightness color buckets (dark → bright)
COLOR_MAP = [
    "#1a1a2e",  # near-black (empty)
    "#16213e",
    "#0f3460",
    "#1a4a7a",
    "#00509d",
    "#006dbd",
    "#0090d5",
    "#00bcd4",
    "#00e5ff",
    "#4dd0e1",
    "#ffd700",  # bright highlights → gold
    "#ffe066",
    "#ffffff",  # brightest → white
]


def get_font(size: int) -> ImageFont.FreeTypeFont:
    paths = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/lucon.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def frame_to_ascii_colored(
    frame_img: Image.Image,
    ascii_w: int = 72,
    ascii_h: int = 50,
) -> list[tuple[str, list[str]]]:
    """
    Returns a list of (char, color) per character, organized as rows.
    Each row is a list of (char, color_hex).
    """
    # Always center-crop square
    w, h = frame_img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    frame_img = frame_img.crop((left, top, left + side, top + side))

    gray = frame_img.convert("L")
    # Adaptive contrast + mild sharpness
    contrasted = ImageOps.autocontrast(gray, cutoff=1)
    sharpened = contrasted.filter(ImageFilter.UnsharpMask(radius=1, percent=80, threshold=2))
    enhanced = ImageEnhance.Contrast(sharpened).enhance(1.3)
    resized = enhanced.resize((ascii_w, ascii_h), Image.Resampling.LANCZOS)

    pixels = resized.load()
    ramp_len = len(ASCII_RAMP)
    cmap_len = len(COLOR_MAP)
    rows = []

    for y in range(ascii_h):
        row = []
        for x in range(ascii_w):
            val = pixels[x, y]
            c_idx = int((val / 255.0) * (ramp_len - 1))
            col_idx = int((val / 255.0) * (cmap_len - 1))
            row.append((ASCII_RAMP[c_idx], COLOR_MAP[col_idx]))
        rows.append(row)

    return rows


def render_frame(
    rows: list[list[tuple[str, str]]],
    frame_index: int,
    total_frames: int,
    card_w: int = 520,
    card_h: int = 540,
) -> Image.Image:
    """Renders a single premium ASCII frame onto a luxury dark terminal card."""
    card = Image.new("RGB", (card_w, card_h), color=(9, 13, 22))
    draw = ImageDraw.Draw(card)

    font_hdr = get_font(11)
    font_ascii = get_font(8)

    # === Outer border glow (2px) ===
    draw.rectangle([(0, 0), (card_w - 1, card_h - 1)], outline="#1e3a5f", width=2)

    # === Header bar ===
    draw.rectangle([(2, 2), (card_w - 2, 36)], fill="#0d1117")
    draw.line([(2, 36), (card_w - 2, 36)], fill="#21262d", width=1)

    # Window dots
    draw.ellipse([(14, 12), (24, 22)], fill="#ff5f56")
    draw.ellipse([(30, 12), (40, 22)], fill="#ffbd2e")
    draw.ellipse([(46, 12), (56, 22)], fill="#27c93f")

    # Frame counter badge (top right)
    pct = int((frame_index / max(1, total_frames - 1)) * 100)
    badge = f"{pct:3d}%"
    draw.text((card_w - 52, 13), badge, fill="#00f2fe", font=font_hdr)

    # Title text
    title = f"{config.USERNAME.lower()}@github:~$ play ascii_video.mp4"
    draw.text((68, 13), title, fill="#6e7681", font=font_hdr)

    # === ASCII content ===
    start_x = 10
    start_y = 44
    char_w = 6.5
    line_h = 9.6

    for row_idx, row in enumerate(rows):
        y_pos = int(start_y + row_idx * line_h)
        for col_idx, (ch, color) in enumerate(row):
            if ch.strip():  # only draw non-space
                x_pos = int(start_x + col_idx * char_w)
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                draw.text((x_pos, y_pos), ch, fill=(r, g, b), font=font_ascii)

    # === Scanline sweep (bright glowing line) ===
    progress = frame_index / max(1, total_frames - 1)
    scan_y = int(38 + progress * (card_h - 40))
    # Glow: 3 overlapping lines with decreasing opacity
    for offset, alpha in [(0, 60), (1, 30), (-1, 30)]:
        sy = scan_y + offset
        if 38 <= sy < card_h:
            # Blend cyan glow onto card
            scan_strip = Image.new("RGBA", (card_w - 4, 1), (0, 242, 254, alpha))
            card_rgba = card.convert("RGBA")
            card_rgba.paste(scan_strip, (2, sy), scan_strip)
            card = card_rgba.convert("RGB")
            draw = ImageDraw.Draw(card)

    # === Subtle vignette (darken corners) ===
    vignette = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for i in range(30):
        alpha = int(80 * (1 - i / 30))
        vd.rectangle([(i, i), (card_w - i, card_h - i)], outline=(0, 0, 0, alpha))
    card = Image.alpha_composite(card.convert("RGBA"), vignette).convert("RGB")

    # === Bottom status bar ===
    bar_y = card_h - 22
    draw = ImageDraw.Draw(card)
    draw.rectangle([(2, bar_y), (card_w - 2, card_h - 2)], fill="#0d1117")
    draw.line([(2, bar_y), (card_w - 2, bar_y)], fill="#21262d", width=1)

    frame_txt = f"▶  frame {frame_index + 1:02d}/{total_frames:02d}  |  {config.FULL_NAME}  |  soyal1007@github"
    draw.text((10, bar_y + 4), frame_txt, fill="#3d444d", font=font_hdr)

    # Cyan dot (active)
    dot_x = card_w - 18
    draw.ellipse([(dot_x, bar_y + 7), (dot_x + 8, bar_y + 15)], fill="#00f2fe")

    return card


def extract_video_frames(video_path: Path, max_frames: int = 60) -> list[Image.Image]:
    """Extracts frames from MP4/MOV/WEBM with temporal smoothing."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return []

    total_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 100
    step = max(1, total_count // max_frames)
    frames = []
    prev_frame = None

    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Temporal blend with previous frame for smoothness
            if prev_frame is not None:
                blended = cv2.addWeighted(prev_frame, 0.25, rgb, 0.75, 0)
            else:
                blended = rgb
            prev_frame = rgb.copy()
            frames.append(Image.fromarray(blended))
            if len(frames) >= max_frames:
                break
        idx += 1

    cap.release()
    return frames


def generate_ascii_gif() -> Path:
    video_extensions = [".mp4", ".gif", ".mov", ".webm", ".avi"]
    found_file = None

    for ext in video_extensions:
        candidate = ROOT_DIR / f"source{ext}"
        if candidate.exists():
            found_file = candidate
            break

    rendered_frames = []

    if found_file:
        print(f"[*] Processing {found_file.name} -> premium ASCII animation...")
        if found_file.suffix.lower() == ".gif":
            with Image.open(found_file) as gif:
                raw_frames = [f.copy() for f in ImageSequence.Iterator(gif)]
            step = max(1, len(raw_frames) // 60)
            frames = raw_frames[::step][:60]
        else:
            frames = extract_video_frames(found_file, max_frames=60)

        total = len(frames)
        print(f"[*] Rendering {total} frames with per-character color mapping...")
        for idx, frame in enumerate(frames):
            rows = frame_to_ascii_colored(frame)
            card = render_frame(rows, idx, total)
            rendered_frames.append(card)
            if (idx + 1) % 10 == 0:
                print(f"    {idx + 1}/{total} frames done...")

    else:
        photo_path = ROOT_DIR / "source-photo.jpg"
        print(f"[*] No video found. Using {photo_path.name} with animated scanline...")
        if photo_path.exists():
            with Image.open(photo_path) as ph:
                rows = frame_to_ascii_colored(ph)
            total = 30
            for idx in range(total):
                card = render_frame(rows, idx, total)
                rendered_frames.append(card)

    if rendered_frames:
        rendered_frames[0].save(
            OUTPUT_GIF_PATH,
            save_all=True,
            append_images=rendered_frames[1:],
            duration=70,      # ~14fps — smooth motion
            loop=0,
            optimize=True,
        )
        size_kb = OUTPUT_GIF_PATH.stat().st_size // 1024
        print(f"[+] Premium ASCII GIF saved → {OUTPUT_GIF_PATH.name} ({len(rendered_frames)} frames, ~{size_kb} KB)")

    return OUTPUT_GIF_PATH


if __name__ == "__main__":
    generate_ascii_gif()
