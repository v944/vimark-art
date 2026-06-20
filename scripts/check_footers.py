import os, re

BASE = "D:\\Concept_work\\Vimark_art"

pages = [
    ("ru/index.html", ), ("ru/contact.html", ), ("ru/book-covers.html", ),
    ("ru/faq.html", ), ("ru/reviews.html", ), ("ru/services.html", ),
    ("ru/book-illustrations.html", ), ("ru/visual-stories.html", ),
]

for (p,) in pages:
    path = os.path.join(BASE, p.replace("/", os.sep))
    with open(path, encoding="utf-8") as f:
        c = f.read()

    # Find footer-links section
    m = re.search(r'<div class="footer-links">(.*?)</div>', c, re.DOTALL)
    if m:
        footer = m.group(1)
        has_work = 'href="work.html">Работы' in footer
        has_blog_ru = 'href="blog/">Блог' in footer
        print(f"{p:35s} work={has_work} blog_ru={has_blog_ru}")
    else:
        print(f"{p:35s} NO FOOTER")

# Also check blog RU pages
print()
blog_pages = [
    ("ru/blog/index.html", ), ("ru/blog/skolko-stoit-oblozhka-knigi.html", ),
    ("ru/blog/trendy-dizaina-oblozhek-2026.html", ),
]
for (p,) in blog_pages:
    path = os.path.join(BASE, p.replace("/", os.sep))
    if not os.path.exists(path):
        print(f"MISSING: {p}")
        continue
    with open(path, encoding="utf-8") as f:
        c = f.read()
    m = re.search(r'<div class="footer-links">(.*?)</div>', c, re.DOTALL)
    if m:
        footer = m.group(1)
        has_work = 'href="../work.html">Работы' in footer
        has_blog_ru = 'href="../blog/">Блог' in footer
        print(f"{p:35s} work={has_work} blog_ru={has_blog_ru}")
    else:
        print(f"{p:35s} NO FOOTER")
