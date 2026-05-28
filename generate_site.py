#!/usr/bin/env python3
"""Generate portfolio site inspired by tobiaskwan.com.
Top-level folders become menu sections.
Sub-folders become sub-menu items.
"""
import os
import html
import urllib.parse
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
PINTEREST_DIR = WEBSITE / "pinterest"
PINTEREST_IMAGES_DIR = PINTEREST_DIR / "images"
PINTEREST_PINS_PATH = PINTEREST_DIR / "pins.json"
PINTEREST_IMAGE_SIZE = (1200, 1800)

PINTEREST_BOARD_MAP = {
    "bookcover": "Book Cover Design",
    "book-illustrations": "Dark Fantasy Illustration",
    "comic": "Comic Art & Sequential",
    "personal": "Maxim Mitenkov Portfolio",
    "character-design": "Character Design & Concept Art",
    "board-game": "Game Art & Illustration",
    "matte-painting": "Environment & Matte Painting",
}

PINTEREST_CATEGORY_TAGS = {
    "bookcover": ["#bookcover", "#coverdesign", "#bookillustration"],
    "book-illustrations": ["#bookillustration", "#darkart", "#fantasyart"],
    "comic": ["#comicart", "#sequentialart", "#darkart"],
    "personal": ["#personalart", "#darkart", "#fantasyart"],
}


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
    """Collect images from HERO2 or HERO folder for hero banners."""
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    for folder_name in ("HERO2", "HERO"):
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


def ensure_pinterest_image(original_path, project_id):
    """Generate a 2:3 vertical Pinterest image (1200x1800) from the first project image."""
    if not HAS_PILLOW:
        return None
    PINTEREST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    dest = PINTEREST_IMAGES_DIR / f"{project_id}.webp"

    # Reuse if up to date
    if dest.exists() and dest.stat().st_mtime >= original_path.stat().st_mtime:
        return f"pinterest/images/{project_id}.webp"

    try:
        with Image.open(original_path) as im:
            if im.mode in ('RGBA', 'P'):
                im_rgb = im.convert('RGB')
            else:
                im_rgb = im
            w, h = im_rgb.size
            target_ratio = 2 / 3  # width / height
            current_ratio = w / h
            if current_ratio > target_ratio:
                new_w = int(h * target_ratio)
                left = (w - new_w) // 2
                im_cropped = im_rgb.crop((left, 0, left + new_w, h))
            else:
                new_h = int(w / target_ratio)
                top = (h - new_h) // 2
                im_cropped = im_rgb.crop((0, top, w, top + new_h))
            im_final = im_cropped.resize(PINTEREST_IMAGE_SIZE, Image.LANCZOS)
            im_final.save(dest, "WEBP", quality=90, method=6)
        return f"pinterest/images/{project_id}.webp"
    except Exception as e:
        print(f"  Warning: could not create Pinterest image for {project_id}: {e}")
        return None


def build_pinterest_pin(project_id, sub_info_or_label, proj, images, pinterest_rel, cat_key):
    if isinstance(sub_info_or_label, dict):
        label = sub_info_or_label.get("label", project_id)
    else:
        label = sub_info_or_label
    title = proj.get("title", label)
    client = proj.get("client", "")
    description = proj.get("description", "")
    board = PINTEREST_BOARD_MAP.get(cat_key, "Maxim Mitenkov Portfolio")
    alt_text = f"{title} — {description[:120] if description else 'Digital painting'} by Maxim Mitenkov"

    cat_hashtags = PINTEREST_CATEGORY_TAGS.get(cat_key, ["#illustration", "#artwork"])
    hashtags = list(dict.fromkeys(cat_hashtags + ["#digitalpainting", "#maximmitenkov", "#vimarkart"]))

    desc_parts = [title]
    if client:
        desc_parts.append(f"for {client}")
    if description:
        short_desc = description.strip()
        if len(short_desc) > 200:
            short_desc = short_desc[:197].rsplit(' ', 1)[0] + "..."
        desc_parts.append(short_desc)
    desc_parts.append("Digital painting by Maxim Mitenkov.")

    pin_description = ". ".join(desc_parts) + "\n\n" + " ".join(hashtags)
    image_url = (
        f"https://vimark.art/{pinterest_rel}"
        if pinterest_rel
        else (f"https://vimark.art/{images[0]['src']}" if images else "https://vimark.art/Mitenkov600.jpg")
    )
    link = f"https://www.vimark.art/project/{project_id}.html"

    return {
        "pin_id": project_id,
        "status": "ready_to_publish",
        "board": board,
        "image_url": image_url,
        "link": link,
        "title": f"{title} · Maxim Mitenkov",
        "description": pin_description,
        "alt_text": alt_text,
        "tags": [h.lstrip("#") for h in hashtags],
        "date_created": datetime.date.today().isoformat(),
        "date_published": None,
    }


def update_pins_json(new_pins):
    PINTEREST_DIR.mkdir(parents=True, exist_ok=True)
    existing_map = {}
    if PINTEREST_PINS_PATH.exists():
        try:
            existing = json.loads(PINTEREST_PINS_PATH.read_text(encoding="utf-8"))
            existing_map = {p["pin_id"]: p for p in existing}
        except Exception:
            pass
    for pin in new_pins:
        old = existing_map.get(pin["pin_id"])
        if old and old.get("status") == "published":
            pin["status"] = "published"
            pin["date_published"] = old.get("date_published")
            pin["pinterest_pin_id"] = old.get("pinterest_pin_id")
    PINTEREST_PINS_PATH.write_text(json.dumps(new_pins, indent=2, ensure_ascii=False), encoding="utf-8")


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


STAR_SVG = '<svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'

GAUGE_IMG_MAP = {
    'Professionalism': 'gauge-professionalism.png',
    'Quality': 'gauge-quality.png',
    'Value': 'gauge-value.png',
    'Responsiveness': 'gauge-responsiveness.png',
    'Профессионализм': 'gauge-professionalism.png',
    'Качество': 'gauge-quality.png',
    'Ценность': 'gauge-value.png',
    'Отзывчивость': 'gauge-responsiveness.png',
}

REEDSY_LOGO = '<svg class="reedsy-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 24" width="80" height="24" fill="currentColor"><text x="2" y="18" font-family="Georgia, serif" font-size="20" font-style="italic">reedsy</text></svg>'


