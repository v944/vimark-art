# Work Log

## Book Cover Year Card Randomization

Randomized the displayed covers for each year card in the Book Covers section on the homepage.

### Behavior
- Each year card (2026, 2025, 2024) now shows a random main cover + 3 random thumbnails from that year's pool on every page load.
- All 4 images per card are distinct and selected independently per year.
- Static fallback content remains intact for no-JS browsers.

### Implementation
- Added `data-cover-pool` JSON attribute to each year card in `index.html` and `ru/index.html` listing all covers for that year.
- Added `randomizeBookCoverYearCards()` to `script.js` (runs only on the homepage):
  - Parses each card's cover pool.
  - Shuffles the pool and picks the first 4 entries.
  - Updates `.project-card-main` `src`, `data-full`, and `alt`.
  - Updates the 3 `.project-card-thumbs img` elements' `src` and `alt`.

### Files changed
- `index.html`
- `ru/index.html`
- `script.js`

---

## Homepage Card Randomization + Khton Cover Update

### Homepage randomization (`index.html`, `ru/index.html`, `script.js`)
- Added hidden card pools (`.projects-grid-pool`) for **Book Illustrations** and **Visual Stories → Series**.
- `script.js` now randomly selects **3 cards** from the full pool on every page load:
  - Book Illustrations: 8 cards total (all from `book-illustrations.html`)
  - Visual Stories: 8 Series cards total (all from `visual-stories.html#series`)
- Non-Series Visual Stories cards remain excluded from rotation.

### Khton za okolitsey / Хтонь за околицей cover
- File `BookCover/2026/__0004_01_Khton_2026.jpg` was already in the 2026 collection.
- Added localized display titles:
  - EN: `Khton za okolitsey`
  - RU: `Хтонь за околицей`
- Regenerated thumbnails, project art pages, and sitemaps.
- Removed earlier mistaken `Book Illustrations/MIF/` additions and related config entries.

### Files changed
- `index.html`, `ru/index.html`
- `script.js`
- `captions.txt`, `display_titles.txt`
- `generate_site.py` outputs: `project/`, `ru/project/`, `thumbnails/`, `sitemap.xml`, `image-sitemap.xml`, `pinterest/pins.json`

---

## Humanizer: AI Pattern Removal (Blog + Case Study)

Applied `blader/humanizer` skill (v2.8.0, 33 patterns) to all blog articles and the Hoëbeke case study.

### Changes made to .md sources (blog/*.md, case_study_hoebeke.md):
- **Em dashes (—) removed:** ~350 instances across 5 blog articles + case study
  - Replaced with colons, commas, periods, or restructured sentences
- **En dashes (–) in ranges:** all replaced with regular hyphens (3-5, $100-300)
- **AI vocabulary removed:**
  - `ключевой` → `главный` / dropped
  - `key` → dropped (e.g. "key research" → "research")
  - `critical` → dropped ("critical requirement" → "requirement")
  - `great` → `classic` ("great sci-fi illustration" → "classic sci-fi illustration")
  - `flagship` → dropped
  - `demonstrates` → `shows`
  - `carries expectations` → `comes with expectations`
- **-ing fake depth:** simplified to active voice
- **Generic positive conclusions:** replaced with factual statements
- **Signposting removed:** "Let's dive in", "В этом кейсе", "Почему это работает?"
- **Rule of three:** trimmed where forced
- **Boldface overuse:** reduced
- **Curly quotes:** replaced with straight quotes
- **"not just...but..." constructions:** rephrased

### Files changed: 18 files, 712 insertions, 738 deletions
- 5 blog .md files (with .bak.md originals preserved, gitignored)
- 5 EN blog .html + 5 RU blog .html (regenerated via blog_convert.py)
- 2 case study .html (EN + RU, hand-edited text)
- .gitignore (added *.bak.md, *.humanized.md)

---

## Website Changes

### Phase A: ImageObject + ProfessionalService schema (generate_site.py, index.html, about.html)
- A.4: Add `ImageObject` JSON-LD after `VisualArtwork` on all art pages (192 en + 192 ru)
- C.2: Expand `Person` → `["Person", "ProfessionalService"]` with `hasOfferCatalog`, `areaServed`, `knowsAbout`
- Files: `generate_site.py`, `index.html`, `about.html`, all `project/art/*.html`, `ru/project/art/*.html`

### Services pages (services.html, ru/services.html)
- Created EN/RU services pages with Service schema (BreadcrumbList + Service + hasOfferCatalog + HowTo + FAQPage)
- Added Full-Color Interior Art block ($500+)
- Updated all static page navigation, footer, hreflang JS mapping
- Added to `generate_site.py` landing_pages, sitemap.xml
- Payment FAQ: bank transfer, MoneyGram, crypto (USDT, BTC, ETH)
- CSS: `.service-card`, `.process-step`, `.pricing-table`, `.faq-item`; CTA black color, no underline

---

## Website Changes

### Pricing Update (index.html, ru/index.html)
Updated the Pricing block in the About section:

| Service | Price |
|---------|-------|
| Illustration | from $500 |
| Book cover | from $700 |
| Character design | from $700 |
| Environment concept | from $800 |

Files modified:
- `index.html`
- `ru/index.html`

---

## Desert Giants WebGL Scene (WIP)

**Status:** Work in progress. Not yet linked from the main portfolio.
**Location:** `scenes/desert-giants/`

### Assets
- **Replaced GLB:** `assets/desert_scene.glb` — user-edited version with original desert mesh removed
- **Added normal map:** `assets/Normal_4K_Rippled_Sand.PNG` — 4K rippled sand normal map
- **Removed billboards:** `assets/giant_billboard_01.png`, `assets/giant_billboard_02.png`
- **HDR environment:** `assets/desert_sunset_2k.hdr` (unchanged)

### Scene Implementation
- **Infinite desert plane:** `PlaneGeometry(1000, 1000)` with `MeshStandardMaterial`
  - Color: dark brown `0x5a3d20`
  - Roughness: 0.9
  - Normal map tiling: 120
  - Normal scale: 1.0
  - Shadows enabled
- **Ground fog:** 5 shader-based `PlaneGeometry(120, 120)` layers
  - Opacity: 0.15
  - Spread along Z: -45 to +40
  - Drift speed: 0.05
  - Color: warm brown `vec3(0.55, 0.45, 0.30)`
- **Sand particles:** 1200 `Points` drifting along +X with reset loop
- **Camera:**
  - FOV: 75°
  - Position: `(-55, 1.2, 12)`
  - Target: `(-32, 3, 0)`
  - Low angle, behind the shepherds, framing all giants
- **Lighting:**
  - Sun: `DirectionalLight(0xffaa66, 1.5)` at `(50, 80, 30)`
  - Fill: `DirectionalLight(0x6688ff, 0.3)` at `(-30, 40, -20)`
  - Ambient: `AmbientLight(0x404040, 0.4)`
- **Controls:** OrbitControls with damping, min/max distance, max polar angle

### Dev Tools
- **test.js** — Playwright script for automated screenshot capture
  - Serves local server on `127.0.0.1:9090`
  - Waits 10 seconds for scene load
  - Saves `test-result.png` and `test-logs.json`
- **open-browser.js** — Helper to open browser for local testing

### Documentation
- `__UE_web/desert_giants_webgl_brief.md` — Updated to reflect current asset list (no billboards)

---

*Last updated: 2026-07-11*
