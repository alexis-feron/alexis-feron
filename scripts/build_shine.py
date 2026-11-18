"""Wrap the profile PNGs in SVGs that play a single shine sweep on load.

Usage (from the repo root):  python scripts/build_shine.py
Re-run it after exporting new PNGs from Figma.
"""

import base64
import math
from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / "assets"
IMAGES = ["desktop-profil", "mobile-profil"]

DELAY = "0.5s"      # wait before the shine starts
DURATION = "1.4s"   # time for one sweep across the image
ANGLE = 20          # tilt of the shine band, in degrees
BAND_RATIO = 0.22   # band width relative to image width
PEAK_OPACITY = 0.55


def build(name: str) -> None:
    png = ASSETS / f"{name}.png"
    width, height = Image.open(png).size
    data = base64.b64encode(png.read_bytes()).decode()

    band = round(width * BAND_RATIO)
    skew = math.tan(math.radians(ANGLE)) * height
    start, end = -band, round(width + skew)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>@media (prefers-reduced-motion: reduce) {{ .shine {{ display: none; }} }}</style>
  <defs>
    <image id="img" width="{width}" height="{height}" href="data:image/png;base64,{data}"/>
    <mask id="cards" mask-type="alpha" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="0" y="0" width="{width}" height="{height}">
      <use href="#img"/>
    </mask>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fff" stop-opacity="{PEAK_OPACITY}"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <use href="#img"/>
  <g class="shine" mask="url(#cards)">
    <g transform="translate({start} 0)">
      <animateTransform attributeName="transform" type="translate" from="{start} 0" to="{end} 0" begin="{DELAY}" dur="{DURATION}" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1" fill="freeze"/>
      <rect x="0" y="0" width="{band}" height="{height}" fill="url(#shine)" transform="skewX(-{ANGLE})"/>
    </g>
  </g>
</svg>
"""
    out = ASSETS / f"{name}.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"{out.name}: {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    for image in IMAGES:
        build(image)
