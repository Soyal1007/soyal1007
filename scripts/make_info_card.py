#!/usr/bin/env python3
"""
make_info_card.py: Generates an animated terminal info card SVG.
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
    """Generates the animated terminal info card SVG."""
    svg_width = 460
    svg_height = 500

    # Information items to render
    tech_langs = ", ".join(config.TECH_STACK.get("Languages", [])[:4])
    tech_fw = ", ".join(config.TECH_STACK.get("Frameworks", [])[:3])
    
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="card-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Accent Gradient -->
    <linearGradient id="accent-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#58a6ff" />
      <stop offset="50%" stop-color="#3fb950" />
      <stop offset="100%" stop-color="#bc8cff" />
    </linearGradient>

    <style>
      .card-rect {{ fill: url(#card-bg); rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1.5px; }}
      .header-bg {{ fill: #161b22; }}
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}
      
      .font-mono {{ font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace; }}
      .header-title {{ font-size: 11px; fill: #8b949e; font-weight: 600; }}

      .prompt-user {{ fill: #58a6ff; font-weight: 700; font-size: 13px; }}
      .prompt-host {{ fill: #3fb950; font-weight: 700; font-size: 13px; }}
      .prompt-cmd {{ fill: #c9d1d9; font-weight: 600; font-size: 13px; }}

      .label {{ fill: #8b949e; font-size: 12.5px; font-weight: 600; }}
      .val-blue {{ fill: #58a6ff; font-size: 12.5px; font-weight: 500; }}
      .val-green {{ fill: #3fb950; font-size: 12.5px; font-weight: 500; }}
      .val-purple {{ fill: #bc8cff; font-size: 12.5px; font-weight: 500; }}
      .val-orange {{ fill: #f0883e; font-size: 12.5px; font-weight: 500; }}
      .val-white {{ fill: #e6edf3; font-size: 12.5px; font-weight: 500; }}

      .badge {{ fill: #21262d; stroke: #30363d; stroke-width: 1px; rx: 4px; ry: 4px; }}
      .badge-text {{ fill: #58a6ff; font-size: 11px; font-weight: 600; }}

      /* Keyframe Animations */
      .fade-line {{
        opacity: 0;
        animation: fadeInLine 0.6s ease-out forwards;
      }}

      .line-1 {{ animation-delay: 0.2s; }}
      .line-2 {{ animation-delay: 0.5s; }}
      .line-3 {{ animation-delay: 0.8s; }}
      .line-4 {{ animation-delay: 1.1s; }}
      .line-5 {{ animation-delay: 1.4s; }}
      .line-6 {{ animation-delay: 1.7s; }}
      .line-7 {{ animation-delay: 2.0s; }}
      .line-8 {{ animation-delay: 2.3s; }}
      .line-9 {{ animation-delay: 2.6s; }}

      .cursor {{
        fill: #58a6ff;
        animation: blink 1s step-end infinite;
      }}

      @keyframes fadeInLine {{
        from {{ opacity: 0; transform: translateY(4px); }}
        to {{ opacity: 1; transform: translateY(0); }}
      }}

      @keyframes blink {{
        50% {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <!-- Base Card -->
  <rect class="card-rect" width="{svg_width}" height="{svg_height}" x="0" y="0" />

  <!-- Window Header -->
  <path d="M 0 12 C 0 5.37 5.37 0 12 0 L {svg_width - 12} 0 C {svg_width - 5.37} 0 {svg_width} 5.37 {svg_width} 12 L {svg_width} 36 L 0 36 Z" class="header-bg" />
  <line x1="0" y1="36" x2="{svg_width}" y2="36" stroke="#30363d" stroke-width="1" />
  
  <circle class="dot-red" cx="20" cy="18" r="5" />
  <circle class="dot-yellow" cx="36" cy="18" r="5" />
  <circle class="dot-green" cx="52" cy="18" r="5" />
  
  <text class="font-mono header-title" x="{svg_width / 2}" y="22" text-anchor="middle">developer_info.sh</text>

  <!-- Terminal Command Line Prompt -->
  <g class="font-mono fade-line line-1" transform="translate(24, 66)">
    <text class="prompt-user" x="0" y="0">{config.USERNAME.lower()}</text>
    <text class="prompt-cmd" x="72" y="0">@github:~$ whoami --verbose</text>
  </g>

  <!-- Separator Line -->
  <line class="fade-line line-2" x1="24" y1="80" x2="{svg_width - 24}" y2="80" stroke="url(#accent-grad)" stroke-width="1.5" stroke-dasharray="4 2" />

  <!-- Card Details Grid -->
  <!-- Name -->
  <g class="font-mono fade-line line-2" transform="translate(24, 114)">
    <text class="label" x="0" y="0">👤 Name:</text>
    <text class="val-white" x="120" y="0">{config.FULL_NAME}</text>
  </g>

  <!-- Role -->
  <g class="font-mono fade-line line-3" transform="translate(24, 150)">
    <text class="label" x="0" y="0">⚡ Role:</text>
    <text class="val-blue" x="120" y="0">Full-Stack &amp; Software Dev</text>
  </g>

  <!-- Focus -->
  <g class="font-mono fade-line line-4" transform="translate(24, 186)">
    <text class="label" x="0" y="0">🎯 Focus:</text>
    <text class="val-green" x="120" y="0">Safety Systems &amp; Web Apps</text>
  </g>

  <!-- Languages -->
  <g class="font-mono fade-line line-5" transform="translate(24, 222)">
    <text class="label" x="0" y="0">💻 Stack:</text>
    <text class="val-purple" x="120" y="0">{tech_langs}</text>
  </g>

  <!-- Frameworks -->
  <g class="font-mono fade-line line-6" transform="translate(24, 258)">
    <text class="label" x="0" y="0">🚀 Frameworks:</text>
    <text class="val-orange" x="120" y="0">{tech_fw}</text>
  </g>

  <!-- Status / Location -->
  <g class="font-mono fade-line line-7" transform="translate(24, 294)">
    <text class="label" x="0" y="0">📍 Location:</text>
    <text class="val-white" x="120" y="0">{config.LOCATION}</text>
  </g>

  <!-- Major Project Highlight -->
  <g class="font-mono fade-line line-8" transform="translate(24, 340)">
    <text class="label" x="0" y="0">🌟 Highlight:</text>
    <rect class="badge" x="120" y="-14" width="140" height="22" />
    <text class="badge-text" x="128" y="1">RAKSHAK / SafeHer</text>
  </g>

  <g class="font-mono fade-line line-8" transform="translate(24, 380)">
    <text class="label" x="0" y="0">📦 Utilities:</text>
    <rect class="badge" x="120" y="-14" width="105" height="22" />
    <text class="badge-text" x="128" y="1">smart-print</text>
  </g>

  <!-- Terminal Output Bottom Section -->
  <line class="fade-line line-9" x1="24" y1="420" x2="{svg_width - 24}" y2="420" stroke="#30363d" stroke-width="1" />
  
  <g class="font-mono fade-line line-9" transform="translate(24, 452)">
    <text class="prompt-host" x="0" y="0">SYSTEM READY.</text>
    <text class="prompt-cmd" x="120" y="0">Listening for events...</text>
    <rect class="cursor" x="310" y="-11" width="8" height="14" />
  </g>

</svg>
"""

    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Animated Info Card SVG generated at {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    generate_info_card_svg()
