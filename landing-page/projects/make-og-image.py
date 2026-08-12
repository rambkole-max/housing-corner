#!/usr/bin/env python3
"""
HousingCorner — project share-image generator
=============================================

Builds the 1200x630 PNG that WhatsApp, Facebook and LinkedIn show when
someone shares a project page. Every project page needs one, or the share
renders as a bare grey link.

USAGE
-----
    pip install cairosvg
    python make-og-image.py royal-paradise

The slug must match the project folder name. Edit the PROJECTS dict below
to add a new listing, then run the script with that slug. The PNG is written
to <slug>/og-<slug>.png, which is exactly where the page's og:image tag
already points.

WHY A SCRIPT AND NOT A DESIGN FILE
----------------------------------
These images are pure text-on-brand-colour. Generating them keeps every
listing visually identical, means a brand change is a one-line edit here
rather than 30 re-exports, and takes about a second per image.

NOTE ON FONTS
-------------
Fraunces and Inter are the brand fonts. If they are not installed on the
machine running this script, it falls back to the closest available serif
and sans. Install both from Google Fonts for pixel-accurate output:
https://fonts.google.com/specimen/Fraunces  ·  https://fonts.google.com/specimen/Inter
"""

import sys
import os
import html

# --------------------------------------------------------------------------
# Add a new listing here, then run:  python make-og-image.py <slug>
# --------------------------------------------------------------------------
PROJECTS = {
    "royal-paradise": {
        "name": "Royal Paradise",
        "locality": "Warje Malwadi, Pune",
        "headline": "2 BHK homes on the Pune–Bangalore Highway",
        "chip_left": "From ₹75.1 L",
        "chip_right": "MahaRERA P52100049617",
    },
    # "example-project": {
    #     "name": "Example Project",
    #     "locality": "Latur, Maharashtra",
    #     "headline": "3 BHK homes near the ring road",
    #     "chip_left": "From ₹45 L",
    #     "chip_right": "MahaRERA P5210000XXXX",
    # },
}

# Brand tokens — single source of truth is logo-design-reference.md
FOREST = "#2F5D3A"
TERRACOTTA = "#C77E52"
SAGE = "#8BA888"
CREAM = "#F5F0E6"
INK = "#1F2A24"
STONE = "#8A7E6E"
FOREST_SOFT = "#5C7A4F"

SERIF = "Fraunces, 'Playfair Display', Georgia, 'Century Schoolbook L', 'Bitstream Charter', serif"
SANS = "Inter, 'Helvetica Neue', 'Liberation Sans', Arial, sans-serif"

# Fallbacks that actually exist on most Linux boxes. cairosvg drops to its
# default sans when the first family in a stack is unknown, so for the raster
# pass we hand it a family we know resolves.
SERIF_RENDER = "Lora"
SANS_RENDER = "Lato"

ICON = """
  <g transform="translate({x}, {y}) scale({s})">
    <path d="M 58 220 L 58 128 Q 58 120 64 114 L 124 56 Q 130 50 136 56 L 196 114 Q 202 120 202 128 L 202 220 Q 202 226 196 226 L 64 226 Q 58 226 58 220 Z" fill="{forest}"/>
    <circle cx="130" cy="158" r="13" fill="{cream}"/>
    <path d="M 118 168 Q 118 164 122 164 L 138 164 Q 142 164 142 168 L 142 220 L 118 220 Z" fill="{cream}"/>
    <path d="M 130 64 Q 130 38 152 32 Q 150 52 138 60 Q 134 62 130 64 Z" fill="{sage}"/>
    <path d="M 130 70 L 130 64" stroke="{sage}" stroke-width="3" stroke-linecap="round"/>
    <path d="M 196 114 L 202 128 L 188 128 Z" fill="{terracotta}"/>
  </g>
"""


def estimate_width(text, font_size, weight=400):
    """Rough advance-width estimate so chips size to their label."""
    factor = 0.54 if weight >= 600 else 0.51
    return len(text) * font_size * factor