def render_reviews_bar(base, t):
    reviews_bar_stars = STAR_SVG * 5
    reviews_bar_categories = [
        (t.get('professionalism', 'Professionalism'), 5),
        (t.get('quality', 'Quality'), 5),
        (t.get('value', 'Value'), 5),
        (t.get('responsiveness', 'Responsiveness'), 5),
    ]
    reviews_bar_cats_html = ""
    for cat_label, cat_rating in reviews_bar_categories:
        cat_img = GAUGE_IMG_MAP.get(cat_label, 'gauge-bg.png')
        reviews_bar_cats_html += f'<div class="reviews-bar-category"><div class="reviews-gauge"><img src="{base}thumbnails/reviews/{cat_img}" alt="{html.escape(cat_label)}" class="reviews-gauge-img"></div></div>'
    return f'''<section class="reviews-bar">
      <div class="reviews-bar-summary">
        <a href="{base}reviews.html" class="reviews-bar-count-link"><span class="reviews-bar-count">71 {t.get('reviews', 'Reviews').lower()}</span></a>
        <span class="reviews-bar-on">on <a href="https://reedsy.com/freelancers/maxim-m" target="_blank" rel="noopener">{REEDSY_LOGO}</a></span>
        <div class="reviews-bar-stars">{reviews_bar_stars}</div>
      </div>
      <a href="{base}reviews.html" class="reviews-bar-categories-link">
        <div class="reviews-bar-categories">{reviews_bar_cats_html}</div>
      </a>
    </section>'''


def render_reviews_hero(base, t):
    reviews_bar_stars = STAR_SVG * 5
    gauge_imgs = ""
    for label in ['Professionalism', 'Quality', 'Value', 'Responsiveness']:
        cat_img = GAUGE_IMG_MAP.get(label, 'gauge-bg.png')
        gauge_imgs += f'<img src="{base}thumbnails/reviews/{cat_img}" alt="{html.escape(label)}" class="hero-reviews-gauge">'
    return f'''<div class="hero-reviews">
  <div class="hero-reviews-gauges">{gauge_imgs}</div>
  <div class="hero-reviews-summary">
    <a href="{base}reviews.html" class="hero-reviews-count-link"><span class="hero-reviews-count">71 {t.get('reviews', 'Reviews').lower()}</span></a>
    <span class="hero-reviews-on">on <a href="https://reedsy.com/freelancers/maxim-m" target="_blank" rel="noopener">{REEDSY_LOGO}</a></span>
    <div class="hero-reviews-stars">{reviews_bar_stars}</div>
  </div>
</div>'''


def load_reviews():
    rev_path = WEBSITE / "Reedsy" / "reviews.json"
    if rev_path.exists():
        return json.loads(rev_path.read_text(encoding="utf-8"))
    return {"reviews": []}


def load_art_reviews():
    """Load art-to-review mapping from art_reviews.ini."""
    reviews = {}
    ini_path = WEBSITE / "art_reviews.ini"
    if not ini_path.exists():
        return reviews
    cfg = configparser.ConfigParser()
    cfg.read(ini_path, encoding="utf-8")
    for section in cfg.sections():
        reviewer = cfg.get(section, "reviewer", fallback="")
        date = cfg.get(section, "date", fallback="")
        text = cfg.get(section, "text", fallback="")
        if reviewer and text:
            reviews[section] = {
                "reviewer": reviewer,
                "date": date,
                "text": text,
            }
    return reviews


def find_wip_images(art_slug, project_folder):
    """Find WIP images for a specific artwork in the project/wip folder."""
    wip_dir = ROOT / project_folder / "wip"
    if not wip_dir.exists():
        return []
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    wip_images = []
    for p in sorted(wip_dir.iterdir()):
        if p.is_file() and p.suffix.lower() in exts:
            if art_slug.lower() in p.stem.lower():
                rel = os.path.relpath(p, WEBSITE).replace("\\", "/")
                wip_images.append({"src": rel, "name": clean_name(p.stem)})
    return wip_images


