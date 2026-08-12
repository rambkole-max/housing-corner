# Image spec — project pages

Every image slot on a project page has a filename baked into the HTML. **Name a
file exactly as listed and drop it in the project folder, and it appears.** No
HTML editing. Until a file exists the slot shows a branded dashed placeholder
rather than a broken-image icon, so a page is safe to publish half-shot.

---

## 1 · Royal Paradise — what already exists

All eleven of these were extracted from the developer's own PDFs by
`extract-assets.py` and are already live on the page. **You do not need to
recreate them.**

| Filename | What it is | Source | Pixels |
|---|---|---|---|
| `elevation.jpg` | Dusk render — page hero, and the home page residential card | Brochure p.2 | 1600 × 1200 |
| `front-elevation.jpg` | Front elevation, full height | `FRONT EVEVATION.jpg.jpeg` | 1200 × 1600 |
| `daylight-view.jpg` | Three-quarter daylight render | Brochure p.8 | 1600 × 1200 |
| `rooftop-amenities.jpg` | Proposed rooftop deck, aerial | Brochure p.5 | 1600 × 900 |
| `shops.jpg` | The four shopfronts — home page commercial card | Cropped from the elevation | 1600 × 1000 |
| `floor-plan-typical.jpg` | Architect's typical floor plan, 1st–7th | A3 plan PDF | 1800 × 1350 |
| `floor-plan-ground.jpg` | Ground floor — shops, parking, lobby | Brochure p.6 | 1400 × 1400 |
| `plan-3d-800.jpg` | 3D cutaway, ~800 sq ft 2 BHK | Brochure p.9 | 1600 × 1100 |
| `plan-3d-840.jpg` | 3D cutaway, ~840 sq ft 2 BHK | Brochure p.9 | 1600 × 1100 |
| `location-map.jpg` | Connectivity map | Brochure p.10 | 1600 × 1000 |
| `project-logo.jpg` | Royal Paradise lockup — in the hero | Brochure p.1 | 729 × 868 |
| `developer-logo.jpg` | Royal Properties mark — developer section | Brochure p.1 | 240 × 295 |

To regenerate any of them after tweaking a crop:

```bash
pip install pillow          # poppler-utils must also be installed
python extract-assets.py
```

### What is still missing: your own photographs

Every image above is an **artist's impression**, and the page says so under each
one. The one thing renders cannot do is show a buyer what is actually standing
on the site today. The gallery has an empty slot reserved for exactly that:

| Filename | What it is | Pixels | Aspect | Target size |
|---|---|---|---|---|
| `site-progress.jpg` | Current construction status, dated | 1600 × 900 | 16:9 | ≤ 200 KB |

Shoot it on a site visit, name it `site-progress.jpg`, drop it in
`projects/royal-paradise/`, and replace the placeholder div in the gallery with
an `<img>` following the pattern of the slots above. A dated progress photo is
the single most persuasive image you can put on this page, because no competitor
listing has one.

---

## 2 · Rules that matter more than resolution

**Weight beats megapixels.** A 180 KB photo that loads in half a second sells
better than a 4 MB one that makes a buyer on mobile data give up. Anything over
300 KB should be recompressed. Total page weight target: under 3 MB with all
images loaded.

**Shoot landscape.** Most slots are 16:9 or 4:3. Portrait phone photos get
centre-cropped and you lose the top and bottom of the frame.

**Plans are never cropped.** The plan slots use `object-fit: contain` on white,
so the whole drawing is always visible. A clipped dimension is a misleading
dimension.

**Label renders as renders.** Every render on the page carries a caption saying
so. The rooftop aerial carries a stronger one, because the developer's own
brochure disclaimer says the rooftop amenities and the front Wing A building are
*proposed and yet to be sanctioned*. Do not quietly drop that caption to make the
page look better — it is the difference between marketing and misrepresentation,
and it is the whole reason a buyer should prefer you to a portal.

**Do not lift a competitor's photography, or stock images from a brochure.**
`extract-assets.py` deliberately skips the eleven stock photos in the Royal
Paradise brochure — the smiling families, the yoga at sunrise, the pharmacist.
They are not this project, and the developer has no right to sub-license them to
you. The list is at the bottom of that script. For a business whose pitch is
documentation and compliance, a copyright complaint is an expensive kind of irony.

---

## 3 · Alt text

The `alt` attributes are written for every slot and are not decoration — they
are how a blind visitor and Google both understand the image. If you change what
a slot contains, update its `alt` text to match. Search the filename in
`index.html` to find it.

---

## 4 · For the next project

Run `extract-assets.py` against the new developer's PDFs first — most builders
supply the same three things (brochure, cost sheet, architect's plan) and you
will usually get a full page of imagery out of them in one pass. Point the
`CLIENT`, `BROCHURE` and `PLAN_A3` paths at the new files and adjust the crop
fractions; the comments in the script explain each one.

Then run `python check-listings.py` before uploading. It lists which slots are
still empty and fails the build on anything actually broken.
