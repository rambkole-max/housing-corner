# HousingCorner — SEO status

*Last updated 12 August 2026.*

This is a plain-language record of what has been done to make the site findable,
what it means, and what still has to happen. The short version: **the on-page
work is finished, and none of it does anything until the site is uploaded and
submitted to Google.** SEO has two halves — the technical foundation, which is
a one-off job that's now complete, and authority, which is earned slowly and
has barely started.

---

## 1 · What "SEO" actually means here

Three separate things get confused under one word:

| | What it is | Status |
|---|---|---|
| **Technical SEO** | Can Google read, understand and index the pages? | Done |
| **On-page SEO** | Does each page clearly answer a real search? | Done |
| **Off-page / authority** | Does anyone link to you, review you, know you exist? | Not started |

The first two are craft — you either did them or you didn't. The third is
reputation, and it takes months. A perfectly built site with no authority still
ranks below a badly built portal that's been around for ten years. That is not a
reason to skip the first two; it's a reason to be realistic about timelines.

---

## 2 · Technical foundation

**Three indexable URLs**, each on its own clean folder path:

```
housingcorner.in/
housingcorner.in/projects/
housingcorner.in/projects/royal-paradise/
```

Folder URLs rather than `.html` files, so you can nest more under a project later
without breaking links. No server configuration was needed.

**Canonical tags** on every page. This tells Google which URL is the real one, so
`housingcorner.in`, `www.housingcorner.in` and any tracking-parameter variant all
consolidate into a single entry rather than competing as duplicates.

**sitemap.xml** listing all three URLs, and **robots.txt** pointing at it and
blocking `/projects/_template/` — the source file for new listings, which would
otherwise get indexed as a duplicate of Royal Paradise.

**Page weight is 2.46 MB total** across the whole site, with every image lazy-loaded
below the fold and every one carrying explicit `width` and `height`. Those
dimensions stop the page jumping around as images load, which is a direct Google
ranking signal (Cumulative Layout Shift). No JavaScript frameworks, no build step —
the pages are close to as fast as static HTML gets.

**All 15 images have alt text**, written to describe the image rather than to stuff
keywords. This is how a blind visitor and Google Images both understand them.

---

## 3 · On-page: how each page is targeted

Each page targets a different kind of search, and none of them compete with each
other. That's deliberate — two pages chasing the same phrase split your own
authority.

### Home — `/`
Targets brand and category searches: *housingcorner*, *real estate channel partner
Latur*, *RERA registered property agent Maharashtra*.
1,392 words · one H1, seven H2s · `RealEstateAgent` structured data carrying your
address, hours, phone, founders and service area.

### Projects — `/projects/`
Targets the browse intent: *MahaRERA registered projects Maharashtra*.
A deliberately short page (301 words) whose job is to pass visitors and link
authority down to individual listings. `CollectionPage` + `ItemList` structured data.

### Royal Paradise — `/projects/royal-paradise/`
This is the page that will actually earn traffic. **2,709 words**, twelve H2
sections, twelve images. It targets two distinct intents at once:

- *Royal Paradise Warje*, *2 BHK flats Warje Pune*, *2 BHK near Warje bridge*
- *shops for sale in Warje*, *commercial shop Pune Bangalore highway*, *showroom for sale Warje*

Structured data: `BreadcrumbList`, `ApartmentComplex`, **two** `Product` nodes
(one for the flats with real price range, one for the shops), and a ten-question
`FAQPage`.

**Why one page and not two.** Splitting flats and shops into separate URLs was
considered and rejected. They share one MahaRERA number and one location, so two
pages would be near-duplicates competing with each other and halving the authority
of both. The correct fix for a second search intent on one page is a substantial
section for it — which is what the shops now have: their own H2, their own schema,
their own FAQs, and roughly 400 words of shop-specific copy.

---

## 4 · Structured data, and why it matters more than usual for you

Structured data is a machine-readable summary in the page's code. Google uses it
to understand what a page *is*, not just what words it contains.

