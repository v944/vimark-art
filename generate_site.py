#!/usr/bin/env python3
"""Generate portfolio site inspired by tobiaskwan.com.
Top-level folders become menu sections.
Sub-folders become sub-menu items.
"""
import os
import html
import re
import random
import datetime
import configparser
import json
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


def get_avg_color(image_path):
    """Compute average color of an image for use as background.
    Ignores fully transparent pixels in RGBA images."""
    if not HAS_PILLOW:
        return ""
    try:
        with Image.open(image_path) as im:
            if im.mode == 'RGBA':
                # Sample down to 50x50 for speed, then average opaque pixels
                small = im.resize((50, 50), Image.LANCZOS)
                pixels = list(small.get_flattened_data())
                opaque = [(r, g, b) for r, g, b, a in pixels if a > 128]
                if opaque:
                    r = sum(c[0] for c in opaque) // len(opaque)
                    g = sum(c[1] for c in opaque) // len(opaque)
                    b = sum(c[2] for c in opaque) // len(opaque)
                    return f"#{r:02x}{g:02x}{b:02x}"
                return ""
            if im.mode == 'P':
                im = im.convert('RGB')
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im = im.resize((1, 1), Image.LANCZOS)
            r, g, b = im.getpixel((0, 0))
            return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return ""


ROOT = Path("d:/Concept_work/Vimark_art")
WEBSITE = ROOT
CAPTIONS_FILE = WEBSITE / "captions.txt"
THUMBS_DIR = WEBSITE / "thumbnails"
THUMB_SIZE = (600, 600)
THUMB_QUALITY = 85
PROJECTS_DIR = WEBSITE / "project"


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
            name = clean_name(p.stem)
            files.append({"src": rel, "name": name, "path": p, "mtime": p.stat().st_mtime})
    return files


def collect_hero_images():
    """Collect images from STRONG (preferred), HERO2, or HERO folder for hero banners."""
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    for folder_name in ("STRONG", "HERO2", "HERO"):
        hero_dir = ROOT / folder_name
        if not hero_dir.exists():
            continue
        files = []
        for p in sorted(hero_dir.iterdir()):
            if p.is_file() and p.suffix.lower() in exts:
                rel = os.path.relpath(p, WEBSITE).replace("\\", "/")
                name = clean_name(p.stem)
                files.append({"src": rel, "name": name, "path": p, "bgcolor": get_avg_color(p)})
        if files:
            print(f"Found {len(files)} hero image(s) in {folder_name}.")
            return files
    return []


def slugify(name):
    # Normalize various apostrophes and quotes
    s = name.lower()
    s = s.replace("'", "").replace("'", "").replace("'", "").replace("'", "")
    s = s.replace(" ", "-").replace("&", "and")
    # Remove any non-alphanumeric except hyphens
    s = re.sub(r'[^a-z0-9\-]+', '', s)
    s = re.sub(r'\-+', '-', s).strip('-')
    return s


def load_captions():
    """Load custom captions from captions.txt if it exists."""
    captions = {}
    if not CAPTIONS_FILE.exists():
        return captions
    for line in CAPTIONS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        path_part, caption = line.split('=', 1)
        path_part = path_part.strip()
        caption = caption.strip()
        if path_part and caption:
            captions[path_part] = caption
    return captions


def ensure_captions_file(items):
    """Create captions.txt template if it doesn't exist yet."""
    if CAPTIONS_FILE.exists():
        return
    lines = [
        "# Custom captions for portfolio images",
        "# Format: relative/path/to/image.jpg = Your custom caption",
        "# Lines starting with # are ignored. If an image is not listed, auto-caption is used.",
        "",
    ]
    for img in items:
        lines.append(f'{img["src"]} = {img["name"]}')
    CAPTIONS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated {CAPTIONS_FILE.name} — edit it to customize image captions.")


def human_label(name):
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.title()


