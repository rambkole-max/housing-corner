#!/usr/bin/env python3
"""
HousingCorner — extract project imagery from a developer's PDF pack
===================================================================

Builders hand over a brochure PDF, cost sheets and an architect's floor plan.
Everything a project page needs is usually already in there at print
resolution. This pulls it out.

    pip install pillow
    # also needs poppler-utils for pdftoppm  (apt install poppler-utils)
    python extract-assets.py

WHY RENDER PAGES INSTEAD OF EXTRACTING EMBEDDED IMAGES
------------------------------------------------------
`pdfimages` pulls the raw embedded bitmaps, which sounds better but usually
isn't. In the Royal Paradise brochure the 3D cutaway plans are sliced into
~30 separate tiles, and the floor plans are vector art with no bitmap at all.
Rendering the page composites tiles, vectors and text into one clean image.
We only pull raw bitmaps for the full-bleed photographic renders, where the
embedded original is larger than the page render.

TWO GOTCHAS THAT WILL BITE YOU
------------------------------
1. Adobe writes CMYK JPEGs with inverted channel values. Extract one and it
   looks like a photo negative. The fix is to invert before converting to RGB
   when the APP14 'Adobe' marker is present — handled in `load_cmyk` below.
2. Brochures are full of licensed stock photography — smiling families, yoga
   at sunrise, a pharmacist. Those are not the project, and they are not the
   developer's to sub-license to you. This script deliberately does not
   extract them. See SKIPPED_STOCK at the bottom for the list.
"""

import os
import subprocess
import sys
import shutil

from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
# client pack lives outside the website folder
CLIENT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "client", "Royal Paradise"))
OUT = os.path.join(HERE, "royal-paradise")
TMP = os.path.join(HERE, ".extract-tmp")

BROCHURE = os.path.join(CLIENT, "ROYAL PARADISE BROCHURE.pdf")
PLAN_A3 = os.path.join(CLIENT, "FIRST TO SEVENTH FLOOR PLAN ( RERA CARPET )_260805_124341.pdf")
ELEVATION = os.path.join(CLIENT, "FRONT EVEVATION.jpg.jpeg")

JPEG_Q = 82


def load_cmyk(path):
    """Open a JPEG, undoing Adobe's inverted CMYK if present."""
    im = Image.open(path)
    if im.mode == "CMYK":
        with open(path, "rb") as fh:
            if b"Adobe" in fh.read(4096):
                im = ImageChops.invert(im)
    return im.convert("RGB")


def frac_crop(im, x0, y0, x1, y1):
    """Crop using fractions of the image, so it survives a DPI change."""
    w, h = im.size
    return im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))


def fit_cover(im, target_w, target_h, focus_y=0.5):
    """Scale and centre-crop to exactly target size, preserving aspect."""
    tw, th = target_w, target_h
    scale = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = int((im.height - th) * focus_y)
    return im.crop((left, top, left + tw, top + th))


def fit_contain(im, target_w, target_h, bg=(255, 255, 255)):
    """Scale to fit inside target and pad — for plans, which must never crop."""
    im = im.copy()
    im.thumbnail((target_w, target_h), Image.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), bg)
    canvas.paste(im, ((target_w - im.width) // 2, (target_h - im.height) // 2))
    return canvas


def save(im, name, quality=JPEG_Q):
    path = os.path.join(OUT, name)
    if name.lower().endswith(".png"):
        im.save(path, optimize=True)
    else:
        im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    kb = os.path.getsize(path) / 1024
    flag = "  <-- over 300 KB, consider recompressing" if kb > 300 else ""
    print(f"  {name:<28} {im.width}x{im.height:<6} {kb:6.0f} KB{flag}")


def render_pdf(pdf, prefix, dpi):
    subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-jpeg", "-jpegopt", "quality=95",
         pdf, os.path.join(TMP, prefix)],
        check=True, capture_output=True,
    )


