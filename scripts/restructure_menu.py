"""
Menu restructure script:
- Creates /work.html and /ru/work.html
- Updates all static HTML files: new nav (4 items), new footer (all links)
- Adds Reviews section to about pages
- Adds FAQ accordion to contact pages
- Updates lang-switch mappings
"""
import os
import re

BASE = r"D:\Concept_work\Vimark_art"

# Templates
NEW_NAV_EN = """        <nav class="main-nav">
        <ul>
          <li><a href="work.html">Work</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </nav>
      <a href="/contact.html" class="cta-button">Get a Free Quote</a>"""

NEW_NAV_RU = """        <nav class="main-nav">
        <ul>
          <li><a href="work.html">Работы</a></li>
          <li><a href="services.html">Услуги</a></li>
          <li><a href="about.html">Обо мне</a></li>
          <li><a href="contact.html">Контакты</a></li>
        </ul>
      </nav>
      <a href="/ru/contact.html" class="cta-button">Обсудить проект</a>"""

NEW_NAV_CASE_EN = """        <nav class="main-nav">
        <ul>
          <li><a href="../work.html">Work</a></li>
          <li><a href="../services.html">Services</a></li>
          <li><a href="../about.html">About</a></li>
          <li><a href="../contact.html">Contact</a></li>
        </ul>
      </nav>
      <a href="/contact.html" class="cta-button">Get a Free Quote</a>"""

NEW_NAV_CASE_RU = """        <nav class="main-nav">
        <ul>
          <li><a href="../work.html">Работы</a></li>
          <li><a href="../services.html">Услуги</a></li>
          <li><a href="../about.html">Обо мне</a></li>
          <li><a href="../contact.html">Контакты</a></li>
        </ul>
      </nav>
      <a href="/ru/contact.html" class="cta-button">Обсудить проект</a>"""

NEW_FOOTER_LINKS_EN = """      <p>
        <a href="work.html">Work</a> ·
        <a href="services.html">Services</a> ·
        <a href="about.html">About</a> ·
        <a href="contact.html">Contact</a> ·
        <a href="book-covers.html">Book Covers</a> ·
        <a href="book-illustrations.html">Illustrations</a> ·
        <a href="visual-stories.html">Visual Stories</a> ·
        <a href="case-studies/hoebeke-sci-fi-series.html">Case Studies</a> ·
        <a href="reviews.html">Reviews</a> ·
        <a href="faq.html">FAQ</a> ·
      <a href="blog/">Blog</a></p>"""

NEW_FOOTER_LINKS_RU = """      <p>
        <a href="work.html">Работы</a> ·
        <a href="services.html">Услуги</a> ·
        <a href="about.html">Обо мне</a> ·
        <a href="contact.html">Контакты</a> ·
        <a href="book-covers.html">Обложки книг</a> ·
        <a href="book-illustrations.html">Иллюстрации к книгам</a> ·
        <a href="visual-stories.html">Визуальные истории</a> ·
        <a href="case-studies/hoebeke-sci-fi-series.html">Кейсы</a> ·
        <a href="reviews.html">Отзывы</a> ·
        <a href="faq.html">FAQ</a> ·
      <a href="blog/">Блог</a></p>"""

NEW_FOOTER_CASE_EN = NEW_FOOTER_LINKS_EN.replace('href="', 'href="../')
NEW_FOOTER_CASE_RU = NEW_FOOTER_LINKS_RU.replace('href="', 'href="../')

REVIEWS_SECTION_EN = """      <hr class="about-divider">

      <h2>Reviews</h2>
      <p><strong>71 verified reviews</strong> on <a href="https://www.reedsy.com/vimark" target="_blank" rel="noopener">Reedsy</a> · 5.0 rating</p>
      <p><a href="reviews.html">View all reviews &rarr;</a></p>"""

REVIEWS_SECTION_RU = """      <hr class="about-divider">

      <h2>Отзывы</h2>
      <p><strong>71 проверенных отзыва</strong> на <a href="https://www.reedsy.com/vimark" target="_blank" rel="noopener">Reedsy</a> · Рейтинг 5.0</p>
      <p><a href="reviews.html">Смотреть все отзывы &rarr;</a></p>"""

