# vimark.art — Рабочий план по SEO-улучшениям

> **Дата:** 2026-06-13  
> **Сайт:** https://vimark.art  
> **Статус:** В работе  
> **Цель:** Увеличить органический трафик, улучшить конверсию, укрепить техническую базу.

---

## Легенда приоритетов

| Приоритет | Обозначение | Критерий |
|-----------|-------------|----------|
| **P0** | 🔴 Критично | Делать немедленно. Блокирует индексацию, влияет на конверсию, или исправляет ошибку. |
| **P1** | 🟠 Важно | Делать в течение 1–2 недель. Заметный прирост трафика/UX. |
| **P2** | 🟡 Желательно | Делать в течение месяца. Долгосрочный эффект. |
| **P3** | 🟢 Фоновое | По возможности. Не критично для текущей фазы. |

---

## Фаза 1: Быстрый выигрыш (Неделя 1)

### Задача 1.1 — Исправить `og:image` на абсолютные URL [P0]

**Проблема:** Open Graph и Twitter Cards могут не работать в Pinterest, Facebook, LinkedIn, если путь относительный.  
**Файлы:** `generate_site.py` (шаблоны OG/Twitter), все статичные `.html`  
**Что искать:** `og:image` content="/thumbnails/..." или content="/images/..."

**Было:**
```html
<meta property="og:image" content="/thumbnails/book-covers-2025.webp">
```

**Стало:**
```html
<meta property="og:image" content="https://vimark.art/thumbnails/book-covers-2025.webp">
```

**Проверка:**
- [ ] Открыть https://developers.facebook.com/tools/debug/ → вставить любой URL проекта
- [ ] Открыть https://cards-dev.twitter.com/validator → проверить Twitter Card
- [ ] Открыть страницу → View Source → найти `og:image` → убедиться, что URL начинается с `https://vimark.art/`

---

### Задача 1.2 — Добавить `<meta name="robots" content="index, follow">` на generated-страницы [P0]

**Проблема:** 300+ страниц артворков и проектов не имеют явного robots-meta. Хотя по умолчанию индексируются, явный сигнал надёжнее.  
**Файл:** `generate_site.py` — шаблон HTML для `project/*.html` и `project/art/*.html`  

**Куда вставлять:** в `<head>`, сразу после `<meta charset="UTF-8">`:
```html
<meta name="robots" content="index, follow">
```

**Проверка:**
- [ ] Запустить генератор: `python generate_site.py`
- [ ] Открыть любой `/project/art/*.html` → View Source → найти `meta name="robots"`
- [ ] Проверить 5 случайных страниц

---

### Задача 1.3 — Добавить Schema.org `FAQPage` на `/faq.html` и `/ru/faq.html` [P0]

**Проблема:** FAQ — высококонкурентный запрос. Без `FAQPage` schema нет шансов на rich snippet (раскрывающийся блок в Google).  
**Файлы:** `faq.html`, `ru/faq.html`  

**Куда вставлять:** в `<head>` или перед `</body>` в теге `<script type="application/ld+json">`.

