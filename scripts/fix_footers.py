import os

BASE = "D:\\Concept_work\\Vimark_art"

pages = [
    # (path, is_ru, is_subdir)
    # is_subdir=True means the page is in a subdirectory like case-studies/, blog/
    # is_subdir=False means the page is at root level or ru/ level
    ("index.html", False, False),
    ("about.html", False, False),
    ("contact.html", False, False),
    ("book-covers.html", False, False),
    ("book-illustrations.html", False, False),
    ("visual-stories.html", False, False),
    ("services.html", False, False),
    ("reviews.html", False, False),
    ("faq.html", False, False),
    ("404.html", False, False),
    ("thanks.html", False, False),
    ("privacy.html", False, False),
    ("personal.html", False, False),
    ("ru/index.html", True, False),
    ("ru/about.html", True, False),
    ("ru/contact.html", True, False),
    ("ru/book-covers.html", True, False),
    ("ru/book-illustrations.html", True, False),
    ("ru/visual-stories.html", True, False),
    ("ru/services.html", True, False),
    ("ru/reviews.html", True, False),
    ("ru/faq.html", True, False),
    ("ru/personal.html", True, False),
    ("case-studies/hoebeke-sci-fi-series.html", False, True),
    ("ru/case-studies/hoebeke-sci-fi-series.html", True, True),
]

def make_footer_entry(text, href, is_subdir, is_ru):
    """Make a footer link: <a href="PREFIXtext.html">LABEL</a>"""
    pref = "../" if is_subdir else ""
    label = text if not is_ru else text
    return f'<a href="{pref}{href}">{label}</a>'

# EN footer links (root)
EN_NAV_LINKS = [
    ("Work", "work.html"),
    ("Services", "services.html"),
    ("About", "about.html"),
    ("Contact", "contact.html"),
    ("Book Covers", "book-covers.html"),
    ("Illustrations", "book-illustrations.html"),
    ("Visual Stories", "visual-stories.html"),
    ("Case Studies", "case-studies/hoebeke-sci-fi-series.html"),
    ("Reviews", "reviews.html"),
    ("FAQ", "faq.html"),
    ("Blog", "blog/"),
]

# RU footer links 
RU_NAV_LINKS = [
    ("Work", "work.html"),
    ("Services", "services.html"),
    ("About", "about.html"),
    ("Contact", "contact.html"),
    ("Book Covers", "book-covers.html"),
    ("Illustrations", "book-illustrations.html"),
    ("Visual Stories", "visual-stories.html"),
    ("Case Studies", "case-studies/hoebeke-sci-fi-series.html"),
    ("Reviews", "reviews.html"),
    ("FAQ", "faq.html"),
    ("Blog", "blog/"),
]

for relpath, is_ru, is_subdir in pages:
    filepath = os.path.join(BASE, relpath.replace("/", os.sep))
    if not os.path.exists(filepath):
        print(f"MISSING: {relpath}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if footer already has Work
    markers = [f'href="{p}work.html">{l}</a>' for p, l in [("../", "Work"), ("", "Work"), ("", "Работы"), ("../", "Работы")]]
    has_work = any(m in content for m in markers)

    # Find the footer-links section
    start_marker = '<div class="footer-links">'
    end_marker = '</div>'
    start_idx = content.find(start_marker)

    if start_idx == -1:
        print(f"NO FOOTER: {relpath}")
        continue

    # Find the end of the footer-links div
    end_idx = content.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        print(f"NO FOOTER END: {relpath}")
        continue

    footer_section = content[start_idx:end_idx + len(end_marker)]

    if has_work:
        print(f"OK: {relpath}")
        continue

    # Build new footer section
    pref = "../" if is_subdir else ""
    links = RU_NAV_LINKS if is_ru else EN_NAV_LINKS
    ru_labels = {
        "Work": "Работы", "Services": "Услуги", "About": "Обо мне", "Contact": "Контакты",
        "Book Covers": "Обложки книг", "Illustrations": "Иллюстрации к книгам",
        "Visual Stories": "Визуальные истории", "Case Studies": "Кейсы",
        "Reviews": "Отзывы", "FAQ": "FAQ", "Blog": "Блог",
    }

    parts = []
    for label, href in links:
        if is_ru:
            display = ru_labels.get(label, label)
        else:
            display = label
        parts.append(f'        <a href="{pref}{href}">{display}</a>')

    footer_links = " ·\n".join(parts)
    new_footer = f'''    <div class="footer-links">
      <p>
{footer_links}</p>
      <p>
        <a href="https://reedsy.com/freelancers/maxim-m" target="_blank" rel="noopener">Reedsy</a> ·
        <a href="https://www.behance.net/vimark" target="_blank" rel="noopener">Behance</a> ·
        <a href="https://www.artstation.com/vimark" target="_blank" rel="noopener">ArtStation</a> ·
        <a href="https://www.instagram.com/vimark_art/" target="_blank" rel="noopener">Instagram</a> ·
        <a href="https://www.pinterest.com/vimark" target="_blank" rel="noopener">Pinterest</a> ·
        <a href="https://www.deviantart.com/vimark" target="_blank" rel="noopener">DeviantArt</a>
      </p>
    </div>'''

    if is_subdir:
        # For subdirectories, external links don't need prefix
        pass

    content = content[:start_idx] + new_footer + content[end_idx + len(end_marker):]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"FIXED FOOTER: {relpath}")
