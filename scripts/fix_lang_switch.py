import os

BASE = "D:\\Concept_work\\Vimark_art"

files = [
    "index.html", "about.html", "contact.html", "book-covers.html",
    "book-illustrations.html", "visual-stories.html", "services.html",
    "reviews.html", "faq.html", "404.html", "thanks.html", "privacy.html",
    "personal.html",
    "ru/index.html", "ru/about.html", "ru/contact.html",
    "ru/book-covers.html", "ru/book-illustrations.html",
    "ru/visual-stories.html", "ru/services.html", "ru/reviews.html",
    "ru/faq.html", "ru/personal.html",
    "case-studies/hoebeke-sci-fi-series.html",
    "ru/case-studies/hoebeke-sci-fi-series.html",
    "blog/index.html", "blog/how-much-does-a-book-cover-cost.html",
    "blog/book-cover-design-trends-2026.html",
    "blog/how-to-choose-book-cover-illustrator.html",
    "blog/from-brief-to-final-art-process.html",
    "blog/common-mistakes-when-hiring-illustrator.html",
    "ru/blog/index.html", "ru/blog/skolko-stoit-oblozhka-knigi.html",
    "ru/blog/trendy-dizaina-oblozhek-2026.html",
    "ru/blog/kak-vybrat-illyustratora-oblozhki.html",
    "ru/blog/ot-brifa-do-finalnogo-arta-protsess.html",
    "ru/blog/chastye-oshibki-pri-vybore-illyustratora.html",
]

added = 0
for f in files:
    path = os.path.join(BASE, f.replace("/", os.sep))
    if not os.path.exists(path):
        print(f"MISSING: {f}")
        continue
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    if "/work.html" in content:
        continue
    marker = '"/404.html":"/ru/404.html",'
    if marker in content:
        content = content.replace(
            marker,
            marker + '"/work.html":"/ru/work.html","/ru/work.html":"/work.html",'
        )
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(content)
        print(f"FIXED: {f}")
        added += 1
    else:
        print(f"MARKER NOT FOUND: {f}")

print(f"\nTotal fixed: {added}")
