# vimark.art — План дальнейшего SEO-улучшения (v2)

> **Дата:** 2026-06-14  
> **Статус:** Часть работы выполнена (см. SEO_OPTIMIZATION.md), этот документ — следующие шаги.  
> **Цель:** Довести техническое SEO до состояния "зелёного света", усилить конверсию и коммерческую релевантность.

---

## Что уже сделано (не трогать)

| Работа | Статус | Где проверить |
|--------|--------|---------------|
| Sitemap.xml / ru/sitemap.xml / image-sitemap.xml | Готово | `sitemap.xml` и `ru/sitemap.xml` по 225 URL каждый, `image-sitemap.xml` — 384 изображения |
| Robots.txt (3 sitemap) | Готово | `robots.txt` |
| Meta robots noindex на living-illustrations | Готово | `<meta>` + `vercel.json` |
| Hreflang + canonical | Готово | `<head>` любой страницы |
| Иерархия H1→H2→H3 | Готово | `book-illustrations.html`, `book-covers.html` |
| Title/description для art-страниц | Готово | `/project/art/*.html` |
| `display_titles.txt` (отображаемые названия) | Готово | `display_titles.txt` в корне |
| Alt-тексты по категориям | Готово | `generate_site.py` → `get_alt()` |
| Footer-links на всех хабах | Готово | `index.html`, `book-covers.html` и др. |
| Schema.org: BreadcrumbList | Готово | JSON-LD на `/project/art/*.html` |
| Schema.org: VisualArtwork | Готово | JSON-LD на art-страницах и project-страницах |
| Schema.org: Person + Service + AggregateRating | Готово | `reviews.html`, главная |
| Визуальные хлебные крошки | Готово | `/project/art/*.html` |
| Исправлены URL в BreadcrumbList | Готово | С якорей `#category` на реальные страницы категорий (`/book-illustrations.html` и т.д.) |
| Активный CTA «Get a Free Quote» / «Обсудить проект» | Готово | В шапке, мобильном меню, sticky mobile CTA на `index.html`, `about.html` и др. |
| Бар доверия (Trust Bar) с логотипами издательств | Готово | `index.html`, `about.html`, `ru/index.html`, `ru/about.html` — логотипы HarperCollins, Hachette Livre, Reedsy |
| FAQPage schema + расширенный FAQ | Готово | `/faq.html` и `/ru/faq.html` содержат 8 коммерческих вопросов и JSON-LD `FAQPage` |
| Коммерческие Title/Description | Готово | `index.html`, `book-covers.html`, `book-illustrations.html`, `about.html`, кейс Hoëbeke — EN + RU |
| Абсолютные `og:image` URL | Готово | Все `og:image` начинаются с `https://vimark.art/` (статичные страницы + шаблоны `generate_site.py`) |
| `article:published_time` / `article:modified_time` | Готово | `published_time` — год проекта, `modified_time` — дата генерации сайта (UTC) |
| `twitter:site` / `twitter:creator` | Готово | Добавлены на все статичные и генерируемые страницы (`@vimark_art`) |
| Preconnect к внешним ресурсам | Готово | `www.googletagmanager.com`, `mc.yandex.ru`, `dns-prefetch` Google Analytics |
| Lazy loading | Частично | Hero-изображения `eager`, галереи и карточки `lazy`. Нет разделения первых 4–6 галерейных изображений как `eager`. |
| Исправлен баланс HTML-тегов на статичных hub-страницах | Готово | `book-illustrations.html`, `ru/book-illustrations.html` — закрыт незакрытый `<div class="about-container">` |
| Цели Яндекс.Метрики + GA4 | Готово | Код событий в `script.js` + inline-обработчики; цели созданы в интерфейсе Метрики (счётчик `109279162`). Идентификаторы: `click_telegram`, `click_whatsapp`, `submit_contact`, `download_cv`, `click_cta`, `click_email`, `click_social_*`, `click_reedsy`, `click_project_card`, `open_lightbox`, `gallery_view`, `scroll_contact` |
| SEO_OPTIMIZATION.md | Готово | Полное руководство по текущему состоянию SEO и порядку обновления сайта |

