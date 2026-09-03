#!/usr/bin/env python3
"""
render_heatmap_svg.py: Renders an animated SVG contribution heatmap from data/contributions.json.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config, fetch_contributions
except ImportError:
    import config
    import fetch_contributions

DATA_FILE = ROOT_DIR / "data" / "contributions.json"
OUTPUT_SVG_PATH = ROOT_DIR / "contrib-heatmap.svg"

# Color theme levels matching GitHub Dark Mode
COLOR_LEVELS = {
    0: {"fill": "#161b22", "stroke": "#21262d"},
    1: {"fill": "#0e4429", "stroke": "#006d32"},
    2: {"fill": "#006d32", "stroke": "#26a641"},
    3: {"fill": "#26a641", "stroke": "#39d353"},
    4: {"fill": "#39d353", "stroke": "#56f077"},
}


def render_heatmap_svg() -> Path:
    """Renders the contribution heatmap SVG from contributions.json."""
    if not DATA_FILE.exists():
        fetch_contributions.fetch_contributions()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    days_data = payload.get("days", [])
    total_contributions = payload.get("total", 0)

    # Calculate grid layout parameters
    svg_width = 820
    svg_height = 210
    
    cell_size = 10.5
    cell_gap = 3.0
    cell_step = cell_size + cell_gap
    
    grid_start_x = 42
    grid_start_y = 64

    # Group days into weeks (columns)
    # Filter or organize days by weekday (0=Sun, 6=Sat)
    weeks = []
    current_week = []
    
    for d in days_data:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        wday = dt.weekday()
        # Convert Monday=0 to Sunday=0 layout if desired, or standard GitHub layout (Sun=0)
        # Python weekday(): Mon=0 ... Sun=6. GitHub layout: Sun=0 ... Sat=6.
        gh_wday = (wday + 1) % 7

        if gh_wday == 0 and current_week:
            weeks.append(current_week)
            current_week = []

        current_week.append({
            "date": d["date"],
            "count": d["count"],
            "level": d.get("level", 0),
            "wday": gh_wday,
            "tooltip": d.get("tooltip", "")
        })

    if current_week:
        weeks.append(current_week)

    # Limit to latest 53 weeks for desktop SVG display
    weeks = weeks[-53:]

    # Build month labels
    month_labels = []
    last_month = None
    for w_idx, week in enumerate(weeks):
        if week:
            first_day_dt = datetime.strptime(week[0]["date"], "%Y-%m-%d")
            m_name = first_day_dt.strftime("%b")
            if m_name != last_month:
                month_labels.append({
                    "month": m_name,
                    "x": grid_start_x + (w_idx * cell_step)
                })
                last_month = m_name

    # SVG string construction
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <!-- Glowing Accent -->
    <filter id="glow-l4" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>

    <style>
      .bg {{ fill: url(#bg-grad); rx: 12px; ry: 12px; stroke: #30363d; stroke-width: 1.5px; }}
      .title-bar {{ fill: #161b22; }}
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}
      
      .font-mono {{ font-family: 'Fira Code', 'JetBrains Mono', Consolas, monospace; }}
      .title-text {{ font-size: 11px; fill: #8b949e; font-weight: 600; }}
      .stats-text {{ font-size: 11px; fill: #3fb950; font-weight: 600; }}

      .axis-text {{ font-size: 9.5px; fill: #7d8590; font-weight: 500; }}

      .day-cell {{
        rx: 2.5px;
        ry: 2.5px;
        transition: transform 0.2s ease, filter 0.2s ease;
        animation: cellFadeIn 0.8s ease-out forwards;
        opacity: 0;
      }}

      .day-cell.active {{
        animation: pulseActive 3s ease-in-out infinite alternate;
      }}

      @keyframes cellFadeIn {{
        from {{ opacity: 0; transform: scale(0.6); }}
        to {{ opacity: 1; transform: scale(1); }}
      }}

      @keyframes pulseActive {{
        0% {{ filter: brightness(1); }}
        50% {{ filter: brightness(1.25) drop-shadow(0 0 2px rgba(57, 211, 83, 0.6)); }}
        100% {{ filter: brightness(1); }}
      }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect class="bg" width="{svg_width}" height="{svg_height}" x="0" y="0" />

  <!-- Header Bar -->
  <path d="M 0 12 C 0 5.37 5.37 0 12 0 L {svg_width - 12} 0 C {svg_width - 5.37} 0 {svg_width} 5.37 {svg_width} 12 L {svg_width} 36 L 0 36 Z" class="title-bar" />
  <line x1="0" y1="36" x2="{svg_width}" y2="36" stroke="#30363d" stroke-width="1" />
  
  <circle class="dot-red" cx="20" cy="18" r="5" />
  <circle class="dot-yellow" cx="36" cy="18" r="5" />
  <circle class="dot-green" cx="52" cy="18" r="5" />
  
  <text class="font-mono title-text" x="70" y="22">{config.USERNAME.lower()}@github:~$ git log --contributions --year</text>
  <text class="font-mono stats-text" x="{svg_width - 24}" y="22" text-anchor="end">🔥 {total_contributions} Contributions</text>

  <!-- Month Labels -->
"""

    # Add Month Labels
    for m in month_labels:
        svg_content += f'  <text class="font-mono axis-text" x="{m["x"]}" y="{grid_start_y - 8}">{m["month"]}</text>\n'

    # Add Weekday Labels (Mon, Wed, Fri)
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for d_name, d_idx in day_labels:
        y_pos = grid_start_y + (d_idx * cell_step) + 8.5
        svg_content += f'  <text class="font-mono axis-text" x="{grid_start_x - 28}" y="{y_pos:.1f}">{d_name}</text>\n'

    # Render Grid Cells
    svg_content += '  <!-- Contribution Grid Cells -->\n'
    
    for w_idx, week in enumerate(weeks):
        x_pos = grid_start_x + (w_idx * cell_step)
        for day in week:
            y_pos = grid_start_y + (day["wday"] * cell_step)
            lvl = day["level"]
            colors = COLOR_LEVELS.get(lvl, COLOR_LEVELS[0])
            
            # Staggered animation delay
            anim_delay = (w_idx * 0.015) + (day["wday"] * 0.02)
            active_cls = " active" if lvl > 0 else ""
            
            tooltip_attr = f'title="{day["tooltip"]}"' if day["tooltip"] else ""

            svg_content += f'  <rect class="day-cell{active_cls}" x="{x_pos:.1f}" y="{y_pos:.1f}" width="{cell_size}" height="{cell_size}" fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="0.8" style="animation-delay: {anim_delay:.3f}s;" {tooltip_attr} />\n'

    # Add Legend Footer
    legend_y = svg_height - 18
    legend_x = svg_width - 170
    
    svg_content += f"""
  <!-- Heatmap Legend Footer -->
  <g class="font-mono axis-text" transform="translate({legend_x}, {legend_y})">
    <text x="-34" y="9">Less</text>
"""
    for lvl in range(5):
        c = COLOR_LEVELS[lvl]
        lx = lvl * 14
        svg_content += f'    <rect x="{lx}" y="0" width="10" height="10" rx="2" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="0.8" />\n'

    svg_content += f"""    <text x="74" y="9">More</text>
  </g>
</svg>
"""

    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Animated Heatmap SVG generated at {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    render_heatmap_svg()
