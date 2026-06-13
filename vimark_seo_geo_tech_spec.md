# vimark.art — Техническое задание: SEO + GEO оптимизация

> **Проект:** vimark.art  
> **Исполнитель:** [разработчик]  
> **Заказчик:** Max Mitenkov (vimark)  
> **Дата:** 2026-06-13  
> **Статус:** Техническое задание для внедрения  
> **Цель:** Оптимизация сайта для поисковиков (Google) и AI-агентов (ChatGPT, Perplexity, Gemini)

---

## Содержание

1. [Общие принципы](#1-общие-принципы)
2. [Приоритет P0 — Критично](#2-приоритет-p0--критично)
3. [Приоритет P1 — Важно для AI](#3-приоритет-p1--важно-для-ai)
4. [Приоритет P2 — Улучшение UX и соцсетей](#4-приоритет-p2--улучшение-ux-и-соцсетей)
5. [Приоритет P3 — Полировка](#5-приоритет-p3--полировка)
6. [Чек-лист приёмки](#6-чек-лист-приёмки)

---

## 1. Общие принципы

- **Двуязычность:** Все изменения применяются к EN и RU версиям параллельно.
- **DOM-presence:** Если элемент скрывается через CSS (`display: none`), он должен оставаться в HTML (важно для AI-сканеров).
- **Абсолютные URL:** Все внутренние ссылки, OG-теги, Schema.org — только с `https://www.vimark.art`.
- **Hreflang:** Каждая страница должна иметь `hreflang` EN / RU / x-default.
- **Canonical:** Самоссылка на каждой странице.

---

## 2. Приоритет P0 — Критично

### Задача 2.1. Footer-ссылки на всех страницах

**Проблема:** `.footer-links` есть только на `visual-stories.html` и `book-covers.html`. Остальные 6 хабов (index, book-illustrations, about, contact, reviews, case-studies) не имеют внутренних ссылок в футере.

**Решение:** Добавить `.footer-links` в шаблон всех страниц.

**HTML (вставить перед `</footer>`):**

```html
<nav class="footer-links" aria-label="Footer navigation">
  <a href="/book-covers.html">Book Covers</a>
  <a href="/book-illustrations.html">Book Illustrations</a>
  <a href="/visual-stories.html">Visual Stories</a>
  <a href="/about.html">About</a>
  <a href="/contact.html">Contact</a>
  <a href="/reviews.html">Reviews</a>
  <a href="/case-studies/hoebeke-sci-fi-series.html">Case Studies</a>
</nav>
```

**CSS (добавить в `style.css`):**

```css
.footer-links {
  display: none; /* скрыто на десктопе, видно в DOM для AI */
}

@media (max-width: 800px) {
  .footer-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 40px 20px 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .footer-links a {
    font-size: 13px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.5);
    text-decoration: none;
    transition: color 0.2s;
  }

  .footer-links a:hover {
    color: #fff;
  }
}
```

**Для RU-версий** (`/ru/*.html`) ссылки должны вести на `/ru/` страницы.

**Страницы для внедрения:**
- `/index.html`
- `/book-illustrations.html`
- `/about.html`
- `/contact.html`
- `/reviews.html`
- `/case-studies/hoebeke-sci-fi-series.html`
- + все RU-аналоги

---

### Задача 2.2. Очистить sitemap.xml

**Проблема:** В sitemap висят URL, которые отдают 301 (редирект).

**Удалить из `/sitemap.xml`:**

```xml
<!-- УДАЛИТЬ — мёртвые URL -->
<url><loc>https://vimark.art/comic.html</loc>...</url>
<url><loc>https://vimark.art/bookcover.html</loc>...</url>
<url><loc>https://vimark.art/case-study-hoebeke.html</loc>...</url>
<url><loc>https://vimark.art/ru/comic.html</loc>...</url>
<url><loc>https://vimark.art/ru/bookcover.html</loc>...</url>
```

**Добавить в `/sitemap.xml` (project/art страницы):**

Для каждого арта в `/project/art/` добавить блок:

```xml
<url>
  <loc>https://vimark.art/project/art/ENDYMION-COVER.html</loc>
  <lastmod>2026-06-10</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.6</priority>
  <image:image>
    <image:loc>https://vimark.art/images/projects/endymion-cover.jpg</image:loc>
    <image:title>Endymion by Dan Simmons — Book Cover by vimark</image:title>
  </image:image>
</url>
```

> **Примечание:** Заменить `ENDYMION-COVER.html` и пути на реальные имена файлов из `/project/art/`.

**Проверка:**
- Открыть `https://www.xml-sitemaps.com/validate-xml-sitemap.html`
- Загрузить `sitemap.xml` — ошибок быть не должно.

---

### Задача 2.3. H2-заголовки на book-illustrations.html

**Проблема:** Страница имеет только H1 («Book Illustrations»), без H2. AI и Google не видят структуры контента.

**Решение:** Сгруппировать иллюстрации по проектам/книгам с H2.

**HTML-структура:**

```html
<h1>Book Illustrations</h1>

<section class="illustration-group">
  <h2>20,000 Leagues Under the Sea</h2>
  <div class="gallery-grid">
    <!-- карточки иллюстраций -->
  </div>
</section>

<section class="illustration-group">
  <h2>The Shadow over Innsmouth</h2>
  <div class="gallery-grid">
    <!-- карточки иллюстраций -->
  </div>
</section>

<section class="illustration-group">
  <h2>Personal Projects</h2>
  <div class="gallery-grid">
    <!-- карточки -->
  </div>
</section>
```

**CSS (добавить):**

```css
.illustration-group {
  margin-bottom: 60px;
}

.illustration-group h2 {
  font-size: 24px;
  font-weight: 400;
  letter-spacing: 0.05em;
  margin-bottom: 30px;
  color: rgba(255, 255, 255, 0.8);
}
```

**Для RU:** аналогичная структура с русскими названиями книг.

---

## 3. Приоритет P1 — Важно для AI

### Задача 3.1. Schema.org на страницы project/art/*.html

**Проблема:** Страницы отдельных артов не имеют структурированных данных. AI не понимает, что это за работа, кто автор, какой жанр.

**Решение:** Добавить JSON-LD `VisualArtwork` на каждую страницу `project/art/*.html`.

**Шаблон (вставить в `<head>`):**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VisualArtwork",
  "name": "Endymion — Book Cover Illustration",
  "creator": {
    "@type": "Person",
    "name": "Max Mitenkov",
    "alternateName": "vimark",
    "url": "https://www.vimark.art/about.html"
  },
  "artform": "Digital Painting",
  "artMedium": "Digital",
  "genre": "Science Fiction",
  "about": {
    "@type": "Book",
    "name": "Endymion",
    "author": {
      "@type": "Person",
      "name": "Dan Simmons"
    }
  },
  "image": "https://www.vimark.art/images/projects/endymion-cover.jpg",
  "url": "https://www.vimark.art/project/art/endymion-cover.html",
  "dateCreated": "2025",
  "description": "Science fiction book cover illustration for Dan Simmons' Endymion, featuring a megastructure on a misty lakeside."
}
</script>
```

**Поля для заполнения под каждый арт:**

| Поле | Откуда брать | Пример |
|------|-------------|--------|
| `name` | Название работы | `"Endymion — Book Cover"` |
| `genre` | Жанр | `"Science Fiction"` / `"Fantasy"` / `"Horror"` / `"Dark Fantasy"` |
| `about.name` | Название книги | `"Endymion"` |
| `about.author` | Автор книги | `"Dan Simmons"` |
| `image` | Полный URL превью | `https://www.vimark.art/images/...` |
| `url` | Полный URL страницы | `https://www.vimark.art/project/art/...` |
| `dateCreated` | Год создания | `"2025"` |

**Для артов без книги** (персональные работы):

```json
{
  "@type": "VisualArtwork",
  "name": "Wanderer — Concept Art",
  "genre": "Science Fiction",
  "about": {
    "@type": "Thing",
    "name": "Original Concept Art"
  }
}
```

---

### Задача 3.2. Создать страницу /faq.html (EN + RU)

**Цель:** AI-агенты цитируют FAQ-формат. Страница отвечает на вопросы, которые задают авторы.

**Структура EN-версии:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>FAQ — Commissioning a Book Cover | vimark</title>
  <meta name="description" content="Answers to common questions about commissioning book cover illustrations from Max Mitenkov (vimark). Pricing, timelines, genres, and process.">
  <link rel="canonical" href="https://www.vimark.art/faq.html">
  <link rel="alternate" hreflang="en" href="https://www.vimark.art/faq.html">
  <link rel="alternate" hreflang="ru" href="https://www.vimark.art/ru/faq.html">
  <link rel="alternate" hreflang="x-default" href="https://www.vimark.art/faq.html">

  <!-- Schema FAQPage -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "How much does a sci-fi book cover cost?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Pricing depends on complexity, usage rights, and deadline. For a custom quote, contact Max Mitenkov (vimark) through the contact form or Reedsy. Typical range for a detailed sci-fi cover: $800–2500."
        }
      },
      {
        "@type": "Question",
        "name": "How long does it take to illustrate a book cover?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Typically 2–4 weeks from brief approval to final delivery. Rush orders are possible with advance notice. The process includes sketch approval, color comp, and final rendering stages."
        }
      },
      {
        "@type": "Question",
        "name": "What genres does vimark specialize in?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Max Mitenkov (vimark) specializes in science fiction, dark fantasy, fantasy, horror, and literary fiction book cover illustration. Notable works include covers for Dan Simmons' Endymion and The Shadow over Innsmouth."
        }
      },
      {
        "@type": "Question",
        "name": "How do I commission a book cover from vimark?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Contact through vimark.art/contact or via Reedsy. Provide a brief with genre, mood, key visual elements, and reference images. Max will respond with a timeline and quote within 48 hours."
        }
      },
      {
        "@type": "Question",
        "name": "Do you work with self-published authors?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes. Over 70% of clients are independent authors. The process and pricing are the same regardless of publisher size."
        }
      },
      {
        "@type": "Question",
        "name": "What file formats do you deliver?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Print-ready PDF, high-resolution PNG/TIFF (300 DPI), and web-optimized JPG. Source PSD files are available upon request."
        }
      },
      {
        "@type": "Question",
        "name": "Can you illustrate a series of covers?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Yes. Series packages are available with consistent visual language across all covers. See the Hoebeke sci-fi series case study for an example."
        }
      },
      {
        "@type": "Question",
        "name": "What is your revision policy?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Two rounds of revisions are included at the sketch and color comp stages. Additional revisions are billed hourly."
        }
      }
    ]
  }
  </script>
