"""Reusable sidebar+footer frame matching vimark.art main site."""

def site_frame(base, is_ru, content_html, lang_switch_js):
    """Generate full page frame with sidebar, footer, sticky contact, etc."""
    nav_items_en = [
        ('book-covers.html', 'Book Covers'),
        ('book-illustrations.html', 'Book Illustrations'),
        ('case-studies/hoebeke-sci-fi-series.html', 'Case Studies'),
        ('services.html', 'Services'),
        ('visual-stories.html', 'Visual Stories'),
        ('about.html', 'About'),
        ('contact.html', 'Contact'),
        ('reviews.html', 'Reviews'),
        ('faq.html', 'FAQ'),
        ('blog/', 'Blog'),
    ]
    nav_items_ru = [
        ('book-covers.html', 'Обложки книг'),
        ('book-illustrations.html', 'Иллюстрации к книгам'),
        ('case-studies/hoebeke-sci-fi-series.html', 'Кейсы'),
        ('services.html', 'Услуги'),
        ('visual-stories.html', 'Визуальные истории'),
        ('about.html', 'Об авторе'),
        ('contact.html', 'Контакты'),
        ('reviews.html', 'Отзывы'),
        ('faq.html', 'FAQ'),
        ('blog/', 'Блог'),
    ]
    nav_items = nav_items_ru if is_ru else nav_items_en
    nav_html = '\n'.join(f'          <li><a href="{base}{href}">{label}</a></li>' for href, label in nav_items)

    cta_text = 'Обсудить проект' if is_ru else 'Get a Free Quote'
    cta_link = f'{base}contact.html'

    socials = [
        ('mailto:hello@vimark.art', 'Email',
         '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>'),
        ('https://www.facebook.com/maks.vimark/', 'Facebook',
         '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
        ('https://www.linkedin.com/in/maxim-mitenkov-06192940/', 'LinkedIn',
         '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>'),
        ('https://www.instagram.com/vimark_art/', 'Instagram',
         '<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>'),
    ]
    social_html = ''.join(
        f'      <a href="{href}" aria-label="{label}"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg></a>\n'
        for href, label, path in socials
    )
    social_html += f'      <a href="https://www.behance.net/vimark" aria-label="Behance"><img src="{base}behance.png" alt="Behance" class="social-icon"></a>\n'
    social_html += f'      <a href="https://www.deviantart.com/vimark" aria-label="DeviantArt"><img src="{base}deviantart.png" alt="DeviantArt" class="social-icon"></a>'

    footer_items_en = [
        ('book-covers.html', 'Book Covers'),
        ('book-illustrations.html', 'Book Illustrations'),
        ('case-studies/hoebeke-sci-fi-series.html', 'Case Studies'),
        ('services.html', 'Services'),
        ('visual-stories.html', 'Visual Stories'),
        ('about.html', 'About'),
        ('contact.html', 'Contact'),
        ('reviews.html', 'Reviews'),
        ('faq.html', 'FAQ'),
        ('blog/', 'Blog'),
    ]
    footer_items_ru = [
        ('book-covers.html', 'Обложки книг'),
        ('book-illustrations.html', 'Иллюстрации к книгам'),
        ('case-studies/hoebeke-sci-fi-series.html', 'Кейсы'),
        ('services.html', 'Услуги'),
        ('visual-stories.html', 'Визуальные истории'),
        ('about.html', 'Об авторе'),
        ('contact.html', 'Контакты'),
        ('reviews.html', 'Отзывы'),
        ('faq.html', 'FAQ'),
        ('blog/', 'Блог'),
    ]
    footer_items = footer_items_ru if is_ru else footer_items_en
    footer_nav = ' ·\n      '.join(f'<a href="{base}{href}">{label}</a>' for href, label in footer_items)

    footer_socials = [
        ('https://reedsy.com/freelancers/maxim-m', 'Reedsy'),
        ('https://www.behance.net/vimark', 'Behance'),
        ('https://www.artstation.com/vimark', 'ArtStation'),
        ('https://www.instagram.com/vimark_art/', 'Instagram'),
        ('https://www.pinterest.com/vimark', 'Pinterest'),
        ('https://www.deviantart.com/vimark', 'DeviantArt'),
    ]
    footer_social_html = ' ·\n      '.join(
        f'<a href="{href}" target="_blank" rel="noopener">{label}</a>' for href, label in footer_socials
    )

    mobile_cta_text = 'Обсудить проект' if is_ru else 'Get a Free Quote'
    open_for = 'Open for commissions' if not is_ru else 'Открыт к заказам'

    return f'''<!DOCTYPE html>
<html lang="{'ru' if is_ru else 'en'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
{content_html['head']}
<link rel="stylesheet" href="{base}style.css">
<link rel="stylesheet" href="{base}vimark_typography_system.css">
<link rel="stylesheet" href="{base}blog.css">
<link rel="icon" type="image/png" href="{base}vimark_logo.png">
<link rel="manifest" href="{base}manifest.json">
<!-- Yandex.Metrika counter -->
<script>(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym(109279162,"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true,ecommerce:"dataLayer"}});</script>
<noscript><div><img src="https://mc.yandex.ru/watch/109279162" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
{content_html.get('extra_head', '')}
</head>
<body>
  <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">☀</button>
  <div id="canvasWrapper">
    <aside id="sidebar">
      <header class="sidebar-header">
        <a href="{base}index.html"><img src="{base}Max Mitenkov.png" alt="Max Mitenkov" class="sidebar-photo" style="width: 100%; margin-bottom: 24px; opacity: 0.9;"></a>
        <nav class="main-nav">
        <ul>
{nav_html}
        </ul>
      </nav>
      <a href="{cta_link}" class="cta-button">{cta_text}</a>
      </header>
      <div class="social-links">
{social_html}
    </div>
      <div class="commissions-status"><span class="status-dot"></span><span>{open_for}</span></div>
      <a href="{base}index.html" class="logo-link"><img src="{base}vimark_logo.png" alt="Logo" style="width: 60px;"></a>
    </aside>

    <button class="mobile-toggle">Menu</button>

    <main id="main">
{content_html['main']}
    </main>
  </div>

          <footer class="site-footer">
    <span><b>©</b> Max Mitenkov, 2026.</span>
    <div class="footer-links">
      <p>
      {footer_nav}</p>
      <p>
      {footer_social_html}
      </p>
    </div>
    <div class="lang-switch">
      <a href="#" id="lang-en" title="English"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><path fill="#012169" d="M0,0 h60 v30 h-60 z"/><path stroke="#fff" stroke-width="6" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#C8102E" stroke-width="4" d="M0,0 L60,30 M60,0 L0,30"/><path stroke="#fff" stroke-width="10" d="M30,0 v30 M0,15 h60"/><path stroke="#C8102E" stroke-width="6" d="M30,0 v30 M0,15 h60"/></svg></a>
      <a href="#" id="lang-ru" title="Русский"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 30" width="24" height="12"><rect width="60" height="10" fill="#fff"/><rect y="10" width="60" height="10" fill="#0039A6"/><rect y="20" width="60" height="10" fill="#D52B1E"/></svg></a>
    </div>
    <script>{lang_switch_js}</script>
  </footer>

  <div class="sticky-contact">
      <a href="https://t.me/MaxMitenkov" target="_blank" rel="noopener" aria-label="Telegram" onclick="if(typeof gtag!=='undefined')gtag('event','click_telegram');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_telegram');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.198 2.433a2.242 2.242 0 0 0-1.022.215l-16.031 6.26a2.27 2.27 0 0 0-.093 4.07l3.827 1.558 1.56 4.44a1.5 1.5 0 0 0 2.663.52l2.33-3.14 3.75 2.83a2.27 2.27 0 0 0 3.58-1.74L22.34 3.89a2.24 2.24 0 0 0-1.142-1.457z"/></svg></a>
      <a href="https://wa.me/375296534382" target="_blank" rel="noopener" aria-label="WhatsApp" onclick="if(typeof gtag!=='undefined')gtag('event','click_whatsapp');if(typeof ym!=='undefined')ym(109279162,'reachGoal','click_whatsapp');"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg></a>
    </div>
  <button id="scrollTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top">↑</button>
  <script src="{base}script.js"></script>
  <div class="mobile-cta"><a href="{cta_link}" class="cta-button">{mobile_cta_text}</a></div>
</body>
</html>'''
