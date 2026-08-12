#!/usr/bin/env python3
"""
HousingCorner — rebuild FAQPage schema from the visible FAQ
===========================================================

    python sync-faq-schema.py                # every project page
    python sync-faq-schema.py royal-paradise # one page

Google requires that FAQPage structured data match content the visitor can
actually see. Hand-maintaining two copies of the same eight questions is a
guarantee that they drift, and drifted FAQ markup is a manual-action risk, not
just a lost rich result.

So the page's <details> blocks are the single source of truth. This script
reads them and regenerates the FAQPage node in the JSON-LD to match, exactly.
Edit the FAQ on the page, run this, done.
"""

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {"_template", "__pycache__"}


def strip_tags(fragment):
    text = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(text).strip()


def collapse(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_faq(page_html):
    """Pull (question, answer) from every <details> inside .faq__list."""
    block = re.search(r'<div class="faq__list">(.*?)</div>', page_html, re.S)
    if not block:
        return []
    pairs = []
    for det in re.findall(r"<details[^>]*>(.*?)</details>", block.group(1), re.S):
        q = re.search(r"<summary>(.*?)</summary>", det, re.S)
        answers = re.findall(r"<p>(.*?)</p>", det, re.S)
        if not q or not answers:
            continue
        pairs.append((collapse(strip_tags(q.group(1))),
                      collapse(" ".join(strip_tags(a) for a in answers))))
    return pairs


def sync(path):
    s = open(path, encoding="utf-8").read()
    pairs = extract_faq(s)
    if not pairs:
        return None, "no FAQ found on page"

    m = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n</script>)', s, re.S)
    if not m:
        return None, "no JSON-LD block"

    data = json.loads(m.group(2))
    graph = data.get("@graph")
    if graph is None:
        return None, "JSON-LD has no @graph"

    faq_nodes = [n for n in graph if n.get("@type") == "FAQPage"]
    node = faq_nodes[0] if faq_nodes else {"@type": "FAQPage", "mainEntity": []}
    before = len(node.get("mainEntity", []))

    node["mainEntity"] = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in pairs
    ]
    if not faq_nodes:
        graph.append(node)

    new_json = json.dumps(data, indent=2, ensure_ascii=False)
    s = s[: m.start()] + m.group(1) + new_json + m.group(3) + s[m.end():]
    open(path, "w", encoding="utf-8").write(s)
    return (before, len(pairs)), None


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    targets = []
    for entry in sorted(os.listdir(HERE)):
        if entry in SKIP or (only and entry != only):
            continue
        page = os.path.join(HERE, entry, "index.html")
        if os.path.isdir(os.path.join(HERE, entry)) and os.path.exists(page):
            targets.append((entry, page))

    if not targets:
        print("no project pages found")
        return 1

    failed = False
    for slug, page in targets:
        result, err = sync(page)
        if err:
            print(f"  {slug}: {err}")
            failed = True
        else:
            before, after = result
            note = "unchanged" if before == after else f"{before} -> {after}"
            print(f"  {slug}: FAQ schema rebuilt from page ({after} questions, {note})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
