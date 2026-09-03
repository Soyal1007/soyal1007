#!/usr/bin/env python3
"""
prep_photo.py: Preprocesses user's photo for high-detail ASCII portrait generation.
Crops upper body/face and enhances contrast, sharpness, and brightness.
"""

import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from scripts import config
except ImportError:
    import config

SOURCE_PHOTO_PATH = ROOT_DIR / "source-photo.jpg"
PREPPED_PHOTO_PATH = ROOT_DIR / "source-prepped.png"


def prep_photo(target_width: int = 76, target_height: int = 58) -> Image.Image:
    """Crops and pre-processes photo for ASCII portrait conversion."""
    if not SOURCE_PHOTO_PATH.exists():
        raise FileNotFoundError(f"Source photo missing at {SOURCE_PHOTO_PATH}")

    with Image.open(SOURCE_PHOTO_PATH) as img:
        # Get dimensions
        w, h = img.size

        # Smart crop for upper body & face if image is vertical portrait (e.g. 768x1024)
        if h > w:
            # Crop upper body (approx 18% to 68% of height, centered horizontally)
            left = int(w * 0.15)
            top = int(h * 0.14)
            right = int(w * 0.85)
            bottom = int(h * 0.65)
            cropped_img = img.crop((left, top, right, bottom))
        else:
            cropped_img = img

        # Convert to Grayscale
        gray = cropped_img.convert("L")

        # Auto-contrast to stretch dynamic range
        contrast_img = ImageOps.autocontrast(gray, cutoff=2)

        # Enhance contrast further for crisp facial features
        contrast_enhancer = ImageEnhance.Contrast(contrast_img)
        enhanced_img = contrast_enhancer.enhance(1.45)

        # Enhance sharpness for glasses, hair & collar definition
        sharp_enhancer = ImageEnhance.Sharpness(enhanced_img)
        sharp_img = sharp_enhancer.enhance(1.8)

        # Brightness adjustment
        bright_enhancer = ImageEnhance.Brightness(sharp_img)
        final_img = bright_enhancer.enhance(1.05)

        # Resize to target matrix size
        resized_img = final_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # Save prepped image
        resized_img.save(PREPPED_PHOTO_PATH)
        print(f"[+] Photo prepped and saved to {PREPPED_PHOTO_PATH.name} ({target_width}x{target_height})")
        return resized_img


if __name__ == "__main__":
    prep_photo()