def clean_name(stem):
    """Clean image filename into a human-readable caption."""
    s = stem
    # Remove duplicate extension if still present in stem
    s = re.sub(r'\.(jpg|jpeg|png|webp|gif)$', '', s, flags=re.IGNORECASE)
    # Remove leading numeric batch prefixes: __0001_, _0001_, etc.
    s = re.sub(r'^__?\d+[_\-]', '', s)
    # Remove view/size suffixes first (e.g. -fullview, -pre)
    s = re.sub(r'-(fullview|pre|414w-2x)$', '', s, flags=re.IGNORECASE)
    # Remove author suffixes like _by_vimark_d85g8w5
    s = re.sub(r'_by_[a-z0-9_]+$', '', s)
    # Replace separators with spaces
    s = s.replace('_', ' ').replace('-', ' ')
    # Remove zero-padded numeric tokens (0001, 0002...)
    s = re.sub(r'\b0+\d+\b', '', s)
    # Collapse extra spaces
    s = re.sub(r'\s+', ' ', s).strip()
    # Capitalize first letter
    if s:
        s = s[0].upper() + s[1:]
    return s


def extract_year(text):
    """Extract a 4-digit year from caption or filename text."""
    if not text:
        return 0
    match = re.search(r'\b(19|20)\d{2}\b', text)
    if match:
        return int(match.group(0))
    return 0


def extract_sort_index(stem):
    """Extract leading numeric index from filename stem (e.g. __0001_ -> 1)."""
    match = re.search(r'^__?(\d+)[_\-]', stem)
    if match:
        return int(match.group(1))
    return 999999


def ensure_thumbnail(original_path):
    """Generate a WebP thumbnail if it doesn't exist or is outdated."""
    rel = os.path.relpath(original_path, WEBSITE).replace("\\", "/")
    # Use .webp extension for thumbnails regardless of source format
    thumb_path = (THUMBS_DIR / rel).with_suffix('.webp')
    thumb_rel = os.path.relpath(thumb_path, WEBSITE).replace("\\", "/")
    if not HAS_PILLOW:
        return thumb_rel, "", ""

    thumb_path.parent.mkdir(parents=True, exist_ok=True)

    # If thumbnail exists and is newer than original, reuse it
    if thumb_path.exists() and thumb_path.stat().st_mtime >= original_path.stat().st_mtime:
        try:
            with Image.open(thumb_path) as im:
                w, h = im.size
            return thumb_rel, str(w), str(h)
        except Exception:
            pass  # regenerate if corrupted

    try:
        with Image.open(original_path) as im:
            # Convert palette/RGBA to RGB for WebP
            if im.mode in ('RGBA', 'P'):
                im_rgb = im.convert('RGB')
            else:
                im_rgb = im
            im_rgb.thumbnail(THUMB_SIZE, Image.LANCZOS)
            im_rgb.save(thumb_path, "WEBP", quality=THUMB_QUALITY, method=6)
            w, h = im_rgb.size
        return thumb_rel, str(w), str(h)
    except Exception as e:
        print(f"  Warning: could not thumbnail {rel}: {e}")
        return thumb_rel, "", ""


def load_projects():
    """Load project descriptions from projects.ini if it exists."""
    projects = {}
    ini_path = WEBSITE / "projects.ini"
    if not ini_path.exists():
        return projects
    cfg = configparser.ConfigParser()
    cfg.read(ini_path, encoding="utf-8")
    for section in cfg.sections():
        projects[section] = {
            "title": cfg.get(section, "title", fallback=section),
            "year": cfg.get(section, "year", fallback=""),
            "client": cfg.get(section, "client", fallback=""),
            "description": cfg.get(section, "description", fallback=""),
        }
    return projects


def ensure_projects_file(all_subfolders):
    """Create projects.ini template if it doesn't exist yet."""
    ini_path = WEBSITE / "projects.ini"
    if ini_path.exists():
        return
    cfg = configparser.ConfigParser()
    for sub_key, sub_info in all_subfolders.items():
        cfg.add_section(sub_key)
        cfg.set(sub_key, "title", sub_info["label"])
        cfg.set(sub_key, "year", "")
        cfg.set(sub_key, "client", "")
        cfg.set(sub_key, "description", "")
    with open(ini_path, "w", encoding="utf-8") as f:
        cfg.write(f)
    print(f"Generated {ini_path.name} — edit it to add project descriptions.")


def load_locale():
    """Load translations from locale.ini."""
    locale = {"en": {}, "ru": {}}
    ini_path = WEBSITE / "locale.ini"
    if not ini_path.exists():
        return locale
    cfg = configparser.ConfigParser()
    cfg.read(ini_path, encoding="utf-8")
    for section in cfg.sections():
        if section in locale:
            for key, value in cfg.items(section):
                locale[section][key] = value
    return locale


