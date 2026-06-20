import os

BASE = "D:\\Concept_work\\Vimark_art"

# Fix ru/ pages: they should use direct paths, not ../ prefixed ones
paths = [
    "ru/index.html", "ru/about.html", "ru/contact.html",
    "ru/book-covers.html", "ru/book-illustrations.html",
    "ru/visual-stories.html", "ru/services.html",
    "ru/reviews.html", "ru/faq.html", "ru/personal.html",
]

reps = {
    'href="../work.html"': 'href="work.html"',
    'href="../services.html"': 'href="services.html"',
    'href="../about.html"': 'href="about.html"',
    'href="../contact.html"': 'href="contact.html"',
    'href="../book-covers.html"': 'href="book-covers.html"',
    'href="../book-illustrations.html"': 'href="book-illustrations.html"',
    'href="../visual-stories.html"': 'href="visual-stories.html"',
    'href="../reviews.html"': 'href="reviews.html"',
    'href="../faq.html"': 'href="faq.html"',
    'href="../living-illustrations.html"': 'href="living-illustrations.html"',
    'href="../404.html"': 'href="404.html"',
    'href="../case-studies/': 'href="case-studies/',
    'href="../blog/': 'href="blog/',
}

for p in paths:
    filepath = os.path.join(BASE, p.replace("/", os.sep))
    with open(filepath, "r", encoding="utf-8") as f:
        c = f.read()

    changed = False
    for old, new in reps.items():
        if old in c:
            c = c.replace(old, new)
            changed = True

    # Also fix special case: ../Max Mitenkov.png -> ../Max Mitenkov.png should stay as-is
    # And ../behance.png -> ../behance.png should stay as-is for image src

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"FIXED: {p}")
    else:
        print(f"OK: {p}")
