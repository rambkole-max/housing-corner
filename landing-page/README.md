# HousingCorner Site — Deploy Notes

Static HTML. No build step, no npm, no framework. Open any `index.html` in a browser
to preview. Upload the whole folder to a static host to go live.

## Folder map

```
landing-page/
├── index.html                  Home page (self-contained, inline CSS)
├── og-image.png / .svg         Share preview for the home page
├── favicon-32.png              Tab icon fallback
├── favicon-192.png             Android home screen
├── apple-touch-icon.png        iOS home screen (iOS ignores SVG favicons)
├── sitemap.xml                 Submit once at Google Search Console
├── robots.txt
└── projects/
    ├── index.html              Projects listing page
    ├── project.css             Shared stylesheet for ALL project pages
    ├── make-og-image.py        Generates each project's share image
    ├── check-listings.py       Run before every upload
    ├── IMAGE-SPEC.md           Filenames + sizes for photography
    ├── _template/              Copy this to add a listing — DO NOT UPLOAD
    └── royal-paradise/
        ├── index.html
        ├── og-royal-paradise.png
        └── (photos go here — see IMAGE-SPEC.md)
```

Note that project pages share `projects/project.css` rather than each carrying its
own copy of the styles. With one listing that is a wash; at ten it means a brand
change is one edit instead of ten, and returning visitors download the CSS once.

## Adding a new listing — the short version

1. Copy `projects/_template/` to `projects/<your-slug>/`
2. Replace the eight `{{TOKENS}}`, then **rewrite the content** — the template
   carries Royal Paradise's numbers as a worked example and none of them apply to
   your project. The comment block at the top of the file lists every section.
3. Add the project to `PROJECTS` in `make-og-image.py`, then run
   `python make-og-image.py <your-slug>`
4. Add a card to `projects/index.html` and a `<url>` block to `sitemap.xml`
5. If you edited the FAQ, run `python sync-faq-schema.py <your-slug>` — the
   visible questions are the source of truth and the schema is generated from them
6. Run `python check-listings.py` — it fails on leftover tokens, missing share
   images, broken links, invalid schema, FAQ markup that isn't visible on the
   page, or two projects sharing a RERA number
7. Upload

---

## 1 · What's already baked in

As of the last edit, these values are live across the page — no find-and-replace needed:

- **Founders:** Ram Kole &amp; Rahul Awale (about section, footer, contact block).
- **WhatsApp / phone:** **+91 95619 58445** — the single HousingCorner WhatsApp Business line. Every WhatsApp link, the floating button, the footer, and the form `onSubmit` all point at `wa.me/919561958445`. The founders' personal numbers are no longer published on the site.
- **Location:** Latur, Maharashtra.
- **MahaRERA wording:** All five status disclosures say **"application in process"** (hero eyebrow, trust stat, about stat, FAQ, footer). This is deliberate — until your agent registration number is issued, making stronger claims (e.g. "MahaRERA registered agent" or "competency-exam certified") is a compliance risk. Two such claims were found and removed on 12 Aug 2026.
- **Entity type:** Neutralised to "Founder-led" instead of "Sole proprietorship" everywhere.
- **Listings:** Two real cards for **Royal Paradise** (MahaRERA `P52100049617`, Warje Malwadi, Pune) — 2 BHK flats and retail shops. The third card is a "Custom search" enquiry card rather than a fabricated listing.
- **Social preview:** `og-image.png` (1200×630) plus full Open Graph, Twitter card, canonical, and `RealEstateAgent` JSON-LD. **This file must be uploaded alongside `index.html`** — see §4.

## 2 · Placeholders still to replace when the info arrives

All fabricated listing placeholders are **gone** as of 12 Aug 2026. What remains:

| Placeholder | Where to find your value | Occurrences |
|---|---|---|
| `application in process` → real MahaRERA Agent Reg. no. | Replace once issued | 5 |
| Street-level office address | For the contact block, letterhead, and Google Business | — |

### ⚠️ Open item: confirm the possession dates on the official portal

The Royal Paradise page now publishes the MahaRERA completion dates —
**original 29 June 2025, revised to 29 June 2027** — and leads with them, because
no competing listing shows the revised date. They were read from the MahaRERA
registration record on 12 August 2026, cross-checked against four portals that
agree on the original date.