</head>
<body>
  <!-- Стандартный шаблон сайта (сайдбар, хедер, футер) -->

  <main>
    <h1>FAQ — Commissioning a Book Cover</h1>

    <section class="faq-item">
      <h2>How much does a sci-fi book cover cost?</h2>
      <p>Pricing depends on complexity, usage rights, and deadline. For a custom quote, contact Max Mitenkov (vimark) through the contact form or Reedsy. Typical range for a detailed sci-fi cover: $800–2500.</p>
    </section>

    <section class="faq-item">
      <h2>How long does it take to illustrate a book cover?</h2>
      <p>Typically 2–4 weeks from brief approval to final delivery...</p>
    </section>

    <!-- ... остальные 6 вопросов ... -->
  </main>

  <!-- Footer с .footer-links -->
</body>
</html>
```

**RU-версия:** аналогичная структура, вопросы на русском.

**Добавить в навигацию (сайдбар):**
- EN: `FAQ → /faq.html`
- RU: `FAQ → /ru/faq.html`

**Добавить в sitemap.xml:**
```xml
<url>
  <loc>https://vimark.art/faq.html</loc>
  <lastmod>2026-06-13</lastmod>
  <priority>0.8</priority>
</url>
<url>
  <loc>https://vimark.art/ru/faq.html</loc>
  <lastmod>2026-06-13</lastmod>
  <priority>0.8</priority>