**Шаблон JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How long does it take to create a book cover?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Typically 2–4 weeks depending on complexity. Rush orders are possible with advance notice."
      }
    },
    {
      "@type": "Question",
      "name": "Do you work with self-published authors?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. I work with both indie authors and major publishers like HarperCollins and Hachette Livre."
      }
    }
  ]
}
```

> **Примечание:** В `name` и `text` НЕ использовать HTML-теги. Только plain text. Количество вопросов — минимум 3, оптимально 5–8.

**Проверка:**
- [ ] https://validator.schema.org/ → вставить URL `/faq.html`
- [ ] https://search.google.com/test/rich-results → проверить FAQ rich results
- [ ] Повторить для `/ru/faq.html`

---

### Задача 1.4 — Обновить Title и Description на коммерческие ключевые слова [P0]

**Проблема:** Сейчас Title брендовый («Book Covers · Max Mitenkov»). Нужны ключевые слова, по которым ищут заказчики.  
**Файлы:** `index.html`, `book-covers.html`, `book-illustrations.html`, `about.html`, `ru/index.html`, `ru/book-covers.html`, `ru/book-illustrations.html`, `ru/about.html`

| Страница | Было | Стало (EN) | Стало (RU) |
|----------|------|------------|------------|
| Главная | `Max Mitenkov · Illustrator · Concept Artist` | `Custom Book Cover Illustration & Design · Sci-Fi & Fantasy · Max Mitenkov` | `Иллюстратор и дизайнер обложек книг · научная фантастика, фэнтези · Максим Митенков` |
| Book Covers | `Book Covers · Max Mitenkov` | `Custom Book Cover Design · Sci-Fi, Fantasy & Horror · Max Mitenkov` | `Дизайн обложек книг · фантастика, фэнтези, хоррор · Максим Митенков` |
| Book Illustrations | `Book Illustrations · Max Mitenkov` | `Book Illustration Services · Digital Art for Publishing · Max Mitenkov` | `Иллюстрации к книгам · цифровая живопись для издательств · Максим Митенков` |
| About | `About vimark · Book Cover Illustrator & Designer` | `About Max Mitenkov · Professional Book Cover Illustrator & Designer` | `О Максиме Митенкове · профессиональный иллюстратор обложек` |
| Case Study | `Case Study: Hoëbeke Sci-Fi Covers · Max Mitenkov` | `Sci-Fi Series Cover Design Case Study · Hoëbeke / Hachette Livre · Max Mitenkov` | `Кейс: дизайн серии обложек sci-fi · Hoëbeke / Hachette Livre · Максим Митенков` |

**Description (пример для главной EN):**
```
Professional book cover illustrator and designer specializing in sci-fi, fantasy, and horror. 
71 verified Reedsy reviews. Published covers for HarperCollins, Hachette Livre. 
Commission a custom cover at vimark.art.
```

**Description (пример для главной RU):**
```
Профессиональный иллюстратор и дизайнер обложек книг. Специализация: научная фантастика, 
фэнтези, хоррор. 71 проверенный отзыв на Reedsy. Изданные обложки для HarperCollins, 
Hachette Livre. Заказать обложку — vimark.art.
```

**Проверка:**
- [ ] SERP Simulator (https://www.sistrix.com/serp-snippet-generator/) — проверить длину (Title ≤ 60 символов, Description ≤ 160)
- [ ] Убедиться, что каждая страница имеет УНИКАЛЬНЫЙ Title и Description

---

### Задача 1.5 — Добавить «бар доверия» (Trust Bar) на главную и About [P0]

**Проблема:** Заказчики не видят социального доказательства сразу. Логотипы издательств и платформ повышают конверсию.  
**Файлы:** `index.html`, `ru/index.html`, `about.html`, `ru/about.html`  

**Где размещать:** Под hero-секцией, над портфолио. Надпись: «Published with» / «Издано при участии».

**Логотипы для отображения:**
- HarperCollins
- Hachette Livre / Hoëbeke
- Reedsy (как платформа верификации)
- Amazon (если есть публикации)
- (опционально) Логотипы конкретных издательств, если есть разрешение

**Требования:**
- Логотипы в SVG или PNG с прозрачным фоном
- Высота 40–60px
- Grayscale + opacity 0.6, при hover — opacity 1.0
- Ссылки — на соответствующие страницы (Amazon, Reedsy profile и т.д.)

**Accessibility:**
```html
<a href="https://www.amazon.fr/..." target="_blank" rel="noopener" aria-label="Published on Amazon">
  <img src="/images/logos/amazon.svg" alt="Amazon Publishing" loading="lazy" width="120" height="40">
