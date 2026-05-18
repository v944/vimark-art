#!/usr/bin/env python3
"""Generate portfolio site inspired by tobiaskwan.com.
Top-level folders become menu sections.
Sub-folders become sub-menu items.
"""
import os
import html
import re
import datetime
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
      <a href="mailto:hello@vimark.art" aria-label="Email"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
      <a href="https://www.facebook.com/maks.vimark/" aria-label="Facebook"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
      <a href="https://www.linkedin.com/in/maxim-mitenkov-06192940/" aria-label="LinkedIn"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
      <a href="https://www.instagram.com/vimark_art/" aria-label="Instagram"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
      <a href="https://www.behance.net/vimark" aria-label="Behance"><img src="behance.png" alt="Behance" class="social-icon"></a>
      <a href="https://www.deviantart.com/vimark" aria-label="DeviantArt"><img src="deviantart.png" alt="DeviantArt" class="social-icon"></a>
    </div>'''

    about_html = '''      <section id="about" class="hidden">
        <div class="about-container">
          <div class="about-photo">
            <img src="Mitenkov600.jpg" alt="Max Mitenkov">
          </div>
          <div class="about-content">
            <h1>About</h1>
            <p class="about-intro">I'm Max Mitenkov, an illustrator and concept designer with over 12 years of professional experience. I've worked on projects for studios in Belarus, the USA, and the UAE — from NFT character design to photorealistic environments in Unreal Engine 5.</p>

            <div class="about-section">
              <h2>Skills</h2>
              <p>Photoshop, ZBrush, Houdini, Substance Painter, Substance Designer, Unreal Engine 4/5.</p>
            </div>

            <div class="about-section">
              <h2>Work Experience</h2>
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
              <h2>Education</h2>
              <p>Belarusian State University of Informatics and Radioelectronics (BSUIR)<br>
              Faculty of Computer-Aided Design <span class="job-date">(1993–1998)</span></p>
            </div>

            <div class="about-section">
              <h2>Professional Development</h2>
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
              <h2>Portfolio</h2>
              <div class="portfolio-buttons">
                <a href="https://vimark.art" target="_blank" rel="noopener">vimark.art</a>
                <a href="https://artstation.com/vimark" target="_blank" rel="noopener">ArtStation</a>
                <a href="https://behance.net/vimark" target="_blank" rel="noopener">Behance</a>
                <a href="https://linkedin.com/in/maxim-mitenkov-06192940" target="_blank" rel="noopener">LinkedIn</a>
              </div>
            </div>

            <div class="about-section">
              <h2>Contact</h2>
              <p>Email: <a href="mailto:hello@vimark.art">hello@vimark.art</a></p>
              <p>Phone / WhatsApp: <a href="tel:+375296534382">(+375) 29 653-43-82</a></p>
              <p>Telegram: <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener">@MaxMitenkov</a></p>
              <p class="about-closing">I'm open to remote work, one-time commissions, and long-term collaboration. Feel free to reach out — let's create visual content for your book, game, animation, or advertising campaign.</p>
            </div>
          </div>
        </div>
      </section>'''

    contact_html = '''      <section id="contact" class="hidden">
        <div class="contact-container">
          <h1>Contact</h1>
          <form action="https://api.web3forms.com/submit" method="POST" class="contact-form">
            <input type="hidden" name="access_key" value="211a1ef5-25ea-4d59-9b9c-33b5f9126f21">
            <input type="hidden" name="redirect" value="https://vimark.art/thanks.html">
            <input type="hidden" name="subject" value="New message from vimark.art">
            <div class="form-group">
              <label for="email">Email <span class="required">(required)</span></label>
              <input type="email" id="email" name="email" required>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label for="first-name">First Name <span class="required">(required)</span></label>
                <input type="text" id="first-name" name="first-name" required>
              </div>
              <div class="form-group">
                <label for="last-name">Last Name <span class="required">(required)</span></label>
                <input type="text" id="last-name" name="last-name" required>
              </div>
            </div>
            <div class="form-group">
              <label for="message">Message</label>
              <textarea id="message" name="message" rows="6" required></textarea>
            </div>
            <button type="submit" class="submit-btn">Submit</button>
          </form>
        </div>
      </section>'''

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Max Mitenkov · Illustrator · Concept Artist</title>
<meta name="description" content="Portfolio of Max Mitenkov, illustrator and concept artist with 12+ years of experience in games, books, and NFT projects.">
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

    (WEBSITE / "index.html").write_text(html_content, encoding="utf-8")
    print(f"Generated index.html with {len(all_items)} images.")
    for key, info in categories.items():
        subs = ", ".join(info["subfolders"].keys()) if info["subfolders"] else "none"
        print(f"  - {key}: {len(info['images'])} images (subfolders: {subs})")
    print(f"Select preview: {len(select_items)} images.")

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
    (WEBSITE / "sitemap.xml").write_text(sitemap_content, encoding="utf-8")
    print("Generated sitemap.xml")


if __name__ == "__main__":
    build()