FAQ_SECTION_EN = """      <hr class="contact-divider">

      <section id="faq" class="contact-faq">
        <h2>Frequently Asked Questions</h2>
        <details>
          <summary>How long does it take to create a book cover?</summary>
          <p>Typically 2–4 weeks depending on complexity. Rushed orders may be available for an additional fee.</p>
        </details>
        <details>
          <summary>Do you work with self-published authors?</summary>
          <p>Yes. I work with both indie authors and major publishers. Every project receives the same level of attention and quality.</p>
        </details>
        <details>
          <summary>What formats do you deliver?</summary>
          <p>High-resolution print-ready files (CMYK), web-optimized versions (RGB), and layered source files upon request.</p>
        </details>
        <details>
          <summary>How do I start a project?</summary>
          <p>Use the contact form above or email me directly at hello@vimark.art with a brief description of your project.</p>
        </details>
        <details>
          <summary>What if I need revisions?</summary>
          <p>Each project includes a revision round. Additional revisions are available at an agreed rate.</p>
        </details>
        <p><a href="faq.html">View all FAQ &rarr;</a></p>
      </section>"""

FAQ_SECTION_RU = """      <hr class="contact-divider">

      <section id="faq" class="contact-faq">
        <h2>Часто задаваемые вопросы</h2>
        <details>
          <summary>Сколько времени занимает создание обложки книги?</summary>
          <p>Обычно 2–4 недели в зависимости от сложности. Срочные заказы возможны за дополнительную плату.</p>
        </details>
        <details>
          <summary>Работаете ли вы с самиздатом?</summary>
          <p>Да. Я работаю как с независимыми авторами, так и с крупными издательствами. Каждый проект получает одинаковый уровень внимания и качества.</p>
        </details>
        <details>
          <summary>В каких форматах вы сдаёте работу?</summary>
          <p>Высококачественные файлы для печати (CMYK), веб-версии (RGB) и исходные файлы по запросу.</p>
        </details>
        <details>
          <summary>Как начать проект?</summary>
          <p>Используйте форму связи выше или напишите мне напрямую на hello@vimark.art с кратким описанием вашего проекта.</p>
        </details>
        <details>
          <summary>Что если нужны правки?</summary>
          <p>Каждый проект включает раунд правок. Дополнительные правки — по согласованной ставке.</p>
        </details>
        <p><a href="faq.html">Все вопросы &rarr;</a></p>
      </section>"""


def main():
    # ── 1. Create /work.html (EN) ──
    create_work_en()
    # ── 2. Create /ru/work.html (RU) ──
    create_work_ru()
    # ── 3. Update all static HTML files ──
    update_all_files()
    # ── 4. Add Reviews to about pages ──
    add_reviews_to_about()
    # ── 5. Add FAQ to contact pages ──
    add_faq_to_contact()


def get_sidebar_style():
    return """        <img src="Max Mitenkov.png" alt="Max Mitenkov" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
"""

def get_sidebar_style_ru():
    return """        <img src="../Max Mitenkov.png" alt="Максим Митенков" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;">
"""


