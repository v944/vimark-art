#!/usr/bin/env python3
"""Generate portfolio site inspired by tobiaskwan.com.
Top-level folders become menu sections.
Sub-folders become sub-menu items.
"""
import os
import html
import re
import datetime
import configparser
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

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


def ensure_thumbnail(original_path):
    """Generate a JPEG thumbnail if it doesn't exist or is outdated."""
    rel = os.path.relpath(original_path, WEBSITE).replace("\\", "/")
    if not HAS_PILLOW:
        return rel, "", ""

    thumb_path = THUMBS_DIR / rel
    thumb_path.parent.mkdir(parents=True, exist_ok=True)

    # If thumbnail exists and is newer than original, reuse it
    if thumb_path.exists() and thumb_path.stat().st_mtime >= original_path.stat().st_mtime:
        try:
            with Image.open(thumb_path) as im:
                w, h = im.size
            return rel, str(w), str(h)
        except Exception:
            pass  # regenerate if corrupted

    try:
        with Image.open(original_path) as im:
            # Convert palette/RGBA to RGB for JPEG
            if im.mode in ('RGBA', 'P'):
                im_rgb = im.convert('RGB')
            else:
                im_rgb = im
            im_rgb.thumbnail(THUMB_SIZE, Image.LANCZOS)
            im_rgb.save(thumb_path, "JPEG", quality=THUMB_QUALITY, optimize=True)
            w, h = im_rgb.size
        thumb_rel = os.path.relpath(thumb_path, WEBSITE).replace("\\", "/")
        return thumb_rel, str(w), str(h)
    except Exception as e:
        print(f"  Warning: could not thumbnail {rel}: {e}")
        return rel, "", ""


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
    categories = {}
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name.startswith("_"):
            continue
        if entry.name in ("website", "thumbnails", "project"):
            continue

        # Discover subfolders
        subfolders = {}
        for sub in sorted(entry.iterdir()):
            if sub.is_dir():
                sub_imgs = collect_images_from_path(os.path.join(entry.name, sub.name))
                if sub_imgs:
                    sub_key = slugify(sub.name)
                    subfolders[sub_key] = {
                        "label": t.get(sub_key, human_label(sub.name)),
                        "images": sub_imgs,
                    }

        # Collect all images in category (including root files and all subfolders)
        all_cat_images = collect_images_from_path(entry.name)

        if not all_cat_images and not subfolders:
            continue

        cat_key = slugify(entry.name)
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

    # Collect all subfolders flat map
    all_subfolders = {}
    for cat_key, info in categories.items():
        all_subfolders.update(info["subfolders"])

    # Load or create captions file
    captions = load_captions()
    ensure_captions_file(all_items)

    # Load or create projects file
    projects = load_projects()
    ensure_projects_file(all_subfolders)

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

    def gallery_html(items):
        lines = ['<div class="gallery-grid">']
        for img in items:
            src = html.escape(img["src"], quote=True)
            thumb = html.escape(img.get("thumb", img["src"]), quote=True)
            alt = html.escape(captions.get(img["src"], img["name"]), quote=True)
            cat = html.escape(img["category"], quote=True)
            sub = html.escape(img.get("subcategory", ""), quote=True)
            w = img.get("width", "")
            h = img.get("height", "")
            dim_attr = f' width="{w}" height="{h}"' if w and h else ''
            lines.append(f'  <div class="gallery-item" data-category="{cat}" data-subcategory="{sub}">')
            lines.append(f'    <img src="{thumb}" data-full="{src}" alt="{alt}" loading="lazy"{dim_attr}>')
            lines.append('  </div>')
        lines.append('</div>')
        return "\n".join(lines)

    def project_gallery_html(items):
        lines = ['<div class="gallery-grid">']
        for img in items:
            src = html.escape(img["src"], quote=True)
            thumb = html.escape(img.get("thumb", img["src"]), quote=True)
            alt = html.escape(captions.get(img["src"], img["name"]), quote=True)
            w = img.get("width", "")
            h = img.get("height", "")
            dim_attr = f' width="{w}" height="{h}"' if w and h else ''
            lines.append(f'  <div class="gallery-item">')
            lines.append(f'    <img src="{thumb}" data-full="{src}" alt="{alt}" loading="lazy"{dim_attr}>')
            lines.append('  </div>')
        lines.append('</div>')
        return "\n".join(lines)

    def build_project_page(sub_key, proj, items):
        title = html.escape(proj.get("title", sub_key))
        year = html.escape(proj.get("year", ""))
        client = html.escape(proj.get("client", ""))
        description = html.escape(proj.get("description", ""))
        og_image = html.escape(items[0]["src"], quote=True) if items else "Mitenkov600.jpg"

        meta_parts = [p for p in [year, client] if p]
        meta_html = f'<p class="project-meta">{" · ".join(meta_parts)}</p>' if meta_parts else ''
        desc_html = f'<p class="project-desc">{description}</p>' if description else ''

        social_html_project = social_html.replace('src="behance.png"', 'src="../behance.png"').replace('src="deviantart.png"', 'src="../deviantart.png"')

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
<link rel="stylesheet" href="../style.css">
<link rel="icon" type="image/png" href="../vimark_logo.png">

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
      <img src="../Max Mitenkov.png" alt="Max Mitenkov" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
      <nav class="main-nav">
        <ul>
          <li><a href="../index.html">← Portfolio</a></li>
        </ul>
      </nav>
      {social_html_project}
      <div class="lang-switch">
        <a href="#" id="lang-en">EN</a>
        <span>/</span>
        <a href="#" id="lang-ru">RU</a>
      </div>
      <script>(function(){{ var p=location.pathname; var e=document.getElementById('lang-en'); var r=document.getElementById('lang-ru'); e.href=p.replace(/^\\/ru/, '')||'/'; r.href='/ru'+(p.replace(/^\\/ru/, '')||'/'); if(p.startsWith('/ru')){{r.classList.add('active');}}else{{e.classList.add('active');}} }})();</script>
      <img src="../vimark_logo.png" alt="Logo" style="width: 60px; margin-top: auto; margin-bottom: 100px; opacity: 0.9; align-self: center;">
    </aside>

    <button class="mobile-toggle">{t.get('menu', 'Menu')}</button>

    <main id="main">
      <div class="project-header">
        <a href="/index.html" class="back-link">{t.get('back_to_portfolio', '← Back to portfolio')}</a>
        <h1>{title}</h1>
        {meta_html}
        {desc_html}
      </div>
      {project_gallery_html(items)}
    </main>
  </div>

  <div class="site-footer"><b>©</b> Max Mitenkov.</div>

  <div id="lightbox">
    <button class="lightbox-close" aria-label="Close">×</button>
    <button class="lightbox-prev" aria-label="Previous image">‹</button>
    <img class="lightbox-img" src="" alt="">
    <button class="lightbox-next" aria-label="Next image">›</button>
    <div class="lightbox-caption"></div>
    <div class="lightbox-counter"></div>
  </div>

  <script src="../script.js"></script>
