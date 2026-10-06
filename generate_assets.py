#!/usr/bin/env python3
"""
Asset Generator for Neon City using Google Gemini (Nano Banana Pro)
Generates cyberpunk-themed pixel art sprites and tiles.
"""

import os
import sys
import base64
import json
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests

# Configuration
API_KEY = os.environ.get('GEMINI_API_KEY', '')
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"

ASSETS_DIR = Path(__file__).parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

# Asset definitions with prompts
ASSETS = {
    "buildings": [
        {
            "name": "tower_neon_01",
            "prompt": "Pixel art cyberpunk skyscraper, tall narrow building with glowing neon windows, pink and cyan lights, dark background, 64x128 pixels, side view, 2D game asset, transparent background"
        },
        {
            "name": "tower_industrial_01",
            "prompt": "Pixel art industrial tower, rusty metal pipes and vents, orange warning lights, steam vents, dark cyberpunk style, 64x96 pixels, side view, 2D game asset"
        },
        {
            "name": "apartment_block_01",
            "prompt": "Pixel art cyberpunk apartment building, stacked balconies with laundry, mixed neon signs, dense urban style, 96x80 pixels, side view, 2D game asset"
        },
    ],
    "signs": [
        {
            "name": "neon_bar_01",
            "prompt": "Pixel art neon sign spelling BAR, hot pink glowing tubes, slight flicker effect implied, cyberpunk style, 48x24 pixels, transparent background"
        },
        {
            "name": "neon_hotel_01",
            "prompt": "Pixel art vertical neon sign spelling HOTEL, cyan blue glow, cyberpunk aesthetic, 24x64 pixels, transparent background"
        },
        {
            "name": "neon_ramen_01",
            "prompt": "Pixel art Japanese ramen shop sign with noodle bowl icon, warm orange and red neon, 48x32 pixels, cyberpunk style"
        },
        {
            "name": "hologram_ad_01",
            "prompt": "Pixel art holographic advertisement billboard, translucent blue projection effect, futuristic product ad, 64x48 pixels, cyberpunk"
        },
    ],
    "props": [
        {
            "name": "vending_machine_01",
            "prompt": "Pixel art cyberpunk vending machine, glowing drink options, neon accents, 32x48 pixels, side view, 2D game asset"
        },
        {
            "name": "trash_pile_01",
            "prompt": "Pixel art garbage pile with neon debris, broken electronics, cyberpunk urban decay, 48x32 pixels"
        },
        {
            "name": "street_vendor_01",
            "prompt": "Pixel art cyberpunk street food cart, steam rising, neon menu sign, 48x48 pixels, side view"
        },
        {
            "name": "hover_car_01",
            "prompt": "Pixel art parked hover car, sleek futuristic design, glowing undercarriage, 64x32 pixels, side view"
        },
    ],
    "backgrounds": [
        {
            "name": "skyline_layer_01",
            "prompt": "Pixel art distant cyberpunk city skyline silhouette, foggy atmosphere, scattered building lights, 256x128 pixels, dark purple and blue tones"
        },
        {
            "name": "clouds_neon_01",
            "prompt": "Pixel art night clouds with neon light pollution, pink and cyan reflections on clouds, 256x64 pixels, seamless horizontal tile"
        },
    ],
    "tiles": [
        {
            "name": "street_wet_01",
            "prompt": "Pixel art wet street tile, puddle reflections of neon lights, dark asphalt, 32x32 pixels, seamless tileable"
        },
        {
            "name": "building_wall_01",
            "prompt": "Pixel art cyberpunk building wall texture, metal panels with rust, exposed wiring, 32x32 pixels, seamless tileable"
        },
    ],
}


def generate_image(prompt: str, filename: str) -> bool:
    """Generate an image using Gemini API."""

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [{
            "parts": [{
                "text": f"Generate a pixel art image: {prompt}. Style: retro pixel art, limited color palette, clean pixels, no anti-aliasing, suitable for 2D side-scrolling game."
            }]
        }],
        "generationConfig": {
            "temperature": 0.9,
            "topK": 40,
            "topP": 0.95,
        }
    }

    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()

            # Check for image data in response
            if "candidates" in data:
                for candidate in data["candidates"]:
                    if "content" in candidate:
                        for part in candidate["content"].get("parts", []):
                            if "inlineData" in part:
                                image_data = part["inlineData"]["data"]
                                image_bytes = base64.b64decode(image_data)

                                filepath = ASSETS_DIR / f"{filename}.png"
                                with open(filepath, "wb") as f:
                                    f.write(image_bytes)

                                print(f"  Generated: {filepath}")
                                return True

            # If no image, the model might not support image generation
            print(f"  Note: Text response received (model may not support image generation)")
            print(f"  Response preview: {str(data)[:200]}...")
            return False

        else:
            print(f"  Error {response.status_code}: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"  Error: {e}")
        return False


def generate_placeholder(name: str, category: str) -> None:
    """Generate a placeholder SVG asset."""
    colors = {
        "buildings": ("#1a1a2e", "#ff2a6d"),
        "signs": ("#0a0a0f", "#05d9e8"),
        "props": ("#15152a", "#ff6b2b"),
        "backgrounds": ("#0d0d1a", "#d300c5"),
        "tiles": ("#101020", "#00ff9f"),
    }

    bg, accent = colors.get(category, ("#1a1a2e", "#ff2a6d"))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="{bg}"/>
  <rect x="8" y="8" width="48" height="48" fill="none" stroke="{accent}" stroke-width="2"/>
  <text x="32" y="36" font-family="monospace" font-size="8" fill="{accent}" text-anchor="middle">{name[:10]}</text>
</svg>'''

    filepath = ASSETS_DIR / f"{name}.svg"
    with open(filepath, "w") as f:
        f.write(svg)
    print(f"  Placeholder: {filepath}")


def main():
    print("=" * 60)
    print("NEON CITY Asset Generator")
    print("Using Gemini 2.0 Flash (Nano Banana Pro)")
    print("=" * 60)

    total = sum(len(assets) for assets in ASSETS.values())
    generated = 0

    for category, assets in ASSETS.items():
        print(f"\n[{category.upper()}]")
        category_dir = ASSETS_DIR / category
        category_dir.mkdir(exist_ok=True)

        for asset in assets:
            print(f"  Generating: {asset['name']}...")

            success = generate_image(asset["prompt"], f"{category}/{asset['name']}")

            if not success:
                # Create placeholder
                generate_placeholder(asset["name"], category)
            else:
                generated += 1

    print("\n" + "=" * 60)
    print(f"Complete! Generated {generated}/{total} assets")
    print(f"Assets saved to: {ASSETS_DIR}")
    print("=" * 60)

    # Generate manifest
    manifest = {
        "generated": generated,
        "total": total,
        "categories": {cat: [a["name"] for a in assets] for cat, assets in ASSETS.items()}
    }

    with open(ASSETS_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest saved to: {ASSETS_DIR / 'manifest.json'}")


if __name__ == "__main__":
    main()
