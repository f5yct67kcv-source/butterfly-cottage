#!/usr/bin/env python3
"""Optimiert die Originalfotos: WebP in zwei Groessen + JPEG-Fallback."""
import json
from PIL import Image, ImageOps
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "assets/img"
OUT = ROOT / "assets/photos"
OUT.mkdir(parents=True, exist_ok=True)

# WebP quality. 80 barely beat JPEG on the leafy autumn hero; 74 is visually
# equivalent on these photos and roughly 17% smaller across the set.
WEBP_QUALITY = 74

# name -> (quelldatei, langseite gross, langseite klein)
JOBS = {
    "hero-autumn": ("slider_herbst_01.png", 2400, 1200),
    "hero-winter": ("slider_winter_01.png", 2400, 1200),
    "hero-spring": ("slider_fruehling_01.png", 2400, 1200),
    "terrace":     ("cottage_01_sitzplatz.png", 1600, 800),
    "garden":      ("cottage_02_sitzplatz.png", 1600, 800),
    "hall":        ("cottage_03_eingang.png", 1600, 800),
    "open-plan":   ("cottage_04_ueberblick.png", 1600, 800),
    "bed-window":  ("cottage_05_ueberblick.png", 1600, 800),
    "doors":       ("cottage_06_eingang.png", 1600, 800),
    "kitchen":     ("cottage_07_kueche.png", 1600, 800),
    "dining":      ("cottage_08_kueche.png", 1600, 800),
    "bedroom":     ("cottage_09_schlafen.png", 1600, 800),
    "bedroom-2":   ("cottage_10_schlafen.png", 1600, 800),
    "bedroom-3":   ("cottage_11_schlafen.png", 1600, 800),
    "bath-basin":  ("cottage_12_bad.png", 1600, 800),
    "bath-shower": ("cottage_13_bad.png", 1600, 800),
    "host-sarah":  ("sarah.png", 480, 480),
    "host-daniel": ("dani.png", 480, 480),
    "host-lucy":   ("lucy.png", 480, 480),
}

total = 0
sizes = {}  # basename -> (width, height), so the HTML can carry true dimensions
for name, (src, big, small) in JOBS.items():
    path = SRC / src
    if not path.exists():
        print("fehlt:", src)
        continue
    base = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    for suffix, longest in (("", big), ("-sm", small)):
        im = base.copy()
        im.thumbnail((longest, longest), Image.LANCZOS)
        sizes[f"{name}{suffix}"] = im.size
        for ext, kwargs in (("webp", dict(quality=WEBP_QUALITY, method=6)),
                            ("jpg", dict(quality=82, optimize=True, progressive=True))):
            target = OUT / f"{name}{suffix}.{ext}"
            im.save(target, **kwargs)
            total += target.stat().st_size
    print(f"{name:12s} {base.size[0]}x{base.size[1]} -> ok")

# The originals are smaller than the target long sides above, so the real output
# dimensions differ from what the JOBS table suggests. Write them out for the
# HTML patcher instead of hard-coding guesses.
(OUT / "sizes.json").write_text(
    json.dumps({k: list(v) for k, v in sorted(sizes.items())}, indent=1), encoding="utf-8")

print(f"\nGesamt: {total/1024/1024:.2f} MB in {OUT}")
