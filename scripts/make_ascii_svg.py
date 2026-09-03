#!/usr/bin/env python3
"""
make_ascii_svg.py: Converts preprocessed photo into an animated luxury ASCII SVG portrait.
Ensures full opacity visibility on GitHub with subtle glow animations.
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

# Fine-tuned ASCII ramp for realistic facial shading
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


def generate_ascii_svg(width: int = 74, height: int = 52) -> Path:
    """Generates the luxury animated ASCII SVG portrait."""
    prepped_img = prep_photo.prep_photo(target_width=width, target_height=height)
    ascii_lines = image_to_ascii(prepped_img)

    # Card Dimensions (matches info-card.svg height perfectly: 480x520)
    svg_width = 480
    svg_height = 520

    start_x = 22
    start_y = 56
    line_height = 8.6
    font_size = 7.6

    escaped_lines = []
    for line in ascii_lines:
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        escaped_lines.append(escaped)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="ascii-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="50%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Luxury Multi-Tone ASCII Text Gradient -->
    <linearGradient id="portrait-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="35%" stop-color="#4facfe" />
      <stop offset="70%" stop-color="#ffd700" />
      <stop offset="100%" stop-color="#bc8cff" />
    </linearGradient>

    <!-- Scanline Sweep Gradient -->
    <linearGradient id="scan-glow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="rgba(0, 242, 254, 0.0)" />
      <stop offset="50%" stop-color="rgba(0, 242, 254, 0.15)" />
      <stop offset="100%" stop-color="rgba(0, 242, 254, 0.0)" />
    </linearGradient>

    <style>
      /* BASE STYLING: Always Visible (opacity: 1) for GitHub compatibility */
      .card-box {{ fill: url(#ascii-bg); rx: 14px; ry: 14px; stroke: #30363d; stroke-width: 1.5px; }}
      .header-bar {{ fill: #161b22; }}
      
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}
      
      .header-title {{
        font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace;
        font-size: 11.5px;
        fill: #8b949e;
        font-weight: 600;
      }}

      .ascii-art {{
        font-family: 'Courier New', Consolas, 'Fira Code', monospace;
        font-size: {font_size}px;
        fill: url(#portrait-grad);
        letter-spacing: 1.1px;
        white-space: pre;
        opacity: 1; /* Guaranteed visible on GitHub */
        animation: pulseShine 4s ease-in-out infinite alternate;
      }}

      .scanline-overlay {{
        fill: url(#scan-glow);
        animation: sweepMotion 6s linear infinite;
      }}

      @keyframes pulseShine {{
        0% {{ filter: drop-shadow(0 0 1px rgba(0, 242, 254, 0.3)); }}
        50% {{ filter: drop-shadow(0 0 5px rgba(255, 215, 0, 0.5)); }}
        100% {{ filter: drop-shadow(0 0 2px rgba(188, 140, 255, 0.4)); }}
      }}

      @keyframes sweepMotion {{
        0% {{ transform: translateY(0px); }}
        100% {{ transform: translateY(460px); }}
      }}
    </style>
  </defs>

  <!-- Main Glassmorphic Container -->
  <rect class="card-box" width="{svg_width}" height="{svg_height}" x="0" y="0" />

  <!-- Terminal Header Bar -->
  <path d="M 0 14 C 0 6.27 6.27 0 14 0 L {svg_width - 14} 0 C {svg_width - 6.27} 0 {svg_width} 6.27 {svg_width} 14 L {svg_width} 38 L 0 38 Z" class="header-bar" />
  <line x1="0" y1="38" x2="{svg_width}" y2="38" stroke="#30363d" stroke-width="1" />

  <!-- Terminal Window Controls -->
  <circle class="dot-red" cx="22" cy="19" r="5" />
  <circle class="dot-yellow" cx="38" cy="19" r="5" />
  <circle class="dot-green" cx="54" cy="19" r="5" />

  <!-- Header Title -->
  <text class="header-title" x="{svg_width / 2}" y="23" text-anchor="middle">{config.USERNAME.lower()}@github:~$ cat portrait_matrix.txt</text>

  <!-- Scanline Sweep Animation Overlay -->
  <rect class="scanline-overlay" x="2" y="39" width="{svg_width - 4}" height="60" pointer-events="none" />

  <!-- ASCII Art Content -->
  <text class="ascii-art">
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
