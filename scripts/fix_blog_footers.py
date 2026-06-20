import os

BASE = "D:\\Concept_work\\Vimark_art"

# Blog pages also need footer fixes
pages = [
    ("blog/index.html", False, True),
    ("blog/how-much-does-a-book-cover-cost.html", False, True),
    ("blog/book-cover-design-trends-2026.html", False, True),
    ("blog/how-to-choose-book-cover-illustrator.html", False, True),
    ("blog/from-brief-to-final-art-process.html", False, True),
    ("blog/common-mistakes-when-hiring-illustrator.html", False, True),
    ("ru/blog/index.html", True, True),
    ("ru/blog/skolko-stoit-oblozhka-knigi.html", True, True),
    ("ru/blog/trendy-dizaina-oblozhek-2026.html", True, True),
    ("ru/blog/kak-vybrat-illyustratora-oblozhki.html", True, True),
    ("ru/blog/ot-brifa-do-finalnogo-arta-protsess.html", True, True),
    ("ru/blog/chastye-oshibki-pri-vybore-illyustratora.html", True, True),
]

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

ru_labels = {
    "Work": "Работы", "Services": "Услуги", "About": "Обо мне", "Contact": "Контакты",
    "Book Covers": "Обложки книг", "Illustrations": "Иллюстрации к книгам",
    "Visual Stories": "Визуальные истории", "Case Studies": "Кейсы",
    "Reviews": "Отзывы", "FAQ": "FAQ", "Blog": "Блог",
}

for relpath, is_ru, is_subdir in pages:
    filepath = os.path.join(BASE, relpath.replace("/", os.sep))
    if not os.path.exists(filepath):
        print(f"MISSING: {relpath}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for Work in nav or footer
    has_work = "work.html" in content
    if has_work:
        print(f"OK: {relpath}")
        continue

    # Find footer-links
    start_marker = '<div class="footer-links">'
    end_marker = '</div>'
    start_idx = content.find(start_marker)

    if start_idx == -1:
        print(f"NO FOOTER: {relpath}")
        continue

    end_idx = content.find(end_marker, start_idx + len(start_marker))
    pref = "../" if is_subdir else ""
    links = RU_NAV_LINKS if is_ru else EN_NAV_LINKS

    parts = []
    for label, href in links:
        display = ru_labels.get(label, label) if is_ru else label
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

    content = content[:start_idx] + new_footer + content[end_idx + len(end_marker):]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"FIXED: {relpath}")
