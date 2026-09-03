#!/usr/bin/env python3
"""
make_ascii_gif.py: Converts MP4, GIF, MOV, or WEBM video files into an animated terminal ASCII GIF.
Supports video files placed directly in the repository root.
"""

import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageSequence

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config
except ImportError:
    import config

OUTPUT_GIF_PATH = ROOT_DIR / "avi-ascii.gif"
ASCII_RAMP = " .':-+=*#%@"


def get_consolas_font(size: int) -> ImageFont.FreeTypeFont:
    """Tries to load Consolas monospace font from system directory."""
    font_paths = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/lucon.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for fp in font_paths:
        if Path(fp).exists():
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def process_pil_frame(frame_img: Image.Image, width: int = 68, height: int = 46) -> list[str]:
    """Crops, enhances, and converts a single PIL image frame to ASCII lines."""
    w, h = frame_img.size
    if h > w:
        left, top, right, bottom = int(w * 0.15), int(h * 0.14), int(w * 0.85), int(h * 0.65)
        frame_img = frame_img.crop((left, top, right, bottom))

    gray = frame_img.convert("L")
    contrast_img = ImageOps.autocontrast(gray, cutoff=2)
    enhanced_img = ImageEnhance.Contrast(contrast_img).enhance(1.4)
    resized_img = enhanced_img.resize((width, height), Image.Resampling.LANCZOS)

    pixels = resized_img.load()
    ramp_len = len(ASCII_RAMP)
    ascii_lines = []

    for y in range(height):
        line_chars = []
        for x in range(width):
            val = pixels[x, y]
            idx = int((val / 255.0) * (ramp_len - 1))
            line_chars.append(ASCII_RAMP[idx])
        ascii_lines.append("".join(line_chars))

    return ascii_lines


def render_ascii_card_frame(
    ascii_lines: list[str],
    frame_index: int,
    total_frames: int,
    card_width: int = 480,
    card_height: int = 520,
) -> Image.Image:
    """Renders a single ASCII frame onto a luxury dark glassmorphic terminal card."""
    card = Image.new("RGB", (card_width, card_height), color="#090d16")
    draw = ImageDraw.Draw(card)

    font_title = get_consolas_font(12)
    font_ascii = get_consolas_font(9)

    # Terminal Header Bar
    draw.rectangle([(0, 0), (card_width, 38)], fill="#161b22")
    draw.line([(0, 38), (card_width, 38)], fill="#30363d", width=1)
    draw.rectangle([(0, 0), (card_width - 1, card_height - 1)], outline="#30363d", width=2)

    # Window Control Dots
    draw.ellipse([(17, 14), (27, 24)], fill="#ff5f56")
    draw.ellipse([(33, 14), (43, 24)], fill="#ffbd2e")
    draw.ellipse([(49, 14), (59, 24)], fill="#27c93f")

    # Header Title
    title_text = f"{config.USERNAME.lower()}@github:~$ cat ascii_video.gif"
    draw.text((120, 11), title_text, fill="#8b949e", font=font_title)

    # ASCII Content Color Gradient per line
    start_x = 24
    start_y = 52
    line_spacing = 9.8
    colors = ["#00f2fe", "#4facfe", "#ffd700", "#ffbd2e", "#bc8cff"]

    for i, line in enumerate(ascii_lines):
        c_idx = (i + frame_index) % len(colors)
        line_color = colors[c_idx]
        y_pos = start_y + (i * line_spacing)
        draw.text((start_x, y_pos), line, fill=line_color, font=font_ascii)

    # Scanline light bar
    scan_y = int(40 + ((frame_index / max(1, total_frames - 1)) * 450)) % 520
    draw.line([(2, scan_y), (card_width - 2, scan_y)], fill="#00f2fe", width=1)

    return card


def extract_video_frames(video_path: Path, max_frames: int = 40) -> list[Image.Image]:
    """Extracts frames uniformly from an MP4, MOV, WEBM video file using OpenCV."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return []

    total_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_count <= 0:
        total_count = 100

    step = max(1, total_count // max_frames)
    frames = []

    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            # OpenCV BGR -> RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            frames.append(pil_img)
            if len(frames) >= max_frames:
                break
        idx += 1

    cap.release()
    return frames


def generate_ascii_gif() -> Path:
    """Finds available video or GIF sources and generates avi-ascii.gif."""
    video_extensions = [".mp4", ".gif", ".mov", ".webm", ".avi"]
    found_file = None

    for ext in video_extensions:
        candidate = ROOT_DIR / f"source{ext}"
        if candidate.exists():
            found_file = candidate
            break

    rendered_frames = []

    if found_file:
        print(f"[*] Found video/GIF source file at {found_file.name}, processing frames...")
        if found_file.suffix.lower() == ".gif":
            with Image.open(found_file) as gif:
                raw_frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
            step = max(1, len(raw_frames) // 40)
            frames = raw_frames[::step][:40]
        else:
            frames = extract_video_frames(found_file, max_frames=40)

        total = len(frames)
        for idx, frame in enumerate(frames):
            ascii_lines = process_pil_frame(frame)
            card_img = render_ascii_card_frame(ascii_lines, idx, total)
            rendered_frames.append(card_img)

    else:
        photo_path = ROOT_DIR / "source-photo.jpg"
        print(f"[*] No video file found. Processing photo {photo_path.name}...")
        if photo_path.exists():
            with Image.open(photo_path) as photo:
                base_ascii = process_pil_frame(photo)
            total = 20
            for idx in range(total):
                card_img = render_ascii_card_frame(base_ascii, idx, total)
                rendered_frames.append(card_img)

    if rendered_frames:
        rendered_frames[0].save(
            OUTPUT_GIF_PATH,
            save_all=True,
            append_images=rendered_frames[1:],
            duration=90,
            loop=0,
            optimize=True,
        )
        print(f"[+] Animated ASCII GIF generated successfully at {OUTPUT_GIF_PATH.name} ({len(rendered_frames)} frames)")

    return OUTPUT_GIF_PATH


if __name__ == "__main__":
    generate_ascii_gif()