</url>
```

---

### Задача 3.3. Дополнить Schema.org на существующих страницах

**index.html — дополнить `Person`:**

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Max Mitenkov",
  "alternateName": "vimark",
  "url": "https://www.vimark.art",
  "jobTitle": "Book Cover Illustrator and Designer",
  "description": "Professional book cover illustrator specializing in science fiction, dark fantasy, fantasy, horror, and literary fiction. 71 reviews on Reedsy.",
  "knowsAbout": [
    "Science Fiction Book Cover Design",
    "Dark Fantasy Book Cover Illustration",
    "Fantasy Book Cover Art",
    "Horror Book Cover Design",
    "Literary Fiction Cover Illustration",
    "Digital Painting",
    "Concept Art"
  ],
  "sameAs": [
    "https://www.reedsy.com/vimark",
    "https://www.behance.net/vimark",
    "https://www.instagram.com/vimark_art",
    "https://www.pinterest.com/vimark",
    "https://vimark.deviantart.com",
    "https://www.artstation.com/vimark"
  ],
  "makesOffer": {
    "@type": "Offer",
    "itemOffered": {
      "@type": "Service",
      "name": "Book Cover Illustration",
      "description": "Custom book cover design and illustration for authors and publishers in sci-fi, dark fantasy, fantasy, horror, and literary fiction genres."
    }
  }
}
```