def build_lang(lang='en'):
    locale = load_locale()
    t = locale.get(lang, {})
    out_dir = WEBSITE if lang == 'en' else WEBSITE / "ru"
    out_dir.mkdir(exist_ok=True)
    base_index = "" if lang == 'en' else "../"
    base_project = "../" if lang == 'en' else "../../"
    year = datetime.date.today().year
    lang_attr = 'en' if lang == 'en' else 'ru'
    canonical_root = 'https://vimark.art/' if lang == 'en' else 'https://vimark.art/ru/'
    hero_name = html.escape(t.get('hero_name', 'Max Mitenkov'))
    reviews_data = load_reviews()
    categories = {}
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name.startswith("_"):
            continue
        if entry.name.lower() in ("website", "thumbnails", "project", "hero", "hero2", "strong", "reedsy", "pinterest"):
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

    YEAR_FIRST_CATEGORIES = {"bookcover"}

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

    # Custom order for personal subfolders: Recent → Growth → Early
    if "personal" in categories and categories["personal"]["subfolders"]:
        personal_order = {"personal-recent-work": 0, "personal-professional-growth": 1, "personal-early-work": 2}
        sorted_personal = dict(sorted(
            categories["personal"]["subfolders"].items(),
            key=lambda x: personal_order.get(x[0], 99)
        ))
        categories["personal"]["subfolders"] = sorted_personal

    # Collect all subfolders flat map (after sorting)
    all_subfolders = {}
    for cat_key, info in categories.items():
        all_subfolders.update(info["subfolders"])

    # Load or create projects file
    projects = load_projects()
    ensure_projects_file(all_subfolders)

    # Generate Pinterest images and pins registry
    pinterest_pins = []
    if HAS_PILLOW:
        print("Generating Pinterest images...")
        PINTEREST_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for sub_key, sub_info in all_subfolders.items():
        proj_images = [img for img in all_items if img.get("subcategory") == sub_key]
        if not proj_images:
            continue
        proj = projects.get(sub_key, {"title": sub_info["label"], "year": "", "client": "", "description": ""})
        cat_key = None
        for ck, ci in categories.items():
            if sub_key in ci.get("subfolders", {}):
                cat_key = ck
                break
        pinterest_rel = ensure_pinterest_image(proj_images[0]["path"], sub_key) if HAS_PILLOW and proj_images else None
        pinterest_pins.append(build_pinterest_pin(sub_key, sub_info, proj, proj_images, pinterest_rel, cat_key))

    for cat_key, info in categories.items():
        if info["subfolders"]:
            continue
        proj_images = info["images"]
        if not proj_images:
            continue
        proj = projects.get(cat_key, {"title": info["label"], "year": "", "client": "", "description": ""})
        pinterest_rel = ensure_pinterest_image(proj_images[0]["path"], cat_key) if HAS_PILLOW and proj_images else None
        pinterest_pins.append(build_pinterest_pin(cat_key, info["label"], proj, proj_images, pinterest_rel, cat_key))

    update_pins_json(pinterest_pins)
    print(f"Updated pinterest/pins.json with {len(pinterest_pins)} pins.")

    # Collect HERO images for random banners
    hero_images = collect_hero_images()
    if hero_images:
        print(f"Found {len(hero_images)} HERO image(s) for random banners.")

    # Collect STRONG images for OG/social sharing
    strong_images = collect_images_from_path("STRONG")
    if strong_images:
        print(f"Found {len(strong_images)} STRONG image(s) for social preview.")
        if HAS_PILLOW:
            for img in strong_images:
                thumb_rel, w, h = ensure_thumbnail(img["path"])
                img["thumb"] = thumb_rel
                img["width"] = w
                img["height"] = h
    og_strong = random.choice(strong_images) if strong_images else None
    og_strong_src = html.escape(og_strong.get("thumb", og_strong["src"]) if og_strong else "Mitenkov600.jpg", quote=True)
    og_strong_width = html.escape(og_strong.get("width", "600"), quote=True) if og_strong else "600"
    og_strong_height = html.escape(og_strong.get("height", "600"), quote=True) if og_strong else "600"

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

    def hero_html(items, base="", pool=None, reviews_hero=""):
        banner_pool = pool if pool is not None else hero_images
        if banner_pool:
            hero = random.choice(banner_pool)
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
        switch_pool = strong_images if strong_images else hero_images
        for img in switch_pool:
            hero_pool.append({
                "src": html.escape(base + img["src"], quote=True),
                "full": html.escape(base + img["src"], quote=True),
                "alt": html.escape(captions.get(img["src"], img["name"]), quote=True)
            })
        pool_json = html.escape(json.dumps(hero_pool), quote=True)
        hero_title = t.get('hero_name', 'Max Mitenkov')
        hero_sub = t.get('job_title', 'Illustrator · Concept Artist')
        hero_cta = t.get('view_portfolio', 'View Portfolio')
        return f'''<section class="hero" data-hero-pool="{pool_json}">
  <img src="{img_src}" data-full="{src}" alt="{alt}" loading="eager" fetchpriority="high">
  <div class="hero-overlay">
    {reviews_hero}
    <h1>{hero_title}</h1>
    <p class="hero-subtitle">{hero_sub}</p>
    <a href="#book-illustrations" class="hero-cta">{hero_cta}</a>
  </div>
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
    <div class="project-card-overlay">
      <span class="overlay-title">{html.escape(label)}</span>
      <span class="overlay-count">{count} {count_label}</span>
    </div>
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
            year = img.get("year", "")
            year_meta = f'<meta itemprop="dateCreated" content="{year}">' if year else ''
            w = img.get("width", "")
            h = img.get("height", "")
            dim_attr = f' width="{w}" height="{h}"' if w and h else ''
            lines.append(f'  <figure class="gallery-item" itemscope itemtype="https://schema.org/VisualArtwork">')
            lines.append(f'    <img src="{thumb}" data-full="{src}" alt="{alt}" loading="lazy"{dim_attr} itemprop="image">')
            lines.append(f'    {year_meta}')
            lines.append(f'    <figcaption itemprop="name">{alt}</figcaption>')
            lines.append('  </figure>')
        lines.append('</div>')
        return "\n".join(lines)

    def project_gallery_html(items, base=""):
        lines = ['<div class="gallery-grid">']
        for img in items:
            src = html.escape(base + img["src"], quote=True)
            thumb = html.escape(base + img.get("thumb", img["src"]), quote=True)
            alt = html.escape(captions.get(img["src"], img["name"]), quote=True)
            year = img.get("year", "")
            year_meta = f'<meta itemprop="dateCreated" content="{year}">' if year else ''
            w = img.get("width", "")
            h = img.get("height", "")
            dim_attr = f' width="{w}" height="{h}"' if w and h else ''
            art_slug = slugify(captions.get(img["src"], img["name"]))
            art_href = f"art/{art_slug}.html"
            lines.append(f'  <a href="{art_href}" class="gallery-item" itemscope itemtype="https://schema.org/VisualArtwork">')
            lines.append(f'    <img src="{thumb}" alt="{alt}" loading="lazy"{dim_attr} itemprop="image">')
            lines.append(f'    {year_meta}')
            lines.append(f'    <figcaption itemprop="name">{alt}</figcaption>')
            lines.append('  </a>')
        lines.append('</div>')
        return "\n".join(lines)

    def build_project_page(sub_key, proj, items, base="../"):
        page_lang = 'ru' if lang == 'ru' else 'en'
        page_canonical = f"https://vimark.art/ru/project/{sub_key}.html" if page_lang == 'ru' else f"https://vimark.art/project/{sub_key}.html"
        page_hreflang = f'''<!-- hreflang -->
