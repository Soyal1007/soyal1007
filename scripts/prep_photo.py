#!/usr/bin/env python3
"""
prep_photo.py: Downloads/prepares photo for ASCII portrait conversion.
"""

import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps
import requests

# Add root directory to sys.path to import config
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config
except ImportError:
    import config

SOURCE_PHOTO_PATH = ROOT_DIR / "source-photo.jpg"
PREPPED_PHOTO_PATH = ROOT_DIR / "source-prepped.png"


def download_avatar_if_needed():
    """Downloads GitHub avatar if source-photo.jpg does not exist."""
    if not SOURCE_PHOTO_PATH.exists():
        print(f"[*] 'source-photo.jpg' not found. Fetching GitHub avatar for '{config.USERNAME}'...")
        try:
            res = requests.get(config.AVATAR_URL, timeout=10)
            if res.status_code == 200:
                with open(SOURCE_PHOTO_PATH, "wb") as f:
                    f.write(res.content)
                print(f"[+] Saved avatar to {SOURCE_PHOTO_PATH.name}")
            else:
                raise Exception(f"HTTP Status {res.status_code}")
        except Exception as e:
            print(f"[!] Warning: Could not download avatar ({e}). Generating fallback image.")
            # Create placeholder image
            img = Image.new("RGB", (300, 300), color=(22, 27, 34))
            img.save(SOURCE_PHOTO_PATH)


def prep_photo(target_width: int = 70, target_height: int = 55) -> Image.Image:
    """Preprocesses photo for ASCII art conversion: contrast boost & grayscale."""
    download_avatar_if_needed()

    if not SOURCE_PHOTO_PATH.exists():
        raise FileNotFoundError(f"Source photo missing at {SOURCE_PHOTO_PATH}")

    with Image.open(SOURCE_PHOTO_PATH) as img:
        # Convert to Grayscale
        gray = img.convert("L")
        
        # Auto-contrast to maximize dynamic range
        contrast_img = ImageOps.autocontrast(gray, cutoff=2)
        
        # Enhance contrast further
        enhancer = ImageEnhance.Contrast(contrast_img)
        enhanced_img = enhancer.enhance(1.4)

        # Sharpness boost
        sharp_enhancer = ImageEnhance.Sharpness(enhanced_img)
        sharp_img = sharp_enhancer.enhance(1.5)

        # Resize to target ASCII matrix size
        resized_img = sharp_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Save prepped visualization
        resized_img.save(PREPPED_PHOTO_PATH)
        print(f"[+] Photo prepped and saved to {PREPPED_PHOTO_PATH.name} ({target_width}x{target_height})")
        return resized_img


if __name__ == "__main__":
    prep_photo()
