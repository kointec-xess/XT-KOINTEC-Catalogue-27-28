#!/usr/bin/env python3
"""Build the KOINTEC catalogue site (GitHub Pages ready).

Usage:
    python tools/build.py                       # uses BASE_URL below
    python tools/build.py --base https://<user>.github.io/<repo>/

Reads  data/products.json + tools/flipbook.template.html
Writes index.html, finishes/**/index.html, sitemap.xml, robots.txt, 404.html
No third-party packages needed (Python 3.8+).
"""
import json, math, os, re, sys, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- settings
BASE_URL = "https://catalogue.interiorfilm.com/"   # change, or pass --base
MAIN = "https://interiorfilm.com/uae/en"
PDF_URL = "https://xesstrading.com/KOINTEC-XT-catalogue-27-28.pdf"
CONTACT = {
    "company": "XESS Trading LLC",
    "phone": "+971 52 456 9900",
    "whatsapp": "+971 55 217 8882",
    "email": "info@xesstrading.com",
    "street": "No 4, 10, 20A Street, Al Marabea' St, Al Quoz Industrial Area 4",
    "city": "Dubai", "country": "AE",
}
if "--base" in sys.argv:
    BASE_URL = sys.argv[sys.argv.index("--base") + 1]
BASE_URL = BASE_URL.rstrip("/") + "/"
TODAY = datetime.date.today().isoformat()

APPS = {
    "kitchen": ("Kitchen wrapping", f"{MAIN}/kitchen-wrapping"),
    "bathroom": ("Bathroom remodeling", f"{MAIN}/bathroom-remodeling"),
    "hotel": ("Hotel interior finishing", f"{MAIN}/hotel-interior-finishing"),
    "office": ("Office interior wrap", f"{MAIN}/office-interior-wrap"),
    "restaurant": ("Restaurant interior", f"{MAIN}/restaurant-interior"),
    "furniture": ("Furniture wraps", f"{MAIN}/furniture-wraps"),
    "residential": ("Residential interior", f"{MAIN}/residential-interior"),
    "floor": ("Floor vinyl", f"{MAIN}/floor-vinyl"),
}