<link rel="alternate" hreflang="en" href="https://vimark.art/project/{sub_key}.html" />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/project/{sub_key}.html" />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/project/{sub_key}.html" />'''
        year = datetime.date.today().year
        title = html.escape(proj.get("title", sub_key))
        hero_name = html.escape(t.get('hero_name', 'Max Mitenkov'))
        year = html.escape(proj.get("year", ""))
        client = html.escape(proj.get("client", ""))
        description = html.escape(proj.get("description", ""))
        first_item = items[0] if items else None
        og_image = html.escape(first_item.get("thumb", first_item["src"]), quote=True) if first_item else "Mitenkov600.jpg"
        og_image_width = html.escape(first_item.get("width", "600"), quote=True) if first_item else "600"
        og_image_height = html.escape(first_item.get("height", "600"), quote=True) if first_item else "600"

        # Breadcrumb data
        cat_key = None
        cat_label = "Portfolio"
        for ck, ci in categories.items():
            if sub_key in ci.get("subfolders", {}):
                cat_key = ck
                cat_label = ci["label"]
                break
        breadcrumb_json = json.dumps({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Portfolio", "item": "https://vimark.art/"},
                {"@type": "ListItem", "position": 2, "name": cat_label, "item": f"https://vimark.art/#{cat_key}" if cat_key else "https://vimark.art/"},
                {"@type": "ListItem", "position": 3, "name": title, "item": page_canonical}
            ]
        }, ensure_ascii=False)

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
            f'    <li><a href="{base}reviews.html">{t.get("reviews", "Reviews")}</a></li>',
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

        cta_text = t.get('project_cta_text', 'Interested in something similar?')
        cta_btn = t.get('discuss_project', 'Discuss a project')
        project_cta_html = f'''<div class="project-cta">
        <p>{cta_text}</p>
        <a href="{base}index.html#contact" class="hero-cta">{cta_btn}</a>
      </div>'''

        back_href = f"{base}index.html#{cat_key}" if cat_key else f"{base}index.html"

        page_content = f"""<!DOCTYPE html>
<html lang="{page_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · {hero_name}</title>
<meta name="description" content="{title} — {description or 'Portfolio project by Max Mitenkov'}">
<link rel="canonical" href="{page_canonical}">
{page_hreflang}
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="stylesheet" href="{base}style.css">
<link rel="icon" type="image/png" href="{base}vimark_logo.png">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vimark.art/project/{sub_key}.html">
<meta property="og:title" content="{title} · {hero_name}">
<meta property="og:description" content="{description or 'Portfolio project by Max Mitenkov'}">
<meta property="og:image" content="https://vimark.art/{og_image}">
<meta property="og:image:width" content="{og_image_width}">
<meta property="og:image:height" content="{og_image_height}">
<link rel="image_src" href="https://vimark.art/{og_image}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vimark.art/project/{sub_key}.html">
<meta property="twitter:title" content="{title} · {hero_name}">
<meta property="twitter:description" content="{description or 'Portfolio project by Max Mitenkov'}">
<meta property="twitter:image" content="https://vimark.art/{og_image}">

<!-- Pinterest Rich Pins -->
<meta name="pinterest-rich-pin" content="true">
<meta property="article:published_time" content="{year or datetime.date.today().year}-01-01">

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
<!-- BreadcrumbList -->
<script type="application/ld+json">
{breadcrumb_json}
</script>
</head>
<body>
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
        <img src="{base}Max Mitenkov.png" alt="{hero_name}" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
        {project_nav_html}
      </header>
      {social_html_project}
      {commissions_html}
      <a href="{base}index.html" class="logo-link"><img src="{base}vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>

    <button class="mobile-toggle">{t.get('menu', 'Menu')}</button>

    <main id="main">
      <section class="project-hero"{bg_style}>
        <img src="{hero_display}" data-full="{hero_src}" alt="{hero_alt}" loading="eager" fetchpriority="high">
      </section>
      <div class="project-header">
        <a href="{back_href}" class="back-link">{t.get('back_to_portfolio', '← Back to portfolio')}</a>
        <h1>{title}</h1>
        {meta_html}
        {desc_html}
      </div>
      {project_gallery_html(items, base)}
      {project_cta_html}
    </main>
  </div>

  <footer class="site-footer">
    <span><b>©</b> {hero_name}, {year}.</span>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){{var p=location.pathname.split('\\\\').join('/');var h=location.hash;if(p==='/'||p==='')p='/index.html';var i=p.indexOf('/ru/')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(i){{e.href=p.replace('/ru/','/')+h;r.href=p+h;}}else{{r.href=p.replace('/project/','/ru/project/').replace('/index.html','/ru/index.html').replace('/reviews.html','/ru/reviews.html')+h;e.href=p+h;}}if(i){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
  </footer>

  {sticky_contact_html}
  <button id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top">↑</button>
  <script src="{base}script.js"></script>
</body>
</html>
"""
        return page_content

    def build_art_page(art, proj, review, wip_images, base="../../"):
        page_lang = 'ru' if lang == 'ru' else 'en'
        art_slug = slugify(captions.get(art["src"], art["name"]))
        art_name = html.escape(captions.get(art["src"], art["name"]))
        art_src = html.escape(base + art["src"], quote=True)
        hero_name = html.escape(t.get('hero_name', 'Max Mitenkov'))
        year = html.escape(proj.get("year", ""))
        title = html.escape(proj.get("title", ""))
        cat_key = art.get("category", "")
        cat_label = t.get(cat_key, human_label(cat_key))
        back_href = f"{base}project/{art.get('subcategory', cat_key)}.html"
        og_image = html.escape(base + art.get("thumb", art["src"]), quote=True)
        og_image_width = html.escape(art.get("width", "600"), quote=True)
        og_image_height = html.escape(art.get("height", "600"), quote=True)
        page_canonical = f"https://vimark.art/project/art/{art_slug}.html"
        page_hreflang = f'''<!-- hreflang -->
<link rel="alternate" hreflang="en" href="https://vimark.art/project/art/{art_slug}.html" />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/project/art/{art_slug}.html" />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/project/art/{art_slug}.html" />'''
        breadcrumb_json = json.dumps({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Portfolio", "item": "https://vimark.art/"},
                {"@type": "ListItem", "position": 2, "name": cat_label, "item": f"https://vimark.art/#{cat_key}"},
                {"@type": "ListItem", "position": 3, "name": title, "item": back_href.replace(base, "https://vimark.art/")},
                {"@type": "ListItem", "position": 4, "name": art_name, "item": page_canonical}
            ]
        }, ensure_ascii=False)
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
            f'    <li><a href="{base}reviews.html">{t.get("reviews", "Reviews")}</a></li>',
            '  </ul>',
            '</nav>',
        ])
        project_nav_html = "\n      ".join(project_nav)
        review_html = ""
        if review:
            reviewer = html.escape(review['reviewer'])
            initials = reviewer[0] if reviewer else 'R'
            # Find reviewer photo from reviews.json
            rev_photo = ""
            for rev in load_reviews().get("reviews", []):
                if rev.get("name") == review['reviewer']:
                    rev_photo = rev.get("photo", "")
                    break
            if rev_photo:
                avatar_html = f'<img src="{base}{html.escape(rev_photo)}" alt="{reviewer}" class="review-card-avatar" loading="lazy">'
            else:
                avatar_html = f'<div class="review-card-avatar review-avatar-default"><span>{initials}</span></div>'
            stars = '<svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>' * 5
            date_str = html.escape(review['date']) if review.get('date') else ''
            review_html = f'''<article class="review-card">
  <div class="review-card-header">
    {avatar_html}
    <div class="review-card-meta">
      <span class="review-card-name">{reviewer}</span>
      <span class="review-card-date">{date_str}</span>
    </div>
  </div>
  <div class="review-card-stars">{stars}</div>
  <div class="review-card-text"><p>{html.escape(review['text'])}</p></div>