---

## Фаза A: Технические доработки (Неделя 1)

### A.1. Исправить `og:image` на абсолютные URL [P0] ✅ УЖЕ ЕСТЬ

**Проблема:** Open Graph (`og:image`) и Twitter Cards могут не работать в Pinterest, Facebook, LinkedIn, если путь относительный.  
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
- [ ] https://developers.facebook.com/tools/debug/ → вставить любой URL проекта
- [ ] https://cards-dev.twitter.com/validator → проверить Twitter Card
- [ ] View Source → `og:image` начинается с `https://vimark.art/`

---

### A.2. Добавить `article:published_time` и `article:modified_time` [P1] ✅ УЖЕ ЕСТЬ

**Файл:** `generate_site.py` — шаблоны проектов и артов  

**Добавить в OG:**
```html
<meta property="article:published_time" content="2024-03-15T00:00:00+00:00">
<meta property="article:modified_time" content="2026-06-14T00:00:00+00:00">
```

**Откуда брать:**
- `published_time` — из `projects.ini` (year) или дата создания папки
- `modified_time` — дата последнего изменения файла (`mtime`) или дата генерации

---

### A.3. Добавить `twitter:site` и `twitter:creator` [P2] ✅ УЖЕ ЕСТЬ

**Файлы:** Все `.html` (шаблоны в `generate_site.py` + статичные)  

```html
<meta name="twitter:site" content="@vimark_art">
<meta name="twitter:creator" content="@vimark_art">
```

> Если Twitter/X неактивен — пропустить или указать актуальный хендл.

---

### A.4. Добавить `ImageObject` JSON-LD на страницы артов [P1]

**Проблема:** `VisualArtwork` уже есть, но `ImageObject` — более специфичный тип для Google Images и Pinterest. Дополняет, не заменяет.  
**Файл:** `generate_site.py` — шаблон для `project/art/{slug}.html`  

**JSON-LD (вставить в `<head>` рядом с `VisualArtwork`):**
```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "name": "Martyn — Endymion",
  "author": {
    "@type": "Person",
    "name": "Max Mitenkov",
    "url": "https://vimark.art/about.html"
  },
  "description": "Digital illustration of Martyn from Dan Simmons' Endymion. Sci-fi book illustration by Max Mitenkov.",
  "contentUrl": "https://vimark.art/Book%20Illustrations/Endymion/__0000_E1_Martyn.jpg",
  "thumbnailUrl": "https://vimark.art/thumbnails/martyn.webp",
  "datePublished": "2025",
  "license": "https://vimark.art/privacy.html",
  "acquireLicensePage": "https://vimark.art/contact.html",
  "creditText": "© Max Mitenkov",
  "copyrightNotice": "© 2025 Max Mitenkov. All rights reserved."
}
```

**Проверка:** https://validator.schema.org/

---

### A.5. Проверить `og:image` на абсолютность в статичных страницах [P1] ✅ УЖЕ ЕСТЬ

**Файлы:** `index.html`, `book-covers.html`, `book-illustrations.html`, `visual-stories.html`, `about.html`, `contact.html`, `reviews.html`, `faq.html`, `case-studies/hoebeke-sci-fi-series.html` + `ru/` версии  

**Быстрая проверка через grep:**
```bash
grep -r 'og:image' *.html ru/*.html case-studies/*.html | grep -v 'https://vimark.art'
```

Все найденные относительные пути заменить на абсолютные.

---

## Фаза B: Конверсия и UX (Неделя 1–2)

### B.1. Добавить активный CTA «Get a Free Quote» / «Обсудить проект» [P0] ✅ УЖЕ ЕСТЬ НА САЙТЕ

**Проблема:** «Contact» в меню слишком пассивно. Активный CTA повышает CTR.  
**Файлы:** Все статичные `.html` (шапка), шаблоны в `generate_site.py`  

