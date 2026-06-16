# vimark.art — что уже сделано (SEO / GEO / техника)

Живой документ. Добавляем сюда всё, что реализовано.

---

## Микроразметка (Schema.org)

| Что | Где | Статус |
|-----|-----|--------|
| `["Person", "ProfessionalService"]` | index.html, about.html, services.html, generate_site.py (все project/art) | ✅ |
| `WebSite` + `SearchAction` | index.html, about.html, ru/about.html, generate_site.py (все art-страницы) | ✅ |
| `Organization` (отдельная, с founder) | index.html, about.html, ru/about.html, generate_site.py (все art-страницы) | ✅ |
| `hasOfferCatalog` (2–3 услуги) | index.html, about.html, ru/about.html, generate_site.py | ✅ |
| `knowsAbout` (6–7 тем) | index.html, about.html, ru/about.html, generate_site.py | ✅ |
| `sameAs` (Behance, Instagram, DeviantArt, ArtStation, Reedsy, Pinterest) | index.html, about.html, ru/about.html, generate_site.py | ✅ |
| `ImageObject` (name, author, description, contentUrl, thumbnailUrl, datePublished, license, acquireLicensePage, creditText, copyrightNotice, **width, height**) | Все art-страницы (192 en + 192 ru) | ✅ |
| `BreadcrumbList` | Все страницы | ✅ |
| `FAQPage` | faq.html, ru/faq.html | ✅ |
| `Article` | about.html, case-studies/hoebeke-sci-fi-series.html | ✅ |
| `areaServed: Country[]` (US, UK, CA, AU, RU, DE, FR) | index.html, about.html, ru/about.html, generate_site.py | ✅ |

---

## Open Graph / Twitter Cards

| Что | Где | Статус |
|-----|-----|--------|
| `og:type`, `og:url`, `og:title`, `og:description`, `og:image` | Все страницы | ✅ |
| `og:image:width`, `og:image:height` | Все страницы | ✅ |
| `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` | Все страницы | ✅ |
| `twitter:site`, `twitter:creator` | Все страницы | ✅ |
| `article:published_time`, `article:modified_time` | Все art-страницы | ✅ |

---

## Техническое SEO

| Что | Где | Статус |
|-----|-----|--------|
| `sitemap.xml` (en + ru) | Корень + ru/ | ✅ |
| `image-sitemap.xml` (384 изображения) | Корень | ✅ |
| `robots.txt` | Корень | ✅ |
| `canonical` | Все страницы | ✅ |
| `hreflang` (en, ru, x-default) | Все страницы | ✅ |
| `meta name="robots" content="index, follow"` | Все страницы | ✅ |
| `meta name="msvalidate.01"` (Bing) | Все страницы | ✅ |
| `link rel="image_src"` | Все страницы | ✅ |
| `link rel="manifest"` + `manifest.json` | Все страницы | ✅ |
| `301 redirects` (www, старые URL, Blog→blog) | vercel.json | ✅ |
| `X-Content-Type-Options: nosniff` | Все ответы (vercel.json) | ✅ |
| `X-Frame-Options: DENY` | Все ответы (vercel.json) | ✅ |
| `Referrer-Policy: strict-origin-when-cross-origin` | Все ответы (vercel.json) | ✅ |
| `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` | Все ответы (vercel.json) | ✅ |
| `Permissions-Policy` (camera=(), microphone=(), geolocation=(), interest-cohort=()) | Все ответы (vercel.json) | ✅ |
| `Content-Security-Policy` (default-src, script-src, style-src, img-src, connect-src, form-action, font-src, frame-src, object-src, base-uri) | Все ответы (vercel.json) | ✅ |
| `X-Robots-Tag: noindex` (living-illustrations) | vercel.json | ✅ |

---

## Производительность (Core Web Vitals)

| Что | Статус |
|-----|--------|
| `loading="eager"` + `fetchpriority="high"` на hero-изображениях | ✅ |
| `loading="eager"` на первых 4 изображениях галерей, `loading="lazy"` на остальных | ✅ |
| `loading="lazy"` на всех не-hero изображениях | ✅ |
| `srcset` + `sizes` (400w, 600w) на thumbnails: hero, галереи, related works, about-галерея | ✅ |
| `.sm.webp` (400×400) для мобильных | ✅ |
| WebP формат для всех thumbnails | ✅ |
| `preconnect` для Google Tag Manager, Yandex Metrica | ✅ |
| `dns-prefetch` для Google Analytics | ✅ |