def main():
    for tool in ("pdftoppm", "pdfimages"):
        if not shutil.which(tool):
            print(f"{tool} not found. Install poppler-utils.")
            return 1
    for f in (BROCHURE, PLAN_A3, ELEVATION):
        if not os.path.exists(f):
            print(f"missing source file: {f}")
            return 1

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)

    print("Rendering PDF pages...")
    render_pdf(BROCHURE, "br", 200)
    render_pdf(PLAN_A3, "plan", 300)

    print("Extracting full-bleed renders...")
    subprocess.run(["pdfimages", "-j", "-p", BROCHURE, os.path.join(TMP, "img")],
                   check=True, capture_output=True)

    print("\nWriting assets:")

    # --- Photographic renders (artist's impressions, labelled as such on the page)
    dusk = load_cmyk(os.path.join(TMP, "img-002-002.jpg"))
    save(fit_cover(frac_crop(dusk, 0.48, 0.0, 1.0, 1.0), 1600, 1200), "elevation.jpg", quality=76)

    front = Image.open(ELEVATION).convert("RGB")
    save(fit_cover(front, 1200, 1600, focus_y=0.42), "front-elevation.jpg")

    # Ground-floor retail strip, cropped from the elevation render. Used on the
    # home page commercial card so it shows shops rather than the whole tower.
    save(fit_cover(frac_crop(front, 0.03, 0.735, 0.97, 0.925), 1600, 1000),
         "shops.jpg")

    day = load_cmyk(os.path.join(TMP, "img-005-014.jpg"))
    save(fit_cover(frac_crop(day, 0.0, 0.18, 1.0, 1.0), 1600, 1200), "daylight-view.jpg")

    roof = load_cmyk(os.path.join(TMP, "img-005-013.jpg"))
    save(fit_cover(roof, 1600, 900), "rooftop-amenities.jpg", quality=74)

    # --- Plans. Contain, never crop, white ground so dimensions stay legible.
    plan = Image.open(os.path.join(TMP, "plan-1.jpg")).convert("RGB")
    save(fit_contain(frac_crop(plan, 0.07, 0.02, 0.95, 0.91), 1800, 1350),
         "floor-plan-typical.jpg", quality=80)

    p6 = Image.open(os.path.join(TMP, "br-06.jpg")).convert("RGB")
    save(fit_contain(frac_crop(p6, 0.195, 0.02, 0.505, 0.98), 1400, 1400),
         "floor-plan-ground.jpg", quality=88)

    p9 = Image.open(os.path.join(TMP, "br-09.jpg")).convert("RGB")
    save(fit_contain(frac_crop(p9, 0.185, 0.01, 0.45, 0.48), 1600, 1100,
                     bg=(240, 238, 234)), "plan-3d-800.jpg", quality=88)
    save(fit_contain(frac_crop(p9, 0.18, 0.45, 0.45, 0.97), 1600, 1100,
                     bg=(240, 238, 234)), "plan-3d-840.jpg", quality=88)

    # --- Location map
    p10 = Image.open(os.path.join(TMP, "br-10.jpg")).convert("RGB")
    save(fit_contain(frac_crop(p10, 0.435, 0.02, 0.995, 0.98), 1600, 1000,
                     bg=(243, 239, 240)), "location-map.jpg", quality=88)

    # --- Logos
    p1 = Image.open(os.path.join(TMP, "br-01.jpg")).convert("RGB")
    save(frac_crop(p1, 0.6725, 0.212, 0.8245, 0.694), "project-logo.jpg", quality=90)
    save(frac_crop(p1, 0.2265, 0.288, 0.2765, 0.452), "developer-logo.jpg", quality=90)

    shutil.rmtree(TMP, ignore_errors=True)
    print("\nDone. Temporary render files removed.")
    return 0


# Deliberately NOT extracted — licensed stock photography from the brochure,
# none of which depicts this project and none of which the developer has
# granted us rights to republish:
SKIPPED_STOCK = [
    "img-001-001  yoga at sunrise",
    "img-003-006  father and child indoors",
    "img-004-011  woman skipping rope",
    "img-006-019  clothing store interior",
    "img-006-020  optician with customer",
    "img-006-021  pharmacy counter",
    "img-006-022  grocery produce display",
    "img-007-023  woman doing yoga on a terrace",
    "img-007-024  child in a ball pit",
    "img-007-026  man walking a dog",
    "img-007-027  grandfather and child on grass",
]


if __name__ == "__main__":
    sys.exit(main())