</article>'''
        wip_html = ""
        if wip_images:
            wip_slides = "\n".join(
                f'      <div class="wip-slide"><img src="{base}{html.escape(w["src"])}" alt="{html.escape(w["name"])}" loading="lazy"><div class="wip-label">{html.escape(w["name"])}</div></div>'
                for w in wip_images
            )
            wip_html = f'''<div class="wip-section">
      <h3>Process</h3>
      <div class="wip-slider">
{wip_slides}
      </div>
    </div>'''
        cta_text = t.get('project_cta_text', 'Interested in something similar?')
        cta_btn = t.get('discuss_project', 'Discuss a project')
        return f"""<!DOCTYPE html>
<html lang="{page_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{art_name} · {hero_name}</title>
<meta name="description" content="{art_name} — {title} by {hero_name}">
<link rel="canonical" href="{page_canonical}">
{page_hreflang}
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="stylesheet" href="{base}style.css">
<link rel="icon" type="image/png" href="{base}vimark_logo.png">
<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:url" content="{page_canonical}">
<meta property="og:title" content="{art_name} · {hero_name}">
<meta property="og:description" content="{art_name} — {title} by {hero_name}">
<meta property="og:image" content="https://vimark.art/{og_image}">
<meta property="og:image:width" content="{og_image_width}">
<meta property="og:image:height" content="{og_image_height}">
<link rel="image_src" href="https://vimark.art/{og_image}">
<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="{page_canonical}">
<meta property="twitter:title" content="{art_name} · {hero_name}">
<meta property="twitter:description" content="{art_name} — {title} by {hero_name}">
<meta property="twitter:image" content="https://vimark.art/{og_image}">
<!-- Pinterest Rich Pins -->
<meta name="pinterest-rich-pin" content="true">
<meta property="article:published_time" content="{year or datetime.date.today().year}-01-01">
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
<!-- BreadcrumbList -->
<script type="application/ld+json">
{breadcrumb_json}
</script>
</head>
<body>
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
        <img src="{base}Max Mitenkov.png" alt="{hero_name}" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
        {project_nav_html}
      </header>
      {social_html_project}
      {commissions_html}
      <a href="{base}index.html" class="logo-link"><img src="{base}vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>
    <button class="mobile-toggle">{t.get('menu', 'Menu')}</button>
    <main id="main">
      <div class="art-header">
        <a href="{back_href}" class="back-link">← Back to project</a>
        <h1>{art_name}</h1>
        <p class="art-meta">{title}{' · ' + year if year else ''}</p>
      </div>
      <section class="art-hero">
        <img src="{art_src}" alt="{art_name}" loading="eager" fetchpriority="high">
      </section>
      {review_html}
      {wip_html}
      <div class="project-cta">
        <p>{cta_text}</p>
        <a href="{base}index.html#contact" class="hero-cta">{cta_btn}</a>
      </div>
    </main>
  </div>
  <footer class="site-footer">
    <span><b>©</b> {hero_name}, {year}.</span>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){{var p=location.pathname.split('\\\\').join('/');var h=location.hash;if(p==='/'||p==='')p='/index.html';var i=p.indexOf('/ru/')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(i){{e.href=p.replace('/ru/','/')+h;r.href=p+h;}}else{{r.href=p.replace('/project/','/ru/project/').replace('/index.html','/ru/index.html').replace('/reviews.html','/ru/reviews.html')+h;e.href=p+h;}}if(i){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
  </footer>
  {sticky_contact_html}
  <button id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top">↑</button>
  <script src="{base}script.js"></script>
</body>
</html>
"""

    def build_category_page(cat_key, info, base=""):
        page_lang = 'ru' if lang == 'ru' else 'en'
        cat_label = html.escape(info["label"])
        cat_canonical = f"https://vimark.art/{cat_key}.html" if page_lang == 'en' else f"https://vimark.art/ru/{cat_key}.html"
        page_hreflang = f'''<!-- hreflang -->
<link rel="alternate" hreflang="en" href="https://vimark.art/{cat_key}.html" />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/{cat_key}.html" />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/{cat_key}.html" />'''
        breadcrumb_json = json.dumps({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Portfolio", "item": "https://vimark.art/"},
                {"@type": "ListItem", "position": 2, "name": cat_label, "item": cat_canonical}
            ]
        }, ensure_ascii=False)
        # Build cards
        cards = []
        if info["subfolders"]:
            for sub_key, sub_info in info["subfolders"].items():
                proj_images = [img for img in all_items if img.get("subcategory") == sub_key]
                card = project_card_html(sub_key, sub_info["label"], proj_images, base)
                if card:
                    cards.append(card)
        else:
            proj_images = [img for img in all_items if img["category"] == cat_key]
            card = project_card_html(cat_key, cat_label, proj_images, base)
            if card:
                cards.append(card)
        cards_str = "\n".join(cards) if cards else ""
        meta_desc = f"{cat_label} — portfolio works by {hero_name}."
        # Category nav
        cat_nav_lines = [
            '<nav class="main-nav">',
            '  <ul>',
        ]
        for key, cinfo in categories.items():
            if key == cat_key:
                cat_nav_lines.append(f'    <li><a href="{base}index.html#{key}">{html.escape(cinfo["label"])}</a></li>')
            else:
                cat_nav_lines.append(f'    <li><a href="{base}{key}.html">{html.escape(cinfo["label"])}</a></li>')
        cat_nav_lines.extend([
            f'    <li><a href="{base}index.html#about">{t.get("about", "About")}</a></li>',
            f'    <li><a href="{base}index.html#contact">{t.get("contact", "Contact")}</a></li>',
            '  </ul>',
            '</nav>',
        ])
        cat_nav_html = "\n      ".join(cat_nav_lines)
        social_html_cat = social_html.replace('src="behance.png"', f'src="{base}behance.png"').replace('src="deviantart.png"', f'src="{base}deviantart.png"')
        year_num = datetime.date.today().year
        return f"""<!DOCTYPE html>
<html lang="{page_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cat_label} · {hero_name}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{cat_canonical}">
{page_hreflang}
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="stylesheet" href="{base}style.css">
<link rel="icon" type="image/png" href="{base}vimark_logo.png">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="{cat_canonical}">
<meta property="og:title" content="{cat_label} · {hero_name}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://vimark.art/{og_strong_src}">
<meta property="og:image:width" content="{og_strong_width}">
<meta property="og:image:height" content="{og_strong_height}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="{cat_canonical}">
<meta property="twitter:title" content="{cat_label} · {hero_name}">
<meta property="twitter:description" content="{meta_desc}">
<meta property="twitter:image" content="https://vimark.art/{og_strong_src}">

<!-- BreadcrumbList -->
<script type="application/ld+json">
{breadcrumb_json}
</script>

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
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
        <img src="{base}Max Mitenkov.png" alt="{hero_name}" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
        {cat_nav_html}
      </header>
      {social_html_cat}
      {commissions_html}
      <a href="{base}index.html" class="logo-link"><img src="{base}vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>

    <button class="mobile-toggle">{t.get('menu', 'Menu')}</button>

    <main id="main">
      <section class="category-page">
        <h1>{cat_label}</h1>
        <div class="projects-grid">
          {cards_str}
        </div>
      </section>
    </main>
  </div>

  <footer class="site-footer">
    <span><b>©</b> {hero_name}, {year_num}.</span>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){{var p=location.pathname.split('\\\\').join('/');var h=location.hash;var cat='{cat_key}.html';var isRu=p.indexOf('/ru/')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(isRu){{e.href='/'+cat+h;r.href='/ru/'+cat+h;}}else{{r.href='/ru/'+cat+h;e.href='/'+cat+h;}}if(isRu){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
  </footer>

  <div id="lightbox">
    <button class="lightbox-close" aria-label="Close">×</button>
    <button class="lightbox-prev" aria-label="Previous image">‹</button>
    <img class="lightbox-img" src="" alt="">
    <button class="lightbox-next" aria-label="Next image">›</button>
    <div class="lightbox-caption"></div>
    <div class="lightbox-counter"></div>
  </div>

  {sticky_contact_html}
  <button id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top">↑</button>
  <script src="{base}script.js"></script>
</body>
</html>
"""

    def build_reviews_page(base=""):
        page_lang = 'ru' if lang == 'ru' else 'en'
        reviews_canonical = f"https://vimark.art/reviews.html" if page_lang == 'en' else f"https://vimark.art/ru/reviews.html"
        page_hreflang = f'''<!-- hreflang -->
