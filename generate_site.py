#!/usr/bin/env python3
"""Generate portfolio site inspired by tobiaskwan.com.
Top-level folders become menu sections.
Sub-folders become sub-menu items.
"""
import os
import html
import re
from pathlib import Path

ROOT = Path("d:/Concept_work/Vimark_art")
WEBSITE = ROOT

def collect_images_from_path(rel_path):
    """Collect image files from a relative path recursively, sorted."""
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    path = ROOT / rel_path
    if not path.exists():
        return []
    files = []
    for p in sorted(path.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts:
            rel = os.path.relpath(p, WEBSITE).replace("\\", "/")
            name = p.stem.replace("__", "").replace("_", " ").strip()
            files.append({"src": rel, "name": name, "path": p})
    return files

def slugify(name):
    # Normalize various apostrophes and quotes
    s = name.lower()
    s = s.replace("'", "").replace("'", "").replace("'", "").replace("'", "")
    s = s.replace(" ", "-").replace("&", "and")
    # Remove any non-alphanumeric except hyphens
    s = re.sub(r'[^a-z0-9\-]+', '', s)
    s = re.sub(r'\-+', '-', s).strip('-')
    return s

def human_label(name):
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.title()

def build():
    categories = {}
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name.startswith("_"):
            continue
        if entry.name == "website":
            continue

        # Discover subfolders
        subfolders = {}
        for sub in sorted(entry.iterdir()):
            if sub.is_dir():
                sub_imgs = collect_images_from_path(os.path.join(entry.name, sub.name))
                if sub_imgs:
                    sub_key = slugify(sub.name)
                    subfolders[sub_key] = {
                        "label": human_label(sub.name),
                        "images": sub_imgs,
                    }

        # Collect all images in category (including root files and all subfolders)
        all_cat_images = collect_images_from_path(entry.name)

        if not all_cat_images and not subfolders:
            continue

        cat_key = slugify(entry.name)
        categories[cat_key] = {
            "label": human_label(entry.name),
            "folder": entry.name,
            "images": all_cat_images,
            "subfolders": subfolders,
        }

    # Attach category/subcategory keys to each image
    all_items = []
    for cat_key, info in categories.items():
        for img in info["images"]:
            img["category"] = cat_key
            img["subcategory"] = ""
            # Determine which subfolder this image belongs to (compare by src)
            for sub_key, sub_info in info["subfolders"].items():
                if any(img["src"] == s["src"] for s in sub_info["images"]):
                    img["subcategory"] = sub_key
                    break
            all_items.append(img)

    # No "Select" section — show all by default
    select_items = []
    select_set = set()

    def gallery_html(items):
        lines = ['<div class="gallery-grid">']
        for img in items:
            src = html.escape(img["src"], quote=True)
            alt = html.escape(img["name"], quote=True)
            cat = html.escape(img["category"], quote=True)
            sub = html.escape(img.get("subcategory", ""), quote=True)
            lines.append(f'  <div class="gallery-item" data-category="{cat}" data-subcategory="{sub}">')
            lines.append(f'    <img src="{src}" data-full="{src}" alt="{alt}" loading="lazy">')
            lines.append('  </div>')
        lines.append('</div>')
        return "\n".join(lines)

    # Build nav
    nav_lines = [
        '<nav class="main-nav">',
        '  <ul>',
    ]
    for key, info in categories.items():
        if info["subfolders"]:
            nav_lines.append(f'    <li class="folder">')
            nav_lines.append(f'      <a href="#" data-category="{key}">{html.escape(info["label"])}</a>')
            nav_lines.append('      <ul>')
            for sub_key, sub_info in info["subfolders"].items():
                nav_lines.append(f'        <li><a href="#" data-category="{key}" data-subcategory="{sub_key}">{html.escape(sub_info["label"])}</a></li>')
            nav_lines.append('      </ul>')
            nav_lines.append('    </li>')
        else:
            nav_lines.append(f'    <li><a href="#" data-category="{key}">{html.escape(info["label"])}</a></li>')
    nav_lines.extend([
        '  </ul>',
        '</nav>',
    ])

    social_html = '''<div class="social-links">
      <a href="mailto:vimarkart@gmail.com" aria-label="Email"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
      <a href="https://www.facebook.com/maks.vimark/" aria-label="Facebook"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
      <a href="https://www.linkedin.com/in/maxim-mitenkov-06192940/" aria-label="LinkedIn"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
      <a href="https://www.instagram.com/vimark_art/" aria-label="Instagram"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
      <a href="https://www.behance.net/vimark" aria-label="Behance"><img src="behance.png" alt="Behance" class="social-icon"></a>
      <a href="https://www.deviantart.com/vimark" aria-label="DeviantArt"><img src="deviantart.png" alt="DeviantArt" class="social-icon"></a>
    </div>'''

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Max Mitenkov · Illustrator · Concept Artist</title>
<link rel="stylesheet" href="style.css">
<link rel="icon" type="image/png" href="vimark_logo.png">
</head>
<body>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <img src="Max Mitenkov.png" alt="Max Mitenkov" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
      {"\n      ".join(nav_lines)}
      {social_html}
      <img src="vimark_logo.png" alt="Logo" style="width: 60px; margin-top: auto; margin-bottom: 100px; opacity: 0.9; align-self: center;">
    </aside>

    <button class="mobile-toggle">Menu</button>

    <main id="main">
      {gallery_html(all_items)}
    </main>
  </div>

  <div class="site-footer"><b>©</b> Max Mitenkov.</div>

  <div id="lightbox">
    <button class="lightbox-close">×</button>
    <button class="lightbox-prev">‹</button>
    <img class="lightbox-img" src="" alt="">
    <button class="lightbox-next">›</button>
    <div class="lightbox-caption"></div>
    <div class="lightbox-counter"></div>
  </div>

  <script src="script.js"></script>
</body>
</html>
"""

    (WEBSITE / "index.html").write_text(html_content, encoding="utf-8")
    print(f"Generated index.html with {len(all_items)} images.")
    for key, info in categories.items():
        subs = ", ".join(info["subfolders"].keys()) if info["subfolders"] else "none"
        print(f"  - {key}: {len(info['images'])} images (subfolders: {subs})")
    print(f"Select preview: {len(select_items)} images.")

if __name__ == "__main__":
    build()
