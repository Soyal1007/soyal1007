#!/usr/bin/env python3
"""
make_ascii_svg.py: Converts source photo into an animated ASCII SVG portrait.
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

# Carefully tuned ASCII density ramp (from darkest/bg to brightest pixels)
ASCII_RAMP = " .':-+=*#%@"


def image_to_ascii(img: Image.Image) -> list[str]:
    """Converts a grayscale PIL Image to a list of ASCII strings."""
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


def generate_ascii_svg(width: int = 68, height: int = 48) -> Path:
    """Generates the animated ASCII SVG portrait."""
    # Ensure prepped photo exists
    prepped_img = prep_photo.prep_photo(target_width=width, target_height=height)
    ascii_lines = image_to_ascii(prepped_img)

    # SVG Container dimensions
    svg_width = 460
    svg_height = 500
    
    # Text positioning calculations
    start_x = 24
    start_y = 58
    line_height = 8.8
    font_size = 7.5

    # Escape XML characters in ASCII output
    escaped_lines = []
    for line in ascii_lines:
        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&#160;")
        escaped_lines.append(escaped)

    # Build SVG content with responsive glassmorphism & subtle animation
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Text Glow & Color Gradient -->
    <linearGradient id="ascii-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#58a6ff" />
      <stop offset="50%" stop-color="#3fb950" />
      <stop offset="100%" stop-color="#bc8cff" />
    </linearGradient>

    <!-- Scanline Sweep Gradient -->
    <linearGradient id="scan-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="rgba(88, 166, 255, 0.0)" />
      <stop offset="50%" stop-color="rgba(88, 166, 255, 0.15)" />
      <stop offset="100%" stop-color="rgba(88, 166, 255, 0.0)" />
    </linearGradient>

    <style>
      .bg {{ fill: url(#bg-grad); rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1.5px; }}
      .title-bar {{ fill: #161b22; rx: 12px; ry: 12px; }}
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}
      .title-text {{ font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }}
      
      .ascii-text {{
        font-family: 'Courier New', Consolas, 'Fira Code', monospace;
        font-size: {font_size}px;
        fill: url(#ascii-grad);
        letter-spacing: 1.2px;
        white-space: pre;
        animation: pulseGlow 4s ease-in-out infinite alternate;
      }}

      .scanline {{
        fill: url(#scan-grad);
        animation: scanSweep 6s linear infinite;
      }}

      @keyframes pulseGlow {{
        0% {{ opacity: 0.88; filter: drop-shadow(0 0 1px rgba(88, 166, 255, 0.2)); }}
        50% {{ opacity: 1.0; filter: drop-shadow(0 0 4px rgba(63, 185, 80, 0.4)); }}
        100% {{ opacity: 0.88; filter: drop-shadow(0 0 2px rgba(188, 140, 255, 0.3)); }}
      }}

      @keyframes scanSweep {{
        0% {{ transform: translateY(0px); }}
        100% {{ transform: translateY(440px); }}
      }}
    </style>
  </defs>

  <!-- Card Background -->
  <rect class="bg" width="{svg_width}" height="{svg_height}" x="0" y="0" />
  
  <!-- Window Header Bar -->
  <path d="M 0 12 C 0 5.37 5.37 0 12 0 L {svg_width - 12} 0 C {svg_width - 5.37} 0 {svg_width} 5.37 {svg_width} 12 L {svg_width} 36 L 0 36 Z" fill="#161b22" />
  <line x1="0" y1="36" x2="{svg_width}" y2="36" stroke="#30363d" stroke-width="1" />
  
  <!-- Terminal Window Controls -->
  <circle class="dot-red" cx="20" cy="18" r="5" />
  <circle class="dot-yellow" cx="36" cy="18" r="5" />
  <circle class="dot-green" cx="52" cy="18" r="5" />
  
  <!-- Terminal Header Title -->
  <text class="title-text" x="{svg_width / 2}" y="22" text-anchor="middle">{config.USERNAME.lower()}@github:~$ cat ascii_portrait.txt</text>

  <!-- Animated Scanline Sweep overlay -->
  <rect class="scanline" x="2" y="37" width="{svg_width - 4}" height="60" pointer-events="none" />

  <!-- ASCII Art Body -->
  <text class="ascii-text">
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