<link rel="alternate" hreflang="en" href="https://vimark.art/reviews.html" />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/reviews.html" />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/reviews.html" />'''
        breadcrumb_json = json.dumps({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Portfolio", "item": "https://vimark.art/"},
                {"@type": "ListItem", "position": 2, "name": t.get('reviews', 'Reviews'), "item": reviews_canonical}
            ]
        }, ensure_ascii=False)
        if page_lang == 'ru':
            reviews_title_text = f"71 проверенных отзыва на Reedsy · {hero_name} · Иллюстратор и концепт-художник"
            meta_desc = f"Читайте 71 проверенный отзыв с 5 звёздами от клиентов Reedsy, которые нанимали {hero_name}. Оценка 5/5 за профессионализм, качество, ценность и отзывчивость."
            reviews_h1_text = "Featured reviews"
            reviews_subtitle_text = "Оценка 5/5 за профессионализм, качество, ценность и отзывчивость"
        else:
            reviews_title_text = f"71 Verified Reedsy Reviews · {hero_name} · Illustrator & Concept Artist"
            meta_desc = f"Read 71 verified 5-star reviews from Reedsy clients who hired {hero_name} for book covers, illustrations, and concept art. Rated 5/5 for professionalism, quality, value, and responsiveness."
            reviews_h1_text = "Featured reviews"
            reviews_subtitle_text = "Rated 5/5 for professionalism, quality, value, and responsiveness"

        # Reviews nav (same as project nav but with Reviews link active)
        reviews_nav = [
            '<nav class="main-nav">',
            '  <ul>',
        ]
        for key, info in categories.items():
            reviews_nav.append(f'    <li><a href="{base}index.html#{key}">{html.escape(info["label"])}</a></li>')
        reviews_nav.extend([
            f'    <li><a href="{base}index.html#about">{t.get("about", "About")}</a></li>',
            f'    <li><a href="{base}index.html#contact">{t.get("contact", "Contact")}</a></li>',
            f'    <li><a href="{base}reviews.html">{t.get("reviews", "Reviews")}</a></li>',
            '  </ul>',
            '</nav>',
        ])
        reviews_nav_html = "\n      ".join(reviews_nav)
        social_html_reviews = social_html.replace('src="behance.png"', f'src="{base}behance.png"').replace('src="deviantart.png"', f'src="{base}deviantart.png"')

        # Build review cards
        review_cards = []
        for rev in reviews_data.get("reviews", []):
            rev_name = html.escape(rev.get("name", ""))
            rev_date = html.escape(rev.get("date", ""))
            rev_text = html.escape(rev.get("text", ""))
            rev_photo = html.escape(rev.get("photo", ""), quote=True)
            rev_rating = rev.get("rating") or 5
            rev_stars = STAR_SVG * rev_rating
            rev_photo_src = f'{base}{rev_photo}' if rev_photo else ''
            if rev_photo and not rev_photo.endswith('default.png'):
                avatar_html = f'<img src="{rev_photo_src}" alt="{rev_name}" class="review-card-avatar" loading="lazy">'
            else:
                initial = html.escape(rev_name[0]) if rev_name else '?'
                avatar_html = f'<div class="review-card-avatar review-avatar-default"><span>{initial}</span></div>'
            review_cards.append(f'''<article class="review-card">
  <div class="review-card-header">
    {avatar_html}
    <div class="review-card-meta">
      <span class="review-card-name">{rev_name}</span>
      <span class="review-card-date">{rev_date}</span>
    </div>
  </div>
  <div class="review-card-stars">{rev_stars}</div>
  <div class="review-card-text"><p>{rev_text}</p></div>
</article>''')

        cards_str = "\n".join(review_cards)
        year_num = datetime.date.today().year

        return f"""<!DOCTYPE html>
<html lang="{page_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{reviews_title_text}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{reviews_canonical}">
{page_hreflang}
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="stylesheet" href="{base}style.css">
<link rel="icon" type="image/png" href="{base}vimark_logo.png">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="{reviews_canonical}">
<meta property="og:title" content="{reviews_title_text}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://vimark.art/{og_strong_src}">
<meta property="og:image:width" content="{og_strong_width}">
<meta property="og:image:height" content="{og_strong_height}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="{reviews_canonical}">
<meta property="twitter:title" content="{reviews_title_text}">
<meta property="twitter:description" content="{meta_desc}">
<meta property="twitter:image" content="https://vimark.art/{og_strong_src}">

<!-- BreadcrumbList -->
<script type="application/ld+json">
{breadcrumb_json}
</script>

<!-- AggregateRating -->
<script type="application/ld+json">
{{"@context": "https://schema.org", "@type": "Service", "name": "Illustration & Concept Art by {hero_name}", "provider": {{"@type": "Person", "name": "{hero_name}", "url": "{reviews_canonical.replace('/reviews.html', '/')}"}}, "aggregateRating": {{"@type": "AggregateRating", "ratingValue": "5", "reviewCount": "71", "bestRating": "5", "worstRating": "1"}}}}
</script>

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
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
        <img src="{base}Max Mitenkov.png" alt="{hero_name}" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
        {reviews_nav_html}
      </header>
      {social_html_reviews}
      {commissions_html}
      <a href="{base}index.html" class="logo-link"><img src="{base}vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>

    <button class="mobile-toggle">{t.get('menu', 'Menu')}</button>

    <main id="main">
      {render_reviews_bar(base, t)}
      <section class="reviews-page">
        <h1>{reviews_h1_text}</h1>
        <p class="reviews-subtitle">{reviews_subtitle_text}</p>
        <div class="reviews-grid">
          {cards_str}
        </div>
      </section>
    </main>
  </div>

  <footer class="site-footer">
    <span><b>©</b> {hero_name}, {year_num}.</span>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){{var p=location.pathname.split('\\\\').join('/');var h=location.hash;var i=p.indexOf('/ru/')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(i){{e.href=p.replace('/ru/','/')+h;r.href=p+h;}}else{{r.href=p.replace('/project/','/ru/project/').replace('/index.html','/ru/index.html').replace('/contact.html','/ru/contact.html').replace('/reviews.html','/ru/reviews.html')+h;e.href=p+h;}}if(i){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
  </footer>

  <div id="lightbox">
    <button class="lightbox-close" aria-label="Close">×</button>
    <button class="lightbox-prev" aria-label="Previous image">‹</button>
    <img class="lightbox-img" src="" alt="">
    <button class="lightbox-next" aria-label="Next image">›</button>
    <div class="lightbox-caption"></div>
    <div class="lightbox-counter"></div>
  </div>

  {sticky_contact_html}
  <button id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top">↑</button>
  <script src="{base}script.js"></script>
</body>
</html>
"""

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
        f'    <li><a href="{base_index}reviews.html">{t.get("reviews", "Reviews")}</a></li>',
        '  </ul>',
        '</nav>',
    ])

    commissions_status = t.get('commissions_open', 'Open for commissions')
    commissions_html = f'<div class="commissions-status"><span class="status-dot"></span><span>{commissions_status}</span></div>'

    sticky_contact_html = '''<div class="sticky-contact">
      <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener" aria-label="Telegram" onclick="if(typeof gtag!=='undefined')gtag('event','click_telegram');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_telegram');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.198 2.433a2.242 2.242 0 0 0-1.022.215l-16.031 6.26a2.27 2.27 0 0 0-.093 4.07l3.827 1.558 1.56 4.44a1.5 1.5 0 0 0 2.663.52l2.33-3.14 3.75 2.83a2.27 2.27 0 0 0 3.58-1.74L22.34 3.89a2.24 2.24 0 0 0-1.142-1.457z"/></svg></a>
      <a href="https://wa.me/375296534382" target="_blank" rel="noopener" aria-label="WhatsApp" onclick="if(typeof gtag!=='undefined')gtag('event','click_whatsapp');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_whatsapp');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></a>
    </div>'''

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
        about_gallery_items += f'<figure class="gallery-item"><img src="{img_src}" data-full="{img_full}" alt="{img_alt}" loading="lazy"><figcaption>{img_alt}</figcaption></figure>'

    about_gallery_html = f'''<div class="about-section about-gallery">
              <h2>{t.get('portfolio', 'Portfolio')}</h2>
              <div class="about-gallery-grid">{about_gallery_items}</div>
            </div>