**reviews.html — дополнить `AggregateRating`:**

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Max Mitenkov",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "71",
    "bestRating": "5",
    "worstRating": "1"
  }
}
```

---

## 4. Приоритет P2 — Улучшение UX и соцсетей

### Задача 4.1. Абсолютные пути в OG-тегах

**Проблема:** На project/art страницах OG-изображения имеют относительные пути (`../../thumbnails/...`).

**Решение:** Заменить на абсолютные URL.

**Шаблон OG-тегов для project/art:**

```html
<meta property="og:title" content="Endymion — Book Cover by vimark">
<meta property="og:description" content="Science fiction book cover illustration for Dan Simmons' Endymion.">
<meta property="og:image" content="https://www.vimark.art/images/projects/endymion-cover-og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://www.vimark.art/project/art/endymion-cover.html">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Endymion — Book Cover by vimark">
<meta name="twitter:image" content="https://www.vimark.art/images/projects/endymion-cover-og.jpg">
```

> **OG-изображение:** 1200×630px, JPG, < 1 MB.

---

### Задача 4.2. Переключатель языка — карта вместо replace()

**Проблема:** Текущий JS использует `replace()`, который ломается на нестандартных путях.

**Решение:** Жёсткая карта соответствия.

**JavaScript (заменить текущий switcher):**

```javascript
const langMap = {
  // EN → RU
  '/index.html': '/ru/index.html',
  '/about.html': '/ru/about.html',
  '/book-covers.html': '/ru/book-covers.html',
  '/book-illustrations.html': '/ru/book-illustrations.html',
  '/visual-stories.html': '/ru/visual-stories.html',
  '/living-illustrations.html': '/ru/living-illustrations.html',
  '/contact.html': '/ru/contact.html',
  '/reviews.html': '/ru/reviews.html',
  '/faq.html': '/ru/faq.html',
  '/case-studies/hoebeke-sci-fi-series.html': '/ru/case-studies/hoebeke-sci-fi-series.html',
  // project/art — если есть RU-версии

  // RU → EN (обратная карта)
  '/ru/index.html': '/index.html',
  '/ru/about.html': '/about.html',
  '/ru/book-covers.html': '/book-covers.html',
  '/ru/book-illustrations.html': '/book-illustrations.html',
  '/ru/visual-stories.html': '/visual-stories.html',
  '/ru/living-illustrations.html': '/living-illustrations.html',
  '/ru/contact.html': '/contact.html',
  '/ru/reviews.html': '/reviews.html',
  '/ru/faq.html': '/faq.html',
  '/ru/case-studies/hoebeke-sci-fi-series.html': '/case-studies/hoebeke-sci-fi-series.html'
};