---

## Контент и страницы

| Страница | EN | RU | Статус |
|----------|----|----|--------|
| Главная (index) | ✅ | ✅ | Статическая |
| About | ✅ | ✅ | Статическая |
| Services | ✅ | ✅ | Статическая |
| Contact | ✅ | ✅ | Статическая |
| FAQ | ✅ | ✅ | Статическая, FAQPage schema |
| Reviews | ✅ | ✅ | Статическая |
| Case Studies (Hoëbeke) | ✅ | ✅ | Статическая |
| Visual Stories | ✅ | ✅ | Статическая (ребрендинг Comic) |
| Book Covers | ✅ | ✅ | Генерируется |
| Book Illustrations | ✅ | ✅ | Генерируется, порядок проектов вручную |
| Project pages (23 en + 23 ru) | ✅ | ✅ | Генерируются |
| Art pages (192 en + 192 ru) | ✅ | ✅ | Генерируются, ImageObject JSON-LD |

---

## GEO и AI-оптимизация

| Что | Статус |
|-----|--------|
| FAQ с коммерческими вопросами («Сколько стоит?», «Сроки?») | ✅ |
| Related Works (до 6 работ из того же проекта) на art-страницах | ✅ |
| CTA на всех страницах («Get a Free Quote» / «Обсудить проект») | ✅ |
| Бар доверия (Reedsy 71 review, HarperCollins, Hachette и т.д.) | ✅ |

---

## Соцсети и визуальный поиск

| Что | Статус |
|-----|--------|
| Pinterest Rich Pins (`meta name="pinterest-rich-pin"`) | ✅ |
| Pinterest ссылка в футере | ✅ |
| Pinterest API v5 скрипт публикации (`pinterest_publish.py`) | ✅ |
| Pinterest pins.json (23 пина) | ✅ |

---

## Ребрендинг и навигация

| Что | Статус |
|-----|--------|
| «Comic» → «Visual Stories» | ✅ |
| «Living Illustrations» скрыт с главной (noindex) | ✅ |
| Навигация EN + RU: Book Covers, Book Illustrations, Case Studies, Services, Visual Stories, About, Contact, Reviews, FAQ, **Blog** | ✅ |
| Пользовательская сортировка подпапок book-illustrations (Planetes → Creatures → Endymion → ...) | ✅ |
| `display_titles.txt` для правки названий без смены URL | ✅ |

---

## Блог

| Что | Где | Статус |
|-----|-----|--------|
| Структура `/blog/` и `/ru/blog/` | blog/index.html, ru/blog/index.html | ✅ |
| 5 статей EN + 5 RU | blog/*.html, ru/blog/*.html | ✅ |
| Article JSON-LD schema | Все статьи | ✅ |
| Open Graph / Twitter Cards | Все статьи | ✅ |
| hreflang (en, ru, x-default) | Все статьи | ✅ |
| hreflang JS (полный маппинг всех страниц) | Все страницы блога и статические страницы | ✅ |
| blog.css (стили статей, карточек, списка) | blog.css | ✅ |
| Единый сайт-фрейм (sidebar, footer, social, sticky-contact, scrollTop) | site_frame.py | ✅ |
| Blog в боковом меню (sidebar) | Все страницы (через site_frame.py + статические) | ✅ |
| Blog в футере | Все страницы | ✅ |
| Blog → blog redirect (case-sensitive для Vercel/Linux) | vercel.json | ✅ |

---

## Структура проекта

| Файл | Назначение |
|------|-----------|
| `generate_site.py` | Генератор страниц проектов, art-страниц, sitemap |
| `display_titles.txt` | Переопределение названий (не сбрасывается при генерации) |
| `projects.ini` | Конфиг проектов (описания, обложки) |
| `pinterest_publish.py` | Публикация пинов через API |
| `blog_convert.py` | Генератор HTML-страниц блога из MD |
| `site_frame.py` | Единый шаблон sidebar+footer для blog-страниц |
| `vercel.json` | Редиректы, security-заголовки, хостинг |
| `seo_geo_plan_2026.md` | План дальнейших улучшений |
