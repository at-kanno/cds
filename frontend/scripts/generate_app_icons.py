#!/usr/bin/env python3
"""Generate Android/iOS launcher icons from branding/*/app_icon_1024.png."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BRANDING = ROOT / "branding"

ANDROID_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

# (filename, pixel size) matching ios/.../AppIcon.appiconset/Contents.json
IOS_ICONS = [
    ("Icon-App-20x20@1x.png", 20),
    ("Icon-App-20x20@2x.png", 40),
    ("Icon-App-20x20@3x.png", 60),
    ("Icon-App-29x29@1x.png", 29),
    ("Icon-App-29x29@2x.png", 58),
    ("Icon-App-29x29@3x.png", 87),
    ("Icon-App-40x40@1x.png", 40),
    ("Icon-App-40x40@2x.png", 80),
    ("Icon-App-40x40@3x.png", 120),
    ("Icon-App-60x60@2x.png", 120),
    ("Icon-App-60x60@3x.png", 180),
    ("Icon-App-76x76@1x.png", 76),
    ("Icon-App-76x76@2x.png", 152),
    ("Icon-App-83.5x83.5@2x.png", 167),
    ("Icon-App-1024x1024@1x.png", 1024),
]


def _load_square(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGBA")
    if image.size != (1024, 1024):
        image = image.resize((1024, 1024), Image.Resampling.LANCZOS)
    return image


def _save_resized(source: Image.Image, size: int, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    resized = source.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(dest, format="PNG")
    print(f"  wrote {dest.relative_to(ROOT)} ({size}x{size})")


def generate_android(flavor: str, source: Image.Image) -> None:
    base = ROOT / "android" / "app" / "src" / flavor / "res"
    for folder, size in ANDROID_SIZES.items():
        _save_resized(source, size, base / folder / "ic_launcher.png")


def generate_ios(asset_name: str, source: Image.Image, contents_src: Path) -> None:
    dest_dir = ROOT / "ios" / "Runner" / "Assets.xcassets" / asset_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_contents = dest_dir / "Contents.json"
    if dest_contents.resolve() != contents_src.resolve():
        shutil.copy2(contents_src, dest_contents)
    for filename, size in IOS_ICONS:
        _save_resized(source, size, dest_dir / filename)


def main() -> None:
    contents = (
        ROOT / "ios" / "Runner" / "Assets.xcassets" / "AppIcon.appiconset" / "Contents.json"
    )
    if not contents.is_file():
        raise SystemExit(f"Missing iOS Contents.json: {contents}")

    subjects = {
        "cds": {
            "android_flavor": "cds",
            "ios_asset": "AppIcon.appiconset",
        },
        "spanish4": {
            "android_flavor": "spanish4",
            "ios_asset": "AppIcon-Spanish4.appiconset",
        },
        "toeic": {
            "android_flavor": "toeic",
            "ios_asset": "AppIcon-Toeic.appiconset",
        },
    }

    for subject, targets in subjects.items():
        src_path = BRANDING / subject / "app_icon_1024.png"
        if not src_path.is_file() or src_path.stat().st_size == 0:
            print(f"SKIP {subject}: missing {src_path}")
            continue
        print(f"==> {subject}")
        source = _load_square(src_path)
        generate_android(targets["android_flavor"], source)
        generate_ios(targets["ios_asset"], source, contents)
        # Keep a store-ready 1024 copy next to branding.
        store = BRANDING / subject / "store_icon_1024.png"
        shutil.copy2(src_path, store)

    print("Done.")


if __name__ == "__main__":
    main()