function switchLanguage() {
  const currentPath = window.location.pathname;
  const targetPath = langMap[currentPath];

  if (targetPath) {
    window.location.href = targetPath;
  } else {
    // Fallback: если пути нет в карте, пробуем простую замену /ru/
    if (currentPath.startsWith('/ru/')) {
      window.location.href = currentPath.replace('/ru/', '/');
    } else {
      window.location.href = '/ru' + currentPath;
    }
  }
}

// Навесить на кнопку переключения языка
document.querySelector('.lang-switcher').addEventListener('click', switchLanguage);
```

---

## 5. Приоритет P3 — Полировка

### Задача 5.1. Унифицировать навигацию (убрать наследие)

**Проблема:** Страницы `personal.html`, старые `comic.html` и др. имеют устаревшее меню с якорными ссылками (`index.html#`).

**Решение:** На всех страницах наследия заменить меню на современное (7 пунктов + FAQ).

**Современное меню (EN):**
```
Book Covers → /book-covers.html
Book Illustrations → /book-illustrations.html
Case Studies → /case-studies/hoebeke-sci-fi-series.html
Visual Stories → /visual-stories.html
About → /about.html
Contact → /contact.html
Reviews → /reviews.html
FAQ → /faq.html
```

**RU:** аналогично с `/ru/` префиксом.

---

### Задача 5.2. Удалить `/ru/sitemap.xml`

**Проблема:** Дублирование — `/sitemap.xml` уже включает все RU-URL.

**Решение:**
1. Удалить файл `/ru/sitemap.xml`.
2. В `robots.txt` оставить только:
```
Sitemap: https://vimark.art/sitemap.xml
```

---

### Задача 5.3. Закрыть интерактивные страницы от индексации

**Проблема:** `living-illustrations/pilot/index.html` и `after-picasso/index.html` — без canonical/hreflang.

**Решение:** Добавить в `<head>` каждой:

```html
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://vimark.art/living-illustrations.html">
```

---

### Задача 5.4. Meta robots на контентных страницах

**Добавить на все контентные страницы** (index, about, book-covers, book-illustrations, visual-stories, contact, reviews, faq, case-studies):

```html
<meta name="robots" content="index, follow">
```

---

## 6. Чек-лист приёмки

### Техническая проверка

- [x] `.footer-links` присутствует в HTML на всех 8 хабах (EN + RU)
- [x] `.footer-links` скрыт на десктопе (`display: none`), виден на mobile (≤800px)
- [x] `sitemap.xml` проходит валидацию без ошибок
- [x] В sitemap нет URL с 301-редиректом
- [x] В sitemap добавлены все `project/art/*` страницы
- [x] `book-illustrations.html` имеет H2-заголовки по проектам
- [ ] Каждая `project/art/*.html` имеет JSON-LD `VisualArtwork`
- [x] Созданы `/faq.html` и `/ru/faq.html` с `FAQPage` schema
- [ ] Все OG-изображения — абсолютные URL, 1200×630
- [x] Переключатель языка работает на всех страницах без ошибок
- [x] Удалён `/ru/sitemap.xml`
- [x] `robots.txt` содержит только один Sitemap
- [x] Интерактивные страницы имеют `noindex`

### AI-проверка (через 2–4 недели после деплоя)

- [ ] Perplexity: запрос "book cover illustrator sci-fi" — vimark.art в топ-5
- [ ] ChatGPT (с Browse): "who illustrated Endymion cover" — упоминание Max Mitenkov
- [ ] Google Rich Results Test: `/about.html` проходит валидацию Person schema
- [ ] Google Rich Results Test: `/faq.html` проходит валидацию FAQPage schema

---

*Техническое задание составлено для vimark.art — Living Illustrations.*