def build_lang(lang='en'):
    locale = load_locale()
    t = locale.get(lang, {})
    out_dir = WEBSITE if lang == 'en' else WEBSITE / "ru"
    out_dir.mkdir(exist_ok=True)
    base_index = "" if lang == 'en' else "../"
    base_project = "../" if lang == 'en' else "../../"
    year = datetime.date.today().year
    categories = {}
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name.startswith("_"):
            continue
        if entry.name.lower() in ("website", "thumbnails", "project", "hero", "hero2", "strong"):
            continue

        cat_key = slugify(entry.name)

        # Discover subfolders
        subfolders = {}
        for sub in sorted(entry.iterdir()):
            if sub.is_dir():
                sub_imgs = collect_images_from_path(os.path.join(entry.name, sub.name))
                if sub_imgs:
                    sub_slug = slugify(sub.name)
                    sub_key = f"{cat_key}-{sub_slug}"
                    subfolders[sub_key] = {
                        "label": t.get(sub_slug, human_label(sub.name)),
                        "images": sub_imgs,
                    }

        # Collect all images in category (including root files and all subfolders)
        all_cat_images = collect_images_from_path(entry.name)

        if not all_cat_images and not subfolders:
            continue

        categories[cat_key] = {
            "label": t.get(cat_key, human_label(entry.name)),
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

    # Load or create captions file
    captions = load_captions()
    ensure_captions_file(all_items)

    # Extract year and sort index for each image
    for img in all_items:
        caption = captions.get(img["src"], img["name"])
        img["year"] = extract_year(caption)
        img["sort_index"] = extract_sort_index(Path(img["path"]).stem)

    YEAR_FIRST_CATEGORIES = {"bookcover", "single"}

    def sort_key(img):
        cat = img.get("category", "")
        year = -img.get("year", 0)
        idx = img.get("sort_index", 999999)
        mtime = -img["mtime"]
        if cat in YEAR_FIRST_CATEGORIES:
            return (year, idx, mtime)
        return (0, idx, mtime)

    all_items.sort(key=sort_key)

    # Re-sort category and subfolder images to match global order
    for cat_key, info in categories.items():
        info["images"].sort(key=sort_key)
        for sub_key, sub_info in info["subfolders"].items():
            sub_info["images"].sort(key=sort_key)

    # Sort subfolders for year-first categories by year descending
    for cat_key, info in categories.items():
        if cat_key in YEAR_FIRST_CATEGORIES and info["subfolders"]:
            def _sub_year(item):
                parts = item[0].rsplit('-', 1)
                if len(parts) == 2 and parts[-1].isdigit():
                    return -int(parts[-1])
                return 0
            sorted_subs = dict(sorted(info["subfolders"].items(), key=_sub_year))
            info["subfolders"] = sorted_subs

    # Collect all subfolders flat map (after sorting)
    all_subfolders = {}
    for cat_key, info in categories.items():
        all_subfolders.update(info["subfolders"])

    # Load or create projects file
    projects = load_projects()
    ensure_projects_file(all_subfolders)

    # Collect HERO images for random banners
    hero_images = collect_hero_images()
    if hero_images:
        print(f"Found {len(hero_images)} HERO image(s) for random banners.")

    # Collect STRONG images for OG/social sharing
    strong_images = collect_images_from_path("STRONG")
    if strong_images:
        print(f"Found {len(strong_images)} STRONG image(s) for social preview.")
    og_strong = random.choice(strong_images)["src"] if strong_images else "Mitenkov600.jpg"

    # Generate thumbnails
    if HAS_PILLOW:
        print("Generating thumbnails...")
        THUMBS_DIR.mkdir(exist_ok=True)
        for img in all_items:
            thumb_rel, w, h = ensure_thumbnail(img["path"])
            img["thumb"] = thumb_rel
            img["width"] = w
            img["height"] = h
        print("Thumbnails done.")

    # No "Select" section — show all by default
    select_items = []
    select_set = set()

    def hero_html(items, base=""):
        if hero_images:
            hero = random.choice(hero_images)
            use_original = True
        elif items:
            hero = items[0]
            use_original = False
        else:
            return ""
        src = html.escape(base + hero["src"], quote=True)
        thumb = html.escape(base + hero.get("thumb", hero["src"]), quote=True)
        alt = html.escape(captions.get(hero["src"], hero["name"]), quote=True)
        img_src = src if use_original else thumb
        # Build pool of all STRONG images for client-side random switching
        hero_pool = []
        for img in strong_images:
            hero_pool.append({
                "src": html.escape(base + img.get("thumb", img["src"]), quote=True),
                "full": html.escape(base + img["src"], quote=True),
                "alt": html.escape(captions.get(img["src"], img["name"]), quote=True)
            })
        pool_json = html.escape(json.dumps(hero_pool), quote=True)
        return f'''<section class="hero" data-hero-pool="{pool_json}">
  <img src="{img_src}" data-full="{src}" alt="{alt}" loading="eager">
  <div class="hero-overlay"></div>
  <div class="hero-scroll-hint" onclick="document.getElementById('book-illustrations').scrollIntoView({{behavior:'smooth'}})">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
  </div>
</section>'''

    def project_card_html(key, label, images, base=""):
        if not images:
            return ""
        count = len(images)
        main = images[0]
        main_thumb = html.escape(base + main.get("thumb", main["src"]), quote=True)
        main_src = html.escape(base + main["src"], quote=True)
        main_alt = html.escape(captions.get(main["src"], main["name"]), quote=True)
        thumbs_html = ""
        transparent_gif = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        for img in images[1:4]:
            thumb = html.escape(base + img.get("thumb", img["src"]), quote=True)
            alt = html.escape(captions.get(img["src"], img["name"]), quote=True)
            thumbs_html += f'<img src="{thumb}" alt="{alt}" loading="lazy">'
        for _ in range(3 - len(images[1:4])):
            thumbs_html += f'<img src="{transparent_gif}" alt="" loading="lazy">'
        count_label = t.get("artworks", "artworks")
        return f'''<a href="{base}project/{key}.html" class="project-card">
  <div class="project-card-preview">
    <img src="{main_thumb}" data-full="{main_src}" alt="{main_alt}" class="project-card-main" loading="lazy">
    <div class="project-card-thumbs">{thumbs_html}</div>
  </div>
  <div class="project-card-info">
    <h3>{html.escape(label)}</h3>
    <span>{count} {count_label}</span>
  </div>
</a>'''

    def projects_sections_html(base=""):
        sections = []
        for cat_key, info in categories.items():
            cards = []
            if info["subfolders"]:
                for sub_key, sub_info in info["subfolders"].items():
                    proj_images = [img for img in all_items if img.get("subcategory") == sub_key]
                    card = project_card_html(sub_key, sub_info["label"], proj_images, base)
                    if card:
                        cards.append(card)
            else:
                proj_images = [img for img in all_items if img["category"] == cat_key]
                card = project_card_html(cat_key, info["label"], proj_images, base)
                if card:
                    cards.append(card)
            if cards:
                cards_str = "\n".join(cards)
                sections.append(f'<section class="projects-section" id="{cat_key}">\n  <h2>{html.escape(info["label"])}</h2>\n  <div class="projects-grid">\n    {cards_str}\n  </div>\n</section>')
        return "\n".join(sections)

    def gallery_html(items, base=""):
        lines = ['<div class="gallery-grid">']
        for img in items:
            src = html.escape(base + img["src"], quote=True)
            thumb = html.escape(base + img.get("thumb", img["src"]), quote=True)
            alt = html.escape(captions.get(img["src"], img["name"]), quote=True)
            w = img.get("width", "")
            h = img.get("height", "")
            dim_attr = f' width="{w}" height="{h}"' if w and h else ''
            lines.append(f'  <div class="gallery-item">')
            lines.append(f'    <img src="{thumb}" data-full="{src}" alt="{alt}" loading="lazy"{dim_attr}>')
            lines.append('  </div>')
        lines.append('</div>')
        return "\n".join(lines)

    def project_gallery_html(items, base=""):
        lines = ['<div class="gallery-grid">']
        for img in items:
            src = html.escape(base + img["src"], quote=True)
            thumb = html.escape(base + img.get("thumb", img["src"]), quote=True)
            alt = html.escape(captions.get(img["src"], img["name"]), quote=True)
            w = img.get("width", "")
            h = img.get("height", "")
            dim_attr = f' width="{w}" height="{h}"' if w and h else ''
            lines.append(f'  <div class="gallery-item">')
            lines.append(f'    <img src="{thumb}" data-full="{src}" alt="{alt}" loading="lazy"{dim_attr}>')
            lines.append('  </div>')
        lines.append('</div>')
        return "\n".join(lines)

    def build_project_page(sub_key, proj, items, base="../"):
        year = datetime.date.today().year
        title = html.escape(proj.get("title", sub_key))
        year = html.escape(proj.get("year", ""))
        client = html.escape(proj.get("client", ""))
        description = html.escape(proj.get("description", ""))
        og_image = html.escape(items[0]["src"], quote=True) if items else "Mitenkov600.jpg"

        meta_parts = [p for p in [year, client] if p]
        meta_html = f'<p class="project-meta">{" · ".join(meta_parts)}</p>' if meta_parts else ''
        desc_html = f'<p class="project-desc">{description}</p>' if description else ''

        social_html_project = social_html.replace('src="behance.png"', f'src="{base}behance.png"').replace('src="deviantart.png"', f'src="{base}deviantart.png"')

        project_nav = [
            '<nav class="main-nav">',
            '  <ul>',
        ]
        for key, info in categories.items():
            project_nav.append(f'    <li><a href="{base}index.html#{key}">{html.escape(info["label"])}</a></li>')
        project_nav.extend([
            f'    <li><a href="{base}index.html#about">{t.get("about", "About")}</a></li>',
            f'    <li><a href="{base}index.html#contact">{t.get("contact", "Contact")}</a></li>',
            '  </ul>',
            '</nav>',
        ])
        project_nav_html = "\n      ".join(project_nav)

        if hero_images:
            hero_img = random.choice(hero_images)
            use_original = True
        else:
            hero_img = items[0] if items else None
            use_original = False
        if hero_img:
            hero_thumb = html.escape(base + hero_img.get("thumb", hero_img["src"]), quote=True)
            hero_src = html.escape(base + hero_img["src"], quote=True)
            hero_alt = html.escape(captions.get(hero_img["src"], hero_img["name"]), quote=True)
            hero_display = hero_src if use_original else hero_thumb
            bg_color = hero_img.get("bgcolor", "")
            bg_style = f' style="background-color: {bg_color}"' if bg_color else ""
        else:
            hero_thumb = ""
            hero_src = ""
            hero_alt = ""
            hero_display = ""
            bg_style = ""

        page_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Max Mitenkov</title>
<meta name="description" content="{title} — {description or 'Portfolio project by Max Mitenkov'}">
<link rel="canonical" href="https://vimark.art/project/{sub_key}.html">
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="stylesheet" href="{base}style.css">
<link rel="icon" type="image/png" href="{base}vimark_logo.png">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vimark.art/project/{sub_key}.html">
<meta property="og:title" content="{title} · Max Mitenkov">
<meta property="og:description" content="{description or 'Portfolio project by Max Mitenkov'}">
<meta property="og:image" content="https://vimark.art/{og_image}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vimark.art/project/{sub_key}.html">
<meta property="twitter:title" content="{title} · Max Mitenkov">
<meta property="twitter:description" content="{description or 'Portfolio project by Max Mitenkov'}">
<meta property="twitter:image" content="https://vimark.art/{og_image}">

<!-- Google tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-6RBP7X7H88"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-6RBP7X7H88');
</script>

<!-- Yandex.Metrika -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{if (document.scripts[j].src === r) {{ return; }}}}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=109279162', 'ym');
    ym(109279162, 'init', {{ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/109279162" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
</head>
<body>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <img src="{base}Max Mitenkov.png" alt="Max Mitenkov" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
      {project_nav_html}
      {social_html_project}
      <a href="{base}index.html" class="logo-link"><img src="{base}vimark_logo.png" alt="Logo" style="width: 60px; margin-top: auto; margin-bottom: 100px; opacity: 0.9; align-self: center;"></a>
    </aside>

    <button class="mobile-toggle">{t.get('menu', 'Menu')}</button>

    <main id="main">
      <section class="project-hero"{bg_style}>
        <img src="{hero_display}" data-full="{hero_src}" alt="{hero_alt}" loading="eager">
      </section>
      <div class="project-header">
        <a href="{base}index.html" class="back-link">{t.get('back_to_portfolio', '← Back to portfolio')}</a>
        <h1>{title}</h1>
        {meta_html}
        {desc_html}
      </div>
      {project_gallery_html(items, base)}
    </main>
  </div>

  <div class="site-footer">
    <span><b>©</b> Max Mitenkov, {year}.</span>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){{var p=location.pathname.split('\\\\').join('/');var h=location.hash;var i=p.indexOf('/ru/')!==-1||p.indexOf('/ru/')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(i){{e.href=p.replace('/ru/','/')+h;r.href=p+h;}}else{{r.href=p.replace('/project/','/ru/project/').replace('/index.html','/ru/index.html')+h;e.href=p+h;}}if(i){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
  </div>

  <div id="lightbox">
    <button class="lightbox-close" aria-label="Close">×</button>
    <button class="lightbox-prev" aria-label="Previous image">‹</button>
    <img class="lightbox-img" src="" alt="">
    <button class="lightbox-next" aria-label="Next image">›</button>
    <div class="lightbox-caption"></div>
    <div class="lightbox-counter"></div>
  </div>

  <script src="{base}script.js"></script>
</body>
</html>
"""
        return page_content

    # Build nav with category anchors + About + Contact
    nav_lines = [
        '<nav class="main-nav">',
        '  <ul>',
    ]
    for key, info in categories.items():
        nav_lines.append(f'    <li><a href="#{key}">{html.escape(info["label"])}</a></li>')
    nav_lines.extend([
        f'    <li><a href="#about">{t.get("about", "About")}</a></li>',
        f'    <li><a href="#contact">{t.get("contact", "Contact")}</a></li>',
        '  </ul>',
        '</nav>',
    ])

    social_html = '''<div class="social-links">
      <a href="mailto:hello@vimark.art" aria-label="Email"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
      <a href="https://www.facebook.com/maks.vimark/" aria-label="Facebook"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
      <a href="https://www.linkedin.com/in/maxim-mitenkov-06192940/" aria-label="LinkedIn"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
      <a href="https://www.instagram.com/vimark_art/" aria-label="Instagram"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
      <a href="https://www.behance.net/vimark" aria-label="Behance"><img src="behance.png" alt="Behance" class="social-icon"></a>
      <a href="https://www.deviantart.com/vimark" aria-label="DeviantArt"><img src="deviantart.png" alt="DeviantArt" class="social-icon"></a>
    </div>'''

    # Select up to 6 random STRONG works for About gallery
    about_gallery_imgs = random.sample(strong_images, min(6, len(strong_images))) if strong_images else []
    about_gallery_items = ""
    for img in about_gallery_imgs:
        img_src = html.escape(base_index + img.get("thumb", img["src"]), quote=True)
        img_full = html.escape(base_index + img["src"], quote=True)
        img_alt = html.escape(captions.get(img["src"], img["name"]), quote=True)
        about_gallery_items += f'<div class="gallery-item"><img src="{img_src}" data-full="{img_full}" alt="{img_alt}" loading="lazy"></div>'

    about_gallery_html = f'''<div class="about-section about-gallery">
              <h2>{t.get('portfolio', 'Portfolio')}</h2>
              <div class="about-gallery-grid">{about_gallery_items}</div>
            </div>
''' if about_gallery_items else ""

    about_html = f'''      <section id="about" class="hidden">
        <div class="about-container">
          <div class="about-photo">
            <img src="{base_index}Mitenkov600.jpg" alt="Max Mitenkov">
          </div>
          <div class="about-content">
            <h1>{t.get('about', 'About')}</h1>
            <hr class="about-divider">
            <p class="about-intro">{t.get('about_intro_v2', "I'm Max Mitenkov, an award-winning illustrator and concept artist with 12+ years in the entertainment industry. My work spans book covers, AAA game environments, and NFT character design — created with Photoshop, ZBrush, and Unreal Engine 5. I've collaborated with studios in Dubai (Apex Digital), Los Angeles (ICVR), and Minsk (Lunas Pro). Currently open to freelance and full-time opportunities.")}</p>
            <p class="about-tools"><strong>{t.get('about_tools_label', 'Tools')}:</strong> {t.get('about_tools', 'Photoshop · ZBrush · Houdini · UE5 · Substance')}</p>

            <hr class="about-divider">
            <h2>{t.get('about_experience', 'Selected Experience')}</h2>
            <div class="experience-list">
              <p>Senior Concept Artist — Apex Digital VC, Dubai <span class="job-date">(2022–Present)</span></p>
              <p>3D Artist — ICVR, Los Angeles <span class="job-date">(2021–2022)</span></p>
              <p>3D Artist — Lunas pro, Minsk <span class="job-date">(2016–2021)</span></p>
            </div>

            <hr class="about-divider">
            <h2>{t.get('about_contact_title', "Let's work together")}</h2>
            <div class="about-contact">
              <p><a href="mailto:hello@vimark.art">hello@vimark.art</a></p>
              <p>(+375) 29 653-43-82 · <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener">Telegram: @MaxMitenkov</a></p>
              <p><a href="{base_index}2025_Resume_eng_concept.pdf" target="_blank" rel="noopener" class="cv-link">{t.get('about_cv', 'Download CV (PDF)')}</a></p>
            </div>

            {about_gallery_html}
          </div>
        </div>
      </section>'''

    contact_html = f'''      <section id="contact" class="hidden">
        <div class="contact-container">
          <h1>{t.get('contact', 'Contact')}</h1>
          <form action="https://api.web3forms.com/submit" method="POST" class="contact-form">
            <input type="hidden" name="access_key" value="211a1ef5-25ea-4d59-9b9c-33b5f9126f21">
            <input type="hidden" name="redirect" value="https://vimark.art/thanks.html">
            <input type="hidden" name="subject" value="New message from vimark.art">
            <div class="form-group">
              <label for="email">{t.get('email_label', 'Email')} <span class="required">({t.get('required', 'required')})</span></label>
              <input type="email" id="email" name="email" required>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="first-name">{t.get('first_name_label', 'First Name')} <span class="required">({t.get('required', 'required')})</span></label>
                <input type="text" id="first-name" name="first-name" required>
              </div>
              <div class="form-group">
                <label for="last-name">{t.get('last_name_label', 'Last Name')} <span class="required">({t.get('required', 'required')})</span></label>
                <input type="text" id="last-name" name="last-name" required>
              </div>
            </div>
            <div class="form-group">
              <label for="message">{t.get('message_label', 'Message')}</label>
              <textarea id="message" name="message" rows="6" required></textarea>
            </div>
            <button type="submit" class="submit-btn">{t.get('submit', 'Submit')}</button>
          </form>
        </div>
      </section>'''

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Max Mitenkov · {t.get('job_title', 'Illustrator · Concept Artist')}</title>
<meta name="description" content="{t.get('meta_description', 'Portfolio of Max Mitenkov, illustrator and concept artist with 12+ years of experience in games, books, and NFT projects.')}">
<link rel="canonical" href="https://vimark.art/">
<link rel="stylesheet" href="{base_index}style.css">
<link rel="icon" type="image/png" href="{base_index}vimark_logo.png">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vimark.art/">
<meta property="og:title" content="Max Mitenkov · Illustrator · Concept Artist">
<meta property="og:description" content="Gallery of illustrations, concept art, and book covers by Max Mitenkov.">
<meta property="og:image" content="https://vimark.art/{og_strong}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vimark.art/">
<meta property="twitter:title" content="Max Mitenkov · Illustrator · Concept Artist">
<meta property="twitter:description" content="Gallery of illustrations, concept art, and book covers by Max Mitenkov.">
<meta property="twitter:image" content="https://vimark.art/{og_strong}">

<!-- Schema.org -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Max Mitenkov",
  "jobTitle": "Illustrator and Concept Artist",
  "url": "https://vimark.art/",
  "image": "https://vimark.art/{og_strong}",
  "sameAs": [
    "https://www.behance.net/vimark",
    "https://www.linkedin.com/in/maxim-mitenkov-06192940/",
    "https://www.instagram.com/vimark_art/",
    "https://www.deviantart.com/vimark",
    "https://www.facebook.com/maks.vimark/"
  ],
  "description": "Illustrator and concept designer with over 12 years of professional experience. Worked on projects for studios in Belarus, the USA, and the UAE."
}}
</script>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-6RBP7X7H88"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-6RBP7X7H88');
</script>

<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){{
        m[i]=m[i]||function(){{
            (m[i].a=m[i].a||[]).push(arguments)
        }};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {{
            if (document.scripts[j].src === r) {{ return; }}
        }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    }})(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=109279162', 'ym');

    ym(109279162, 'init', {{
        ssr:true,
        webvisor:true,
        clickmap:true,
        ecommerce:"dataLayer",
        referrer: document.referrer,
        url: location.href,
        accurateTrackBounce:true,
        trackLinks:true
    }});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/109279162" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
</head>
<body>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <img src="{base_index}Max Mitenkov.png" alt="Max Mitenkov" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
      {"\n      ".join(nav_lines)}
      {social_html.replace('src=\"behance.png\"', f'src=\"{base_index}behance.png\"').replace('src=\"deviantart.png\"', f'src=\"{base_index}deviantart.png\"')}
      <a href="{base_index}index.html" class="logo-link"><img src="{base_index}vimark_logo.png" alt="Logo" style="width: 60px; margin-top: auto; margin-bottom: 100px; opacity: 0.9; align-self: center;"></a>
    </aside>

    <button class="mobile-toggle">Menu</button>

    <main id="main">
      {hero_html(all_items, base_index)}
      {projects_sections_html(base_index)}
{about_html}
{contact_html}
    </main>
  </div>

  <div class="site-footer">
    <span><b>©</b> Max Mitenkov, {year}.</span>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){{var p=location.pathname.split('\\\\').join('/');var h=location.hash;var i=p.indexOf('/ru/')!==-1||p.indexOf('/ru/')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(i){{e.href=p.replace('/ru/','/')+h;r.href=p+h;}}else{{r.href=p.replace('/project/','/ru/project/').replace('/index.html','/ru/index.html')+h;e.href=p+h;}}if(i){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
  </div>

  <div id="lightbox">
    <button class="lightbox-close">×</button>
    <button class="lightbox-prev">‹</button>
    <img class="lightbox-img" src="" alt="">
    <button class="lightbox-next">›</button>
    <div class="lightbox-caption"></div>
    <div class="lightbox-counter"></div>
  </div>

  <script src="{base_index}script.js"></script>
</body>
</html>
"""

    (out_dir / "index.html").write_text(html_content, encoding="utf-8")
    print(f"Generated {lang}/index.html with {len(all_items)} images.")
    for key, info in categories.items():
        subs = ", ".join(info["subfolders"].keys()) if info["subfolders"] else "none"
        print(f"  - {key}: {len(info['images'])} images (subfolders: {subs})")
    print(f"Select preview: {len(select_items)} images.")

    # Generate project pages for subfolders and standalone categories
    proj_dir = out_dir / "project"
    proj_dir.mkdir(exist_ok=True)
    generated_projects = 0
    # Subfolder projects
    for sub_key, sub_info in all_subfolders.items():
        proj_images = [img for img in all_items if img.get("subcategory") == sub_key]
        if not proj_images:
            continue
        proj = projects.get(sub_key, {
            "title": sub_info["label"],
            "year": "",
            "client": "",
            "description": "",
        })
        proj_base = "../../" if base_index else "../"
        page_html = build_project_page(sub_key, proj, proj_images, base=proj_base)
        (proj_dir / f"{sub_key}.html").write_text(page_html, encoding="utf-8")
        generated_projects += 1
    # Standalone categories (no subfolders)
    for cat_key, info in categories.items():
        if info["subfolders"]:
            continue
        proj_images = info["images"]
        if not proj_images:
            continue
        proj = projects.get(cat_key, {
            "title": info["label"],
            "year": "",
            "client": "",
            "description": "",
        })
        proj_base = "../../" if base_index else "../"
        page_html = build_project_page(cat_key, proj, proj_images, base=proj_base)
        (proj_dir / f"{cat_key}.html").write_text(page_html, encoding="utf-8")
        generated_projects += 1
    print(f"Generated {generated_projects} {lang}/project pages.")

    # Generate sitemap.xml
    today = datetime.date.today().isoformat()
    urls = [
        ("https://vimark.art/", "1.0"),
        (f"https://vimark.art/{base_index}index.html", "1.0"),
    ]
    for sub_key in projects.keys():
        urls.append((f"https://vimark.art/project/{sub_key}.html", "0.8"))
    for cat_key, info in categories.items():
        if not info["subfolders"]:
            urls.append((f"https://vimark.art/project/{cat_key}.html", "0.8"))
    url_entries = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        for loc, priority in urls
    )
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{url_entries}
</urlset>"""
    (out_dir / "sitemap.xml").write_text(sitemap_content, encoding="utf-8")
    print(f"Generated {lang}/sitemap.xml")


if __name__ == "__main__":
    build_lang('en')
    build_lang('ru')
