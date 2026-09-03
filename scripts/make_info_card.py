#!/usr/bin/env python3
"""
make_info_card.py: Generates an animated luxury terminal info card SVG.
Uses opacity: 1 base styling to guarantee 100% visibility on GitHub markdown.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config
except ImportError:
    import config

OUTPUT_SVG_PATH = ROOT_DIR / "info-card.svg"


def generate_info_card_svg() -> Path:
    """Generates the luxury animated terminal info card SVG."""
    # Match avi-ascii.svg dimensions exactly (480x520) for perfect side-by-side alignment!
    svg_width = 480
    svg_height = 520

    tech_langs = ", ".join(config.TECH_STACK.get("Languages", [])[:4])
    tech_fw = ", ".join(config.TECH_STACK.get("Frameworks", [])[:3])

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="50%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Accent Gradient -->
    <linearGradient id="accent-gold-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe" />
      <stop offset="50%" stop-color="#3fb950" />
      <stop offset="100%" stop-color="#ffd700" />
    </linearGradient>

    <style>
      /* BASE STYLING: Guaranteed 100% visible on GitHub (opacity: 1) */
      .card-box {{ fill: url(#card-bg); rx: 14px; ry: 14px; stroke: #30363d; stroke-width: 1.5px; opacity: 1; }}
      .header-bar {{ fill: #161b22; opacity: 1; }}
      
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}

      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace; }}
      .header-title {{ font-size: 11.5px; fill: #8b949e; font-weight: 600; }}

      /* Command Prompt */
      .prompt-user {{ fill: #00f2fe; font-weight: 700; font-size: 13px; opacity: 1; }}
      .prompt-host {{ fill: #3fb950; font-weight: 700; font-size: 13px; opacity: 1; }}
      .prompt-cmd {{ fill: #e6edf3; font-weight: 600; font-size: 13px; opacity: 1; }}

      /* Labels & Values */
      .label {{ fill: #8b949e; font-size: 13px; font-weight: 600; opacity: 1; }}
      .val-cyan {{ fill: #00f2fe; font-size: 13px; font-weight: 600; opacity: 1; }}
      .val-green {{ fill: #3fb950; font-size: 13px; font-weight: 600; opacity: 1; }}
      .val-gold {{ fill: #ffd700; font-size: 13px; font-weight: 600; opacity: 1; }}
      .val-purple {{ fill: #bc8cff; font-size: 13px; font-weight: 600; opacity: 1; }}
      .val-white {{ fill: #f0f6fc; font-size: 13px; font-weight: 500; opacity: 1; }}

      /* Badges */
      .badge-bg {{ fill: #161b22; stroke: #30363d; stroke-width: 1.2px; rx: 6px; ry: 6px; opacity: 1; }}
      .badge-gold {{ fill: #161b22; stroke: #ffd700; stroke-width: 1.2px; rx: 6px; ry: 6px; opacity: 1; }}
      .badge-cyan {{ fill: #161b22; stroke: #00f2fe; stroke-width: 1.2px; rx: 6px; ry: 6px; opacity: 1; }}

      .badge-text-gold {{ fill: #ffd700; font-size: 11.5px; font-weight: 700; opacity: 1; }}
      .badge-text-cyan {{ fill: #00f2fe; font-size: 11.5px; font-weight: 700; opacity: 1; }}

      /* Animations: Non-destructive overlays & blinking cursor */
      .cursor {{
        fill: #00f2fe;
        animation: blink 1s step-end infinite;
      }}

      @keyframes blink {{
        50% {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Container -->
  <rect class="card-box" width="{svg_width}" height="{svg_height}" x="0" y="0" />

  <!-- Header Bar -->
  <path d="M 0 14 C 0 6.27 6.27 0 14 0 L {svg_width - 14} 0 C {svg_width - 6.27} 0 {svg_width} 6.27 {svg_width} 14 L {svg_width} 38 L 0 38 Z" class="header-bar" />
  <line x1="0" y1="38" x2="{svg_width}" y2="38" stroke="#30363d" stroke-width="1" />

  <circle class="dot-red" cx="22" cy="19" r="5" />
  <circle class="dot-yellow" cx="38" cy="19" r="5" />
  <circle class="dot-green" cx="54" cy="19" r="5" />

  <text class="font-mono header-title" x="{svg_width / 2}" y="23" text-anchor="middle">developer_profile.sh</text>

  <!-- Command Line Prompt -->
  <g class="font-mono" transform="translate(24, 70)">
    <text class="prompt-user" x="0" y="0">{config.USERNAME.lower()}</text>
    <text class="prompt-cmd" x="76" y="0">@github:~$ whoami --verbose</text>
  </g>

  <!-- Accent Divider -->
  <line x1="24" y1="84" x2="{svg_width - 24}" y2="84" stroke="url(#accent-gold-cyan)" stroke-width="1.5" stroke-dasharray="4 2" />

  <!-- Developer Attributes Grid -->
  <!-- Name -->
  <g class="font-mono" transform="translate(24, 120)">
    <text class="label" x="0" y="0">👤 Name:</text>
    <text class="val-gold" x="130" y="0">{config.FULL_NAME}</text>
  </g>

  <!-- Role -->
  <g class="font-mono" transform="translate(24, 158)">
    <text class="label" x="0" y="0">⚡ Role:</text>
    <text class="val-cyan" x="130" y="0">Full-Stack &amp; Systems Dev</text>
  </g>

  <!-- Focus -->
  <g class="font-mono" transform="translate(24, 196)">
    <text class="label" x="0" y="0">🎯 Focus:</text>
    <text class="val-green" x="130" y="0">Safety Platforms &amp; Web Apps</text>
  </g>

  <!-- Languages -->
  <g class="font-mono" transform="translate(24, 234)">
    <text class="label" x="0" y="0">💻 Stack:</text>
    <text class="val-purple" x="130" y="0">{tech_langs}</text>
  </g>

  <!-- Frameworks -->
  <g class="font-mono" transform="translate(24, 272)">
    <text class="label" x="0" y="0">🚀 Frameworks:</text>
    <text class="val-white" x="130" y="0">{tech_fw}</text>
  </g>

  <!-- Location -->
  <g class="font-mono" transform="translate(24, 310)">
    <text class="label" x="0" y="0">📍 Location:</text>
    <text class="val-gold" x="130" y="0">{config.LOCATION}</text>
  </g>

  <!-- Featured Highlights -->
  <g class="font-mono" transform="translate(24, 356)">
    <text class="label" x="0" y="0">🌟 Highlight:</text>
    <rect class="badge-gold" x="130" y="-15" width="146" height="23" />
    <text class="badge-text-gold" x="138" y="0">RAKSHAK / SafeHer</text>
  </g>

  <g class="font-mono" transform="translate(24, 396)">
    <text class="label" x="0" y="0">📦 Utilities:</text>
    <rect class="badge-cyan" x="130" y="-15" width="110" height="23" />
    <text class="badge-text-cyan" x="138" y="0">smart-print</text>
  </g>

  <!-- Terminal Status Footer -->
  <line x1="24" y1="436" x2="{svg_width - 24}" y2="436" stroke="#30363d" stroke-width="1" />

  <g class="font-mono" transform="translate(24, 472)">
    <text class="prompt-host" x="0" y="0">SYSTEM READY.</text>
    <text class="prompt-cmd" x="130" y="0">Listening for events...</text>
    <rect class="cursor" x="325" y="-11" width="8" height="15" />
  </g>

</svg>
"""

    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Luxury Animated Info Card SVG generated at {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    generate_info_card_svg()
