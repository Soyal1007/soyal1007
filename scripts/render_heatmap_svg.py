#!/usr/bin/env python3
"""
render_heatmap_svg.py: Renders an animated luxury SVG contribution heatmap from data/contributions.json.
Guarantees 100% base visibility (opacity: 1) on GitHub.
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

# Luxury Theme Levels
COLOR_LEVELS = {
    0: {"fill": "#161b22", "stroke": "#21262d"},
    1: {"fill": "#0e4429", "stroke": "#006d32"},
    2: {"fill": "#006d32", "stroke": "#26a641"},
    3: {"fill": "#26a641", "stroke": "#39d353"},
    4: {"fill": "#00f2fe", "stroke": "#38ef7d"},
}


def render_heatmap_svg() -> Path:
    """Renders the contribution heatmap SVG from contributions.json."""
    if not DATA_FILE.exists():
        fetch_contributions.fetch_contributions()

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    days_data = payload.get("days", [])
    total_contributions = payload.get("total", 0)

    svg_width = 820
    svg_height = 210

    cell_size = 10.5
    cell_gap = 3.0
    cell_step = cell_size + cell_gap

    grid_start_x = 42
    grid_start_y = 64

    weeks = []
    current_week = []

    for d in days_data:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        wday = dt.weekday()
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

    weeks = weeks[-53:]

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

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="heatmap-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="50%" stop-color="#0d1117" />
      <stop offset="100%" stop-color="#161b22" />
    </linearGradient>

    <style>
      .bg-card {{ fill: url(#heatmap-bg); rx: 14px; ry: 14px; stroke: #30363d; stroke-width: 1.5px; opacity: 1; }}
      .header-bar {{ fill: #161b22; opacity: 1; }}
      .dot-red {{ fill: #ff5f56; }}
      .dot-yellow {{ fill: #ffbd2e; }}
      .dot-green {{ fill: #27c93f; }}

      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace; }}
      .title-text {{ font-size: 11.5px; fill: #8b949e; font-weight: 600; opacity: 1; }}
      .stats-text {{ font-size: 11.5px; fill: #ffd700; font-weight: 700; opacity: 1; }}

      .axis-text {{ font-size: 9.5px; fill: #7d8590; font-weight: 500; opacity: 1; }}

      .day-cell {{
        rx: 2.5px;
        ry: 2.5px;
        opacity: 1; /* Guaranteed 100% visible on GitHub */
      }}

      .day-cell.active {{
        animation: pulseHeatmap 3s ease-in-out infinite alternate;
      }}

      @keyframes pulseHeatmap {{
        0% {{ filter: brightness(1); }}
        50% {{ filter: brightness(1.3) drop-shadow(0 0 2px rgba(0, 242, 254, 0.6)); }}
        100% {{ filter: brightness(1); }}
      }}
    </style>
  </defs>

  <!-- Container Box -->
  <rect class="bg-card" width="{svg_width}" height="{svg_height}" x="0" y="0" />

  <!-- Header Bar -->
  <path d="M 0 14 C 0 6.27 6.27 0 14 0 L {svg_width - 14} 0 C {svg_width - 6.27} 0 {svg_width} 6.27 {svg_width} 14 L {svg_width} 38 L 0 38 Z" class="header-bar" />
  <line x1="0" y1="38" x2="{svg_width}" y2="38" stroke="#30363d" stroke-width="1" />

  <circle class="dot-red" cx="22" cy="19" r="5" />
  <circle class="dot-yellow" cx="38" cy="19" r="5" />
  <circle class="dot-green" cx="54" cy="19" r="5" />

  <text class="font-mono title-text" x="72" y="23">{config.USERNAME.lower()}@github:~$ git log --contributions --year</text>
  <text class="font-mono stats-text" x="{svg_width - 24}" y="23" text-anchor="end">🔥 {total_contributions} Contributions</text>

  <!-- Month Labels -->
"""

    for m in month_labels:
        svg_content += f'  <text class="font-mono axis-text" x="{m["x"]}" y="{grid_start_y - 8}">{m["month"]}</text>\n'

    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for d_name, d_idx in day_labels:
        y_pos = grid_start_y + (d_idx * cell_step) + 8.5
        svg_content += f'  <text class="font-mono axis-text" x="{grid_start_x - 28}" y="{y_pos:.1f}">{d_name}</text>\n'

    svg_content += '  <!-- Contribution Grid Cells -->\n'

    for w_idx, week in enumerate(weeks):
        x_pos = grid_start_x + (w_idx * cell_step)
        for day in week:
            y_pos = grid_start_y + (day["wday"] * cell_step)
            lvl = day["level"]
            colors = COLOR_LEVELS.get(lvl, COLOR_LEVELS[0])
            active_cls = " active" if lvl > 0 else ""
            tooltip_attr = f'title="{day["tooltip"]}"' if day["tooltip"] else ""

            svg_content += f'  <rect class="day-cell{active_cls}" x="{x_pos:.1f}" y="{y_pos:.1f}" width="{cell_size}" height="{cell_size}" fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="0.8" {tooltip_attr} />\n'

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

    print(f"[+] Luxury Heatmap SVG generated at {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    render_heatmap_svg()