**They have not yet been confirmed against maharera.maharashtra.gov.in directly.**
Search P52100049617 there, open the registration certificate, confirm both dates
and screenshot it. Then edit the sourcing paragraph in the `#possession` section —
it currently says we are re-confirming — and replace it with the certificate
reference. If a buyer ever challenges the date, that screenshot is what you produce.

Also open: the registry records **59 units**; the sanctioned floor plan implies 56
flats plus 4 shops = 60. The page says so plainly and says we have asked the
developer. Update the note in `#overview` when they answer.

### ⚠️ Numbers to re-verify before the next buyer sees them

The Royal Paradise figures on the page come from the developer's own cost sheets in `client/Royal Paradise/`, **and those sheets contain arithmetic errors.** What's published is the corrected math:

- **Flats.** The uniform rate is ~₹9,520/sq ft. The sheet's *Agreement Cost* column understates rows 2–7 by ₹3.7–4 L each (it implies ~₹9,046/sq ft), but the stamp duty, GST, and **Total** columns are all computed off the correct higher base. The published "Starting ₹75.1 L / all-in ₹84.5 L" uses the correct base. Ask Royal Properties for a corrected sheet before quoting.
- **Shops.** Rate is a flat ₹34,500/sq ft, but Shop 3 (288 sq ft) and Shop 4 (403 sq ft) have their basic costs swapped. That sheet also **expired 30 Sept 2025** and its header reads `A52100049617` where the brochure says `P52100049617`. This is why the commercial card says **"Price on request"** rather than a number.

Do not publish shop pricing until you have a current, corrected rate card.

**Heads-up on entity type.** Two founders strongly implies a **Partnership firm** (Indian Partnership Act, 1932), not a sole proprietorship. This changes the MahaRERA agent application: a registered partnership firm applies with partnership deed + firm PAN + partners' list, while a sole proprietor applies in one individual's name. Decide early — it changes your PAN, GST, bank account, and the form you file. Full note at the end of `logo-design-reference.md §7`.

---

## 3 · How the contact form works

The form does NOT submit to a backend. When a visitor clicks **Send enquiry**, the browser:

1. Packages their answers into a pre-formatted message.
2. Opens `https://wa.me/919561958445` (the HousingCorner business line) in a new tab with the message pre-filled.
3. The visitor taps **Send** in WhatsApp and the message lands in your WhatsApp Business inbox.

This is deliberate — no server to run, no database to maintain, no spam filter to configure. Your CRM is your WhatsApp chat history until you outgrow it.

