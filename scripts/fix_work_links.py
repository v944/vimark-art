import os, re

BASE = "D:\\Concept_work\\Vimark_art"

# All static HTML files that might contain work.html links
files = [
    # Root EN
    "index.html", "about.html", "contact.html", "book-covers.html",
    "book-illustrations.html", "visual-stories.html", "services.html",
    "reviews.html", "faq.html", "404.html", "thanks.html", "privacy.html",
    "personal.html",
    # Root RU
    "ru/index.html", "ru/about.html", "ru/contact.html",
    "ru/book-covers.html", "ru/book-illustrations.html",
    "ru/visual-stories.html", "ru/services.html", "ru/reviews.html",
    "ru/faq.html", "ru/personal.html",
    # Case study root
    "case-studies.html",
    # Case studies subdir
    "case-studies/hoebeke-sci-fi-series.html",
    "ru/case-studies.html",
    "ru/case-studies/hoebeke-sci-fi-series.html",
    # Blog EN
    "blog/index.html", "blog/how-much-does-a-book-cover-cost.html",
    "blog/book-cover-design-trends-2026.html",
    "blog/how-to-choose-book-cover-illustrator.html",
    "blog/from-brief-to-final-art-process.html",
    "blog/common-mistakes-when-hiring-illustrator.html",
    # Blog RU
    "ru/blog/index.html", "ru/blog/skolko-stoit-oblozhka-knigi.html",
    "ru/blog/trendy-dizaina-oblozhek-2026.html",
    "ru/blog/kak-vybrat-illyustratora-oblozhki.html",
    "ru/blog/ot-brifa-do-finalnogo-arta-protsess.html",
    "ru/blog/chastye-oshibki-pri-vybore-illyustratora.html",
]

# Also get all project pages
project_dir = os.path.join(BASE, "project")
for fname in os.listdir(project_dir):
    if fname.endswith(".html"):
        files.append(f"project/{fname}")

ru_project_dir = os.path.join(BASE, "ru", "project")
for fname in os.listdir(ru_project_dir):
    if fname.endswith(".html"):
        files.append(f"ru/project/{fname}")

# Art pages
art_dir = os.path.join(BASE, "project", "art")
for fname in os.listdir(art_dir):
    if fname.endswith(".html"):
        files.append(f"project/art/{fname}")

ru_art_dir = os.path.join(BASE, "ru", "project", "art")
for fname in os.listdir(ru_art_dir):
    if fname.endswith(".html"):
        files.append(f"ru/project/art/{fname}")

changes = 0
for f in files:
    path = os.path.join(BASE, f.replace("/", os.sep))
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()

    original = content

    # EN nav: href="work.html" in sidebar nav
    content = content.replace('href="work.html">Work', 'href="/#work">Work')

    # EN nav: href="../work.html" in subdirs
    content = content.replace('href="../work.html">Work', 'href="/#work">Work')

    # RU nav: href="work.html">Работы
    content = content.replace('href="work.html">Работы', 'href="/ru/#work">Работы')

    # RU nav: href="../work.html">Работы
    content = content.replace('href="../work.html">Работы', 'href="/ru/#work">Работы')

    # EN footer: href="work.html">Work
    content = content.replace('href="work.html">Work</a>', 'href="/#work">Work</a>')

    # EN footer: href="../work.html">Work
    content = content.replace('href="../work.html">Work</a>', 'href="/#work">Work</a>')

    # RU footer: href="work.html">Работы
    content = content.replace('href="work.html">Работы</a>', 'href="/ru/#work">Работы</a>')

    # RU footer: href="../work.html">Работы
    content = content.replace('href="../work.html">Работы</a>', 'href="/ru/#work">Работы</a>')

    if content != original:
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(content)
        print(f"UPDATED: {f}")
        changes += 1

print(f"\nTotal files updated: {changes}")
