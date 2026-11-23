# KOINTEC Interior Film Catalogue 27/28

Interactive page-turning catalogue of the 196 KOINTEC architectural interior film finishes, plus nine search-friendly finish pages (one per material). Built for **GitHub Pages**. No server, no database, no build step needed to publish.

Distributed by XESS Trading LLC · [interiorfilm.com](https://interiorfilm.com)

---

## What is in this repository

| Path | What it is |
|---|---|
| `index.html` | The flipbook (home page) |
| `finishes/index.html` | All 9 materials as one overview page |
| `finishes/<material>/index.html` | One crawlable page per material: every finish with code, swatch, description, link to the product on interiorfilm.com, FAQ and schema |
| `img/s/` · `img/a/` | Swatches and interior photos (182 products each) |
| `img/cover.jpg`, `img/logo-*.png` | Cover and logos |
| `assets/` | Page-turn script (MIT licence), site stylesheet, favicon |
| `data/products.json` | The product data every page is built from |
| `tools/build.py` | Rebuilds every page from the data (Python 3, no extra packages) |
| `tools/flipbook.template.html` | Flipbook template used by the build |
| `sitemap.xml`, `robots.txt`, `404.html`, `.nojekyll` | Search and hosting files |

The pages are **already built**. You only need `tools/build.py` when you change products or the web address.

---

## 1. Put the code on GitHub

You need a free GitHub account. Pick **one** way.

### Option A: GitHub Desktop (easiest on Windows)

1. Install GitHub Desktop from <https://desktop.github.com> and sign in.
2. **File → New repository**
   - Name: `kointec-catalogue`
   - Local path: any folder, for example `D:\GitHub`
   - Click **Create repository**.
3. Open the new folder (**Repository → Show in Explorer**) and copy **everything inside this zip** into it, including the hidden `.nojekyll` file. `index.html` must sit at the top level of the folder.
4. Back in GitHub Desktop, type a summary such as `First version of the catalogue`, then click **Commit to main**.
5. Click **Publish repository**. **Untick “Keep this code private”** (GitHub Pages on a free account needs a public repository), then click **Publish repository**.

> Why not upload in the browser? GitHub's web upload takes at most 100 files at a time, and this site has about 380. GitHub Desktop sends them all in one go.

### Option B: command line (Git)

```bash
cd kointec-catalogue          # the unzipped folder
git init -b main
git add .
git commit -m "First version of the catalogue"
git remote add origin https://github.com/<your-username>/kointec-catalogue.git
git push -u origin main
```

Create the empty `kointec-catalogue` repository on github.com first (**New repository → Public**, no README).

---

## 2. Turn on GitHub Pages

1. On github.com, open the repository → **Settings** → **Pages**.
2. **Source:** *Deploy from a branch*. **Branch:** `main`, folder `/ (root)`. Click **Save**.
3. Wait 1–2 minutes. The page shows your address, for example `https://<your-username>.github.io/kointec-catalogue/`.

---

## 3. Use your own address (recommended for SEO)

A `github.io` address builds authority for GitHub's domain, not yours. Serve the catalogue from **`catalogue.interiorfilm.com`** so every visit, link and mention counts toward the interiorfilm.com brand.

1. **DNS:** at the company that manages interiorfilm.com's DNS, add one record:

   | Type | Name / Host | Value / Points to |
   |---|---|---|
   | `CNAME` | `catalogue` | `<your-username>.github.io` |

2. **GitHub:** repository → **Settings → Pages → Custom domain** → enter `catalogue.interiorfilm.com` → **Save**. GitHub adds a `CNAME` file to the repository by itself.
3. When the DNS check turns green (from a few minutes up to 24 hours), tick **Enforce HTTPS**.
4. Recommended: **Settings → Pages → Verify a domain** (GitHub's guide shows the TXT record). This stops anyone else from claiming the subdomain.

The pages are built for `https://catalogue.interiorfilm.com/`. **If you use a different address**, rebuild once so the canonical links, sitemap and schema point to it:

```bash
python tools/build.py --base https://<your-username>.github.io/kointec-catalogue/
```

Then commit and push again.

---

## 4. Get it indexed by Google and Bing

1. **Google Search Console** (<https://search.google.com/search-console>)
   - Add a **Domain** property for `interiorfilm.com` if you don't have one; it covers the `catalogue.` subdomain automatically. Otherwise add a **URL prefix** property for `https://catalogue.interiorfilm.com/`.
   - **Sitemaps** → submit `https://catalogue.interiorfilm.com/sitemap.xml`.
   - **URL Inspection** → paste the home page and each `/finishes/…/` page → **Request indexing**.
2. **Bing Webmaster Tools** (<https://www.bing.com/webmasters>) → **Import from Google Search Console**. Bing also powers Microsoft Copilot and feeds other AI search tools.
3. **Link to the catalogue from interiorfilm.com.** This is the single most important step. A new subdomain with no links pointing at it will not rank. Add:
   - a menu or footer link **“Online Catalogue”** on every page
   - on each category page (Wood, Metal…), a link to the matching finish page, for example *“See all 58 wood finishes in the KOINTEC catalogue”*
   - next to the existing *Download catalogue (PDF)* button, a **“View online”** link to the flipbook
4. Share the link: Google Business Profile post, Instagram bio and story, WhatsApp catalogue messages, and email signatures.

---

## 5. Update products later

1. Edit `data/products.json`. Each product looks like this:
   ```json
   {"code": "CNW631", "group": "PREMIUM WOOD", "name": "Natural Oak Wood Interior Film",
    "desc": "…", "img": true, "akind": "Application",
    "url": "https://interiorfilm.com/uae/en/category/wood/premium-wood/natural-oak-wood-interior-film"}
   ```
   - `group` must be one of the collection names used in `tools/build.py` (WOOD, PREMIUM WOOD, MARBLE, SOLID…).
   - `img: true` needs both `img/s/<CODE>.jpg` (swatch, 520×390) and `img/a/<CODE>.jpg` (interior photo, about 1100 px wide).
2. Run `python tools/build.py`.
3. Commit and push. GitHub Pages republishes within a minute or two.

Contact details, the web address and the intro copy for each material are settings at the top of `tools/build.py`.

---

## What the SEO setup already does

- **10 indexable pages**: the flipbook home, an overview of all finishes, and 9 material pages. Each has a unique title (60 characters or fewer), meta description, canonical URL, Open Graph image and one H1.
- **Material pages target the finish searches** from the SEO plan: *wood vinyl wrap*, *marble interior film*, *metallic vinyl wrap*, *leather interior film*, *concrete interior film* and others. All products are in plain HTML, so no JavaScript is needed to read them.
- **Structured data:** Organization, WebSite, CollectionPage, BreadcrumbList, ItemList of Product (with SKU = product code and brand = KOINTEC), and FAQPage.
- **176 deep links** to the exact product pages on interiorfilm.com. The rest link to the category page or to the Floor Vinyl page.
- Links to the application pages (kitchen wrapping, bathroom remodeling, hotel interior finishing, office interior wrap, restaurant interior, furniture wraps, residential interior, floor vinyl), using the keyword as the link text.
- An image sitemap for all swatches, descriptive alt text, lazy-loaded images, a mobile-friendly layout, and light and dark themes.
- Fast hosting: static files on GitHub's CDN, with no CDN dependencies except Google Fonts.

---

© 2026 XESS Trading Co LLC. All rights reserved. See [LICENSE](LICENSE).
