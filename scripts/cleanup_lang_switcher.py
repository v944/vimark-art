import os

BASE = "D:\\Concept_work\\Vimark_art"

files = [
    "index.html", "about.html", "contact.html", "book-covers.html",
    "book-illustrations.html", "visual-stories.html", "services.html",
    "reviews.html", "faq.html", "personal.html",
    "case-studies.html", "ru/case-studies.html",
]

target = '"/work.html":"/ru/work.html","/ru/work.html":"/work.html",'

for f in files:
    path = os.path.join(BASE, f.replace("/", os.sep))
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    if target in content:
        content = content.replace(target, "")
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(content)
        print(f"CLEANED: {f}")
    else:
        print(f"SKIPPED (not found): {f}")
