#!/usr/bin/env python3
"""
make_ascii_svg.py: Converts preprocessed photo into an animated luxury ASCII SVG portrait.
Uses INLINE SVG attributes to bypass GitHub SVG CSS sanitizer stripping.
"""

import sys
from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config, prep_photo
except ImportError:
    import config
    import prep_photo

OUTPUT_SVG_PATH = ROOT_DIR / "avi-ascii.svg"

ASCII_RAMP = " .':-+=*#%@"


def image_to_ascii(img: Image.Image) -> list[str]:
    """Converts a grayscale PIL Image into ASCII string lines."""
    width, height = img.size
    pixels = img.load()
    ascii_lines = []

    ramp_len = len(ASCII_RAMP)
    for y in range(height):
        line_chars = []
        for x in range(width):
            val = pixels[x, y]  # 0 to 255
            idx = int((val / 255.0) * (ramp_len - 1))
            line_chars.append(ASCII_RAMP[idx])
        ascii_lines.append("".join(line_chars))
    return ascii_lines


def generate_ascii_svg(width: int = 72, height: int = 48) -> Path:
    """Generates the luxury animated ASCII SVG portrait."""
    prepped_img = prep_photo.prep_photo(target_width=width, target_height=height)
    ascii_lines = image_to_ascii(prepped_img)

    svg_width = 480
    svg_height = 520

    start_x = 22
    start_y = 56
    line_height = 8.8
    font_size = 7.6

    escaped_lines = []
    for line in ascii_lines:
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        escaped_lines.append(escaped)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <linearGradient id="portrait-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="35%" stop-color="#4facfe" />
      <stop offset="70%" stop-color="#ffd700" />
      <stop offset="100%" stop-color="#bc8cff" />
    </linearGradient>

    <linearGradient id="scan-glow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="rgba(0, 242, 254, 0.0)" />
      <stop offset="50%" stop-color="rgba(0, 242, 254, 0.15)" />
      <stop offset="100%" stop-color="rgba(0, 242, 254, 0.0)" />
    </linearGradient>

    <style>
      @keyframes pulseShine {{
        0% {{ filter: drop-shadow(0 0 1px rgba(0, 242, 254, 0.3)); }}
        50% {{ filter: drop-shadow(0 0 4px rgba(255, 215, 0, 0.5)); }}
        100% {{ filter: drop-shadow(0 0 2px rgba(188, 140, 255, 0.4)); }}
      }}

      @keyframes sweepMotion {{
        0% {{ transform: translateY(0px); }}
        100% {{ transform: translateY(460px); }}
      }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect width="{svg_width}" height="{svg_height}" x="0" y="0" fill="#090d16" rx="14" ry="14" stroke="#30363d" stroke-width="1.5" />

  <!-- Terminal Header Bar -->
  <path d="M 0 14 C 0 6.27 6.27 0 14 0 L {svg_width - 14} 0 C {svg_width - 6.27} 0 {svg_width} 6.27 {svg_width} 14 L {svg_width} 38 L 0 38 Z" fill="#161b22" />
  <line x1="0" y1="38" x2="{svg_width}" y2="38" stroke="#30363d" stroke-width="1" />

  <!-- Terminal Window Controls -->
  <circle cx="22" cy="19" r="5" fill="#ff5f56" />
  <circle cx="38" cy="19" r="5" fill="#ffbd2e" />
  <circle cx="54" cy="19" r="5" fill="#27c93f" />

  <!-- Header Title -->
  <text x="{svg_width / 2}" y="23" text-anchor="middle" fill="#8b949e" font-family="'JetBrains Mono', 'Fira Code', Consolas, monospace" font-size="11.5px" font-weight="600">{config.USERNAME.lower()}@github:~$ cat portrait_matrix.txt</text>

  <!-- Scanline Overlay -->
  <rect x="2" y="39" width="{svg_width - 4}" height="60" fill="url(#scan-glow)" pointer-events="none" style="animation: sweepMotion 6s linear infinite;" />

  <!-- ASCII Art Body with Direct Inline Attributes -->
  <text fill="url(#portrait-grad)" font-family="'Courier New', Consolas, 'Fira Code', monospace" font-size="{font_size}px" letter-spacing="1.1px" xml:space="preserve" style="animation: pulseShine 4s ease-in-out infinite alternate;">
"""

    for i, line in enumerate(escaped_lines):
        y_pos = start_y + (i * line_height)
        svg_content += f'    <tspan x="{start_x}" y="{y_pos:.1f}">{line}</tspan>\n'

    svg_content += """  </text>
</svg>
"""

    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Animated ASCII SVG successfully generated at {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    generate_ascii_svg()
