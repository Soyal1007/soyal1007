#!/usr/bin/env python3
"""
make_stats_card.py: Generates a premium inline SVG stats & analytics card.
Fully inline attributes (no CSS classes) for guaranteed GitHub rendering.
"""

import json
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config
except ImportError:
    import config

OUTPUT_SVG_PATH = ROOT_DIR / "stats-card.svg"


def fetch_github_stats() -> dict:
    stats = {"public_repos": 4, "followers": 3, "stars": 0,
             "languages": {"Python": 40, "JavaScript": 25, "TypeScript": 20, "Dart": 15}}
    try:
        req = urllib.request.Request(
            f"https://api.github.com/users/{config.USERNAME}",
            headers={"User-Agent": "Python-Profile-Builder"})
        with urllib.request.urlopen(req) as r:
            d = json.loads(r.read().decode())
            stats["public_repos"] = d.get("public_repos", 4)
            stats["followers"] = d.get("followers", 3)
    except Exception:
        pass
    try:
        req = urllib.request.Request(
            f"https://api.github.com/users/{config.USERNAME}/repos?per_page=100",
            headers={"User-Agent": "Python-Profile-Builder"})
        with urllib.request.urlopen(req) as r:
            repos = json.loads(r.read().decode())
            stats["stars"] = sum(repo.get("stargazers_count", 0) for repo in repos)
            lang_counts = {}
            for repo in repos:
                lang = repo.get("language")
                if lang:
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1
            if lang_counts:
                total = sum(lang_counts.values())
                stats["languages"] = {
                    k: round((v / total) * 100)
                    for k, v in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:6]
                }
    except Exception:
        pass
    return stats


def generate_stats_card_svg() -> Path:
    stats = fetch_github_stats()
    svg_w = 860
    svg_h = 230
    ff = "'JetBrains Mono', 'Fira Code', Consolas, monospace"

    langs = list(stats["languages"].items())[:6]
    lang_colors = ["#00f2fe", "#bc8cff", "#3fb950", "#ffd700", "#e040fb", "#ff6b6b"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}" height="{svg_h}">
  <defs>
    <linearGradient id="sc-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <linearGradient id="sc-div" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#21262d"/>
      <stop offset="50%" stop-color="#3d444d"/>
      <stop offset="100%" stop-color="#21262d"/>
    </linearGradient>
  </defs>

  <!-- Container -->
  <rect width="{svg_w}" height="{svg_h}" rx="14" ry="14" fill="url(#sc-bg)" stroke="#1e2d3d" stroke-width="1.5"/>

  <!-- Header Bar -->
  <path d="M0 14 Q0 0 14 0 L{svg_w-14} 0 Q{svg_w} 0 {svg_w} 14 L{svg_w} 38 L0 38Z" fill="#0d1117"/>
  <line x1="0" y1="38" x2="{svg_w}" y2="38" stroke="#21262d" stroke-width="1"/>

  <!-- Window dots -->
  <circle cx="20" cy="19" r="5.5" fill="#ff5f56"/>
  <circle cx="37" cy="19" r="5.5" fill="#ffbd2e"/>
  <circle cx="54" cy="19" r="5.5" fill="#27c93f"/>

  <!-- Header text -->
  <text x="72" y="24" fill="#6e7681" font-family="{ff}" font-size="11px" font-weight="600">{config.USERNAME.lower()}@github:~$ git log --stat --analytics 2024</text>
  <text x="{svg_w-20}" y="24" text-anchor="end" fill="#ffd700" font-family="{ff}" font-size="11px" font-weight="700">⚡ Live Stats</text>

  <!-- LEFT: Metric Cards -->
  <g transform="translate(24, 54)">
"""

    metrics = [
        ("📦", "Repositories", stats['public_repos'], "#00f2fe"),
        ("⭐", "Total Stars", stats['stars'], "#ffd700"),
        ("👥", "Followers", stats['followers'], "#3fb950"),
        ("⚡", "Status", "Active Dev", "#bc8cff"),
    ]

    card_w_m = 132
    gap = 12
    for i, (icon, label, val, color) in enumerate(metrics):
        cx = i * (card_w_m + gap)
        svg += f"""
    <!-- Metric {i} -->
    <rect x="{cx}" y="0" width="{card_w_m}" height="74" rx="8" ry="8" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <text x="{cx + card_w_m//2}" y="22" text-anchor="middle" fill="{color}" font-family="{ff}" font-size="18px">{icon}</text>
    <text x="{cx + card_w_m//2}" y="44" text-anchor="middle" fill="{color}" font-family="{ff}" font-size="20px" font-weight="700">{val}</text>
    <text x="{cx + card_w_m//2}" y="62" text-anchor="middle" fill="#6e7681" font-family="{ff}" font-size="10px">{label}</text>
"""

    svg += f"""  </g>

  <!-- Vertical divider -->
  <rect x="584" y="50" width="1" height="{svg_h - 68}" fill="url(#sc-div)"/>

  <!-- RIGHT: Top Languages -->
  <g transform="translate(600, 50)">
    <text x="0" y="14" fill="#8b949e" font-family="{ff}" font-size="11px" font-weight="700" letter-spacing="2">TOP LANGUAGES</text>
"""

    bar_max_w = 240
    for i, (lang, pct) in enumerate(langs):
        c = lang_colors[i % len(lang_colors)]
        bar_w = int((pct / 100) * bar_max_w)
        y = 30 + i * 26
        svg += f"""
    <text x="0" y="{y}" fill="#c9d1d9" font-family="{ff}" font-size="11.5px" font-weight="600">{lang}</text>
    <text x="{bar_max_w + 50}" y="{y}" text-anchor="end" fill="{c}" font-family="{ff}" font-size="11.5px" font-weight="700">{pct}%</text>
    <rect x="0" y="{y + 4}" width="{bar_max_w}" height="7" rx="3" ry="3" fill="#161b22" stroke="#21262d" stroke-width="0.5"/>
    <rect x="0" y="{y + 4}" width="{bar_w}" height="7" rx="3" ry="3" fill="{c}"/>
"""

    svg += f"""  </g>

  <!-- Footer -->
  <line x1="24" y1="{svg_h - 24}" x2="{svg_w - 24}" y2="{svg_h - 24}" stroke="#21262d" stroke-width="1"/>
  <text x="24" y="{svg_h - 8}" fill="#3d444d" font-family="{ff}" font-size="10px">Auto-updated daily via GitHub Actions · github.com/{config.USERNAME}</text>
  <circle cx="{svg_w - 28}" cy="{svg_h - 14}" r="4" fill="#3fb950"/>
  <text x="{svg_w - 20}" y="{svg_h - 9}" fill="#3fb950" font-family="{ff}" font-size="10px">LIVE</text>

</svg>
"""

    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"[+] Premium Stats Card SVG generated → {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    generate_stats_card_svg()