</a>
```

**Проверка:**
- [ ] Визуально — логотипы не перегружают страницу
- [ ] Мобильная версия — логотипы складываются в 2 строки или горизонтальный скролл
- [ ] Все ссылки работают, нет битых изображений

---

### Задача 1.6 — Добавить активный CTA «Get a Free Quote» / «Обсудить проект» [P1]

**Проблема:** «Contact» в меню — пассивно. Нужен явный призыв к действию.  
**Файлы:** Все статичные `.html` (шапка), `index.html`, `book-covers.html`, `book-illustrations.html`, `case-studies/hoebeke-sci-fi-series.html`, `ru/...`

**Где размещать:**
1. **Шапка** — кнопка рядом с меню (на десктопе), в боковом меню (на мобильном)
2. **Конец каждой страницы проекта / артворка** — блок «Liked this style? Let's work together»
3. **Конец кейса Hoëbeke** — «Want a series like this? Get in touch»
4. **Sticky-бар на мобильных** — кнопка «Contact" при скролле вниз

**HTML шаблон:**
```html
<a href="/contact.html" class="cta-button" aria-label="Request a free quote for book cover design">
  Get a Free Quote
</a>
```

**CSS (добавить в `style.css`):**
```css
.cta-button {
  display: inline-block;
  padding: 12px 28px;
  background: #e8b86d; /* акцентный цвет */
  color: #1a1a1a;
  font-weight: 600;
  border-radius: 4px;
  text-decoration: none;
  transition: background 0.2s, transform 0.1s;
}
.cta-button:hover {
  background: #f0c67d;
  transform: translateY(-1px);
}
```

**Проверка:**
- [ ] Кнопка видна на всех landing-страницах
- [ ] На мобильном не перекрывает контент
- [ ] Ведёт на `/contact.html` (или `/ru/contact.html` для RU-версии)

---

## Фаза 2: Структура и индексация (Недели 2–3)

### Задача 2.1 — Вернуть автогенерацию `sitemap.xml` и `image-sitemap.xml` [P0]

**Проблема:** Статичные карты устаревают при добавлении новых проектов. Google не найдёт новые URL.  
**Файл:** `generate_site.py`  

**Подход:**
1. Генератор должен пересоздавать `sitemap.xml` и `image-sitemap.xml` ПОСЛЕ генерации всех страниц.
2. НО: landing-страницы (`index.html`, `book-covers.html` и т.д.) должны быть в sitemap всегда, даже если генератор их не трогает. Захардкодить список landing-страниц в генераторе.
3. Добавить `<lastmod>` — дата последнего изменения (можно взять `mtime` файла или текущую дату генерации).

**Структура `sitemap.xml`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Landing pages — hardcoded -->
  <url>
    <loc>https://vimark.art/</loc>
    <lastmod>2026-06-13</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://vimark.art/book-covers.html</loc>
    <lastmod>2026-06-13</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <!-- Generated pages — dynamic -->
  <url>
    <loc>https://vimark.art/project/book-illustrations-endymion.html</loc>
    <lastmod>2026-06-13</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://vimark.art/project/art/the-giant-squid.html</loc>
    <lastmod>2026-06-13</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>
```

**Структура `image-sitemap.xml`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://vimark.art/project/art/the-giant-squid.html</loc>
    <image:image>
      <image:loc>https://vimark.art/images/Book%20Illustrations/20000-leagues/the-giant-squid.jpg</image:loc>
      <image:caption>The giant squid attacks the Nautilus — digital illustration by Max Mitenkov for 20,000 Leagues Under the Sea</image:caption>
      <image:title>The Giant Squid — 20,000 Leagues Under the Sea</image:title>
    </image:image>
  </url>
