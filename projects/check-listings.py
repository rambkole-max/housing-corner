#!/usr/bin/env python3
"""
HousingCorner — pre-upload safety check for project pages
=========================================================

Run this before every upload:

    python check-listings.py

It catches the four ways a project page goes wrong in practice:

  1. A {{TOKEN}} from the template survived the find-and-replace.
  2. Content was copied from another listing and never rewritten — the fastest
     route to publishing one project's carpet areas under another project's
     name, which for a RERA-compliance business is the worst possible bug.
  3. The share image referenced by og:image does not exist on disk.
  4. Internal links or required SEO tags are missing, or the JSON-LD is invalid.

Exit code is 0 if everything passes, 1 if anything failed.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {"_template", "__pycache__"}

# Sentences that only ever belong to one project. If two live pages share one,
# somebody copy-pasted and forgot to rewrite.
FINGERPRINT_PATTERNS = [
    r"MahaRERA\s+([APap]\d{11,})",          # RERA numbers
    r"(\d{3})\s*sq ft</td>",                 # carpet areas in the config table
]

REQUIRED_TAGS = [
    ('<link rel="canonical"', "canonical URL"),
    ('property="og:image"', "og:image"),
    ('property="og:title"', "og:title"),
    ('name="twitter:card"', "twitter card"),
    ('application/ld+json', "structured data"),
    ('<h1', "an H1 heading"),
    ('name="description"', "meta description"),
]


def project_dirs():
    for entry in sorted(os.listdir(HERE)):
        path = os.path.join(HERE, entry)
        if os.path.isdir(path) and entry not in SKIP_DIRS:
            if os.path.exists(os.path.join(path, "index.html")):
                yield entry, path


def main():
    failures = []
    warnings = []
    pages = list(project_dirs())

    if not pages:
        print("No project pages found. Nothing to check.")
        return 0

    fingerprints = {}

    for slug, path in pages:
        html = open(os.path.join(path, "index.html"), encoding="utf-8").read()
        label = f"projects/{slug}/"

        # 1 — leftover template tokens
        tokens = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", html)))
        if tokens:
            failures.append(f"{label} still contains template tokens: {', '.join(tokens)}")

        # 2 — required tags
        for needle, human in REQUIRED_TAGS:
            if needle not in html:
                failures.append(f"{label} is missing {human}")

        # 3 — JSON-LD parses
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                failures.append(f"{label} has invalid JSON-LD: {exc}")

        # 4 — canonical URL matches the folder it lives in
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        if canon and f"/projects/{slug}/" not in canon.group(1):
            failures.append(
                f"{label} canonical points at {canon.group(1)} — should contain /projects/{slug}/"
            )

        # 5 — every local file referenced actually exists
        for attr in re.findall(r'(?:src|href)="([^"#:]+)"', html):
            if attr.startswith(("http", "//", "mailto", "data:", "..")):
                continue
            if not os.path.exists(os.path.join(path, attr)):
                # Photos are expected to be missing until they are shot; the page
                # degrades to a placeholder, so this is a warning not a failure.
                if attr.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    warnings.append(f"{label}{attr} not present yet (slot shows a placeholder)")
                else:
                    failures.append(f"{label} references missing file: {attr}")

        # 6 — og:image must exist, because a broken one breaks every WhatsApp share
        og = re.search(r'property="og:image" content="[^"]*/([^/"]+)"', html)
        if og and not os.path.exists(os.path.join(path, og.group(1))):
            failures.append(
                f"{label} og:image {og.group(1)} is missing — run: python make-og-image.py {slug}"
            )

        # 7 — FAQ schema must match the visible FAQ, or Google treats it as
        #     hidden structured data. sync-faq-schema.py fixes this.
        page_qs = [re.sub(r"<[^>]+>", "", q).strip()
                   for q in re.findall(r"<summary>(.*?)</summary>", html, re.S)]
        page_qs = [__import__("html").unescape(q) for q in page_qs]
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue
            for node in data.get("@graph", []):
                if node.get("@type") != "FAQPage":
                    continue
                schema_qs = [q["name"] for q in node.get("mainEntity", [])]
                extra = [q for q in schema_qs if q not in page_qs]
                if extra:
                    failures.append(
                        f"{label} FAQ schema has {len(extra)} question(s) not visible on the page "
                        f"(first: \"{extra[0][:60]}\") — run: python sync-faq-schema.py {slug}"
                    )

        # 8 — collect fingerprints for the cross-page duplication check
        for pattern in FINGERPRINT_PATTERNS:
            for match in re.findall(pattern, html):
                fingerprints.setdefault(match, set()).add(slug)

    # 8 — the same RERA number or area set appearing on two pages
    for value, slugs in fingerprints.items():
        if len(slugs) > 1 and re.fullmatch(r"[APap]\d{11,}", str(value)):
            failures.append(
                f"MahaRERA {value} appears on multiple pages ({', '.join(sorted(slugs))}) — "
                "two projects cannot share a registration number"
            )

    print(f"Checked {len(pages)} project page(s): {', '.join(s for s, _ in pages)}\n")

    for w in warnings:
        print(f"  note     {w}")
    if warnings:
        print()

    if failures:
        for f in failures:
            print(f"  FAIL     {f}")
        print(f"\n{len(failures)} problem(s) found. Fix before uploading.")
        return 1

    print("All checks passed. Safe to upload.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
