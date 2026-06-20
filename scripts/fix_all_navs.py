import os, re

BASE = "D:\\Concept_work\\Vimark_art"

# ── Files with the OLD nav (8-10 items) → replace the entire nav block ──
old_nav_files = [
    # EN
    ("404.html", """
        <nav class="main-nav">
          <ul>
            <li><a href="/#work">Work</a></li>
            <li><a href="services.html">Services</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="blog/">Blog</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </nav>"""),
    ("living-illustrations.html", """
        <nav class="main-nav">
          <ul>
            <li><a href="/#work">Work</a></li>
            <li><a href="services.html">Services</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="blog/">Blog</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </nav>"""),
    ("comic.html", """
        <nav class="main-nav">
          <ul>
            <li><a href="/#work">Work</a></li>
            <li><a href="services.html">Services</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="blog/">Blog</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </nav>"""),
    ("bookcover.html", """
        <nav class="main-nav">
          <ul>
            <li><a href="/#work">Work</a></li>
            <li><a href="services.html">Services</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="blog/">Blog</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </nav>"""),
    # RU
    ("ru/living-illustrations.html", """
        <nav class="main-nav">
          <ul>
            <li><a href="/ru/#work">Работы</a></li>
            <li><a href="services.html">Услуги</a></li>
            <li><a href="about.html">Обо мне</a></li>
            <li><a href="blog/">Блог</a></li>
            <li><a href="contact.html">Контакты</a></li>
          </ul>
        </nav>"""),
    ("ru/comic.html", """
        <nav class="main-nav">
          <ul>
            <li><a href="/ru/#work">Работы</a></li>
            <li><a href="services.html">Услуги</a></li>
            <li><a href="about.html">Обо мне</a></li>
            <li><a href="blog/">Блог</a></li>
            <li><a href="contact.html">Контакты</a></li>
          </ul>
        </nav>"""),
    ("ru/bookcover.html", """
        <nav class="main-nav">
          <ul>
            <li><a href="/ru/#work">Работы</a></li>
            <li><a href="services.html">Услуги</a></li>
            <li><a href="about.html">Обо мне</a></li>
            <li><a href="blog/">Блог</a></li>
            <li><a href="contact.html">Контакты</a></li>
          </ul>
        </nav>"""),
]

for fname, new_nav in old_nav_files:
    path = os.path.join(BASE, fname.replace("/", os.sep))
    if not os.path.exists(path):
        print(f"MISSING: {fname}")
        continue
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    # Find <nav class="main-nav">...</nav> block
    m = re.search(r'<nav class="main-nav">.*?</nav>', content, re.DOTALL)
    if m:
        old_block = m.group(0)
        content = content.replace(old_block, new_nav, 1)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(content)
        print(f"FIXED (old nav): {fname}")
    else:
        print(f"NO NAV FOUND: {fname}")

# ── Files with 4-item nav (missing Blog) → add Blog after About ──
four_item_files = [
    # EN
    "about.html", "services.html", "contact.html", "reviews.html",
    "faq.html", "personal.html", "book-covers.html", "book-illustrations.html",
    "visual-stories.html", "case-studies.html",
    "case-studies/hoebeke-sci-fi-series.html",
    # RU
    "ru/about.html", "ru/services.html", "ru/contact.html", "ru/reviews.html",
    "ru/faq.html", "ru/personal.html", "ru/book-covers.html", "ru/book-illustrations.html",
    "ru/visual-stories.html", "ru/case-studies.html",
    "ru/case-studies/hoebeke-sci-fi-series.html",
]

# For EN files, add Blog after About
# For RU files, add Блог after Обо мне

for fname in four_item_files:
    path = os.path.join(BASE, fname.replace("/", os.sep))
    if not os.path.exists(path):
        print(f"MISSING: {fname}")
        continue
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    
    # EN: <li><a href="about.html">About</a></li> → add Blog after
    # Need to handle both relative paths: href="about.html" and href="../about.html"
    
    en_blog_after = '<li><a href="blog/">Blog</a></li>\n'
    en_patterns = [
        ('<li><a href="about.html">About</a></li>\n          <li><a href="contact.html">', 
         '<li><a href="about.html">About</a></li>\n          ' + en_blog_after + '          <li><a href="contact.html">'),
        ('<li><a href="../about.html">About</a></li>\n          <li><a href="../contact.html">',
         '<li><a href="../about.html">About</a></li>\n          ' + '<li><a href="../blog/">Blog</a></li>\n' + '          <li><a href="../contact.html">'),
    ]
    
    ru_blog_after = '<li><a href="blog/">Блог</a></li>\n'
    ru_patterns = [
        ('<li><a href="about.html">Обо мне</a></li>\n          <li><a href="contact.html">',
         '<li><a href="about.html">Обо мне</a></li>\n          ' + ru_blog_after + '          <li><a href="contact.html">'),
        ('<li><a href="../about.html">Обо мне</a></li>\n          <li><a href="../contact.html">',
         '<li><a href="../about.html">Обо мне</a></li>\n          ' + '<li><a href="../blog/">Блог</a></li>\n' + '          <li><a href="../contact.html">'),
    ]
    
    changed = False
    for old, new in en_patterns + ru_patterns:
        if old in content:
            content = content.replace(old, new, 1)
            changed = True
            print(f"FIXED (4-item): {fname}")
            break
    
    if not changed:
        # Check if the file already has the correct 5-item nav (skip)
        if 'Blog' in content or 'Блог' in content:
            if '<li><a href="blog/">' in content or '<li><a href="../blog/">' in content:
                print(f"ALREADY OK: {fname}")
                continue
        print(f"NO MATCH: {fname}")
        continue
    
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)

print("\nDone!")
