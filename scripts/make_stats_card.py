#!/usr/bin/env python3
"""
make_stats_card.py: Scrapes GitHub profile stats and renders a luxury, zero-dependency SVG stats card.
Bypasses 3rd party Vercel downtime and GitHub SVG sanitizer CSS stripping.
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
    """Fetches public profile stats for the user."""
    user_url = f"https://api.github.com/users/{config.USERNAME}"
    repos_url = f"https://api.github.com/users/{config.USERNAME}/repos?per_page=100"

    stats = {
        "public_repos": 4,
        "followers": 3,
        "stars": 0,
        "languages": {"Python": 45, "JavaScript": 25, "TypeScript": 15, "Dart": 15}
    }

    try:
        req = urllib.request.Request(user_url, headers={"User-Agent": "Python-Profile-Builder"})
        with urllib.request.urlopen(req) as resp:
            u_data = json.loads(resp.read().decode("utf-8"))
            stats["public_repos"] = u_data.get("public_repos", stats["public_repos"])
            stats["followers"] = u_data.get("followers", stats["followers"])
    except Exception as e:
        print(f"[!] Warning: Could not fetch user data from API: {e}")

    try:
        req = urllib.request.Request(repos_url, headers={"User-Agent": "Python-Profile-Builder"})
        with urllib.request.urlopen(req) as resp:
            r_data = json.loads(resp.read().decode("utf-8"))
            stars = sum(repo.get("stargazers_count", 0) for repo in r_data)
            stats["stars"] = stars

            # Calculate language distribution
            lang_counts = {}
            for repo in r_data:
                lang = repo.get("language")
                if lang:
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1

            if lang_counts:
                total_langs = sum(lang_counts.values())
                stats["languages"] = {
                    k: round((v / total_langs) * 100) for k, v in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:4]
                }
    except Exception as e:
        print(f"[!] Warning: Could not fetch repos data from API: {e}")

    return stats


def generate_stats_card_svg() -> Path:
    """Renders the luxury SVG stats card."""
    stats = fetch_github_stats()
    svg_width = 820
    svg_height = 220
    font_family = "'JetBrains Mono', 'Fira Code', Consolas, monospace"

    langs = stats.get("languages", {"Python": 45, "JavaScript": 25, "TypeScript": 15, "Dart": 15})
    colors = ["#00f2fe", "#3fb950", "#ffd700", "#bc8cff"]

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <!-- Container Box -->
  <rect width="{svg_width}" height="{svg_height}" x="0" y="0" fill="#090d16" rx="14" ry="14" stroke="#30363d" stroke-width="1.5" />

  <!-- Header Bar -->
  <path d="M 0 14 C 0 6.27 6.27 0 14 0 L {svg_width - 14} 0 C {svg_width - 6.27} 0 {svg_width} 6.27 {svg_width} 14 L {svg_width} 38 L 0 38 Z" fill="#161b22" />
  <line x1="0" y1="38" x2="{svg_width}" y2="38" stroke="#30363d" stroke-width="1" />

  <!-- Terminal Window Controls -->
  <circle cx="22" cy="19" r="5" fill="#ff5f56" />
  <circle cx="38" cy="19" r="5" fill="#ffbd2e" />
  <circle cx="54" cy="19" r="5" fill="#27c93f" />

  <!-- Header Title -->
  <text x="72" y="23" fill="#8b949e" font-family="{font_family}" font-size="11.5px" font-weight="600">{config.USERNAME.lower()}@github:~$ git stats --analytics</text>

  <!-- Left Column: Metrics -->
  <g transform="translate(32, 60)">
    <!-- Public Repos -->
    <g transform="translate(0, 20)">
      <text x="0" y="0" fill="#8b949e" font-family="{font_family}" font-size="13px" font-weight="600">📦 Public Repositories:</text>
      <text x="210" y="0" fill="#00f2fe" font-family="{font_family}" font-size="14px" font-weight="700">{stats['public_repos']}</text>
    </g>

    <!-- Stars -->
    <g transform="translate(0, 56)">
      <text x="0" y="0" fill="#8b949e" font-family="{font_family}" font-size="13px" font-weight="600">🌟 Total Stars Earned:</text>
      <text x="210" y="0" fill="#ffd700" font-family="{font_family}" font-size="14px" font-weight="700">{stats['stars']}</text>
    </g>

    <!-- Followers -->
    <g transform="translate(0, 92)">
      <text x="0" y="0" fill="#8b949e" font-family="{font_family}" font-size="13px" font-weight="600">👥 GitHub Followers:</text>
      <text x="210" y="0" fill="#3fb950" font-family="{font_family}" font-size="14px" font-weight="700">{stats['followers']}</text>
    </g>

    <!-- Status -->
    <g transform="translate(0, 128)">
      <text x="0" y="0" fill="#8b949e" font-family="{font_family}" font-size="13px" font-weight="600">⚡ Developer Status:</text>
      <text x="210" y="0" fill="#bc8cff" font-family="{font_family}" font-size="13px" font-weight="700">Active Contributor</text>
    </g>
  </g>

  <!-- Divider Line -->
  <line x1="390" y1="56" x2="390" y2="194" stroke="#30363d" stroke-width="1.2" stroke-dasharray="4 3" />

  <!-- Right Column: Top Languages -->
  <g transform="translate(420, 60)">
    <text x="0" y="16" fill="#f0f6fc" font-family="{font_family}" font-size="13px" font-weight="700">📊 Top Languages &amp; Stack</text>
"""

    y_offset = 46
    for idx, (lang_name, pct) in enumerate(langs.items()):
        c = colors[idx % len(colors)]
        bar_width = int(pct * 2.4)  # Max width 240px

        svg_content += f"""
    <!-- {lang_name} -->
    <g transform="translate(0, {y_offset})">
      <text x="0" y="0" fill="#c9d1d9" font-family="{font_family}" font-size="12px" font-weight="600">{lang_name}</text>
      <text x="320" y="0" fill="{c}" font-family="{font_family}" font-size="12px" font-weight="700" text-anchor="end">{pct}%</text>

      <!-- Progress Bar Track -->
      <rect x="0" y="8" width="320" height="8" fill="#161b22" rx="4" ry="4" stroke="#30363d" stroke-width="0.8" />
      <!-- Progress Bar Fill -->
      <rect x="0" y="8" width="{bar_width}" height="8" fill="{c}" rx="4" ry="4" />
    </g>
"""
        y_offset += 32

    svg_content += """  </g>
</svg>
"""

    with open(OUTPUT_SVG_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Luxury Native GitHub Stats Card SVG generated at {OUTPUT_SVG_PATH.name}")
    return OUTPUT_SVG_PATH


if __name__ == "__main__":
    generate_stats_card_svg()