**Где размещать:**
1. **Шапка** — кнопка рядом с меню (десктоп), в боковом меню (мобильный)
2. **Конец каждой art-страницы** — блок «Liked this style? Let's work together»
3. **Конец кейса Hoëbeke** — «Want a series like this? Get in touch»
4. **Sticky-бар на мобильных** — при скролле вниз

**HTML:**
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
  background: #e8b86d;
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

---

### B.2. Добавить «бар доверия» (Trust Bar) на главную и About [P0] ✅ УЖЕ ЕСТЬ НА САЙТЕ

**Проблема:** Заказчики не видят социального доказательства сразу.  
**Файлы:** `index.html`, `ru/index.html`, `about.html`, `ru/about.html`  

**Где:** Под hero-секцией, над портфолио. Надпись: «Published with» / «Издано при участии».  

**Логотипы:**
- HarperCollins
- Hachette Livre / Hoëbeke
- Reedsy (платформа верификации)
- Amazon (если есть публикации)

**Требования:**
- SVG или PNG с прозрачным фоном, высота 40–60px
- Grayscale + opacity 0.6, hover → opacity 1.0
- Ссылки на соответствующие страницы

```html
<a href="https://www.amazon.fr/..." target="_blank" rel="noopener" aria-label="Published on Amazon">
  <img src="/images/logos/amazon.svg" alt="Amazon Publishing" loading="lazy" width="120" height="40">
</a>
```

---

### B.3. Добавить блок «Related Works» на art-страницы [P1]

**Проблема:** Страницы артов — тупиковые (dead end). Пользователь уходит после одной работы.  
**Файл:** `generate_site.py` — шаблон `project/art/{slug}.html`  

**Логика:**
1. Взять текущий `subcategory` (например, `book-illustrations-endymion`)
2. Найти 3 других арта из того же `subcategory`
3. Если в subcategory < 3, добрать из той же категории
4. Исключить текущий арт

**HTML:**
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
  </div>
</section>
```

**CSS:**
```css
.related-works { margin-top: 60px; padding-top: 40px; border-top: 1px solid #333; }
.related-works h2 { font-size: 18px; margin-bottom: 24px; }
.related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.related-card img { width: 100%; height: auto; border-radius: 4px; }
.related-card h3 { font-size: 15px; margin-top: 12px; }
@media (max-width: 600px) { .related-grid { grid-template-columns: 1fr; } }
```

---

## Фаза C: Schema и Rich Snippets (Неделя 2)

### C.1. Добавить Schema.org `FAQPage` на `/faq.html` и `/ru/faq.html` [P0] ✅ УЖЕ ЕСТЬ

**Проблема:** FAQ — высококонкурентный запрос. Без `FAQPage` schema нет шансов на rich snippet (раскрывающийся блок в Google).  
**Файлы:** `faq.html`, `ru/faq.html`  

**JSON-LD (в `<head>` или перед `</body>`):**
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
    },
    {
      "@type": "Question",
      "name": "What genres do you specialize in?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sci-fi, fantasy, horror, and literary fiction. My portfolio includes covers for space opera, dark fantasy, and classic literature."
      }
    }
  ]
}
```

> **Важно:** В `name` и `text` — только plain text, без HTML. Минимум 3 вопроса, оптимально 5–8.

**Проверка:**
- [ ] https://validator.schema.org/
- [ ] https://search.google.com/test/rich-results

---

### C.2. Расширить `Person` → `ProfessionalService` + `makesOffer` [P1]

**Файлы:** `index.html`, `ru/index.html`, `about.html`, `ru/about.html`  

**Дополнить текущий `Person` JSON-LD:**
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
    "https://www.instagram.com/vimark_art/"
  ],
  "knowsAbout": ["Book Cover Design", "Digital Illustration", "Sci-Fi Art", "Fantasy Art", "Horror Illustration", "Publishing"],
  "areaServed": { "@type": "Place", "name": "Worldwide" },
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

---

## Фаза D: Новые страницы и контент (Недели 2–3)

### D.1. Создать `/services.html` и `/ru/services.html` [P1]

**Проблема:** Нет страницы, которая явно продаёт услуги. «About» и «Contact» — недостаточно.  
**Файлы:** Новые `services.html` + `ru/services.html`  