# id must match FAMS ids in the flipbook template; order = book order
FAMILIES = [
    dict(id="wood", slug="wood-interior-film", name="Wood",
         title="Wood Vinyl Wrap & Wood Interior Film | KOINTEC UAE",
         h1="Wood Interior Film & Wood Vinyl Wrap",
         kw="wood vinyl wrap", main=f"{MAIN}/category/wood",
         groups=[("WOOD", "Wood"), ("PREMIUM WOOD", "Premium Wood"), ("PAINTED WOOD", "Painted Wood"), ("TEXTURE WOOD", "Texture Wood")],
         apps=["kitchen", "furniture", "hotel", "residential"],
         intro="KOINTEC wood interior film gives cabinets, doors, wardrobes and wall panels the look and grain of real timber without sanding, staining or replacing the surface underneath. This page lists every wood finish in the KOINTEC 27/28 catalogue, from light oak and maple to walnut, cherry and painted timber, each with its product code. Premium Wood adds deeper grain and richer tones for hospitality and reception joinery, while Painted and Texture Wood cover matt painted looks and tactile grains. Use the codes below to request a quote or to compare finishes in the flipbook."),
    dict(id="stone", slug="marble-stone-interior-film", name="Stone & Marble",
         title="Marble & Stone Interior Film Catalogue | KOINTEC UAE",
         h1="Marble & Stone Interior Film",
         kw="marble interior film", main=f"{MAIN}/category/stone-marble",
         groups=[("MARBLE", "Marble"), ("STONE", "Stone"), ("PREMIUM STONE", "Premium Stone"), ("BRICK", "Brick")],
         apps=["hotel", "bathroom", "kitchen", "furniture"],
         intro="KOINTEC marble and stone interior film brings veined marble, natural stone and brick to reception desks, columns, feature walls, counters and furniture at a fraction of the weight of real stone. This page lists every Stone & Marble finish in the KOINTEC 27/28 catalogue with its code: white and grey marbles with fine or gold veining, warm beige stones, premium stone textures and brick. Each finish is shown as a swatch and, where available, in an interior, so you can judge the vein and colour before you order."),
    dict(id="metal", slug="metal-interior-film", name="Metal",
         title="Brushed Metal & Metallic Vinyl Wrap | KOINTEC UAE",
         h1="Brushed Metal & Mirror Interior Film",
         kw="metallic vinyl wrap", main=f"{MAIN}/category/metal",
         groups=[("BRUSHED METAL", "Brushed Metal"), ("PRINTED METAL", "Printed Metal"), ("MIRROR", "Mirror")],
         apps=["office", "hotel", "restaurant", "kitchen"],
         intro="KOINTEC metal interior film gives lift lobbies, door frames, retail fixtures, trims and kitchen fronts a brushed or mirror metal finish without fabricating sheet metal. This page lists every metal finish in the KOINTEC 27/28 catalogue with its product code, from soft and pearl silver brushed metals to bronze, champagne and gold tones, plus mirror films. Compare the swatches here, then open any product on interiorfilm.com for availability and a quote."),
    dict(id="concrete", slug="concrete-interior-film", name="Concrete",
         title="Concrete Interior Film & Vinyl Wrap | KOINTEC UAE",
         h1="Concrete Interior Film",
         kw="concrete interior film", main=f"{MAIN}/category/concrete",
         groups=[("CONCRETE", "Texture Concrete"), ("PREM PAINTED CONCRETE", "Premium Painted Concrete"), ("CEMENT", "Cement")],
         apps=["office", "restaurant", "residential", "furniture"],
         intro="KOINTEC concrete interior film recreates raw, textured and painted concrete on walls, columns, counters and furniture, with none of the weight, dust or curing time of a real screed. This page lists every concrete finish in the KOINTEC 27/28 catalogue with its code: Texture Concrete for tactile industrial surfaces and Premium Painted Concrete for smoother, coloured looks. Use it to shortlist finishes for offices, restaurants and residential projects."),
    dict(id="solid", slug="solid-colour-interior-film", name="Solid",
         title="Solid Colour Vinyl Wrap & Interior Film | KOINTEC UAE",
         h1="Solid Colour Interior Film",
         kw="solid colour vinyl wrap", main=f"{MAIN}/category/solid",
         groups=[("SOLID", "Solid"), ("SOLID GLOSSY", "Solid Glossy"), ("EMBO SOLID", "Embo Solid")],
         apps=["kitchen", "office", "furniture", "residential"],
         intro="KOINTEC solid interior film covers cabinetry, doors, partitions and furniture in a flat colour, from whites and greys to deep blues, greens and reds. This page lists every solid finish in the KOINTEC 27/28 catalogue with its code: Solid in a matt finish, Solid Glossy for high-shine kitchen and retail fronts, and Embo Solid with an embossed texture. The swatch colours are photographs, so confirm a final colour with a physical sample before a large project."),
    dict(id="soft", slug="soft-matt-interior-film", name="Soft",
         title="Soft Matt Interior Film Catalogue | KOINTEC UAE",
         h1="Soft Matt Interior Film",
         kw="soft matt interior film", main=f"{MAIN}/category/soft",
         groups=[("SOFT MATT", "Soft Matt"), ("TEXTURE SOFT MATT", "Texture Soft Matt")],
         apps=["kitchen", "residential", "furniture", "hotel"],
         intro="KOINTEC soft matt interior film has a velvety, low-sheen surface that suits kitchen fronts, bedroom furniture and wardrobes. This page lists every Soft Matt and Texture Soft Matt finish in the KOINTEC 27/28 catalogue with its code, from pearl grey and warm neutrals to textured wood looks. Open a finish to see it in an interior, or go to interiorfilm.com for the full product details."),
    dict(id="fabric", slug="leather-fabric-interior-film", name="Fabric & Leather",
         title="Leather & Fabric Interior Film Catalogue | KOINTEC UAE",
         h1="Leather & Fabric Interior Film",
         kw="leather interior film", main=f"{MAIN}/category/fabric-leather",
         groups=[("FABRIC", "Fabric"), ("LEATHER", "Leather")],
         apps=["hotel", "office", "restaurant", "residential"],
         intro="KOINTEC fabric and leather interior film adds woven and leather textures to headboards, wall panels, reception desks and hospitality joinery, in a surface that wipes clean. This page lists every Fabric & Leather finish in the KOINTEC 27/28 catalogue with its code. Compare the swatches, see each finish in an interior, and send the code to our team for a quote."),
    dict(id="special", slug="glitter-decoration-film", name="Special",
         title="Glitter Vinyl Film & Design Film | KOINTEC UAE",
         h1="Glitter & Design Films",
         kw="glitter vinyl film", main=f"{MAIN}/category/special/glitter",
         groups=[("GLITTER", "Glitter"), ("DECO FILM", "Design Films")],
         apps=["restaurant", "hotel", "residential", "bathroom"],
         intro="KOINTEC glitter and design films are made for statement surfaces: bar fronts, stair risers, retail displays, vanities and feature walls. This page lists every Special finish in the KOINTEC 27/28 catalogue with its code, from silver, gold and champagne glitter to rose gold and black, plus Design Films in metallic, mirror, holographic and iridescent finishes. Each finish is shown up close and, where available, in an interior."),
    dict(id="flooring", slug="floor-vinyl-film", name="Flooring",
         title="Floor Vinyl Film | KOINTEC Flooring Pro Catalogue UAE",
         h1="Flooring Pro Floor Vinyl Film",
         kw="floor vinyl film", main=f"{MAIN}/floor-vinyl",
         groups=[("FLOORING", "Flooring Pro")],
         apps=["floor", "office", "residential", "hotel"],
         intro="KOINTEC Flooring Pro is an interior floor film range for offices, showrooms and residential renovations. This page lists every Flooring Pro finish in the KOINTEC 27/28 catalogue with its code, from light oak to classic walnut. Use the codes to ask our team about availability and installation for your floor area."),
]

def nat(s):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)]

def esc(s):
    return html.escape(str(s or ""), quote=True)

def title_name(p, gname):
    if p.get("name"):
        return p["name"]
    return "Design Film" if p["group"] == "DECO FILM" else f"{gname} Interior Film"

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

