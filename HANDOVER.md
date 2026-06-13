# Handover: vimark.art restructure

**Date:** 2026-06-13  
**Branch:** `master`  
**Last commit:** `20ebbe2 Add Vercel redirects and noindex headers for site restructure`  
**Local server:** `python3 -m http.server 8000`

---

## What was done today

### Visual Stories → Series structure (point 2)
- **`visual-stories.html` and `ru/visual-stories.html`** — Series section expanded from 1 to 8 series cards:
  - Biological Deviations (7), Faceless (10), Geologyst (8), Nemirum (5), The Symbol Of Faith (5), Wanderer (7), Winter (7), Vegetation (10)
  - Same thumbnail layout as on `comic.html`, with 1 main + 3 thumbnails per card
  - JSON-LD `hasPart` updated with all 8 series on both EN and RU pages
- Standalone gallery (genre tabs) unchanged.

### Index teaser mode (point 1)
- **`index.html` and `ru/index.html`** — all 5 sections rewritten to **teaser mode v2**:
  - Book Illustrations: 3 featured cards + "View all" → `book-illustrations.html`
  - Book Covers: 2 featured cards + "View all" → `book-covers.html`
  - Visual Stories (ex-Comic): 3 featured cards + "View all" → `visual-stories.html`
  - Personal: 2 featured cards (no hub page)
  - Living Illustrations: 1 card (unchanged)
- Filter bar labels updated: "Comic" → "Visual Stories" (EN), "Комиксы" → "Визуальные истории" (RU)
- Section headings standardized: "Book Cover" → "Book Covers", "Обложки" → "Обложки книг"
- **`style.css`**: added `.section-cta` styles.

---

## Active issues / next steps

1. ✅ **Visual Stories → Series** — DONE
2. ✅ **Index teaser mode** — DONE
3. ✅ **Footer consistency (medium priority)** — DONE
   - Copied the flat footer structure from `visual-stories.html` to all hub pages.
   - Updated EN: `index.html`, `book-illustrations.html`, `about.html`, `contact.html`, `reviews.html`, `faq.html`, `case-studies/hoebeke-sci-fi-series.html`.
   - Updated RU: `ru/index.html`, `ru/book-illustrations.html`, `ru/about.html`, `ru/contact.html`, `ru/reviews.html`, `ru/faq.html`, `ru/case-studies/hoebeke-sci-fi-series.html`.
   - Verified: each page has exactly one `footer-links`, `sticky-contact`, and `script.js` reference.
4. **Commit & deploy**
   - Many files are modified/untracked (see list below).
   - Before deploy: run local checks, then commit and push to `master` (Vercel auto-deploys).
5. **Old `/project/...` pages**
   - Leave as-is per “no move” rule. They keep old breadcrumbs/navigation.
6. **Cache reminder for Visual Stories**
   - If tabs still appear stuck in a real browser, hard-refresh (`Ctrl+F5`) / incognito. The code itself is correct.

---

## Key files

| Page / asset | Path |
|--------------|------|
| EN Visual Stories | `visual-stories.html` |
| RU Visual Stories | `ru/visual-stories.html` |
| EN Book Covers | `book-covers.html` |
| RU Book Covers | `ru/book-covers.html` |
| EN About | `about.html` |
| RU About | `ru/about.html` |
| EN Case Study | `case-studies/hoebeke-sci-fi-series.html` |
| RU Case Study | `ru/case-studies/hoebeke-sci-fi-series.html` |
| Styles | `style.css` |
| Scripts | `script.js` |
| Redirects / headers | `vercel.json` |
| Sitemap | `sitemap.xml` |

---

## Working environment

- **Project root:** `d:\Concept_work\Vimark_art`
- **Preview URL:** `http://localhost:8000/`
- **Restart server if needed:**
  ```bash
  cd "d:\Concept_work\Vimark_art" && python3 -m http.server 8000
  ```

---

## Quick verification commands

```bash
# Tab switching smoke test (requires selenium + Chrome)
python3 - <<'PY'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
opts = Options(); opts.add_argument('--headless'); opts.add_argument('--no-sandbox')
d = webdriver.Chrome(options=opts)
d.get('http://localhost:8000/visual-stories.html')
[t.click() for t in d.find_elements(By.CSS_SELECTOR, '.genre-tab')]
for p in d.find_elements(By.CSS_SELECTOR, '.genre-panel'):
    print(p.get_attribute('id'), p.value_of_css_property('display'))
d.quit()
PY
```

---

## Git status snapshot

Modified:

```
.gitignore
404.html
book-illustrations.html
contact.html
index.html
reviews.html
ru/book-illustrations.html
ru/contact.html
ru/index.html
ru/reviews.html
sitemap.xml
style.css
vercel.json
```

Untracked (new):

```
about.html
book-covers.html
case-studies/
images/
ru/about.html
ru/book-covers.html
ru/case-studies/
ru/visual-stories.html
visual-stories.html
```

---

## Notes for next session

- **Footer audit** — ensure flat footer with `footer-links` is on all remaining pages (book-illustrations.html, contact.html, reviews.html, their RU variants).
- Before any deploy, verify the Visual Stories tabs one more time in a normal browser window.
- Do not edit `/project/...` pages unless explicitly asked.