def create_work_en():
    path = os.path.join(BASE, "work.html")
    if os.path.exists(path):
        print("work.html already exists, skipping")
        return
    content = r"""<!DOCTYPE html>
<html lang="en">
<head>
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="msvalidate.01" content="AB1E76A05E75CD49B462D5745E8337FF">
<meta name="robots" content="index, follow">
<title>Portfolio · Book Covers & Illustrations · Max Mitenkov</title>
<meta name="description" content="Portfolio of Max Mitenkov: book cover design, book illustrations, visual stories and case studies for sci-fi, fantasy and horror publishing.">
<link rel="canonical" href="https://vimark.art/work.html">
<!-- hreflang -->
<link rel="alternate" hreflang="en" href="https://vimark.art/work.html" />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/work.html" />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/work.html" />
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="vimark_typography_system.css">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="icon-192.png">
<link rel="manifest" href="manifest.json">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vimark.art/work.html">
<meta property="og:title" content="Portfolio · Book Covers & Illustrations · Max Mitenkov">
<meta property="og:description" content="Portfolio of Max Mitenkov: book cover design, book illustrations, visual stories and case studies.">
<meta property="og:image" content="https://vimark.art/thumbnails/STRONG/faceless2.webp">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="300">
<link rel="image_src" href="https://vimark.art/thumbnails/STRONG/faceless2.webp">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vimark.art/work.html">
<meta property="twitter:title" content="Portfolio · Book Covers & Illustrations · Max Mitenkov">
<meta property="twitter:description" content="Portfolio of Max Mitenkov: book cover design, book illustrations, visual stories and case studies.">
<meta property="twitter:image" content="https://vimark.art/thumbnails/STRONG/faceless2.webp">
<meta property="twitter:site" content="@vimark_art">
<meta property="twitter:creator" content="@vimark_art">

<!-- Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Portfolio · Max Mitenkov",
  "description": "Book cover design, illustrations, visual stories and case studies.",
  "url": "https://vimark.art/work.html",
  "isPartOf": {
    "@type": "WebSite",
    "name": "vimark.art",
    "url": "https://vimark.art"
  },
  "hasPart": [
    {
      "@type": "WebPage",
      "name": "Book Covers",
      "url": "https://vimark.art/book-covers.html"
    },
    {
      "@type": "WebPage",
      "name": "Book Illustrations",
      "url": "https://vimark.art/book-illustrations.html"
    },
    {
      "@type": "WebPage",
      "name": "Visual Stories",
      "url": "https://vimark.art/visual-stories.html"
    },
    {
      "@type": "CreativeWork",
      "name": "Case Study: Hoëbeke Sci-Fi Series",
      "url": "https://vimark.art/case-studies/hoebeke-sci-fi-series.html"
    }
  ]
}
</script>
</head>
<body class="work-page">
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
""" + get_sidebar_style() + NEW_NAV_EN + """
      </header>
      <div class="social-links">
      <a href="mailto:hello@vimark.art" aria-label="Email"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
      <a href="https://www.facebook.com/maks.vimark/" aria-label="Facebook"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
      <a href="https://www.linkedin.com/in/maxim-mitenkov-06192940/" aria-label="LinkedIn"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
      <a href="https://www.instagram.com/vimark_art/" aria-label="Instagram"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
      <a href="https://www.behance.net/vimark" aria-label="Behance"><img src="behance.png" alt="Behance" class="social-icon"></a>
      <a href="https://www.deviantart.com/vimark" aria-label="DeviantArt"><img src="deviantart.png" alt="DeviantArt" class="social-icon"></a>
    </div>
      <div class="commissions-status"><span class="status-dot"></span><span>Open for commissions</span></div>
      <a href="index.html" class="logo-link"><img src="vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>

    <button class="mobile-toggle">Menu</button>

    <main id="main">
      <section class="work-hero">
        <h1>Work</h1>
        <p class="lead">Book cover design, illustrations and visual stories for publishing.</p>
      </section>

      <!-- Case Study Banner -->
      <section class="case-study-banner" aria-label="Featured case study">
        <a href="case-studies/hoebeke-sci-fi-series.html">
          <img src="images/case-study/planetes-cover.jpg" alt="Hoëbeke Sci-Fi Series case study" loading="eager">
          <div class="banner-text">
            <span class="label">Case Study</span>
            <h2>Hoëbeke Sci-Fi Series</h2>
            <p>7 covers for Hachette Livre · Consistent series design</p>
          </div>
        </a>
      </section>

      <!-- Grid -->
      <section class="work-grid" aria-label="Portfolio categories">
        <article>
          <a href="book-covers.html">
            <img src="thumbnails/STRONG/nemirum_cover.webp" alt="Book cover design by Max Mitenkov" loading="lazy">
            <h2>Book Covers</h2>
            <p>Custom covers for sci-fi, fantasy and horror</p>
          </a>
        </article>
        <article>
          <a href="book-illustrations.html">
            <img src="thumbnails/illustrations/endymion.webp" alt="Book illustrations by Max Mitenkov" loading="lazy">
            <h2>Book Illustrations</h2>
            <p>Interior art for novels and series</p>
          </a>
        </article>
        <article>
          <a href="visual-stories.html">
            <img src="thumbnails/visual-stories/faceless.webp" alt="Visual stories and comics by Max Mitenkov" loading="lazy">
            <h2>Visual Stories</h2>
            <p>Comics and sequential art</p>
          </a>
        </article>
      </section>
    </main>
  </div>

          <footer class="site-footer">
    <span><b>&copy;</b> Max Mitenkov, 2026.</span>
    <div class="footer-links">
""" + NEW_FOOTER_LINKS_EN + """
      <p>
        <a href="https://reedsy.com/freelancers/maxim-m" target="_blank" rel="noopener">Reedsy</a> ·
        <a href="https://www.behance.net/vimark" target="_blank" rel="noopener">Behance</a> ·
        <a href="https://www.artstation.com/vimark" target="_blank" rel="noopener">ArtStation</a> ·
        <a href="https://www.instagram.com/vimark_art/" target="_blank" rel="noopener">Instagram</a> ·
        <a href="https://www.pinterest.com/vimark" target="_blank" rel="noopener">Pinterest</a> ·
        <a href="https://www.deviantart.com/vimark" target="_blank" rel="noopener">DeviantArt</a>
      </p>
    </div>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){var p=location.pathname.replace(/\\/g,"/");var h=location.hash;if(p==="/"||p==="")p="/index.html";var i=p.indexOf("/ru/")!==-1;var e=document.getElementById("lang-en");var r=document.getElementById("lang-ru");var m={"/index.html":"/ru/index.html","/about.html":"/ru/about.html","/work.html":"/ru/work.html","/book-covers.html":"/ru/book-covers.html","/book-illustrations.html":"/ru/book-illustrations.html","/visual-stories.html":"/ru/visual-stories.html","/contact.html":"/ru/contact.html","/reviews.html":"/ru/reviews.html","/faq.html":"/ru/faq.html","/services.html":"/ru/services.html","/case-studies/hoebeke-sci-fi-series.html":"/ru/case-studies/hoebeke-sci-fi-series.html","/living-illustrations.html":"/ru/living-illustrations.html","/404.html":"/ru/404.html","/ru/index.html":"/index.html","/ru/about.html":"/about.html","/ru/work.html":"/work.html","/ru/book-covers.html":"/book-covers.html","/ru/book-illustrations.html":"/book-illustrations.html","/ru/visual-stories.html":"/visual-stories.html","/ru/contact.html":"/contact.html","/ru/reviews.html":"/reviews.html","/ru/faq.html":"/faq.html","/ru/services.html":"/services.html","/ru/case-studies/hoebeke-sci-fi-series.html":"/case-studies/hoebeke-sci-fi-series.html","/ru/living-illustrations.html":"/living-illustrations.html","/ru/404.html":"/404.html"};if(i){e.href=(m[p]||p.replace("/ru/","/"))+h;r.href=p+h;}else{r.href=(m[p]||p.replace("/project/","/ru/project/"))+h;e.href=p+h;}if(i){r.classList.add("active");}else{e.classList.add("active");}})();</script>
  </footer>

  <div class="sticky-contact">
      <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener" aria-label="Telegram" onclick="if(typeof gtag!=='undefined')gtag('event','click_telegram');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_telegram');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.198 2.433a2.242 2.242 0 0 0-1.022.215l-16.031 6.26a2.27 2.27 0 0 0-.093 4.07l3.827 1.558 1.56 4.44a1.5 1.5 0 0 0 2.663.52l2.33-3.14 3.75 2.83a2.27 2.27 0 0 0 3.58-1.74L22.34 3.89a2.24 2.24 0 0 0-1.142-1.457z"/></svg></a>
      <a href="https://wa.me/375296534382" target="_blank" rel="noopener" aria-label="WhatsApp" onclick="if(typeof gtag!=='undefined')gtag('event','click_whatsapp');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_whatsapp');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></a>
    </div>
  <button id="scrollTop" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">↑</button>
  <script src="script.js"></script>
  <div class="mobile-cta"><a href="/contact.html" class="cta-button">Get a Free Quote</a></div>
</body>
</html>"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created work.html")


def create_work_ru():
    path = os.path.join(BASE, "ru", "work.html")
    if os.path.exists(path):
        print("ru/work.html already exists, skipping")
        return
    content = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="dns-prefetch" href="https://www.google-analytics.com">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="msvalidate.01" content="AB1E76A05E75CD49B462D5745E8337FF">
<meta name="robots" content="index, follow">
<title>Портфолио · Обложки и иллюстрации · Максим Митенков</title>
<meta name="description" content="Портфолио Максима Митенкова: дизайн обложек книг, иллюстрации, визуальные истории и кейсы для научной фантастики, фэнтези и хоррора.">
<link rel="canonical" href="https://vimark.art/ru/work.html">
<!-- hreflang -->
<link rel="alternate" hreflang="en" href="https://vimark.art/work.html" />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/work.html" />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/work.html" />
<link rel="stylesheet" href="../style.css">
<link rel="stylesheet" href="../vimark_typography_system.css">
<link rel="icon" type="image/x-icon" href="../favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="../icon-192.png">
<link rel="manifest" href="../manifest.json">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://vimark.art/ru/work.html">
<meta property="og:title" content="Портфолио · Обложки и иллюстрации · Максим Митенков">
<meta property="og:description" content="Портфолио Максима Митенкова: дизайн обложек книг, иллюстрации к книгам, визуальные истории и кейсы.">
<meta property="og:image" content="https://vimark.art/thumbnails/STRONG/faceless2.webp">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="300">
<link rel="image_src" href="https://vimark.art/thumbnails/STRONG/faceless2.webp">

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://vimark.art/ru/work.html">
<meta property="twitter:title" content="Портфолио · Обложки и иллюстрации · Максим Митенков">
<meta property="twitter:description" content="Портфолио Максима Митенкова: дизайн обложек книг, иллюстрации, визуальные истории и кейсы.">
<meta property="twitter:image" content="https://vimark.art/thumbnails/STRONG/faceless2.webp">
<meta property="twitter:site" content="@vimark_art">
<meta property="twitter:creator" content="@vimark_art">

<!-- Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Портфолио · Максим Митенков",
  "description": "Дизайн обложек книг, иллюстрации, визуальные истории и кейсы.",
  "url": "https://vimark.art/ru/work.html",
  "isPartOf": {
    "@type": "WebSite",
    "name": "vimark.art",
    "url": "https://vimark.art"
  }
}
</script>
</head>
<body class="work-page">
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
""" + get_sidebar_style_ru() + NEW_NAV_RU + """
      </header>
      <div class="social-links">
      <a href="mailto:hello@vimark.art" aria-label="Email"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>
      <a href="https://www.facebook.com/maks.vimark/" aria-label="Facebook"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg></a>
      <a href="https://www.linkedin.com/in/maxim-mitenkov-06192940/" aria-label="LinkedIn"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></a>
      <a href="https://www.instagram.com/vimark_art/" aria-label="Instagram"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
      <a href="https://www.behance.net/vimark" aria-label="Behance"><img src="../behance.png" alt="Behance" class="social-icon"></a>
      <a href="https://www.deviantart.com/vimark" aria-label="DeviantArt"><img src="../deviantart.png" alt="DeviantArt" class="social-icon"></a>
    </div>
      <div class="commissions-status"><span class="status-dot"></span><span>Open for commissions</span></div>
      <a href="index.html" class="logo-link"><img src="../vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>

    <button class="mobile-toggle">Меню</button>

    <main id="main">
      <section class="work-hero">
        <h1>Работы</h1>
        <p class="lead">Дизайн обложек книг, иллюстрации и визуальные истории для издательств.</p>
      </section>

      <!-- Баннер кейса -->
      <section class="case-study-banner" aria-label="Featured case study">
        <a href="../case-studies/hoebeke-sci-fi-series.html">
          <img src="../images/case-study/planetes-cover.jpg" alt="Hoëbeke Sci-Fi Series" loading="eager">
          <div class="banner-text">
            <span class="label">Кейс</span>
            <h2>Hoëbeke Sci-Fi Series</h2>
            <p>7 обложек для Hachette Livre · Единый дизайн серии</p>
          </div>
        </a>
      </section>

      <!-- Сетка -->
      <section class="work-grid" aria-label="Категории портфолио">
        <article>
          <a href="../book-covers.html">
            <img src="../thumbnails/STRONG/nemirum_cover.webp" alt="Обложки книг" loading="lazy">
            <h2>Обложки книг</h2>
            <p>Обложки для научной фантастики, фэнтези и хоррора</p>
          </a>
        </article>
        <article>
          <a href="../book-illustrations.html">
            <img src="../thumbnails/illustrations/endymion.webp" alt="Иллюстрации к книгам" loading="lazy">
            <h2>Иллюстрации к книгам</h2>
            <p>Интерьерные иллюстрации для романов и серий</p>
          </a>
        </article>
        <article>
          <a href="../visual-stories.html">
            <img src="../thumbnails/visual-stories/faceless.webp" alt="Визуальные истории" loading="lazy">
            <h2>Визуальные истории</h2>
            <p>Комиксы и последовательное искусство</p>
          </a>
        </article>
      </section>
    </main>
  </div>

          <footer class="site-footer">
    <span><b>&copy;</b> Max Mitenkov, 2026.</span>
    <div class="footer-links">
""" + NEW_FOOTER_LINKS_RU.replace('href="', 'href="../') + """
      <p>
        <a href="https://reedsy.com/freelancers/maxim-m" target="_blank" rel="noopener">Reedsy</a> ·
        <a href="https://www.behance.net/vimark" target="_blank" rel="noopener">Behance</a> ·
        <a href="https://www.artstation.com/vimark" target="_blank" rel="noopener">ArtStation</a> ·
        <a href="https://www.instagram.com/vimark_art/" target="_blank" rel="noopener">Instagram</a> ·
        <a href="https://www.pinterest.com/vimark" target="_blank" rel="noopener">Pinterest</a> ·
        <a href="https://www.deviantart.com/vimark" target="_blank" rel="noopener">DeviantArt</a>
      </p>
    </div>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>(function(){var p=location.pathname.replace(/\\/g,"/");var h=location.hash;if(p==="/"||p==="")p="/index.html";var i=p.indexOf("/ru/")!==-1;var e=document.getElementById("lang-en");var r=document.getElementById("lang-ru");var m={"/index.html":"/ru/index.html","/about.html":"/ru/about.html","/work.html":"/ru/work.html","/book-covers.html":"/ru/book-covers.html","/book-illustrations.html":"/ru/book-illustrations.html","/visual-stories.html":"/ru/visual-stories.html","/contact.html":"/ru/contact.html","/reviews.html":"/ru/reviews.html","/faq.html":"/ru/faq.html","/services.html":"/ru/services.html","/case-studies/hoebeke-sci-fi-series.html":"/ru/case-studies/hoebeke-sci-fi-series.html","/living-illustrations.html":"/ru/living-illustrations.html","/404.html":"/ru/404.html","/ru/index.html":"/index.html","/ru/about.html":"/about.html","/ru/work.html":"/work.html","/ru/book-covers.html":"/book-covers.html","/ru/book-illustrations.html":"/book-illustrations.html","/ru/visual-stories.html":"/visual-stories.html","/ru/contact.html":"/contact.html","/ru/reviews.html":"/reviews.html","/ru/faq.html":"/faq.html","/ru/services.html":"/services.html","/ru/case-studies/hoebeke-sci-fi-series.html":"/case-studies/hoebeke-sci-fi-series.html","/ru/living-illustrations.html":"/living-illustrations.html","/ru/404.html":"/404.html"};if(i){e.href=(m[p]||p.replace("/ru/","/"))+h;r.href=p+h;}else{r.href=(m[p]||p.replace("/project/","/ru/project/"))+h;e.href=p+h;}if(i){r.classList.add("active");}else{e.classList.add("active");}})();</script>
  </footer>

  <div class="sticky-contact">
      <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener" aria-label="Telegram" onclick="if(typeof gtag!=='undefined')gtag('event','click_telegram');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_telegram');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.198 2.433a2.242 2.242 0 0 0-1.022.215l-16.031 6.26a2.27 2.27 0 0 0-.093 4.07l3.827 1.558 1.56 4.44a1.5 1.5 0 0 0 2.663.52l2.33-3.14 3.75 2.83a2.27 2.27 0 0 0 3.58-1.74L22.34 3.89a2.24 2.24 0 0 0-1.142-1.457z"/></svg></a>
      <a href="https://wa.me/375296534382" target="_blank" rel="noopener" aria-label="WhatsApp" onclick="if(typeof gtag!=='undefined')gtag('event','click_whatsapp');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_whatsapp');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></a>
    </div>
  <button id="scrollTop" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">↑</button>
  <script src="../script.js"></script>
  <div class="mobile-cta"><a href="/ru/contact.html" class="cta-button">Обсудить проект</a></div>
</body>
</html>"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Created ru/work.html")


NAV_PATTERN_EN = r'<li><a href="book-covers\.html">Book Covers</a></li>.*?<li><a href="blog/">Blog</a></li>'
NAV_PATTERN_RU = r'<li><a href="book-covers\.html">Обложки книг</a></li>.*?<li><a href="blog/">Блог</a></li>'
NAV_PATTERN_CASE = r'<li><a href="\.\./book-covers\.html">Book Covers</a></li>.*?<li><a href="\.\./blog/">Blog</a></li>'
NAV_PATTERN_CASE_RU = r'<li><a href="\.\./book-covers\.html">Обложки книг</a></li>.*?<li><a href="\.\./blog/">Блог</a></li>'

FOOTER_PATTERN_EN = r'<p>\s*<a href="book-covers\.html">Book Covers</a>.*?<a href="blog/">Blog</a></p>'
FOOTER_PATTERN_RU = r'<p>\s*<a href="book-covers\.html">Обложки книг</a>.*?<a href="blog/">Блог</a></p>'
FOOTER_CASE_EN = r'<p>\s*<a href="\.\./book-covers\.html">Book Covers</a>.*?<a href="\.\./blog/">Blog</a></p>'
FOOTER_CASE_RU = r'<p>\s*<a href="\.\./book-covers\.html">Обложки книг</a>.*?<a href="\.\./blog/">Блог</a></p>'


def update_nav_and_footer(filepath, is_ru=False, prefix='', cta_path=None):
    """Replace old nav and footer links in a static HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine which nav/footer patterns to use
    use_case_prefix = prefix == '../'

    # Build the new nav
    if use_case_prefix:
        new_nav = NEW_NAV_CASE_RU if is_ru else NEW_NAV_CASE_EN
    else:
        new_nav = NEW_NAV_RU if is_ru else NEW_NAV_EN

    # Build the new footer
    if use_case_prefix:
        ru_footer = NEW_FOOTER_CASE_RU if is_ru else NEW_FOOTER_CASE_EN
    else:
        ru_footer = NEW_FOOTER_LINKS_RU if is_ru else NEW_FOOTER_LINKS_EN

    # Replace nav (find the pattern between <nav> and CTA button)
    old_nav = None
    if is_ru:
        if use_case_prefix:
            old_nav = r'<nav class="main-nav">.*?</nav>\s*<a href="[^"]*?" class="cta-button">[^<]+</a>'
        else:
            old_nav = r'<nav class="main-nav">.*?</nav>\s*<a href="[^"]*?" class="cta-button">[^<]+</a>'
    else:
        old_nav = r'<nav class="main-nav">.*?</nav>\s*<a href="[^"]*?" class="cta-button">[^<]+</a>'

    content = re.sub(old_nav, new_nav, content, flags=re.DOTALL)

    # Replace footer links section
    # Match from <p> with book-covers to </p> after Blog
    # Need to handle both EN and RU patterns
    for pattern in [FOOTER_PATTERN_EN, FOOTER_PATTERN_RU, FOOTER_CASE_EN, FOOTER_CASE_RU]:
        content = re.sub(pattern, ru_footer, content, flags=re.DOTALL)

    # Update lang-switch mappings: add work.html entries
    # The lang-switch JS block already contains a mapping object
    # We need to add /work.html and /ru/work.html entries
    if hasattr(update_nav_and_footer, '_lang_updated') and update_nav_and_footer._lang_updated:
        pass
    else:
        lang_mark = r'"404\.html":"/ru/404\.html"}'
        lang_repl = r'"404.html":"/ru/404.html","/work.html":"/ru/work.html","/ru/work.html":"/work.html"}'
        content = re.sub(lang_mark, lang_repl, content)

        lang_mark_opposite = r'"404\.html":"/404\.html"}'
        lang_repl_opposite = r'"404.html":"/404.html","/work.html":"/ru/work.html","/ru/work.html":"/work.html"}'
        content = re.sub(lang_mark_opposite, lang_repl_opposite, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def update_all_files():
    """Update all static HTML files with new nav and footer."""
    files = [
        # Root EN
        ("index.html", False, ''),
        ("about.html", False, ''),
        ("contact.html", False, ''),
        ("services.html", False, ''),
        ("book-covers.html", False, ''),
        ("book-illustrations.html", False, ''),
        ("visual-stories.html", False, ''),
        ("reviews.html", False, ''),
        ("faq.html", False, ''),
        ("404.html", False, ''),
        ("thanks.html", False, ''),
        ("privacy.html", False, ''),
        ("personal.html", False, ''),
        # Root RU
        ("ru/index.html", True, '../'),
        ("ru/about.html", True, '../'),
        ("ru/contact.html", True, '../'),
        ("ru/services.html", True, '../'),
        ("ru/book-covers.html", True, '../'),
        ("ru/book-illustrations.html", True, '../'),
        ("ru/visual-stories.html", True, '../'),
        ("ru/reviews.html", True, '../'),
        ("ru/faq.html", True, '../'),
        ("ru/404.html", True, '../'),
        ("ru/personal.html", True, '../'),
        # Case studies
        ("case-studies/hoebeke-sci-fi-series.html", False, '../'),
        ("ru/case-studies/hoebeke-sci-fi-series.html", True, '../'),
    ]

    for relpath, is_ru, prefix in files:
        filepath = os.path.join(BASE, relpath.replace('/', os.sep))
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {relpath}")
            continue
        try:
            update_nav_and_footer(filepath, is_ru, prefix)
            print(f"  OK: {relpath}")
        except Exception as e:
            print(f"  ERROR: {relpath}: {e}")

    # Handle blog pages (they use ../ prefix)
    blog_files = [
        ("blog/index.html", False, '../'),
        ("blog/how-much-does-a-book-cover-cost.html", False, '../'),
        ("blog/book-cover-design-trends-2026.html", False, '../'),
        ("blog/how-to-choose-book-cover-illustrator.html", False, '../'),
        ("blog/from-brief-to-final-art-process.html", False, '../'),
        ("blog/common-mistakes-when-hiring-illustrator.html", False, '../'),
        ("ru/blog/index.html", True, '../'),
        ("ru/blog/skolko-stoit-oblozhka-knigi.html", True, '../'),
        ("ru/blog/trendy-dizaina-oblozhek-2026.html", True, '../'),
        ("ru/blog/kak-vybrat-illyustratora-oblozhki.html", True, '../'),
        ("ru/blog/ot-brifa-do-finalnogo-arta-protsess.html", True, '../'),
        ("ru/blog/chastye-oshibki-pri-vybore-illyustratora.html", True, '../'),
    ]
    for relpath, is_ru, prefix in blog_files:
        filepath = os.path.join(BASE, relpath.replace('/', os.sep))
        if not os.path.exists(filepath):
            print(f"  SKIP (not found): {relpath}")
            continue
        try:
            update_nav_and_footer(filepath, is_ru, prefix)
            print(f"  OK: {relpath}")
        except Exception as e:
            print(f"  ERROR: {relpath}: {e}")


def add_reviews_to_about():
    """Add Reviews section to about pages before the footer."""
    # EN
    filepath = os.path.join(BASE, "about.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find insertion point: before the Let's Work Together section
    # Insert Reviews after "What Authors Say" section
    marker = '<h2>Beyond Book Covers</h2>'
    if marker in content and 'id="reviews"' not in content:
        content = content.replace(marker, REVIEWS_SECTION_EN + '\n\n          ' + marker)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Added Reviews to about.html")
    else:
        print("  SKIP about.html (already has Reviews or marker not found)")

    # RU
    filepath = os.path.join(BASE, "ru", "about.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    marker_ru = '<h2>Помимо обложек</h2>'
    alt_marker = '<h2>Beyond Book Covers</h2>'
    # Check both possible markers
    for m in [marker_ru, alt_marker]:
        if m in content and 'id="reviews"' not in content:
            content = content.replace(m, REVIEWS_SECTION_RU + '\n\n          ' + m)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Added Reviews to ru/about.html")
            break
    else:
        print("  SKIP ru/about.html (already has Reviews or marker not found)")


def add_faq_to_contact():
    """Add FAQ accordion to contact pages before the footer."""
    # EN
    filepath = os.path.join(BASE, "contact.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    marker = '</main>'
    if marker in content and 'id="faq"' not in content:
        faq_block = FAQ_SECTION_EN + '\n    '
        content = content.replace(marker, faq_block + marker)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Added FAQ to contact.html")
    else:
        print("  SKIP contact.html (already has FAQ or marker not found)")

    # RU
    filepath = os.path.join(BASE, "ru", "contact.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if marker in content and 'id="faq"' not in content:
        faq_block = FAQ_SECTION_RU + '\n    '
        content = content.replace(marker, faq_block + marker)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  Added FAQ to ru/contact.html")
    else:
        print("  SKIP ru/contact.html (already has FAQ or marker not found)")


if __name__ == '__main__':
    main()
