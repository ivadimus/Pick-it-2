"""Generate Pick-it home-screen / favicon icons (cloud on sky-blue)."""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CLOUD_CANDIDATES = [
    ROOT / "Assets" / "cloud11.png",
    Path(
        r"C:\Users\vadimt\.cursor\projects\c-Users-vadimt-OneDrive-Playtika-Ltd-Desktop-Pick-it-main-Final-Prize\assets\cloud11-c5a501c9-3cbe-4ac3-971a-d1d6ae77707a.png"
    ),
]
OUT_DIR = ROOT / "Assets" / "icons"

TOP = (158, 221, 255)
MID = (126, 200, 240)
BOTTOM = (61, 168, 218)


def pick_cloud() -> Path:
    for path in CLOUD_CANDIDATES:
        if path.is_file():
            return path
    raise FileNotFoundError("cloud11.png not found")


def sky_gradient(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(img)
    for y in range(size):
        t = y / max(size - 1, 1)
        if t < 0.55:
            u = t / 0.55
            r = int(TOP[0] + (MID[0] - TOP[0]) * u)
            g = int(TOP[1] + (MID[1] - TOP[1]) * u)
            b = int(TOP[2] + (MID[2] - TOP[2]) * u)
        else:
            u = (t - 0.55) / 0.45
            r = int(MID[0] + (BOTTOM[0] - MID[0]) * u)
            g = int(MID[1] + (BOTTOM[1] - MID[1]) * u)
            b = int(MID[2] + (BOTTOM[2] - MID[2]) * u)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    return img


def soft_vignette(base: Image.Image) -> Image.Image:
  rgba = base.convert("RGBA")
  w, h = rgba.size
  overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
  draw = ImageDraw.Draw(overlay)
  draw.ellipse((-w * 0.08, -h * 0.12, w * 1.08, h * 1.04), fill=(255, 255, 255, 38))
  draw.ellipse((w * 0.22, h * 0.68, w * 0.92, h * 1.12), fill=(22, 120, 175, 52))
  return Image.alpha_composite(rgba, overlay)


def compose_icon(size: int, cloud: Image.Image) -> Image.Image:
    base = soft_vignette(sky_gradient(size))
    target_w = int(size * 0.72)
    ratio = target_w / cloud.width
    target_h = int(cloud.height * ratio)
    cloud_resized = cloud.resize((target_w, target_h), Image.Resampling.LANCZOS)
    x = (size - target_w) // 2
    y = int(size * 0.26) + (size - target_h) // 2 - int(size * 0.08)
    base.paste(cloud_resized, (x, y), cloud_resized)
    return base.convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cloud = Image.open(pick_cloud()).convert("RGBA")
    master = compose_icon(512, cloud)
    sizes = {
        "icon-512.png": 512,
        "icon-192.png": 192,
        "apple-touch-icon.png": 180,
        "favicon-32.png": 32,
    }
    for name, dim in sizes.items():
        out = master.resize((dim, dim), Image.Resampling.LANCZOS)
        out.save(OUT_DIR / name, format="PNG", optimize=True)
    master.save(OUT_DIR / "icon-master-512.png", format="PNG", optimize=True)
    print(f"Wrote {len(sizes)} icons to {OUT_DIR}")


if __name__ == "__main__":
    main()