''' if about_gallery_items else ""

    reviews_summary_html = render_reviews_bar(base_index, t)

    about_html = f'''      <section id="about" class="hidden">
        <div class="about-container">
          <div class="about-photo">
            <img src="{base_index}Mitenkov600.jpg" alt="{hero_name}" loading="lazy">
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
            <h2>{t.get('pricing_title', 'Pricing')}</h2>
            <div class="pricing-list">
              <p>{t.get('pricing_illustration', 'Illustration')} <span class="pricing-from">$500</span></p>
              <p>{t.get('pricing_cover', 'Book cover')} <span class="pricing-from">$700</span></p>
              <p>{t.get('pricing_character', 'Character design')} <span class="pricing-from">$700</span></p>
              <p>{t.get('pricing_env', 'Environment concept')} <span class="pricing-from">$800</span></p>
            </div>

            <hr class="about-divider">
            <h2>{t.get('about_contact_title', "Let's work together")}</h2>
            <div class="about-contact">
              <p><a href="mailto:hello@vimark.art">hello@vimark.art</a></p>
              <p>(+375) 29 653-43-82 · <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener">Telegram: @MaxMitenkov</a></p>
              <p><a href="{base_index}2025_Resume_eng_concept.pdf" target="_blank" rel="noopener" class="cv-link" onclick="if(typeof gtag!=='undefined')gtag('event','download_cv');if(typeof ym!=='undefined')ym(109279162,'reachGoal','download_cv');">{t.get('about_cv', 'Download CV (PDF)')}</a></p>
            </div>

            {about_gallery_html}
          </div>
        </div>
      </section>'''

    project_type_options = [
        ("", t.get('select', 'Select...')),
        ("Book cover", "Book cover"),
        ("Illustration", "Illustration"),
        ("Concept art", "Concept art"),
        ("Other", t.get('other', 'Other')),
    ]
    project_type_options_html = "\n".join(f'              <option value="{html.escape(v)}">{html.escape(l)}</option>' for v, l in project_type_options)

    contact_html = f'''      <section id="contact" class="hidden">
        <div class="contact-container">
          <h1>{t.get('contact', 'Contact')}</h1>
          <form action="https://api.web3forms.com/submit" method="POST" class="contact-form" onsubmit="if(typeof gtag!=='undefined')gtag('event','submit_contact');if(typeof ym!=='undefined')ym(109279162,'reachGoal','submit_contact');">
            <input type="hidden" name="access_key" value="211a1ef5-25ea-4d59-9b9c-33b5f9126f21">
            <input type="hidden" name="redirect" value="https://vimark.art/thanks.html">
            <input type="hidden" name="subject" value="New message from vimark.art">
            <div class="form-group hp-field" style="display:none !important">
              <label for="hp-name">Name</label>
              <input type="text" id="hp-name" name="hp-name" tabindex="-1" autocomplete="off">
            </div>
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
              <label for="project-type">{t.get('project_type_label', 'Project type')}</label>
              <select id="project-type" name="project-type">
{project_type_options_html}
              </select>
            </div>
            <div class="form-group">
              <label for="message">{t.get('message_label', 'Message')}</label>
              <textarea id="message" name="message" rows="6" required></textarea>
            </div>
            <button type="submit" class="submit-btn">{t.get('submit', 'Submit')}</button>
          </form>
        </div>
      </section>'''

    hreflang_block = f'''<!-- hreflang -->