</urlset>
```

**Проверка:**
- [ ] После генерации открыть `/sitemap.xml` — нет ошибок XML
- [ ] https://www.xml-sitemaps.com/validate-xml-sitemap.html
- [ ] Google Search Console → Sitemaps → добавить `/sitemap.xml` и `/image-sitemap.xml`
- [ ] Убедиться, что ВСЕ generated-страницы (`project/*.html`, `project/art/*.html`, `ru/...`) присутствуют

---

### Задача 2.2 — Добавить `ImageObject` JSON-LD на страницы артворков [P1]

**Проблема:** Google Images и Pinterest не понимают контекст изображения без structured data.  
**Файл:** `generate_site.py` — шаблон для `project/art/{slug}.html`  

**JSON-LD шаблон (вставлять в `<head>`):**
```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "name": "The Giant Squid — 20,000 Leagues Under the Sea",
  "author": {
    "@type": "Person",
    "name": "Max Mitenkov",
    "url": "https://vimark.art/about.html"
  },
  "description": "Digital illustration of a giant squid attacking the Nautilus submarine for the Jules Verne classic. Created by Max Mitenkov.",
  "contentUrl": "https://vimark.art/images/Book%20Illustrations/20000-leagues/the-giant-squid.jpg",
  "thumbnailUrl": "https://vimark.art/thumbnails/the-giant-squid.webp",
  "datePublished": "2024-03-15",
  "license": "https://vimark.art/privacy.html",
  "acquireLicensePage": "https://vimark.art/contact.html",
  "creditText": "© Max Mitenkov",
  "copyrightNotice": "© 2024 Max Mitenkov. All rights reserved."
}
```

**Откуда брать данные:**
- `name` — из `projects.ini` (title) + `captions.txt`
- `description` — из `captions.txt` или `projects.ini` (description)
- `contentUrl` — абсолютный путь к оригиналу
- `thumbnailUrl` — абсолютный путь к thumbnail
- `datePublished` — из `projects.ini` (year) или `mtime` файла

**Проверка:**
- [ ] https://validator.schema.org/ → проверить 3 случайных артворка
- [ ] Убедиться, что `contentUrl` отдаёт изображение (нет 404)

---

### Задача 2.3 — Добавить `BreadcrumbList` JSON-LD на все landing-страницы [P1]

**Проблема:** Сейчас хлебные крошки только на проектах. Landing-страницы тоже нужны для навигации в SERP.  
**Файлы:** Все статичные `.html` и шаблоны в `generate_site.py`  

**Для `/book-covers.html`:**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://vimark.art/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Book Covers",
      "item": "https://vimark.art/book-covers.html"
    }
  ]
}
```

**Для `/project/art/the-giant-squid.html`:**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://vimark.art/" },
    { "@type": "ListItem", "position": 2, "name": "Book Illustrations", "item": "https://vimark.art/book-illustrations.html" },
    { "@type": "ListItem", "position": 3, "name": "20,000 Leagues Under the Sea", "item": "https://vimark.art/project/book-illustrations-20000-leagues.html" },
    { "@type": "ListItem", "position": 4, "name": "The Giant Squid", "item": "https://vimark.art/project/art/the-giant-squid.html" }
  ]
}
```

**Проверка:**
- [ ] https://search.google.com/test/rich-results → проверить breadcrumb на 5 страницах
- [ ] Убедиться, что `item` везде — абсолютный URL

---

### Задача 2.4 — Улучшить alt-тексты через `captions.txt` [P1]

**Проблема:** Сейчас alt «есть», но не описательные. Google Images не поймёт контекст.  
**Файл:** `captions.txt` + шаблон в `generate_site.py`  

**Формат `captions.txt` (обновить):**
```
# Формат: filename | alt-text | caption
# alt-text: описательный, 10–15 слов, включает название проекта и жанр
# caption: короткий контекст, 20–30 слов

the-giant-squid.jpg | Digital illustration of a giant squid attacking the Nautilus submarine for 20,000 Leagues Under the Sea by Max Mitenkov | The iconic scene from Jules Verne's classic, reimagined as a dramatic digital painting with cinematic lighting.
endymion-portrait.jpg | Sci-fi character portrait of Endymion from Dan Simmons' Hyperion Cantos by illustrator Max Mitenkov | A detailed character study for the science fiction novel series, emphasizing futuristic armor and melancholic expression.
```

**Требования к alt:**
- Минимум 8 слов
- Включает: что изображено, для какого проекта/книги, жанр, автор
- НЕ начинается с «Image of...» или «Picture of...»
- НЕ содержит «artwork 1", «img_0023" и т.п.

**Проверка:**
- [ ] Открыть 10 случайных страниц артворков → проверить alt через DevTools
- [ ] https://www.seoptimer.com/alt-tag-checker → проверить сайт

---

### Задача 2.5 — Добавить блок «Related Works» в шаблон артворка [P1]

**Проблема:** Страницы артворков — тупиковые (dead end). Пользователь уходит после просмотра одной работы.  
**Файл:** `generate_site.py` — шаблон `project/art/{slug}.html`  

**Логика:**
1. Взять текущий `subcategory` (например, `book-illustrations-endymion`)
2. Найти 3 других артворка из того же `subcategory`
3. Если в subcategory < 3, добрать из той же категории (`book-illustrations`)
4. Исключить текущий артворк

**HTML шаблон:**
```html
<section class="related-works" aria-label="Related works">
  <h2>Related Works</h2>
  <div class="related-grid">
    <article class="related-card">
      <a href="/project/art/another-artwork.html">
        <img src="/thumbnails/another-artwork.webp" alt="..." loading="lazy" width="600" height="600">
        <h3>Another Artwork Title</h3>
        <p>From: Endymion</p>
      </a>
    </article>
    <!-- 2 more cards -->
  </div>
</section>
```

**CSS (добавить в `style.css`):**
```css
.related-works { margin-top: 60px; padding-top: 40px; border-top: 1px solid #333; }
.related-works h2 { font-size: 18px; margin-bottom: 24px; }
.related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.related-card img { width: 100%; height: auto; border-radius: 4px; }
.related-card h3 { font-size: 15px; margin-top: 12px; }
@media (max-width: 600px) { .related-grid { grid-template-columns: 1fr; } }
```

**Проверка:**
- [ ] Открыть любой артворк → прокрутить вниз → видны 3 related works
- [ ] Кликнуть — ссылки работают, нет 404
- [ ] На мобильном — 1 колонка, не перегружено

---

## Фаза 3: Расширение Schema и социальные сигналы (Недели 3–4)

### Задача 3.1 — Расширить `Person` → `ProfessionalService` + `makesOffer` [P1]

**Проблема:** `Person` schema не передаёт коммерческую природу услуги.  
**Файл:** `index.html`, `ru/index.html`, `about.html`, `ru/about.html`  

**JSON-LD (заменить или дополнить текущий `Person`):**
```json
{
  "@context": "https://schema.org",
  "@type": ["Person", "ProfessionalService"],
  "name": "Max Mitenkov",
  "alternateName": "Максим Митенков",
  "jobTitle": "Book Cover Illustrator & Designer",
  "description": "Professional illustrator and designer specializing in custom book covers for sci-fi, fantasy, and horror genres. 71 verified reviews on Reedsy.",
  "url": "https://vimark.art",
  "sameAs": [
    "https://www.reedsy.com/maxim-mitenkov",
    "https://www.behance.net/vimark",
    "https://www.pinterest.com/vimark_art/",
    "https://www.instagram.com/vimark_art/",
    "https://vimarkart.deviantart.com"
  ],
  "knowsAbout": ["Book Cover Design", "Digital Illustration", "Sci-Fi Art", "Fantasy Art", "Horror Illustration", "Publishing"],
  "areaServed": {
    "@type": "Place",
    "name": "Worldwide"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Book Cover Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Custom Book Cover Design",
          "description": "Original cover design for fiction and non-fiction books"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Book Illustration",
          "description": "Interior illustrations and chapter headers for published works"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Series Cover Design",
          "description": "Consistent cover design for book series and trilogies"
        }
      }
    ]
  },
  "makesOffer": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "Contact for pricing",
    "availability": "https://schema.org/InStock",
    "url": "https://vimark.art/contact.html"
  }
}
```

**Проверка:**
- [ ] https://validator.schema.org/ → проверить на ошибки
- [ ] Убедиться, что `sameAs` содержит рабочие ссылки

---

### Задача 3.2 — Добавить `twitter:site` и `twitter:creator` [P2]

**Файлы:** Все `.html` (шаблоны в `generate_site.py` + статичные)  

**Добавить в `<head>`:**
```html
<meta name="twitter:site" content="@vimark_art">
<meta name="twitter:creator" content="@vimark_art">
```

> Если Twitter/X аккаунт неактивен — можно пропустить или указать другой актуальный.

---

### Задача 3.3 — Добавить `article:published_time` и `article:modified_time` [P2]

**Файл:** `generate_site.py` — шаблоны проектов и артворков  

**Добавить в OG:**
```html
<meta property="article:published_time" content="2024-03-15T00:00:00+00:00">
<meta property="article:modified_time" content="2026-06-13T00:00:00+00:00">
```

**Откуда брать:**
- `published_time` — из `projects.ini` (year) или дата создания папки
- `modified_time` — дата последнего изменения файла (`mtime`) или дата генерации

---

### Задача 3.4 — Проверить hreflang на полноту [P1]

**Проблема:** 300+ generated-страниц должны иметь hreflang. Если RU-версии нет, нужен `x-default`.  
**Файл:** `generate_site.py` — шаблоны  

**Проверить на каждой странице:**
```html
<link rel="canonical" href="https://vimark.art/project/art/the-giant-squid.html">
<link rel="alternate" hreflang="en" href="https://vimark.art/project/art/the-giant-squid.html">
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/project/art/the-giant-squid.html">
<link rel="alternate" hreflang="x-default" href="https://vimark.art/project/art/the-giant-squid.html">
```

**Проверка:**
- [ ] https://technicalseo.com/tools/hreflang/ → загрузить sitemap и проверить
- [ ] Убедиться, что нет «Missing return links»
- [ ] Для страниц без RU-версии — `x-default` должен указывать на EN

---

## Фаза 4: Контент и конверсия (Месяц 2)

### Задача 4.1 — Создать страницу `/process` или секцию «Как я работаю» [P1]

**Проблема:** Покупатели боятся неизвестного процесса. Step-by-step снимает барьеры.  
**Файл:** Новый `process.html` + `ru/process.html` (или секция на `about.html`)  

**Структура:**
1. **Brief & Discovery** — обсуждаем жанр, аудиторию, референсы
2. **Concept & Sketch** — 2–3 варианта эскизов, выбор направления
3. **Revision & Refinement** — до 3 раундов правок
4. **Final Delivery** — готовые файлы для печати и digital (PDF, TIFF, PNG)

**Schema.org `HowTo`:**
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Commission a Book Cover with Max Mitenkov",
  "description": "A simple 4-step process for commissioning a custom book cover illustration.",
  "totalTime": "P14D",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Brief & Discovery",
      "text": "We discuss your book's genre, target audience, and visual references. You fill out a short creative brief.",
      "url": "https://vimark.art/process.html#step1"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Concept & Sketch",
      "text": "I create 2–3 rough sketches exploring different compositions and moods. You choose the direction.",
      "url": "https://vimark.art/process.html#step2"
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "Revision & Refinement",
      "text": "Based on your feedback, I refine the chosen sketch. Up to 3 rounds of revisions are included.",
      "url": "https://vimark.art/process.html#step3"
    },
    {
      "@type": "HowToStep",
      "position": 4,
      "name": "Final Delivery",
      "text": "You receive print-ready and digital files in all required formats: PDF, TIFF, PNG with bleed and trim marks.",
      "url": "https://vimark.art/process.html#step4"
    }
  ]
}
```

**Проверка:**
- [ ] https://search.google.com/test/rich-results → проверить HowTo
- [ ] Страница доступна по `/process.html` и `/ru/process.html`
- [ ] В меню добавлен пункт «Process» / «Процесс работы"

---

### Задача 4.2 — Создать лендинг `/series-cover-design` [P2]

**Проблема:** Издательства ищут художников для серий. Hoëbeke — отличный кейс, но нет отдельной страницы под запрос.  
**Файл:** Новый `series-cover-design.html` + `ru/series-cover-design.html`  

**Title:** `Series Cover Design · Consistent Covers for Trilogies & Sagas · Max Mitenkov`  
**H1:** `Series Cover Design`  
**Контент:**
- Проблема: «Readers judge a series by its covers. Inconsistent design kills sales."
- Решение: «I create cohesive visual systems that span 3–10+ books."
- Кейс: Hoëbeke (7 обложек, 1 стиль, 1 издательство)
- Процесс: Style guide → Template → Variations
- CTA: «Discuss your series»

**Schema:** `Service` + `HowTo` + `BreadcrumbList`

---

### Задача 4.3 — Добавить страницу `/clients` или `/publishers` [P2]

**Проблема:** B2B-продажи требуют списка клиентов. Также это страница для ключевика «illustrator for HarperCollins».  
**Файл:** Новый `clients.html` + `ru/clients.html`  

**Содержание:**
- Список издательств с логотипами
- Список платформ (Reedsy, Amazon)
- Цитаты клиентов (2–3 коротких)
- Ссылки на опубликованные книги (Amazon)

**Schema:** `ItemList` + `Review` (если есть отдельные отзывы клиентов)

---

### Задача 4.4 — Начать раздел /blog или /insights [P2]

**Проблема:** Портфолио-сайты редко ранжируются по информационным запросам. Блог даёт трафик.  
**Файл:** Новая папка `/blog/` + индексная страница  

**Первые 3 статьи:**
1. «How to Commission a Book Cover: A Complete Guide for Authors" (EN) / «Как заказать обложку для книги: полное руководство для автора" (RU)
2. «Sci-Fi Cover Design Trends 2026: What Sells on Amazon" (EN)
3. «Digital vs Traditional Illustration for Publishing: Pros and Cons" (EN)

**Требования:**
- Минимум 1200 слов
- H2, H3 структура
- 3–5 изображений из портфолио (с alt!)
- Schema `Article` + `BreadcrumbList`
- Внутренние ссылки на портфолио и contact
- CTA в конце каждой статьи

---

## Фаза 5: Производительность и Core Web Vitals (Параллельно)

### Задача 5.1 — Добавить `srcset` + `sizes` для thumbnails [P1]

**Файл:** `generate_site.py` — шаблоны карточек и галерей  

**Было:**
```html
<img src="/thumbnails/artwork.webp" alt="..." loading="lazy" width="600" height="600">
```

**Стало:**
```html
<img 
  src="/thumbnails/artwork-400.webp" 
  srcset="/thumbnails/artwork-400.webp 400w, /thumbnails/artwork-600.webp 600w"
  sizes="(max-width: 600px) 90vw, 300px"
  alt="..." 
  loading="lazy" 
  width="600" 
  height="600">
```

**Требования:**
- Генератор должен создавать 2 размера: 400×400 и 600×600
- 400×400 для мобильных и сетки 3 колонки
- 600×600 для десктопа и lightbox

---

### Задача 5.2 — Preconnect к внешним ресурсам [P2]

**Файлы:** Все `.html` (добавить в `<head>`)  

```html
<link rel="preconnect" href="https://www.google-analytics.com">
<link rel="preconnect" href="https://mc.yandex.ru">
<link rel="dns-prefetch" href="https://fonts.googleapis.com">
```

---

### Задача 5.3 — Lazy loading: первые 4–6 изображений eager, остальные lazy [P2]

**Файл:** `generate_site.py` — шаблоны галерей  

**Логика:**
- Изображения в первом viewport (первые 4–6) — `loading="eager"`
- Остальные — `loading="lazy"`
- Hero-изображения на landing — всегда `eager`

---

### Задача 5.4 — AVIF как primary, WebP fallback [P3]

**Файл:** `generate_site.py` — добавить генерацию AVIF  

**HTML:**
```html
<picture>
  <source srcset="/thumbnails/artwork.avif" type="image/avif">
  <source srcset="/thumbnails/artwork.webp" type="image/webp">
  <img src="/thumbnails/artwork.jpg" alt="..." loading="lazy" width="600" height="600">
</picture>
```

> **Примечание:** Pillow не поддерживает AVIF из коробки. Нужен `pillow-avif-plugin` или использование `avifenc` через subprocess. Пока отложить, если нет готового пайплайна.

---

## Фаза 6: Pinterest и автоматизация (Параллельно)

### Задача 6.1 — Активировать Pinterest workflow [P2]

**Файл:** `.github/workflows/pinterest.yml.disabled` → переименовать в `.yml`  

**Что нужно:**
1. Pinterest Business Account
2. Pinterest API Token (App ID + Access Token)
3. Добавить секреты в GitHub Settings → Secrets:
   - `PINTEREST_ACCESS_TOKEN`
   - `PINTEREST_BOARD_ID`

**Workflow:**
- Триггер: push в `master` с изменениями в `pinterest/pins.json`
- Действие: публикация новых пинов через Pinterest API

---

### Задача 6.2 — Обогатить `pinterest/pins.json` [P2]

**Файл:** `generate_site.py` — генерация `pins.json`  

**Структура:**
```json
{
  "pins": [
    {
      "title": "The Giant Squid — 20,000 Leagues Under the Sea",
      "description": "Digital illustration of a giant squid attacking the Nautilus. Book cover art by Max Mitenkov for Jules Verne's classic. #bookcover #illustration #scifi",
      "image_url": "https://vimark.art/pinterest/images/the-giant-squid-1200x1800.webp",
      "link": "https://vimark.art/project/art/the-giant-squid.html",
      "alt_text": "Digital illustration of a giant squid attacking a submarine for 20,000 Leagues Under the Sea by Max Mitenkov"
    }
  ]
}
```

**Требования:**
- Title: 100 символов максимум
- Description: 500 символов максимум, включает хэштеги
- Alt text: обязательно, описательный
- Image: 1200×1800 (2:3), WebP

---

## Чек-лист приёма (Definition of Done)

Каждая задача считается выполненной, когда:

- [ ] Код изменён, протестирован локально (`python generate_site.py` проходит без ошибок)
- [ ] Изменения закоммичены и запушены в `master`
- [ ] Vercel deploy успешен (проверить в Dashboard)
- [ ] На продакшене изменения видны (hard-refresh, incognito)
- [ ] Валидаторы пройдены (Schema.org, Google Rich Results, Facebook Sharing Debugger)
- [ ] Google Search Console — нет новых ошибок (проверить через 24–48 часов)
- [ ] Яндекс.Вебмастер — нет новых ошибок

---

## Инструменты для проверки

| Инструмент | URL | Для чего |
|------------|-----|----------|
| Schema Validator | https://validator.schema.org/ | Проверка JSON-LD |
| Google Rich Results | https://search.google.com/test/rich-results | Rich snippets |
| Facebook Debugger | https://developers.facebook.com/tools/debug/ | OG-теги |
| Twitter Validator | https://cards-dev.twitter.com/validator | Twitter Cards |
| Hreflang Checker | https://technicalseo.com/tools/hreflang/ | Мультиязычность |
| XML Sitemap Validator | https://www.xml-sitemaps.com/validate-xml-sitemap.html | Sitemap |
| PageSpeed Insights | https://pagespeed.web.dev/ | Core Web Vitals |
| SERP Simulator | https://www.sistrix.com/serp-snippet-generator/ | Title/Description |
| Alt Tag Checker | https://www.seoptimer.com/alt-tag-checker | Alt-тексты |

---

## Контакты и доступы

- **Репозиторий:** https://github.com/v944/vimark-art
- **Хостинг:** Vercel (автодеплой из `master`)
- **Analytics:** Google Analytics 4 `G-6RBP7X7H88`, Yandex.Metrika `109279162`
- **Search Console:** Google Search Console + Яндекс.Вебмастер

---

> **Последнее обновление:** 2026-06-13  
> **Следующий review:** после завершения Фазы 2 (ориентировочно 2026-06-27)
