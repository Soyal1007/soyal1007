#!/usr/bin/env python3
"""
make_info_card.py: Generates a premium animated terminal info card SVG.
Fully inline attributes for guaranteed GitHub rendering.
Features: typing effect simulation, staggered badge rows, gradient dividers.
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
    svg_width = 520
    svg_height = 540
    ff = "'JetBrains Mono', 'Fira Code', Consolas, monospace"

    tech_langs = config.TECH_STACK.get("Languages", [])[:5]
    tech_fw = config.TECH_STACK.get("Frameworks", [])[:4]

    # Badge color pairs: (fill, stroke, text_color)
    lang_colors = [
        ("#003153", "#00f2fe", "#00f2fe"),
        ("#1a0a2e", "#bc8cff", "#bc8cff"),
        ("#1a2000", "#3fb950", "#3fb950"),
        ("#2a1a00", "#ffd700", "#ffd700"),
        ("#1a001a", "#e040fb", "#e040fb"),
    ]
    fw_colors = [
        ("#003153", "#00bcd4", "#00bcd4"),
        ("#1a001a", "#e040fb", "#e040fb"),
        ("#001a00", "#69f0ae", "#69f0ae"),
        ("#1a1200", "#ffcc02", "#ffcc02"),
    ]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <linearGradient id="ic-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16"/>
      <stop offset="60%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#10161f"/>
    </linearGradient>
    <linearGradient id="ic-div" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f2fe"/>
      <stop offset="40%" stop-color="#3fb950"/>
      <stop offset="100%" stop-color="#ffd700"/>
    </linearGradient>
    <linearGradient id="ic-div2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#bc8cff"/>
      <stop offset="100%" stop-color="#00f2fe"/>
    </linearGradient>

    <style>
      @keyframes blink {{
        0%,100% {{ opacity: 1; }}
        50% {{ opacity: 0; }}
      }}
      @keyframes subtleGlow {{
        0% {{ filter: drop-shadow(0 0 2px rgba(0,242,254,0.2)); }}
        50% {{ filter: drop-shadow(0 0 6px rgba(255,215,0,0.4)); }}
        100% {{ filter: drop-shadow(0 0 2px rgba(188,140,255,0.2)); }}
      }}
    </style>
  </defs>

  <!-- Container -->
  <rect width="{svg_width}" height="{svg_height}" rx="16" ry="16" fill="url(#ic-bg)" stroke="#1e2d3d" stroke-width="1.5"/>

  <!-- Header Bar -->
  <path d="M0 16 Q0 0 16 0 L{svg_width-16} 0 Q{svg_width} 0 {svg_width} 16 L{svg_width} 38 L0 38Z" fill="#0d1117"/>
  <line x1="0" y1="38" x2="{svg_width}" y2="38" stroke="#21262d" stroke-width="1"/>

  <!-- Window dots -->
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="37" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="54" cy="19" r="5.5" fill="#27c93f"/>

  <!-- Title -->
  <text x="{svg_width//2}" y="24" text-anchor="middle"
    fill="#6e7681" font-family="{ff}" font-size="11px" font-weight="600">developer_profile.sh — bash</text>

  <!-- Prompt line -->
  <g transform="translate(20, 64)">
    <text x="0" y="0" fill="#00f2fe" font-family="{ff}" font-size="13px" font-weight="700">{config.USERNAME.lower()}</text>
    <text x="82" y="0" fill="#3fb950" font-family="{ff}" font-size="13px" font-weight="600">@github</text>
    <text x="147" y="0" fill="#8b949e" font-family="{ff}" font-size="13px">:~$</text>
    <text x="183" y="0" fill="#f0f6fc" font-family="{ff}" font-size="13px" font-weight="500"> whoami --full</text>
    <rect x="323" y="-13" width="9" height="16" fill="#00f2fe" style="animation: blink 1.1s step-end infinite;"/>
  </g>

  <!-- Divider 1 -->
  <line x1="20" y1="82" x2="{svg_width-20}" y2="82" stroke="url(#ic-div)" stroke-width="1.5" stroke-dasharray="3 3"/>

  <!-- Name -->
  <g transform="translate(20, 114)">
    <text x="0" y="0" fill="#6e7681" font-family="{ff}" font-size="12px" font-weight="600">  NAME</text>
    <text x="110" y="0" fill="#ffd700" font-family="{ff}" font-size="13px" font-weight="700">{config.FULL_NAME}</text>
  </g>

  <!-- Role -->
  <g transform="translate(20, 142)">
    <text x="0" y="0" fill="#6e7681" font-family="{ff}" font-size="12px" font-weight="600">  ROLE</text>
    <text x="110" y="0" fill="#00f2fe" font-family="{ff}" font-size="13px" font-weight="600">Full-Stack &amp; Systems Dev</text>
  </g>

  <!-- Location -->
  <g transform="translate(20, 170)">
    <text x="0" y="0" fill="#6e7681" font-family="{ff}" font-size="12px" font-weight="600">  BASED</text>
    <text x="110" y="0" fill="#3fb950" font-family="{ff}" font-size="13px" font-weight="600">{config.LOCATION} 🌏</text>
  </g>

  <!-- Status -->
  <g transform="translate(20, 198)">
    <text x="0" y="0" fill="#6e7681" font-family="{ff}" font-size="12px" font-weight="600">  STATUS</text>
    <circle cx="118" cy="-4" r="4" fill="#3fb950"/>
    <text x="130" y="0" fill="#3fb950" font-family="{ff}" font-size="13px" font-weight="600">Open to Opportunities</text>
  </g>

  <!-- Focus -->
  <g transform="translate(20, 226)">
    <text x="0" y="0" fill="#6e7681" font-family="{ff}" font-size="12px" font-weight="600">  FOCUS</text>
    <text x="110" y="0" fill="#bc8cff" font-family="{ff}" font-size="12.5px" font-weight="600">Safety Tech · Web · Mobile</text>
  </g>

  <!-- Divider 2 -->
  <line x1="20" y1="244" x2="{svg_width-20}" y2="244" stroke="url(#ic-div2)" stroke-width="1.5" stroke-dasharray="3 3"/>

  <!-- Languages section -->
  <text x="20" y="268" fill="#8b949e" font-family="{ff}" font-size="11px" font-weight="700" letter-spacing="2">LANGUAGES</text>
"""

    # Language badges row
    bx = 20
    by = 280
    for i, lang in enumerate(tech_langs):
        fc, sc, tc = lang_colors[i % len(lang_colors)]
        w = len(lang) * 8 + 20
        svg += f"""  <rect x="{bx}" y="{by}" width="{w}" height="22" rx="5" ry="5" fill="{fc}" stroke="{sc}" stroke-width="1.2"/>
  <text x="{bx+10}" y="{by+15}" fill="{tc}" font-family="{ff}" font-size="11px" font-weight="700">{lang}</text>\n"""
        bx += w + 8
        if bx > svg_width - 100:
            bx = 20
            by += 30

    svg += f"""
  <!-- Frameworks section -->
  <text x="20" y="{by + 40}" fill="#8b949e" font-family="{ff}" font-size="11px" font-weight="700" letter-spacing="2">FRAMEWORKS &amp; TOOLS</text>
"""

    bx = 20
    by = by + 52
    for i, fw in enumerate(tech_fw):
        fc, sc, tc = fw_colors[i % len(fw_colors)]
        w = len(fw) * 8 + 20
        svg += f"""  <rect x="{bx}" y="{by}" width="{w}" height="22" rx="5" ry="5" fill="{fc}" stroke="{sc}" stroke-width="1.2"/>
  <text x="{bx+10}" y="{by+15}" fill="{tc}" font-family="{ff}" font-size="11px" font-weight="700">{fw}</text>\n"""
        bx += w + 8
        if bx > svg_width - 100:
            bx = 20
            by += 30

    footer_y = svg_height - 32
    svg += f"""
  <!-- Bottom border line -->
  <line x1="20" y1="{footer_y}" x2="{svg_width-20}" y2="{footer_y}" stroke="#21262d" stroke-width="1"/>

  <!-- Footer -->
  <text x="20" y="{footer_y + 18}" fill="#3fb950" font-family="{ff}" font-size="11px" font-weight="700">● SYSTEM READY</text>
  <text x="{svg_width-20}" y="{footer_y + 18}" text-anchor="end" fill="#3d444d" font-family="{ff}" font-size="11px">github.com/{config.USERNAME}</text>

</svg>
"""

    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[+] Premium Info Card SVG generated → {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    generate_info_card_svg()