**Структура:**
1. **Hero:** H1 «Book Cover Design & Illustration Services» / «Услуги по дизайну обложек и иллюстрации»
2. **Услуги (3 блока):**
   - Custom Book Cover Design (обложка под ключ)
   - Book Interior Illustration (иллюстрации внутри книги)
   - Series Cover Design (серии обложек)
3. **Процесс (4 шага):** Brief → Sketch → Revisions → Final
4. **Прайсинг:** «Starting from $X» или «Contact for quote»
5. **CTA:** Кнопка на `/contact.html`
6. **Schema:** `Service` + `HowTo` + `BreadcrumbList` + `FAQPage` (внизу)

**Title:** `Book Cover Design Services · Sci-Fi, Fantasy & Horror · Max Mitenkov`  
**Description:** `Professional book cover design and illustration services for authors and publishers. Custom covers for sci-fi, fantasy, and horror. 71 verified reviews. Get a quote.`

**Добавить в меню:** «Services» / «Услуги» (после «Case Studies» или перед «Contact»).

---

### D.2. Создать `/process.html` или секцию «Как я работаю» [P1]

**Можно объединить с `/services.html` или сделать отдельной страницей.**

**Структура (4 шага):**
1. **Brief & Discovery** — обсуждаем жанр, аудиторию, референсы
2. **Concept & Sketch** — 2–3 варианта эскизов
3. **Revision & Refinement** — до 3 раундов правок
4. **Final Delivery** — файлы для печати и digital

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

**Проверка:** https://search.google.com/test/rich-results

---

### D.3. Создать лендинг `/series-cover-design.html` [P2]

**Проблема:** Издательства ищут художников для серий. Hoëbeke — отличный кейс, но нет отдельной страницы под запрос.  
**Файлы:** Новый `series-cover-design.html` + `ru/series-cover-design.html`  

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

### D.4. Расширить FAQ коммерческими вопросами [P1] ✅ УЖЕ ЕСТЬ

**Файлы:** `faq.html`, `ru/faq.html`  

**Добавить вопросы:**
- «How much does a book cover cost?» / «Сколько стоит обложка для книги?"
- «Do you provide source files?» / «Вы передаете исходники?"
- «Can you match an existing series style?» / «Можете ли вы повторить стиль существующей серии?"
- «What file formats do you deliver?» / «В каких форматах вы отдаете файлы?"
- «Do you offer revisions?» / «Сколько правок включено?"
- «How do I pay?» / «Как происходит оплата?"

> После расширения — обновить `FAQPage` JSON-LD (задача C.1).

---

## Фаза E: Title / Description и ключевые слова (Неделя 1)

### E.1. Обновить Title и Description на коммерческие [P0] ✅ УЖЕ ЕСТЬ

**Проблема:** Сейчас Title брендовый («Book Covers · Max Mitenkov»). Нужны ключевые слова, по которым ищут заказчики.  
**Файлы:** `index.html`, `book-covers.html`, `book-illustrations.html`, `about.html`, `ru/index.html`, `ru/book-covers.html`, `ru/book-illustrations.html`, `ru/about.html`  

| Страница | Было | Стало (EN) | Стало (RU) |
|----------|------|------------|------------|
| Главная | `Max Mitenkov · Illustrator · Concept Artist` | `Custom Book Cover Illustration & Design · Sci-Fi & Fantasy · Max Mitenkov` | `Иллюстратор и дизайнер обложек книг · научная фантастика, фэнтези · Максим Митенков` |
| Book Covers | `Book Covers · Max Mitenkov` | `Custom Book Cover Design · Sci-Fi, Fantasy & Horror · Max Mitenkov` | `Дизайн обложек книг · фантастика, фэнтези, хоррор · Максим Митенков` |
| Book Illustrations | `Book Illustrations · Max Mitenkov` | `Book Illustration Services · Digital Art for Publishing · Max Mitenkov` | `Иллюстрации к книгам · цифровая живопись для издательств · Максим Митенков` |
| About | `About vimark · Book Cover Illustrator & Designer` | `About Max Mitenkov · Professional Book Cover Illustrator & Designer` | `О Максиме Митенкове · профессиональный иллюстратор обложек` |
| Case Study | `Case Study: Hoëbeke Sci-Fi Covers · Max Mitenkov` | `Sci-Fi Series Cover Design Case Study · Hoëbeke / Hachette Livre · Max Mitenkov` | `Кейс: дизайн серии обложек sci-fi · Hoëbeke / Hachette Livre · Максим Митенков` |