Yours describes: a real estate agency in Latur serving Maharashtra, a 56-unit
apartment complex at a specific Pune postcode with eleven named amenities, an
apartment product priced ₹75,14,000–₹79,96,800, a commercial unit product, and ten
questions with answers.

That last one is worth understanding. **FAQ markup must match questions visibly on
the page.** Markup describing content a visitor can't see is a manual-action risk —
Google can penalise the whole site, not just ignore the markup. Your FAQ schema had
drifted out of sync at one point, so `sync-faq-schema.py` now generates it from the
visible page, and `check-listings.py` fails the build if they ever diverge again.

---

## 5 · What is deliberately *not* optimised

Some of these are choices, not oversights, and it's worth knowing why.

**No possession date on the project page.** Nothing in the developer's documents
gives one that can be stood behind, so the page points at the MahaRERA portal
instead. A fabricated date would rank and then destroy trust at possession.

**No shop price.** The commercial rate card expired in September 2025 and contains
a transposition error. "Price on request" costs some search traffic. Publishing a
wrong number costs more.

**No testimonials.** Fabricated reviews are the fastest way to lose the credibility
the entire site is built on. Add them after your first three to five completed
transactions, with verifiable names.

**No keyword stuffing.** Copy reads as prose. Google has penalised keyword density
since roughly 2012; it now rewards pages that answer a question completely.

---

## 6 · What still has to happen — in order

Steps 1 and 2 are the difference between "the site is ready" and "the site is
working." Nothing below step 2 matters until they're done.

**1 · Upload the site.** All of it, folder structure intact. None of this work
exists to Google until the files are on the server.

**2 · Google Search Console.** Verify `housingcorner.in`, submit
`housingcorner.in/sitemap.xml`. This is how you find out what people actually search
before finding you — which is worth more than any guess about keywords. Free.

**3 · Google Business Profile.** For a local business this is probably worth more
than everything on this page combined. It's what puts you in the map pack when
someone searches *property dealer in Latur*. It requires a **street-level address** —
which the site still doesn't have, and which is also needed for the letterhead,
business cards and the MahaRERA application. This is the single biggest blocker.

**4 · Claim the social profiles.** The footer links to Instagram, LinkedIn, Facebook
and YouTube, and the structured data declares them as yours via `sameAs`. If those
handles aren't actually claimed, you're linking to nothing and declaring ownership
of accounts you don't own. Verify or remove them.

**5 · Analytics.** Google Analytics or Plausible in the `<head>`. Without it you're
guessing about which listings get read and where people leave.

**6 · Real site photographs.** The gallery has a slot reserved for
`site-progress.jpg`. A dated construction photo you took yourself is something no
competitor listing has, and Google increasingly favours demonstrably first-hand
content.

**7 · More listings.** Three URLs is a small site. Every well-built project page is
another entry point. The `_template` folder makes each one a copy-paste job.

**8 · Write something worth linking to.** Your genuine advantage is that you can
explain things honestly that portals won't — how RERA carpet area differs from
carpet-plus-balcony, what stamp duty and GST actually add to a Pune flat, how to
read a MahaRERA extract. The carpet-area explainer already on the Royal Paradise
page is the best content on the site. A `/guides/` folder of those would earn links
on merit, which is the only kind of authority worth having.

---

## 7 · Honest expectations

Brand searches — *housingcorner*, *housing corner Latur* — should rank within days
of indexing, because nothing else competes for them.

*Royal Paradise Warje* is winnable within weeks to a few months. The developer's own
site and the big portals will compete, but your page is more thorough than any of
them and is the only one that separates carpet from balcony.

Broad competitive terms — *2 BHK in Pune*, *flats in Warje* — are dominated by
portals with two decades of authority and full-time SEO teams. Do not expect to rank
for those, and do not spend money trying. Your realistic wins are project-name
searches, long-tail questions, and local searches around Latur.

The foundation is built correctly. What it needs now is time, an address, and more
listings.
