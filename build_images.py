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

# ---------------------------------------------------------------------------
# Art-directed hero.
#
# A single wide photo cannot serve both the desktop band and a phone: cropping
# a 2.4:1 source into a portrait-ish box throws away most of the width. So the
# hero is cut twice from the same 4:3 original, once wide and once square, and
# the HTML picks per screen. Boxes are (left, top, right, bottom) on the
# orientation-corrected original.
HERO_SRC = "hero-sunset.jpg"
HERO_CROPS = {
    # sky, roofline and the Butterfly sign; keeps the lamp post, drops the car,
    # the road sign and most of the neighbouring block
    "hero-sunset-wide": ((0, 620, 2950, 1849), 1920, 1200),
    # the whole cottage, for phones
    "hero-sunset-square": ((800, 500, 3100, 2800), 1200, 800),
}

hero_path = SRC / HERO_SRC
if hero_path.exists():
    hero = ImageOps.exif_transpose(Image.open(hero_path)).convert("RGB")
    for name, (box, big, small) in HERO_CROPS.items():
        cut = hero.crop(box)
        for suffix, width in (("", big), ("-sm", small)):
            im = cut.resize((width, round(width * cut.size[1] / cut.size[0])), Image.LANCZOS)
            sizes[f"{name}{suffix}"] = im.size
            for ext, kwargs in (("webp", dict(quality=WEBP_QUALITY, method=6)),
                                ("jpg", dict(quality=82, optimize=True, progressive=True))):
                target = OUT / f"{name}{suffix}.{ext}"
                im.save(target, **kwargs)
                total += target.stat().st_size
        print(f"{name:20s} {cut.size[0]}x{cut.size[1]} -> ok")
else:
    print("fehlt:", HERO_SRC)

# The originals are smaller than the target long sides above, so the real output
# dimensions differ from what the JOBS table suggests. Write them out for the
# HTML patcher instead of hard-coding guesses.
(OUT / "sizes.json").write_text(
    json.dumps({k: list(v) for k, v in sorted(sizes.items())}, indent=1), encoding="utf-8")

print(f"\nGesamt: {total/1024/1024:.2f} MB in {OUT}")