# ---------------------------------------------------------------- data
P = json.load(open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8"))
P = [p for p in P if not p.get("hidden")]  # "hidden": true keeps a product in the data but off the site
gname = {}
for f in FAMILIES:
    f["items"] = []
    for g, n in f["groups"]:
        gname[g] = n
        f["items"] += sorted([p for p in P if p["group"] == g], key=lambda p: nat(p["code"]))
    f["url"] = f"finishes/{f['slug']}/"

# ---------------------------------------------------------------- book plan (single source of page numbers)
R50, R30, R25 = "1.23m x 50 m", "1.23m x 30 m", "1.23m x 25 m"
COLS = {  # collection -> display name split for the two-weight title, roll size, intro (from the KOINTEC master catalogue)
    "BRUSHED METAL": ("Brushed Metal", "Brushed", "Metal", R50, "KOINTEC's Brushed Metal series is infused with a carefully crafted line pattern, so the metal texture changes with the light. It suits commercial and public spaces."),
    "MIRROR": ("Mirror Metal", "Mirror", "Metal", "1m x 25 m", "Mirror Metal film installs easily, expands the sense of space and adds a distinctive reflective touch. Remove the transparent protective film after installation."),
    "SOFT MATT": ("Soft Matt", "Soft", "Matt", R50, "A specially processed surface that is visually calm and gentle to the touch, designed to resist stains, fingerprints and daily scratches."),
    "TEXTURE SOFT MATT": ("Texture Soft Matt", "Texture Soft", "Matt", R50, "The Soft Matt surface with an added texture, turning a plain space into something distinctive."),
    "SOLID": ("Solid", "", "Solid", R50, "Simple, natural colours that follow the trends of the times. Combine colours to find the one that best suits your space."),
    "SOLID GLOSSY": ("Solid Glossy", "Solid", "Glossy", R50, "Solid colours finished with a glossy coating, so they catch the light and set a different mood."),
    "EMBO SOLID": ("Embo Solid", "Embo", "Solid", R50, "Solid colours with an embossed surface texture for walls, cabinetry and retail interiors."),
    "CONCRETE": ("Texture Concrete", "Texture", "Concrete", R50, "The rough, chic texture of concrete finishes modern spaces with an edgy touch and creates a stylish focal point."),
    "PREM PAINTED CONCRETE": ("Premium Painted Concrete", "Premium Painted", "Concrete", R50, "A subtle concrete texture in soft pastel tones for a natural, restrained and premium atmosphere."),
    "CEMENT": ("Cement", "", "Cement", "", "A cement-look surface for walls, columns and furniture."),
    "PREMIUM WOOD": ("Premium Wood", "Premium", "Wood", R50, "A near-flawless imitation of real wood texture. A rich variety of colours and grains makes it a high-quality material that stays stylish year after year."),
    "PAINTED WOOD": ("Painted Wood", "Painted", "Wood", R50, "Warm painted timber that changes the mood of a room the moment you step in."),
    "TEXTURE WOOD": ("Texture Wood", "Texture", "Wood", R50, "Natural wood texture reproduced as it is, with a depth of detail you can see and feel."),
    "WOOD": ("Wood", "", "Wood", R50, "Wood textures in diverse colours and patterns for the most natural look, working with your lighting to keep the atmosphere calm and stable."),
    "PREMIUM STONE": ("Premium Stone", "Premium", "Stone", R50, "Timeless stone for upscale spaces. Advanced coating brings the designs close to the realism of actual stone."),
    "STONE": ("Stone", "", "Stone", R50, "A finely rough surface with a luxurious, sophisticated feel that brings modern charm to any interior."),
    "MARBLE": ("Marble", "", "Marble", R50, "Elegant marble patterns for premium spaces, loved for making interiors look and feel lavish."),
    "BRICK": ("Brick", "", "Brick", R50, "A vintage material for cafes, restaurants, studios and other commercial spaces."),
    "GLITTER": ("Glitter", "", "Glitter", R30, "A gentle starlight theme in trendy colours that shine even more under light, made for special spaces."),
    "DECO FILM": ("Design Films", "Design", "Films", "1m x 50 m", "Metallic, mirror, holographic and iridescent design films for feature surfaces, retail displays and signage."),
    "PRINTED METAL": ("Printed Metal", "Printed", "Metal", R50, "Printed metal finishes for feature walls, fixtures and furniture."),
    "FABRIC": ("Fabric", "", "Fabric", R50, "Fabric patterns that raise the warmth of a room and create a stylish, cosy mood."),
    "LEATHER": ("Leather", "", "Leather", R50, "Feels just like real leather to the touch, for classic and refined spaces."),
    "FLOORING": ("Flooring Pro", "Flooring", "Pro", R25, "An alternative to traditional flooring with its own texture and adhesion technology: bold thickness, convenient installation and a range of materials."),
}
BOOK_FAMS = [  # tab order, as in the printed book
    ("metal", "Metal", ["BRUSHED METAL", "PRINTED METAL", "MIRROR"]),
    ("soft", "Soft", ["SOFT MATT", "TEXTURE SOFT MATT"]),
    ("solid", "Solid", ["SOLID", "SOLID GLOSSY", "EMBO SOLID"]),
    ("concrete", "Concrete", ["CONCRETE", "PREM PAINTED CONCRETE", "CEMENT"]),
    ("wood", "Wood", ["PREMIUM WOOD", "PAINTED WOOD", "TEXTURE WOOD", "WOOD"]),
    ("stone", "Stone & Marble", ["MARBLE", "STONE", "PREMIUM STONE", "BRICK"]),
    ("special", "Special", ["GLITTER", "DECO FILM"]),
    ("fabric", "Fabric & Leather", ["FABRIC", "LEATHER"]),
    ("flooring", "Flooring Pro", ["FLOORING"]),
]
DENSE = {"SOLID"}
CERTS = [
    ("ISO 9001 · ISO 14001", "International standard certification that a product or service meets specified requirements and is operated effectively.", "KS Q ISO 9001:2015 WQ18-0408 · KS I ISO 14001:2015 WE18-0409"),
    ("CE", "Compliance with EU Council directives on safety, health, environment and consumer protection.", "Fire safety 080-025410 · Performance 1020-CPR-010-047083 · Formaldehyde 100-066635, 100-066636"),
    ("ASTM E-84", "The standard flame-retardant test for building materials in the United States.", "221020011SHF-001-R1"),
    ("KFI", "Fire-safety evaluation of products under Korean fire protection regulations.", "No. 2305138"),
    ("KC", "Product safety certification granted by the Korean government.", "Formaldehyde H232-17-07700"),
    ("Indoor architectural material", "Certification by Korea's Ministry of Environment for pollutants emitted from building materials.", "N282-23-00041 · N282-23-00042 · N282-23-00043"),
    ("Korea Eco-Label", "Eco-label certificate.", "No. 29029"),
    ("Hazardous substances (China)", "Assessment for hazardous substances in building environmental products, GB 18585-2001.", "WT2018B01A00538"),
    ("Harmful elements test", "Test report for harmful elements under the common safety standards for children's products.", "F690101 / LF-CTSAYHA23-01357"),
    ("Pollutant emission test", "Pollutants emitted from building finishing materials: TVOC, toluene, formaldehyde.", "N282-23-00041 · 00042 · 00043"),
    ("Anti-microbial · anti-fungal", "Test reports for anti-microbial (bacteria) and anti-fungal film.", "KAAAM200916-015 · TBK-2020-003141"),
    ("Eco-friendly release paper", "Test report for alkali degradability of the eco-friendly release paper.", "M287-23-04764"),
]
INSTALL = {
    "inst1": [
        ("Pre-application planning", [
            ("Inspect the type and condition of the surface before installing, including how dry it is.", ""),
            ("Wood (MDF, PB): apply on thoroughly dried wood of uniform density.", "Adhesion and flame-retardant performance can vary with surface density."),
            ("Metal sheets: clean with alcohol first.", "Sand rough surfaces such as putty and remove the particles."),
            ("Painted surfaces: clean with alcohol and check for damage.", "Fill bumps with putty, sand, and remove dust before installing."),
            ("Overlays and ABS doors: treat contaminated and damaged areas first.", ""),
            ("Inspect the purchased product before installation.", "Condition, LOT, pattern name."),
            ("Cut larger than the surface.", "Release-paper print lines are only a guide; measure for accurate cutting."),
        ], True),
        ("Primer application", [
            ("Apply primer 2–3 times to wood cut edges, which absorb more.", "Apply each coat only after the previous one has fully dried."),
            ("Let the primer dry completely: at least 4 hours, depending on conditions.", ""),
            ("Store remaining primer as its manual recommends.", ""),
        ], True),
        ("Interior film application", [
            ("For overlapping or joined patterns, cut with the pattern joins in mind.", "Cutting along the release-paper lines can mismatch the pattern."),
            ("Apply firm pressure at the edges.", "Too little pressure can cause lifting."),
            ("Prepare and apply at room temperature.", ""),
            ("Deep-embossed patterns have less adhesive contact: prime well and press harder.", ""),
            ("Store and install away from moisture and direct sunlight.", ""),
        ], True),
    ],
    "inst2": [
        ("Cautions for specific products", [
            ("IPT 5000 Mirror Metal", "Remove the transparent protective film after installation and clean-up. A soft wool-felt squeegee is recommended. Wipe with a dry cloth; clean with neutral detergent or water."),
            ("Premium Glow · Brushed Metal · Solid Glossy · Glitter", "The coated surface can dent or scratch: install with care, using a soft wool-felt squeegee."),
            ("Solid · Soft Matt · Texture Soft Matt", "Install in a clean environment. Particles left on the surface show through as bumps."),
            ("Fabric", "Sharp tools such as plastic spatulas can scratch the surface."),
            ("Leather", "The film is thick: apply enough pressure when folding or overlapping."),
            ("Flooring Pro", "Butt-join the seams. Overlapping can leave raised joints."),
        ], "p"),
        ("General cautions", [
            ("KOINTEC interior film is for indoor use.", ""),
            ("Colour can vary between LOTs; do not mix LOTs on one project.", ""),
            ("Store at a controlled temperature, away from moisture and direct sunlight.", ""),
            ("Long exposure to low temperatures can crack the surface and weaken adhesion.", ""),
            ("Long exposure to UV light can cause discolouration.", ""),
            ("Keep the room at room temperature for 1–2 days before and after installation.", ""),
            ("Store leftover film in its original box.", ""),
            ("Colours can differ slightly between samples and the actual product.", ""),
            ("Handle with care in transport; impacts can damage the film.", ""),
            ("Follow this installation guide closely.", ""),
        ], True),
    ],
}

byc = {p["code"]: p for p in P}
def items_of(G):
    return sorted([p for p in P if p["group"] == G], key=lambda p: nat(p["code"]))
used = set()
def pick_photo(cands, prefer_app=True):
    for p in cands:
        if p["img"] and p["code"] not in used and (p.get("akind") == "Application" or not prefer_app):
            used.add(p["code"]); return p["code"]
    for p in cands:
        if p["img"] and p["code"] not in used:
            used.add(p["code"]); return p["code"]
    return None

PAGES, TABS = [], []
def add(k, label, **kw):
    PAGES.append(dict(k=k, label=label, no=len(PAGES) + 1, **kw)); return PAGES[-1]
add("cover", "Cover"); add("intro", "Premium texture and more"); add("toc", "Contents")
APPS_PAGE = [["Kitchen Wrapping", "SM11", f"{MAIN}/kitchen-wrapping"], ["Bathroom Remodeling", "SIP656", f"{MAIN}/bathroom-remodeling"],
             ["Hotel Interior Finishing", "CNW633", f"{MAIN}/hotel-interior-finishing"], ["Office Interior Wrap", "CNW625", f"{MAIN}/office-interior-wrap"],
             ["Furniture Wraps", "IP401", f"{MAIN}/furniture-wraps"]]
add("apps", "Applications")
used.update(c for _, c, _ in APPS_PAGE)
for fid, fname, cols in BOOK_FAMS:
    units, small = [], []
    for G in cols:
        n = len(items_of(G))
        if n == 0:
            continue
        if n >= 6:
            if small: units.append(("compact", small)); small = []
            units.append(("large", G))
        else:
            if small and (sum(len(items_of(g)) for g in small) + n > 6 or len(small) == 2):
                units.append(("compact", small)); small = []
            small.append(G)
    if small: units.append(("compact", small))
    tab = None
    for kind, val in units:
        if kind == "large":
            G, its = val, items_of(val)
            if len(PAGES) % 2 == 0:   # opener must be a left (even) page: add a full-bleed photo page first
                ph = pick_photo(its[3:] + its)
                add("insp", COLS[G][0], photo=ph)
            if tab is None:
                tab = dict(id=fid, label=fname, start=len(PAGES) + 1, sub=" · ".join(COLS[g][0] for g in cols if items_of(g)))
            add("open", COLS[G][0], col=G, photo=pick_photo(its))
            codes = [p["code"] for p in its]
            if G in DENSE:
                for i in range(0, len(codes), 12):
                    add("g3", COLS[G][0], col=G, codes=codes[i:i + 12])
            else:
                i, j = 0, 0
                while i < len(codes):
                    chunk = its[i:i + 4]
                    ph = pick_photo(chunk) if (j % 2 == 1 and len(codes) - i >= 3) else None
                    if ph:
                        add("feat", COLS[G][0], col=G, photo=ph, codes=codes[i:i + 4]); i += 4
                    else:
                        add("g2", COLS[G][0], col=G, codes=codes[i:i + 6]); i += 6
                    j += 1
        else:
            if tab is None:
                tab = dict(id=fid, label=fname, start=len(PAGES) + 1, sub=" · ".join(COLS[g][0] for g in cols if items_of(g)))
            allits = [p for g in val for p in items_of(g)]
            add("compact", " · ".join(COLS[g][0] for g in val), blocks=[dict(col=g, codes=[p["code"] for p in items_of(g)]) for g in val],
                photo=pick_photo(allits))
    TABS.append(tab)
TABS.append(dict(id="cert", label="Certification", start=len(PAGES) + 1, sub="Fire safety and eco-friendly test reports"))
add("cert", "Certification & test report")
TABS.append(dict(id="install", label="Installation", start=len(PAGES) + 1, sub="Preparation, primer, application and cautions"))
add("inst1", "Installation guide"); add("inst2", "Installation guide")
IDX_START = len(PAGES) + 1
add("idx", "Code index", part=0); add("idx", "Code index", part=1)
if (len(PAGES) + 1) % 2:
    add("notes", "Notes")
add("back", "Back cover")
for pg in PAGES:
    for c in pg.get("codes", []):
        byc[c]["page"] = pg["no"]
    for b in pg.get("blocks", []):
        for c in b["codes"]:
            byc[c]["page"] = pg["no"]
assert all("page" in p for p in P), [p["code"] for p in P if "page" not in p]
TABSTART = {t["id"]: t["start"] for t in TABS}
for f in FAMILIES:
    f["start"] = TABSTART[f["id"]]

ORG = {
    "@type": "Organization", "@id": "https://interiorfilm.com/#org",
    "name": CONTACT["company"], "url": "https://interiorfilm.com/",
    "email": CONTACT["email"], "telephone": CONTACT["phone"],
    "address": {"@type": "PostalAddress", "streetAddress": CONTACT["street"], "addressLocality": CONTACT["city"], "addressCountry": CONTACT["country"]},
    "areaServed": ["AE", "SA", "QA"],
}

def head(title, desc, path, extra_ld=(), img="img/cover.jpg", rel=""):
    url = BASE_URL + path
    ld = "".join(jsonld(x) for x in extra_ld)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KOINTEC Interior Film Catalogue">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#082f49">
<link rel="icon" href="{rel}favicon.ico" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
{ld}
"""

def site_header(rel, active):
    nav = [("Flipbook", f"{rel}", "book"), ("All finishes", f"{rel}finishes/", "finishes"), ("Download PDF", PDF_URL, "pdf"), ("interiorfilm.com", f"{MAIN}", "main")]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k == active else ""}{" rel=\"noopener\"" if k in ("main", "pdf") else ""}>{n}</a>' for n, h, k in nav)
    return f"""<header class="top"><div class="wrap top-in">
<a class="logo" href="{rel}"><img src="{rel}img/logo-kointec.png" alt="KOINTEC" width="611" height="219"><span class="sep" aria-hidden="true"></span><span class="cat"><small>Interior Film</small> <b>Catalogue 27/28</b></span></a>
<nav aria-label="Main">{links}</nav></div></header>"""

def site_footer(rel):
    fams = "".join(f'<li><a href="{rel}{f["url"]}">{esc(f["name"])} interior film</a></li>' for f in FAMILIES)
    apps = "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in APPS.values())
    wa = re.sub(r"\D", "", CONTACT["whatsapp"])
    return f"""<footer class="foot"><div class="wrap foot-in">
<div><p class="fh">KOINTEC Interior Film, made in Korea</p>
<p>Supplied in the UAE, Saudi Arabia and Qatar by {esc(CONTACT['company'])}, authorized KOINTEC distributor in the UAE since 2016.</p>
<p>{esc(CONTACT['street'])}, {esc(CONTACT['city'])}<br>Phone <a href="tel:{CONTACT['phone'].replace(' ','')}">{esc(CONTACT['phone'])}</a> · WhatsApp <a href="https://wa.me/{wa}">{esc(CONTACT['whatsapp'])}</a><br><a href="mailto:{CONTACT['email']}">{esc(CONTACT['email'])}</a></p></div>
<div><p class="fh">Finishes</p><ul>{fams}</ul></div>
<div><p class="fh">Applications</p><ul>{apps}</ul></div>
</div><div class="wrap legal">© {datetime.date.today().year} {esc(CONTACT['company'])} · <a href="https://interiorfilm.com/">interiorfilm.com</a></div></footer>"""

WA_ORDER = "971527844188"
def wa_link(name, code):
    from urllib.parse import quote
    return f"https://wa.me/{WA_ORDER}?text=" + quote(f"I'm interested in {name} (SKU: {code})", safe="")

def card(p, rel, fam):
    g = gname[p["group"]]
    nm = title_name(p, g)
    img = (f'<img src="{rel}img/s/{p["code"]}.jpg" alt="{esc(p["code"])} {esc(nm)} swatch" width="520" height="390" loading="lazy" decoding="async">'
           if p["img"] else '<span class="ph">Image coming soon</span>')
    shop = (f'<a class="b pri" href="{p["url"]}">View product</a>' if p.get("url")
            else f'<a class="b pri" href="{fam["main"]}">View {esc(fam["name"].lower())} range</a>')
    return f"""<article class="card" id="{esc(p['code'].lower())}">
<div class="sw">{img}</div>
<div class="meta"><p class="code">{esc(p['code'])}</p><h3>{esc(nm)}</h3>
{f'<p class="d">{esc(p["desc"])}</p>' if p.get('desc') else ''}{f'<p class="sz">Roll size {esc(p["size"])}</p>' if p.get('size') else ''}
<div class="acts">{shop}<a class="b wa" href="{wa_link(nm, p['code'])}" target="_blank" rel="noopener">Order on WhatsApp</a><a class="b" href="{rel}#page-{p['page']}">Flipbook p.{p['page']}</a></div></div></article>"""

# ---------------------------------------------------------------- family pages
CSS_LINK = lambda rel: f'<link rel="stylesheet" href="{rel}assets/site.css">'
for f in FAMILIES:
    rel = "../../"
    n = len(f["items"])
    desc = f"{n} KOINTEC {f['name'].lower()} interior film finishes with codes, swatches and interior photos. {f['kw'].capitalize()} for UAE, KSA and Qatar projects, supplied by XESS Trading."
    if len(desc) > 160:
        desc = desc[:157].rsplit(" ", 1)[0] + "…"
    faqs = [
        (f"What is KOINTEC {f['name'].lower()} interior film?",
         f"It is a self-adhesive architectural film, made in Korea, that gives existing surfaces such as cabinets, doors, walls and furniture a {f['name'].lower()} finish without replacing them."),
        (f"How many {f['name'].lower()} finishes are in the KOINTEC 27/28 catalogue?",
         f"{n} finishes across {', '.join(n2 for g2, n2 in f['groups'] if any(p['group'] == g2 for p in P))}. Each one is listed on this page with its product code."),
        (f"Where can I buy KOINTEC {f['name'].lower()} interior film in the UAE?",
         f"From {CONTACT['company']} in Al Quoz, Dubai, the authorized KOINTEC distributor in the UAE since 2016, through interiorfilm.com. We also supply Saudi Arabia and Qatar."),
        ("How do I get a quote?",
         f"Send the product codes you like to our team through the contact page on interiorfilm.com, by WhatsApp on {CONTACT['whatsapp']} or by email to {CONTACT['email']}."),
    ]
    items_ld = {
        "@type": "ItemList", "name": f"KOINTEC {f['name']} interior film finishes", "numberOfItems": n,
        "itemListElement": [{
            "@type": "ListItem", "position": i + 1,
            "item": {"@type": "Product", "name": title_name(p, gname[p['group']]), "sku": p["code"],
                     **({"brand": {"@type": "Brand", "name": "KOINTEC"}} if p.get("brand", "KOINTEC") else {}),
                     **({"image": f"{BASE_URL}img/s/{p['code']}.jpg"} if p["img"] else {}),
                     **({"description": p["desc"]} if p.get("desc") else {}),
                     "url": p.get("url") or f"{BASE_URL}{f['url']}#{p['code'].lower()}",
                     "category": f"{f['name']} interior film"}} for i, p in enumerate(f["items"])]}
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Catalogue", "item": BASE_URL},
        {"@type": "ListItem", "position": 2, "name": "Finishes", "item": BASE_URL + "finishes/"},
        {"@type": "ListItem", "position": 3, "name": f["name"], "item": BASE_URL + f["url"]}]}
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": f["h1"], "url": BASE_URL + f["url"], "description": desc, "publisher": {"@id": ORG["@id"]}},
        ORG, crumbs, items_ld, faq_ld]}
    hero = next((p for p in f["items"] if p["img"] and p.get("akind") == "Application"), None)
    sections = ""
    for g, gn in f["groups"]:
        its = [p for p in f["items"] if p["group"] == g]
        if not its:
            continue
        sections += f'<section class="grp" id="{esc(gn.lower().replace(" ", "-"))}"><h2>{esc(gn)} <span>{len(its)} finishes</span></h2><div class="grid">{"".join(card(p, rel, f) for p in its)}</div></section>'
    apps = "".join(f'<li><a href="{APPS[a][1]}">{esc(APPS[a][0])} with {esc(f["name"].lower())} interior film</a></li>' for a in f["apps"])
    others = "".join(f'<li><a href="{rel}{o["url"]}">{esc(o["name"])}</a></li>' for o in FAMILIES if o is not f)
    body = f"""{head(f['title'], desc, f['url'], [graph], img=(f'img/a/{hero["code"]}.jpg' if hero else 'img/cover.jpg'), rel=rel)}{CSS_LINK(rel)}
</head><body>
{site_header(rel, 'finishes')}
<main>
<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{rel}">Catalogue</a> › <a href="{rel}finishes/">Finishes</a> › <span>{esc(f['name'])}</span></nav>
<div class="hero">
<div class="hero-t"><p class="eyebrow">KOINTEC 27/28 · {n} finishes</p>
<h1>{esc(f['h1'])}</h1>
<p class="lede">{esc(f['intro'])}</p>
<div class="acts"><a class="b pri" href="{f['main']}">Shop {esc(f['kw'])} on interiorfilm.com</a><a class="b" href="{rel}#page-{f['start']}">Open in flipbook</a></div>
<p class="jump">{' · '.join(f'<a href="#{esc(gn.lower().replace(" ", "-"))}">{esc(gn)}</a>' for _, gn in f['groups'] if any(p['group'] == _ for p in f['items']))}</p></div>
{f'<figure class="hero-i"><img src="{rel}img/a/{hero["code"]}.jpg" alt="{esc(title_name(hero, gname[hero["group"]]))} ({hero["code"]}) in an interior" width="1100" height="825" fetchpriority="high"><figcaption>Shown: {hero["code"]} {esc(title_name(hero, gname[hero["group"]]))}</figcaption></figure>' if hero else ''}
</div>
{sections}
<section class="more">
<div><h2>Where to use {esc(f['name'].lower())} interior film</h2><ul class="links">{apps}</ul></div>
<div><h2>Other finishes</h2><ul class="links">{others}</ul></div>
</section>
<section class="faq"><h2>Questions about {esc(f['name'].lower())} interior film</h2>
{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs)}
</section>
</div>
</main>
{site_footer(rel)}
</body></html>"""
    os.makedirs(os.path.join(ROOT, "finishes", f["slug"]), exist_ok=True)
    open(os.path.join(ROOT, "finishes", f["slug"], "index.html"), "w", encoding="utf-8").write(body)

# ---------------------------------------------------------------- finishes index
rel = "../"
total = len(P)
tiles = ""
for f in FAMILIES:
    sw = [p for p in f["items"] if p["img"]][:4]
    tiles += f"""<a class="fam" href="{rel}{f['url']}"><span class="strip">{''.join(f'<img src="{rel}img/s/{p["code"]}.jpg" alt="" width="520" height="390" loading="lazy">' for p in sw)}</span>
