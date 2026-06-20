import os, re

BASE = "D:\\Concept_work\\Vimark_art"

def fix_footer(filepath, prefix=""):
    """Replace the footer-links block with new links."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = '<div class="footer-links">'
    end_marker = '</div>'

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx + len(start_marker))

    if start_idx == -1 or end_idx == -1:
        return False

    pref = prefix  # "" for root/ru/, "../" for blog/ or case-studies/

    # Detect if this is a RU page (has RU labels)
    is_ru = "\\ru\\" in filepath or "/ru/" in filepath.replace("\\", "/")

    en_links = [
        (f'<a href="{pref}work.html">Work</a>', " "),
        (f'<a href="{pref}services.html">Services</a>', " "),
        (f'<a href="{pref}about.html">About</a>', " "),
        (f'<a href="{pref}contact.html">Contact</a>', " "),
        (f'<a href="{pref}book-covers.html">Book Covers</a>', " "),
        (f'<a href="{pref}book-illustrations.html">Illustrations</a>', " "),
        (f'<a href="{pref}visual-stories.html">Visual Stories</a>', " "),
        (f'<a href="{pref}case-studies/hoebeke-sci-fi-series.html">Case Studies</a>', " "),
        (f'<a href="{pref}reviews.html">Reviews</a>', " "),
        (f'<a href="{pref}faq.html">FAQ</a>', " "),
        (f'<a href="{pref}blog/">Blog</a>', ""),
    ]

    ru_links = [
        (f'<a href="{pref}work.html">Работы</a>', " "),
        (f'<a href="{pref}services.html">Услуги</a>', " "),
        (f'<a href="{pref}about.html">Обо мне</a>', " "),
        (f'<a href="{pref}contact.html">Контакты</a>', " "),
        (f'<a href="{pref}book-covers.html">Обложки книг</a>', " "),
        (f'<a href="{pref}book-illustrations.html">Иллюстрации к книгам</a>', " "),
        (f'<a href="{pref}visual-stories.html">Визуальные истории</a>', " "),
        (f'<a href="{pref}case-studies/hoebeke-sci-fi-series.html">Кейсы</a>', " "),
        (f'<a href="{pref}reviews.html">Отзывы</a>', " "),
        (f'<a href="{pref}faq.html">FAQ</a>', " "),
        (f'<a href="{pref}blog/">Блог</a>', ""),
    ]

    links = ru_links if is_ru else en_links
    # Build the links with separators
    line = "".join(a + sep for a, sep in links)
    line = line.rstrip(" ")  # remove trailing separator

    new_footer_block = f'''    <div class="footer-links">
      <p>
        {line}</p>
      <p>
        <a href="https://reedsy.com/freelancers/maxim-m" target="_blank" rel="noopener">Reedsy</a> ·
        <a href="https://www.behance.net/vimark" target="_blank" rel="noopener">Behance</a> ·
        <a href="https://www.artstation.com/vimark" target="_blank" rel="noopener">ArtStation</a> ·
        <a href="https://www.instagram.com/vimark_art/" target="_blank" rel="noopener">Instagram</a> ·
        <a href="https://www.pinterest.com/vimark" target="_blank" rel="noopener">Pinterest</a> ·
        <a href="https://www.deviantart.com/vimark" target="_blank" rel="noopener">DeviantArt</a>
      </p>
    </div>'''

    old_footer_block = content[start_idx:end_idx + len(end_marker)]
    if old_footer_block != new_footer_block:
        content = content[:start_idx] + new_footer_block + content[end_idx + len(end_marker):]
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


# Process all pages
files = [
    ("ru/index.html", ""),
    ("ru/about.html", ""),
    ("ru/contact.html", ""),
    ("ru/book-covers.html", ""),
    ("ru/book-illustrations.html", ""),
    ("ru/visual-stories.html", ""),
    ("ru/services.html", ""),
    ("ru/reviews.html", ""),
    ("ru/faq.html", ""),
    ("ru/personal.html", ""),
    ("ru/blog/index.html", "../"),
    ("ru/blog/skolko-stoit-oblozhka-knigi.html", "../"),
    ("ru/blog/trendy-dizaina-oblozhek-2026.html", "../"),
    ("ru/blog/kak-vybrat-illyustratora-oblozhki.html", "../"),
    ("ru/blog/ot-brifa-do-finalnogo-arta-protsess.html", "../"),
    ("ru/blog/chastye-oshibki-pri-vybore-illyustratora.html", "../"),
]

fixed = 0
for relpath, prefix in files:
    filepath = os.path.join(BASE, relpath.replace("/", os.sep))
    if not os.path.exists(filepath):
        print(f"MISSING: {relpath}")
        continue
    if fix_footer(filepath, prefix):
        print(f"FIXED: {relpath}")
        fixed += 1
    else:
        print(f"OK: {relpath}")

print(f"\nTotal fixed: {fixed}")