**To switch to a real form backend later**, replace the `handleSubmit` function with a `fetch('/api/enquire', …)` call, or swap `<form>` to point at [Formspree](https://formspree.io), [Basin](https://usebasin.com), or [Web3Forms](https://web3forms.com) — all free-tier friendly.

---

## 4 · Deploying to hostinger.in (or any static host)

Your brand-kit doc already recommends `housingcorner.in`. Assuming you bought it:

### Hostinger (easiest path)
1. Buy hosting → attach `housingcorner.in` as the primary domain.
2. In hPanel → **File Manager** → navigate to `public_html/`.
3. **Delete** the default `index.html`.
4. **Upload the entire contents of this folder** into `public_html/` — `index.html`, `og-image.png`, `sitemap.xml`, `robots.txt` and the whole `projects/` directory, preserving the folder structure. The images must sit beside their HTML or WhatsApp shares render as bare grey links.
5. **Delete `public_html/projects/_template/` from the server.** It is a source file. `robots.txt` already blocks it from indexing, but it does not belong on a live host.
6. Visit `https://housingcorner.in` — you're live. SSL is auto-provisioned by Hostinger. Check that `housingcorner.in/projects/royal-paradise/` loads.
7. Force WhatsApp and Facebook to re-scrape the new preview at [developers.facebook.com/tools/debug](https://developers.facebook.com/tools/debug/) — paste each URL and hit **Scrape Again**. Caches can hold the old preview for days otherwise.
8. Submit `https://www.housingcorner.in/sitemap.xml` once at Google Search Console → Sitemaps.

### Why folder URLs work without configuration

`projects/royal-paradise/index.html` is served at `housingcorner.in/projects/royal-paradise/`
automatically — every web server looks for `index.html` when given a directory. No
rewrite rules, no `.htaccess`. Internal links in the HTML point at `index.html`
explicitly so the pages also work when opened straight off your hard drive.

### Alternative — GitHub Pages (free, useful for staging)
```bash
# From inside F:\HousingCorner\landing-page\
git init
git add index.html README.md
git commit -m "HousingCorner landing page v1"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/housingcorner-site.git
git push -u origin main
# Then on GitHub → Settings → Pages → Source: main branch, /root → Save.
```

### Alternative — Netlify drop (60 seconds)
Drag the `landing-page/` folder onto [app.netlify.com/drop](https://app.netlify.com/drop). Get a live URL immediately. Point `housingcorner.in` at it in your domain DNS later.

---

## 5 · What's NOT on this page yet (by design)

The page is intentionally light on the things that rot fastest. Add these as you grow:

- **Real property images.** Property cards currently use a tinted gradient + icon. Replace the `.property-card__image` div with an `<img>` tag once you have photos. A 1600×1000 JPEG around 180 KB is ideal.
- **Testimonials.** None included because fabricated ones backfire. Add after your first 3–5 successful transactions, each with a client quote and a verifiable name.
- **Blog / resources.** MahaRERA explainers, guides for first-time buyers — add a `/blog/` folder later. Great for SEO.
- **Google Analytics / Tag Manager.** Drop the snippet in the `<head>` when you want tracking.
- **Actual project pages.** Each property card could link to `/projects/project-name.html` — build those as individual pages as your inventory grows.

---

## 6 · Design choices worth knowing

- **Mobile-first, responsive.** Breakpoints at 860px (hero/contact stack) and 720px (footer).
- **No external assets except Google Fonts.** Logo is inline SVG, favicon is a data URI. Page weight is ~40 KB unzipped.
- **Accessibility.** Skip-link-free for simplicity but uses semantic `<nav>`, `<section>`, `<article>`, `<details>` for FAQ, and `aria-label` where needed. WCAG AA contrast on body text.
- **Performance.** No JS frameworks. Single `<script>` block at the end. Should score 95+ on Lighthouse out of the box.
- **Brand discipline.** Every color is one of six tokens defined at the top of the `<style>` block. Changing the brand is a two-line edit.

---

## 7 · Quick customizations

### Change the hero headline
Find `<h1>Find your <span class="accent">corner</span>` and edit the text. The orange-green emphasis is on the word inside `<span class="accent">`.

### Change a color palette globally
Edit the `:root` block at the top of `<style>`:
```css
:root {
  --forest: #2F5D3A;
  --terracotta: #C77E52;
  --sage: #8BA888;
  --cream: #F5F0E6;
  --ink: #1F2A24;
  --stone: #8A7E6E;
}
```

### Add a new property card
Copy one `<article class="property-card">...</article>` block and swap in real values. They auto-flow into the grid.

### Add a new FAQ
Copy one `<details>...</details>` block inside `.faq__list`. The `open` attribute on the first item makes it expanded by default.

---

## 8 · Open questions — what's left

1. **Legal entity decision.** Partnership firm vs. one founder as sole-prop with the other as authorised signatory. This affects the MahaRERA application, PAN, and bank account. See `logo-design-reference.md §7` for the tradeoff.
2. **Street-level office address** for letterhead, card back, footer, and Google Business.
3. **MahaRERA Agent Registration number** — once issued, I'll replace the three "Application in process" strings with the real number.
4. **2–4 more current listings** (name, location, BHK, starting price, project RERA number) to sit alongside Royal Paradise.
5. **Corrected Royal Paradise rate cards** from the developer — see the warning in §2.
6. **Real photography.** The two Royal Paradise cards still use the tinted gradient + icon. `client/Royal Paradise/FRONT EVEVATION.jpg.jpeg` is a usable exterior shot but is 6 MB — resize to ~1600×1000 and ~180 KB before putting it on the page.
7. **Which of the two brand palettes is canonical.** `HousingCorner_Brand_and_MahaRERA.md` §4 specifies deep green + cyan; `logo-design-reference.md` specifies forest + terracotta + cream. The site and all 13 shipping assets follow the second. One doc should be retired.
8. **Entity decision.** The site says "Founder-led firm," the deed sets up a two-partner firm, and the MahaRERA content pack is written entirely as a sole proprietorship with `[Proprietor Full Name]`. That pack needs a rewrite before it can be filed for a partnership.

Send whichever of those are ready and I'll bake them in.