<span class="ft"><b>{esc(f['name'])}</b><em>{len(f['items'])} finishes · {esc(', '.join(n2 for g2, n2 in f['groups'] if any(p['group'] == g2 for p in P)))}</em></span></a>"""
desc = f"All {total} KOINTEC architectural interior film finishes by material: wood, marble, metal, concrete, solid, soft matt, leather, glitter and flooring. UAE, KSA, Qatar."
graph = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": "KOINTEC Interior Film Finishes", "url": BASE_URL + "finishes/", "description": desc, "publisher": {"@id": ORG["@id"]},
     "hasPart": [{"@type": "CollectionPage", "name": f["h1"], "url": BASE_URL + f["url"]} for f in FAMILIES]}, ORG,
    {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Catalogue", "item": BASE_URL},
                                                   {"@type": "ListItem", "position": 2, "name": "Finishes", "item": BASE_URL + "finishes/"}]}]}
page_html = f"""{head('Interior Film Finishes by Material | KOINTEC Catalogue', desc, 'finishes/', [graph], rel=rel)}{CSS_LINK(rel)}
</head><body>
{site_header(rel, 'finishes')}
<main><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{rel}">Catalogue</a> › <span>Finishes</span></nav>
<div class="hero hero-solo"><div class="hero-t"><p class="eyebrow">KOINTEC 27/28 · {total} finishes · 9 materials</p>
<h1>KOINTEC Interior Film Finishes</h1>
<p class="lede">Every finish in the KOINTEC 27/28 architectural interior film catalogue, grouped by material. Open a material to see each finish with its product code, a swatch, a photo in an interior and a link to the product on interiorfilm.com.</p>
<div class="acts"><a class="b pri" href="{rel}">Open the flipbook</a><a class="b" href="{MAIN}/contact">Contact our team</a></div></div></div>
<div class="fams">{tiles}</div>
</div></main>
{site_footer(rel)}
</body></html>"""
os.makedirs(os.path.join(ROOT, "finishes"), exist_ok=True)
open(os.path.join(ROOT, "finishes", "index.html"), "w", encoding="utf-8").write(page_html)

# ---------------------------------------------------------------- flipbook (home)
tpl = open(os.path.join(ROOT, "tools", "flipbook.template.html"), encoding="utf-8").read()
desc = f"Browse all {total} KOINTEC architectural interior film finishes: wood, marble, metal, concrete, solid, leather and more. Made in Korea, supplied in the UAE, KSA and Qatar."
graph = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebSite", "@id": BASE_URL + "#site", "name": "KOINTEC Interior Film Catalogue", "url": BASE_URL, "publisher": {"@id": ORG["@id"]}},
    {"@type": "CollectionPage", "name": "KOINTEC Interior Film Catalogue 27/28", "url": BASE_URL, "description": desc, "isPartOf": {"@id": BASE_URL + "#site"},
     "primaryImageOfPage": BASE_URL + "img/cover.jpg",
     "hasPart": [{"@type": "CollectionPage", "name": f["h1"], "url": BASE_URL + f["url"]} for f in FAMILIES]}, ORG]}
h = head("KOINTEC Interior Film Catalogue 27/28 | 196 Finishes", desc, "", [graph], rel="")
h = h.replace("<!doctype html>\n<html lang=\"en\">\n<head>\n", "")
nos = '<noscript><div style="padding:24px;font-family:Manrope,sans-serif"><p>The flipbook needs JavaScript. Browse the same finishes as web pages:</p><ul>' + "".join(
    f'<li><a href="{f["url"]}">{esc(f["h1"])} ({len(f["items"])})</a></li>' for f in FAMILIES) + "</ul></div></noscript>"
book = {
    "products": [{k: p.get(k) for k in ("code", "group", "name", "desc", "img", "akind", "url", "page", "size", "brand")} for p in P],
    "fams": [dict(id=fid, name=fname, groups=[[g, COLS[g][0]] for g in cols]) for fid, fname, cols in BOOK_FAMS],
    "cols": {g: dict(name=v[0], light=v[1], bold=v[2], roll=v[3], intro=v[4]) for g, v in COLS.items()},
    "pages": PAGES, "tabs": TABS, "idxStart": IDX_START, "tocPage": 3,
    "famlink": {f["id"]: f["main"] for f in FAMILIES}, "apps": APPS_PAGE,
    "certs": CERTS, "install": INSTALL,
}
data = json.dumps(book, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = tpl.replace("__HEAD__", h).replace("__BOOK__", data).replace("__NOSCRIPT__", nos)
out = "<!doctype html>\n<html lang=\"en\">\n<head>\n" + out.replace("<div class=\"app\">", "</head>\n<body>\n<div class=\"app\">", 1) + "\n</body>\n</html>\n"
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
if "--artifact" in sys.argv:   # claude.ai artifact copy: fragment page, CDN script, no site links
    art = tpl.replace("__HEAD__", '<title>KOINTEC Catalogue 27/28</title>\n<meta name="claude:viewport-fit-sides" content="cover">').replace("__BOOK__", data).replace("__NOSCRIPT__", "")
    art = art.replace('<script src="assets/page-flip.browser.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>')
    art = re.sub(r'<a class="tbtn" href="finishes/".*?</a>\n', '', art, flags=re.S)
    open(sys.argv[sys.argv.index("--artifact") + 1], "w", encoding="utf-8").write(art)

# ---------------------------------------------------------------- sitemap, robots, 404
urls = [("", "1.0"), ("finishes/", "0.9")] + [(f["url"], "0.8") for f in FAMILIES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
for u, pr in urls:
    imgs = ""
    if u.startswith("finishes/") and u != "finishes/":
        f = next(f for f in FAMILIES if f["url"] == u)
        imgs = "".join(f"<image:image><image:loc>{BASE_URL}img/s/{p['code']}.jpg</image:loc></image:image>" for p in f["items"] if p["img"])
    sm += f"  <url><loc>{BASE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>{imgs}</url>\n"
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}sitemap.xml\n")
nf = f"""{head('Page not found | KOINTEC Interior Film Catalogue', 'This page is not in the KOINTEC catalogue.', '404.html', rel='/')}<link rel="stylesheet" href="/assets/site.css"><meta name="robots" content="noindex">
</head><body>{site_header('/', '')}<main><div class="wrap"><div class="hero hero-solo"><div class="hero-t"><h1>Page not found</h1>
<p class="lede">This page is not in the catalogue. Open the flipbook or browse finishes by material.</p>
<div class="acts"><a class="b pri" href="/">Open the flipbook</a><a class="b" href="/finishes/">All finishes</a></div></div></div></div></main>{site_footer('/')}</body></html>"""
open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(nf)
print(f"Built for {BASE_URL}: index.html, finishes/ (1 + {len(FAMILIES)} pages), sitemap.xml ({len(urls)} URLs), robots.txt, 404.html")