</body>
</html>
"""
        return page_content

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
                project_link = f'<a href="/project/{sub_key}.html" class="project-link" title="{t.get("project_page", "Project page")}">▶▶</a>' if sub_key in projects else ''
                nav_lines.append(f'        <li><a href="#" data-category="{key}" data-subcategory="{sub_key}">{html.escape(sub_info["label"])}</a> {project_link}</li>')
            nav_lines.append('      </ul>')
            nav_lines.append('    </li>')
        else:
            nav_lines.append(f'    <li><a href="#" data-category="{key}">{html.escape(info["label"])}</a></li>')
    nav_lines.extend([
        f'    <li><a href="#" data-view="about">{t.get("about", "About")}</a></li>',
        f'    <li><a href="#" data-view="contact">{t.get("contact", "Contact")}</a></li>',
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

    about_html = f'''      <section id="about" class="hidden">
        <div class="about-container">
          <div class="about-photo">
            <img src="Mitenkov600.jpg" alt="Max Mitenkov">
          </div>
          <div class="about-content">
            <h1>{t.get('about', 'About')}</h1>
            <p class="about-intro">{t.get('about_intro', "I'm Max Mitenkov, an illustrator and concept designer with over 12 years of professional experience. I've worked on projects for studios in Belarus, the USA, and the UAE — from NFT character design to photorealistic environments in Unreal Engine 5.")}</p>

            <div class="about-section">
              <h2>{t.get('skills', 'Skills')}</h2>
              <p>Photoshop, ZBrush, Houdini, Substance Painter, Substance Designer, Unreal Engine 4/5.</p>
            </div>

            <div class="about-section">
              <h2>{t.get('work_experience', 'Work Experience')}</h2>
              <div class="job">
                <h3>Senior Concept Artist — Apex Digital VC, Dubai, UAE <span class="job-date">(2022 – Present)</span></h3>
                <ul>
                  <li>Created concept art and illustrations for the project "Search for Animera"</li>
                  <li>Developed environmental concept art for "Search for Animera"</li>
                  <li>Designed NFT characters</li>
                </ul>
              </div>
              <div class="job">
                <h3>3D Artist — ICVR, Los Angeles, California <span class="job-date">(2021 – 2022)</span></h3>
                <ul>
                  <li>Collaborated with the director to create photorealistic scenes in Unreal Engine 5</li>
                  <li>Created locations and shaders in UE5 based on concept art</li>
                  <li>Textured assets using Substance Painter</li>
                  <li>Optimized scenes in Unreal Engine 5</li>
                </ul>
              </div>
              <div class="job">
                <h3>3D Artist — Lunas pro, Minsk, Belarus <span class="job-date">(2016 – 2021)</span></h3>
                <ul>
                  <li>Created locations in Unreal Engine 4</li>
                  <li>Prepared high-quality materials in Substance Designer</li>
                  <li>Textured assets using Substance Painter</li>
                  <li>Prepared shaders</li>
                </ul>
              </div>
            </div>

            <div class="about-section">
              <h2>{t.get('education', 'Education')}</h2>
              <p>Belarusian State University of Informatics and Radioelectronics (BSUIR)<br>
              Faculty of Computer-Aided Design <span class="job-date">(1993–1998)</span></p>
            </div>

            <div class="about-section">
              <h2>{t.get('professional_development', 'Professional Development')}</h2>
              <ul class="courses">
                <li><span class="course-year">2024</span> — ZBrush for Concept and Iteration — CGMA</li>
                <li><span class="course-year">2022</span> — Fundamentals of Houdini for 3D Artists — CGMA</li>
                <li><span class="course-year">2021</span> — Advanced Substance for Environment Art — CGMA</li>
                <li><span class="course-year">2020</span> — Creating PBR Materials — Epic Games</li>
                <li><span class="course-year">2020</span> — Organic World Building in UE4 — CGMA</li>
                <li><span class="course-year">2019</span> — VFXlab — Unreal Engine</li>
              </ul>
            </div>

            <div class="about-section">
              <h2>{t.get('portfolio', 'Portfolio')}</h2>
              <div class="portfolio-buttons">
                <a href="https://vimark.art" target="_blank" rel="noopener">vimark.art</a>
                <a href="https://artstation.com/vimark" target="_blank" rel="noopener">ArtStation</a>
                <a href="https://behance.net/vimark" target="_blank" rel="noopener">Behance</a>
                <a href="https://linkedin.com/in/maxim-mitenkov-06192940" target="_blank" rel="noopener">LinkedIn</a>
              </div>
            </div>

            <div class="about-section">
              <h2>{t.get('contact', 'Contact')}</h2>
              <p>Email: <a href="mailto:hello@vimark.art">hello@vimark.art</a></p>
              <p>Phone / WhatsApp: <a href="tel:+375296534382">(+375) 29 653-43-82</a></p>
              <p>Telegram: <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener">@MaxMitenkov</a></p>
              <p class="about-closing">{t.get('about_closing', "I'm open to remote work, one-time commissions, and long-term collaboration. Feel free to reach out — let's create visual content for your book, game, animation, or advertising campaign.")}</p>
            </div>
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
<link rel="stylesheet" href="style.css">
<link rel="icon" type="image/png" href="vimark_logo.png">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vimark.art/">
<meta property="og:title" content="Max Mitenkov · Illustrator · Concept Artist">
<meta property="og:description" content="Portfolio of Max Mitenkov, illustrator and concept artist with 12+ years of experience in games, books, and NFT projects.">
<meta property="og:image" content="https://vimark.art/Mitenkov600.jpg">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vimark.art/">
<meta property="twitter:title" content="Max Mitenkov · Illustrator · Concept Artist">
<meta property="twitter:description" content="Portfolio of Max Mitenkov, illustrator and concept artist with 12+ years of experience in games, books, and NFT projects.">
<meta property="twitter:image" content="https://vimark.art/Mitenkov600.jpg">

<!-- Schema.org -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Max Mitenkov",
  "jobTitle": "Illustrator and Concept Artist",
  "url": "https://vimark.art/",
  "image": "https://vimark.art/Mitenkov600.jpg",
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
      <img src="Max Mitenkov.png" alt="Max Mitenkov" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
      {"\n      ".join(nav_lines)}
      {social_html}
      <div class="lang-switch">
        <a href="#" id="lang-en">EN</a>
        <span>/</span>
        <a href="#" id="lang-ru">RU</a>
      </div>
      <script>(function(){{var p=location.pathname.split('\\\\').join('/');var i=p.indexOf('/ru/')!==-1||p.indexOf('/ru')!==-1;var e=document.getElementById('lang-en');var r=document.getElementById('lang-ru');if(i){{e.href=p.replace('/ru/','/');r.href=p;}}else{{r.href=p.replace('/project/','/ru/project/').replace('/index.html','/ru/index.html');e.href=p;}}if(i){{r.classList.add('active');}}else{{e.classList.add('active');}}}})();</script>
      <img src="vimark_logo.png" alt="Logo" style="width: 60px; margin-top: auto; margin-bottom: 100px; opacity: 0.9; align-self: center;">
    </aside>

    <button class="mobile-toggle">Menu</button>

    <main id="main">
      {gallery_html(all_items)}
{about_html}
{contact_html}
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

    # Convert relative paths to absolute for cross-language compatibility
    html_content = html_content.replace('href="style.css"', 'href="/style.css"')
    html_content = html_content.replace('src="script.js"', 'src="/script.js"')
    html_content = html_content.replace('src="vimark_logo.png"', 'src="/vimark_logo.png"')
    html_content = html_content.replace('src="Max Mitenkov.png"', 'src="/Max Mitenkov.png"')
    html_content = html_content.replace('src="behance.png"', 'src="/behance.png"')
    html_content = html_content.replace('src="deviantart.png"', 'src="/deviantart.png"')
    html_content = html_content.replace('src="thumbnails/', 'src="/thumbnails/')
    html_content = html_content.replace('data-full="Book Illustrations/', 'data-full="/Book Illustrations/')
    html_content = html_content.replace('data-full="BookCover/', 'data-full="/BookCover/')
    html_content = html_content.replace('data-full="comic/', 'data-full="/comic/')
    html_content = html_content.replace('data-full="Single/', 'data-full="/Single/')

    (out_dir / "index.html").write_text(html_content, encoding="utf-8")
    print(f"Generated {lang}/index.html with {len(all_items)} images.")
    for key, info in categories.items():
        subs = ", ".join(info["subfolders"].keys()) if info["subfolders"] else "none"
        print(f"  - {key}: {len(info['images'])} images (subfolders: {subs})")
    print(f"Select preview: {len(select_items)} images.")

    # Generate project pages
    if projects:
        proj_dir = out_dir / "project"
        proj_dir.mkdir(exist_ok=True)
        for sub_key, proj in projects.items():
            proj_images = [img for img in all_items if img.get("subcategory") == sub_key]
            if not proj_images:
                continue
            page_html = build_project_page(sub_key, proj, proj_images)
            # Convert relative paths to absolute
            page_html = page_html.replace('href="../style.css"', 'href="/style.css"')
            page_html = page_html.replace('src="../script.js"', 'src="/script.js"')
            page_html = page_html.replace('src="../vimark_logo.png"', 'src="/vimark_logo.png"')
            page_html = page_html.replace('src="../Max Mitenkov.png"', 'src="/Max Mitenkov.png"')
            page_html = page_html.replace('src="../behance.png"', 'src="/behance.png"')
            page_html = page_html.replace('src="../deviantart.png"', 'src="/deviantart.png"')
            page_html = page_html.replace('src="../thumbnails/', 'src="/thumbnails/')
            page_html = page_html.replace('data-full="../Book Illustrations/', 'data-full="/Book Illustrations/')
            page_html = page_html.replace('data-full="../BookCover/', 'data-full="/BookCover/')
            page_html = page_html.replace('data-full="../comic/', 'data-full="/comic/')
            page_html = page_html.replace('data-full="../Single/', 'data-full="/Single/')
            page_html = page_html.replace('href="../index.html"', 'href="/index.html"')
            (proj_dir / f"{sub_key}.html").write_text(page_html, encoding="utf-8")
        print(f"Generated {len(projects)} {lang}/project pages.")

    # Generate sitemap.xml
    today = datetime.date.today().isoformat()
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://vimark.art/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://vimark.art/index.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
    (out_dir / "sitemap.xml").write_text(sitemap_content, encoding="utf-8")
    print(f"Generated {lang}/sitemap.xml")


if __name__ == "__main__":
    build_lang('en')
    build_lang('ru')
