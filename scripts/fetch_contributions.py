#!/usr/bin/env python3
"""
fetch_contributions.py: Scrapes public GitHub contribution calendar data.
Saves structured contribution json to data/contributions.json.
"""

import json
import re
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config
except ImportError:
    import config

DATA_DIR = ROOT_DIR / "data"
OUTPUT_JSON_PATH = DATA_DIR / "contributions.json"


def fetch_contributions(username: str = None) -> dict:
    """Fetches contribution data from GitHub public profile HTML."""
    if not username:
        username = config.USERNAME

    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Fetching contribution data for '{username}' from {url}...")
    
    days_data = []
    total_contributions = 0

    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code != 200:
            raise Exception(f"HTTP Status {res.status_code}")

        soup = BeautifulSoup(res.text, "html.parser")
        
        # Extract total contributions string if available (e.g., "30 contributions in the last year")
        heading = soup.find("h2", class_=lambda c: c and "f4" in c)
        heading_text = heading.get_text(strip=True) if heading else ""

        # Map tooltip texts by element ID
        tooltips = {}
        for tt in soup.find_all("tool-tip"):
            for_id = tt.get("for")
            if for_id:
                tooltips[for_id] = tt.get_text(strip=True)

        # Parse calendar day elements (<td class="ContributionCalendar-day"> or <rect>)
        day_elements = soup.find_all(
            ["td", "rect"],
            class_=lambda c: c and "ContributionCalendar-day" in c
        )

        for el in day_elements:
            date_str = el.get("data-date")
            if not date_str:
                continue

            try:
                level = int(el.get("data-level", 0))
            except ValueError:
                level = 0

            el_id = el.get("id", "")
            tooltip_txt = tooltips.get(el_id, "")

            count = 0
            match = re.search(r"(\d+)\s+contribution", tooltip_txt, re.IGNORECASE)
            if match:
                count = int(match.group(1))
            elif "No contributions" in tooltip_txt:
                count = 0

            total_contributions += count
            days_data.append({
                "date": date_str,
                "count": count,
                "level": level,
                "tooltip": tooltip_txt
            })

    except Exception as err:
        print(f"[!] Warning: Failed to fetch online contribution data ({err}).")

    # If scraping yielded no days (e.g. offline/network issue), provide graceful structure
    if not days_data:
        print("[!] Generating fallback calendar data structure...")
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=364)
        curr = start_date
        while curr <= end_date:
            days_data.append({
                "date": curr.strftime("%Y-%m-%d"),
                "count": 0,
                "level": 0,
                "tooltip": f"No contributions on {curr.strftime('%b %d, %Y')}"
            })
            curr += timedelta(days=1)

    result_payload = {
        "username": username,
        "total": total_contributions,
        "count_days": len(days_data),
        "days": days_data
    }

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(result_payload, f, indent=2)

    print(f"[+] Contributions saved to {OUTPUT_JSON_PATH.name} (Total: {total_contributions}, Days: {len(days_data)})")
    return result_payload


if __name__ == "__main__":
    fetch_contributions()