<link rel="alternate" hreflang="en" href="https://vimark.art/" />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/" />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/" />'''

    filter_buttons = []
    filter_all = t.get('filter_all', 'All')
    filter_buttons.append(f'<button class="filter-btn active" data-filter="all">{html.escape(filter_all)}</button>')
    for cat_key, info in categories.items():
        filter_buttons.append(f'<button class="filter-btn" data-filter="{cat_key}">{html.escape(info["label"])}</button>')
    filter_bar = f'<div class="filter-bar">\n  {"\n  ".join(filter_buttons)}\n</div>'

    hero_name = html.escape(t.get('hero_name', 'Max Mitenkov'))

    html_content = f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{hero_name} · {t.get('job_title', 'Illustrator · Concept Artist')}</title>
<meta name="description" content="{t.get('meta_description', 'Portfolio of Max Mitenkov, illustrator and concept artist with 12+ years of experience in games, books, and NFT projects.')}">
<link rel="canonical" href="{canonical_root}">
{hreflang_block}
<link rel="stylesheet" href="{base_index}style.css">
<link rel="icon" type="image/png" href="{base_index}vimark_logo.png">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vimark.art/">
<meta property="og:title" content="{hero_name} · Illustrator · Concept Artist">
<meta property="og:description" content="Gallery of illustrations, concept art, and book covers by Max Mitenkov.">
<meta property="og:image" content="https://vimark.art/{og_strong_src}">
<meta property="og:image:width" content="{og_strong_width}">
<meta property="og:image:height" content="{og_strong_height}">
<link rel="image_src" href="https://vimark.art/{og_strong_src}">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vimark.art/">
<meta property="twitter:title" content="{hero_name} · Illustrator · Concept Artist">
<meta property="twitter:description" content="Gallery of illustrations, concept art, and book covers by Max Mitenkov.">
<meta property="twitter:image" content="https://vimark.art/{og_strong_src}">

<!-- Schema.org -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{hero_name}",
  "jobTitle": "Illustrator and Concept Artist",
  "url": "https://vimark.art/",
  "image": "https://vimark.art/{og_strong_src}",
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
<body class="home">
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
        <img src="{base_index}Max Mitenkov.png" alt="{hero_name}" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
        {"\n      ".join(nav_lines)}
      </header>
      {social_html.replace('src=\"behance.png\"', f'src=\"{base_index}behance.png\"').replace('src=\"deviantart.png\"', f'src=\"{base_index}deviantart.png\"')}
      {commissions_html}
      <a href="{base_index}index.html" class="logo-link"><img src="{base_index}vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>

    <button class="mobile-toggle">Menu</button>

    <main id="main">
      {hero_html(all_items, base_index, pool=(strong_images if strong_images else hero_images), reviews_hero=render_reviews_hero(base_index, t))}
      {filter_bar}
      {projects_sections_html(base_index)}
{about_html}
{contact_html}
    </main>
  </div>

  <footer class="site-footer">
    <span><b>©</b> {hero_name}, {year}.</span>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){{var p=location.pathname.split('\\\\').join('/');var h=location.hash;if(p==='/'||p==='')p='/index.html';var i=p.indexOf('/ru/')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(i){{e.href=p.replace('/ru/','/')+h;r.href=p+h;}}else{{r.href=p.replace('/project/','/ru/project/').replace('/index.html','/ru/index.html').replace('/reviews.html','/ru/reviews.html')+h;e.href=p+h;}}if(i){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
  </footer>

  <div id="lightbox">
    <button class="lightbox-close">×</button>
    <button class="lightbox-prev">‹</button>
    <img class="lightbox-img" src="" alt="">
    <button class="lightbox-next">›</button>
    <div class="lightbox-caption"></div>
    <div class="lightbox-counter"></div>
  </div>

  {sticky_contact_html}
  <button id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top">↑</button>
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

    # Generate individual artwork pages
    art_dir = proj_dir / "art"
    art_dir.mkdir(exist_ok=True)
    art_reviews = load_art_reviews()
    generated_arts = 0
    for sub_key, sub_info in all_subfolders.items():
        proj_images = [img for img in all_items if img.get("subcategory") == sub_key]
        if not proj_images:
            continue
        proj = projects.get(sub_key, {"title": sub_info["label"], "year": "", "client": "", "description": ""})
        # Determine project folder for WIP lookup
        project_folder = ""
        if proj_images:
            project_folder = os.path.dirname(proj_images[0]["src"])
        for img in proj_images:
            art_slug = slugify(captions.get(img["src"], img["name"]))
            review = art_reviews.get(art_slug)
            wip_images = find_wip_images(art_slug, project_folder) if project_folder else []
            art_base = "../../../" if base_index else "../../"
            page_html = build_art_page(img, proj, review, wip_images, base=art_base)
            (art_dir / f"{art_slug}.html").write_text(page_html, encoding="utf-8")
            generated_arts += 1
    # Also generate art pages for standalone categories
    for cat_key, info in categories.items():
        if info["subfolders"]:
            continue
        cat_images = info["images"]
        if not cat_images:
            continue
        proj = projects.get(cat_key, {"title": info["label"], "year": "", "client": "", "description": ""})
        project_folder = info["folder"] if info.get("folder") else ""
        for img in cat_images:
            art_slug = slugify(captions.get(img["src"], img["name"]))
            review = art_reviews.get(art_slug)
            wip_images = find_wip_images(art_slug, project_folder) if project_folder else []
            art_base = "../../../" if base_index else "../../"
            page_html = build_art_page(img, proj, review, wip_images, base=art_base)
            (art_dir / f"{art_slug}.html").write_text(page_html, encoding="utf-8")
            generated_arts += 1
    print(f"Generated {generated_arts} {lang}/project/art pages.")

    # Generate category pages
    for cat_key, info in categories.items():
        cat_base = "../" if base_index else ""
        page_html = build_category_page(cat_key, info, base=cat_base)
        (out_dir / f"{cat_key}.html").write_text(page_html, encoding="utf-8")
        print(f"Generated {lang}/{cat_key}.html")

    # Generate reviews page
    reviews_base = base_index
    reviews_html = build_reviews_page(base=reviews_base)
    (out_dir / "reviews.html").write_text(reviews_html, encoding="utf-8")
    print(f"Generated {lang}/reviews.html")

    # Generate sitemap.xml
    today = datetime.date.today().isoformat()
    root_url = "https://vimark.art/" if lang == 'en' else "https://vimark.art/ru/"
    project_base = "https://vimark.art/project/" if lang == 'en' else "https://vimark.art/ru/project/"
    urls = [
        (root_url, "1.0"),
        (f"{root_url}contact.html", "0.5"),
        (f"{root_url}reviews.html", "0.7"),
    ]
    for sub_key in projects.keys():
        urls.append((f"{project_base}{sub_key}.html", "0.9"))
    for cat_key, info in categories.items():
        if not info["subfolders"]:
            urls.append((f"{project_base}{cat_key}.html", "0.9"))
    # Category landing pages
    for cat_key, info in categories.items():
        urls.append((f"{root_url}{cat_key}.html", "0.8"))
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

    if lang == 'en':
        image_urls = []
        title_counts = {}
        for img in all_items:
            src_quoted = urllib.parse.quote(img['src'], safe='/')
            img_loc = f"https://vimark.art/{src_quoted}"
            img_title = html.escape(captions.get(img['src'], img['name']))
            # Make titles unique
            if img_title in title_counts:
                title_counts[img_title] += 1
                img_title = f"{img_title} ({title_counts[img_title]})"
            else:
                title_counts[img_title] = 1
            image_urls.append(f'  <url>\n    <loc>{img_loc}</loc>\n    <image:image>\n      <image:loc>{img_loc}</image:loc>\n      <image:title>{img_title}</image:title>\n    </image:image>\n  </url>')
        image_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{chr(10).join(image_urls)}
</urlset>"""
        (WEBSITE / "image-sitemap.xml").write_text(image_sitemap, encoding="utf-8")
        print(f"Generated image-sitemap.xml with {len(all_items)} images.")


if __name__ == "__main__":
    build_lang('en')
    build_lang('ru')