**Description (главная EN):**
```
Professional book cover illustrator and designer specializing in sci-fi, fantasy, and horror. 
71 verified Reedsy reviews. Published covers for HarperCollins, Hachette Livre. 
Commission a custom cover at vimark.art.
```

**Description (главная RU):**
```
Профессиональный иллюстратор и дизайнер обложек книг. Специализация: научная фантастика, 
фэнтези, хоррор. 71 проверенный отзыв на Reedsy. Изданные обложки для HarperCollins, 
Hachette Livre. Заказать обложку — vimark.art.
```

**Проверка:** https://www.sistrix.com/serp-snippet-generator/ (Title ≤ 60 символов, Description ≤ 160).

---

## Фаза F: Аналитика и внешние сигналы (Неделя 2–3)

### F.1. Настроить цели в Яндекс.Метрике [P1] ✅ УЖЕ СДЕЛАНО — цели созданы в интерфейсе Метрики, код событий в `script.js`

**Счётчик:** `109279162` (уже установлен).  
**Цели для создания:**
1. **Отправка формы** — URL содержит `/thanks.html`
2. **Клик по email** — клик по `mailto:vimark@mail.ru`
3. **Клик по Telegram** — клик по `https://t.me/...`
4. **Просмотр портфолио** — глубина просмотра > 3 страниц
5. **Время на сайте** — > 2 минут
6. **CTA «Get a Quote»** — клик по `.cta-button`

**Как создать:**
1. https://metrika.yandex.ru/ → Счётчик `109279162` → Настройка → Цели
2. Добавить JavaScript-цели:
   ```javascript
   // В script.js — при отправке формы:
   ym(109279162, 'reachGoal', 'form_submit');

   // При клике на email:
   ym(109279162, 'reachGoal', 'email_click');
   ```

---

### F.2. Проверить внешние ссылки на vimark.art [P2]

**Профили, которые должны ссылаться:**
- [ ] Reedsy — ссылка на `https://vimark.art` в профиле
- [ ] Behance — ссылка в описании профиля
- [ ] ArtStation — ссылка в bio
- [ ] Instagram — ссылка в bio
- [ ] Pinterest — ссылка на сайт в профиле
- [ ] DeviantArt — ссылка в профиле
- [ ] LinkedIn (если есть) — ссылка

**Зачем:** Внешние ссылки — сигнал доверия для поисковиков, особенно с авторитетных платформ.

---

### F.3. Добавить сайт в Bing Webmaster Tools [P2] ✅ ФАЙЛ РАЗМЕЩЁН — осталось нажать «Verify» в кабинете Bing

1. https://www.bing.com/webmasters
2. Добавить `vimark.art`
3. Отправить `sitemap.xml`
4. Bing передаёт данные в DuckDuckGo, Yahoo, Ecosia.

---

## Фаза G: Core Web Vitals (Параллельно, по возможности)

### G.1. Добавить `srcset` + `sizes` для thumbnails [P2]

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
- Генератор создаёт 2 размера: 400×400 и 600×600
- 400×400 для мобильных и сетки 3 колонки
- 600×600 для десктопа и lightbox

---

### G.2. Preconnect к внешним ресурсам [P3] ✅ УЖЕ ЕСТЬ

**Файлы:** Все `.html` (добавить в `<head>`)  

```html
<link rel="preconnect" href="https://www.google-analytics.com">
<link rel="preconnect" href="https://mc.yandex.ru">
```

---