def build_svg(p, serif, sans):
    name = html.escape(p["name"])
    locality = html.escape(p["locality"])
    headline = html.escape(p["headline"])
    chip_l = html.escape(p["chip_left"])
    chip_r = html.escape(p["chip_right"])

    # Chip geometry, sized to the text rather than guessed.
    pad = 28
    cl_w = int(estimate_width(chip_l, 22, 600) + pad * 2)
    cr_w = int(estimate_width(chip_r, 22, 500) + pad * 2)
    cl_x, chip_y, chip_h = 96, 470, 52
    cr_x = cl_x + cl_w + 16

    # Headline shrinks a little if it is long, so it never runs off the canvas.
    head_size = 34 if len(headline) <= 46 else 29

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-label="{name} — {locality}">
  <title>{name} — {locality}</title>

  <rect width="1200" height="630" fill="{CREAM}"/>

  <!-- corner accents -->
  <path d="M 6 6 L 156 6 M 6 6 L 6 156" stroke="{TERRACOTTA}" stroke-width="10" fill="none"/>
  <path d="M 1194 624 L 1044 624 M 1194 624 L 1194 474" stroke="{FOREST}" stroke-width="10" fill="none"/>

  <circle cx="1130" cy="140" r="220" fill="{SAGE}" opacity="0.13"/>
{ICON.format(x=96, y=54, s=0.42, forest=FOREST, cream=CREAM, sage=SAGE, terracotta=TERRACOTTA)}
  <text x="200" y="152" font-family="{serif}" font-size="34" fill="{INK}" letter-spacing="-0.5">HousingCorner</text>
  <text x="202" y="180" font-family="{sans}" font-size="15" fill="{FOREST_SOFT}" letter-spacing="2.4">YOUR CORNER OF PROPERTY</text>

  <line x1="96" y1="228" x2="1010" y2="228" stroke="{SAGE}" stroke-width="1.5" opacity="0.8"/>

  <!-- project name -->
  <text x="96" y="316" font-family="{serif}" font-size="72" fill="{INK}" letter-spacing="-1.6">{name}</text>

  <!-- locality -->
  <text x="98" y="366" font-family="{sans}" font-size="27" fill="{FOREST}" font-weight="500">{locality}</text>

  <!-- headline -->
  <text x="98" y="422" font-family="{sans}" font-size="{head_size}" fill="{STONE}">{headline}</text>

  <!-- chips -->
  <rect x="{cl_x}" y="{chip_y}" width="{cl_w}" height="{chip_h}" rx="26" fill="{FOREST}"/>
  <text x="{cl_x + cl_w // 2}" y="{chip_y + 34}" font-family="{sans}" font-size="22" font-weight="600" fill="{CREAM}" text-anchor="middle">{chip_l}</text>

  <rect x="{cr_x}" y="{chip_y}" width="{cr_w}" height="{chip_h}" rx="26" fill="none" stroke="{SAGE}" stroke-width="2"/>
  <text x="{cr_x + cr_w // 2}" y="{chip_y + 34}" font-family="{sans}" font-size="22" font-weight="500" fill="{FOREST}" text-anchor="middle">{chip_r}</text>

  <text x="98" y="580" font-family="{sans}" font-size="19" fill="{STONE}" letter-spacing="1.1">Site visits · written cost breakdowns · housingcorner.in</text>
</svg>
"""


def main():
    if len(sys.argv) < 2:
        print("usage: python make-og-image.py <slug>")
        print("known slugs: " + ", ".join(sorted(PROJECTS)))
        return 1

    slug = sys.argv[1]
    if slug not in PROJECTS:
        print(f"unknown slug '{slug}'. Add it to the PROJECTS dict at the top of this file.")
        return 1

    try:
        import cairosvg
    except ImportError:
        print("cairosvg is not installed.  pip install cairosvg")
        return 1

    p = PROJECTS[slug]
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(here, slug)
    os.makedirs(outdir, exist_ok=True)

    # Source SVG keeps the real brand font stack; the raster pass uses
    # families we know resolve here and that carry the rupee glyph (U+20B9).
    open(os.path.join(outdir, f"og-{slug}.svg"), "w", encoding="utf-8").write(
        build_svg(p, SERIF, SANS)
    )
    png = os.path.join(outdir, f"og-{slug}.png")
    cairosvg.svg2png(
        bytestring=build_svg(p, SERIF_RENDER, SANS_RENDER).encode("utf-8"),
        write_to=png,
        output_width=1200,
        output_height=630,
    )
    print(f"wrote {png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