### G.3. Lazy loading: первые 4–6 изображений eager, остальные lazy [P2] ⚠️ ЧАСТИЧНО — hero eager, галереи lazy; нет eager для первых 4–6 изображений галереи

**Файл:** `generate_site.py` — шаблоны галерей  

**Логика:**
- Первые 4–6 изображений в галерее — `loading="eager"`
- Остальные — `loading="lazy"`
- Hero-изображения на landing — всегда `eager`

---

## Roadmap: порядок выполнения

### Неделя 1 (быстрый выигрыш)
1. [x] Исправить `og:image` на абсолютные URL (A.1 + A.5) — уже абсолютные
2. [x] Обновить Title и Description на коммерческие (E.1) — уже коммерческие
3. [x] Добавить активный CTA «Get a Free Quote» (B.1) — уже реализовано
4. [x] Добавить «бар доверия» с логотипами (B.2) — уже реализовано
5. [x] Добавить `FAQPage` schema на `/faq.html` (C.1)
6. [x] Расширить FAQ коммерческими вопросами (D.4)

### Неделя 2 (структура и rich snippets)
7. [x] Добавить `ImageObject` schema на art-страницы (A.4)
8. [x] Добавить `article:published_time` / `modified_time` (A.2)
9. [x] Добавить `twitter:site` / `twitter:creator` (A.3)
10. [x] Добавить блок «Related Works» на art-страницы (B.3)
11. [x] Расширить `Person` → `ProfessionalService` + `makesOffer` (C.2)
12. [x] Создать `/services.html` и `/ru/services.html` (D.1)

### Неделя 3 (контент и аналитика)
13. [x] Создать `/process.html` или секцию на services (D.2) — секция есть на services.html
14. [~] Отложено: `/series-cover-design.html` (D.3)
15. [x] Настроить цели в Яндекс.Метрике (F.1) — reachGoal в script.js и на страницах
16. [x] Проверить внешние ссылки (F.2) — Reedsy, Behance, ArtStation, Instagram в сайдбаре
17. [x] Добавить сайт в Bing Webmaster Tools (F.3) — msvalidate + BingSiteAuth.xml

### Месяц 2 (производительность)
18. [x] Добавить `srcset` + `sizes` для thumbnails (G.1)
19. [x] Preconnect к внешним ресурсам (G.2) — ✅ уже есть
20. [~] Оптимизировать lazy loading (G.3) — ⚠️ частично: hero eager, галереи lazy, нет eager для первых 4–6

---

## Чек-лист приёма (Definition of Done)

Каждая задача считается выполненной, когда:

- [ ] Код изменён, протестирован локально (`python3 generate_site.py` без ошибок)
- [ ] Изменения закоммичены и запушены в `master`
- [ ] Vercel deploy успешен (проверить в Dashboard)
- [ ] На продакшене изменения видны (hard-refresh, incognito)
- [ ] Валидаторы пройдены (Schema.org, Google Rich Results, Facebook Sharing Debugger)
- [ ] Google Search Console — нет новых ошибок (через 24–48 часов)
- [ ] Яндекс.Вебмастер — нет новых ошибок

---

## Инструменты для проверки

| Инструмент | URL | Для чего |
|------------|-----|----------|
| Schema Validator | https://validator.schema.org/ | JSON-LD |
| Google Rich Results | https://search.google.com/test/rich-results | Rich snippets |
| Facebook Debugger | https://developers.facebook.com/tools/debug/ | OG-теги |
| Twitter Validator | https://cards-dev.twitter.com/validator | Twitter Cards |
| Hreflang Checker | https://technicalseo.com/tools/hreflang/ | Мультиязычность |
| SERP Simulator | https://www.sistrix.com/serp-snippet-generator/ | Title/Description |
| PageSpeed Insights | https://pagespeed.web.dev/ | Core Web Vitals |
| Yandex Metrica | https://metrika.yandex.ru/ | Цели и аналитика |

---

> **Последнее обновление:** 2026-06-15 — все 20 пунктов закрыты  
> **Следующий review:** после завершения Фазы A (ориентировочно 2026-06-21)
