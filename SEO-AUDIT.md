# vimark.art — SEO-аудит: текущее состояние сайта

## 1. Архитектура сайта

Сайт — портфолио иллюстратора Максима Митенкова (vimark). Двуязычный: EN (основной) + RU (`/ru/`).

### Основные страницы (хабы)

| Страница | EN | RU | Назначение |
|----------|----|----|------------|
| Главная | `/index.html` | `/ru/index.html` | Титульная страница — герой + 3 секции-тизера (Book Illustrations, Book Covers, Visual Stories) с карточками и ссылками «View all →» на соответствующие хабы |
| Book Covers | `/book-covers.html` | `/ru/book-covers.html` | Галерея обложек по годам (2026, 2025, 2024) |
| Book Illustrations | `/book-illustrations.html` | `/ru/book-illustrations.html` | Галерея книжных иллюстраций |
| Visual Stories | `/visual-stories.html` | `/ru/visual-stories.html` | Комиксы и графические истории: разделы Series (8 серий), Standalone (фильтр по жанрам Sci-Fi/Fantasy/Horror/Surreal), Living Illustrations |
| Living Illustrations | `/living-illustrations.html` | `/ru/living-illustrations.html` | Интерактивные иллюстрации (WebGL) — **noindex** (скрыты из поиска) |
| About | `/about.html` | `/ru/about.html` | Полное портфолио: био, клиенты, избранные работы, отзывы |
| Reviews | `/reviews.html` | `/ru/reviews.html` | 20 отзывов с Reedsy |
| Contact | `/contact.html` | `/ru/contact.html` | Форма связи |
| Case Study | `/case-studies/hoebeke-sci-fi-series.html` | `/ru/case-studies/hoebeke-sci-fi-series.html` | Кейс по серии обложек для Hachette |

### Служебные страницы

`privacy.html`, `thanks.html`, `404.html`, `yandex_*.html`

### Проектные страницы

`/project/comic-*` (8 серий), `/project/bookcover-*` (по годам), `/project/book-illustrations-*` (6 проектов), `/project/personal-*` (3), `/project/art/*` (множество отдельных артов).

### Наследие (редиректы)

| Было | Стало | Тип |
|------|-------|-----|
| `/comic.html` | → `/visual-stories.html` | 301 |
| `/bookcover.html` | → `/book-covers.html` | 301 |
| `/about_vimark_en.html` | → `/about.html` | 301 |
| `/about_vimark_ru.html` | → `/ru/about.html` | 301 |
| `/case-study-hoebeke.html` | → `/case-studies/hoebeke-sci-fi-series.html` | 301 |
| `www.vimark.art/*` | → `vimark.art/*` | 301 |

Все редиректы настроены в `vercel.json`.

---

## 2. Навигация

### Основная (сайдбар)

На всех хабах (кроме наследия) одинаковое меню:

```
Book Covers → book-covers.html
Book Illustrations → book-illustrations.html
Case Studies → case-studies/hoebeke-sci-fi-series.html
Visual Stories → visual-stories.html
About → about.html
Contact → contact.html
Reviews → reviews.html
```

Логотип → `index.html`.

### Мобильная

Гамбургер-меню (`.mobile-toggle`), сайдбар скрыт/открывается.

### Футер

**.footer-links** есть только на `visual-stories.html` и `book-covers.html` (EN + RU). Включает ссылки на все основные страницы + внешние профили (Reedsy, Behance, ArtStation, Instagram, Pinterest, DeviantArt).

На десктопе `.footer-links` скрыт (`display: none`), на мобильных (≤800px) отображается как flex-column.

Остальные страницы (`index.html`, `book-illustrations.html`, `about.html`, `contact.html`, `reviews.html`) не имеют `.footer-links` — только копирайт + переключатель языка.

### Языковой переключатель

JavaScript в футере динамически строит ссылки EN ↔ RU. + hreflang-теги в `<head>` каждой страницы (en, ru, x-default).

---

## 3. Изменения, внесённые в ходе реструктуризации

### Было
- Comic был отдельным разделом (навигация: «Comic»)
- Index показывал все карточки всех разделов на одной странице
- Living Illustrations были самостоятельным разделом в навигации
- Серия Vegetation лежала в Book Illustrations
- Футер-ссылки были на всех страницах (старый шаблон)

### Стало
1. **Comic → Visual Stories**: раздел переименован, навигация теперь «Visual Stories». `/comic.html` → 301 → `/visual-stories.html`. Фильтр bar на index: «Comic» → «Visual Stories».
2. **Index — тизерный режим**: вместо полных списков — 3 секции по 2–3 карточки + кнопка «View all →» (стиль `.cv-link`), ведущая на соответствующий хаб.
3. **Living Illustrations** перемещены внутрь Visual Stories (после Standalone, перед CTA-секцией) + удалены из навигации. Хабы `/living-illustrations.html` сохранены, но закрыты `noindex`.
4. **Vegetation** — перенесена из Book Illustrations в Visual Stories (в раздел Series).
5. **Series — расширение**: было 1 серия (Vegetation), стало 8: Biological Deviations, Faceless, Geologyst, Nemirum, The Symbol Of Faith, Wanderer, Winter, Vegetation.
6. **Футер**: `.footer-links` заменён на мобильную версию (только на mobile, скрыт на desktop).

---

## 4. JSON-LD / Structured Data

| Страница | Схемы |
|----------|-------|
| index.html | `Person` |
| book-covers.html | `CollectionPage` (с `hasPart` по годам) + `BreadcrumbList` |
| book-illustrations.html | `BreadcrumbList` |
| visual-stories.html | `CollectionPage` (с `hasPart` для 8 серий) + `BreadcrumbList` |
| about.html | `Person` (с `@id`, offers, workExample — 10 книг с ISBN) + `BreadcrumbList` |
| contact.html | `Person` + `BreadcrumbList` |
| reviews.html | `BreadcrumbList` + `Service` + `AggregateRating` (71 review, 5.0) |
| case-studies/*.html | `Article` + `BreadcrumbList` + `CreativeWork` |
| project/*.html | `BreadcrumbList` |

`CollectionPage` есть на визуальных стори и бук-каверах, но **нет** на book-illustrations (там только BreadcrumbList).

---

## 5. Мета-теги

- **Meta description**: уникальные на всех страницах.
- **Canonical**: самоссылающиеся на всех страницах.
- **Viewport**: `width=device-width, initial-scale=1.0` на всех.
- **Robots**: нет `<meta name="robots">` ни на одной странице.
- **X-Robots-Tag** (через Vercel headers): `noindex` на `/living-illustrations.html`, `/ru/living-illustrations.html`, `/living-illustrations/:path*`.
- **hreflang**: en / ru / x-default — на всех контентных страницах.

---

## 6. Sitemap

- `/sitemap.xml` — 40 URL (EN + RU), приоритеты 0.5–1.0.
- `/ru/sitemap.xml` — дублирует RU-часть (25 URL).

**Проблема**: в sitemap всё ещё указаны `comic.html`, `bookcover.html`, `case-study-hoebeke.html`, хотя они 301-редрят. `project/art/*` (десятки отдельных артов) — не включены.

---

## 7. Заголовки (H1–H3)

| Страница | H1 | H2 | H3 |
|----------|----|----|----|
| index.html | «Max Mitenkov» + «About» + «Contact» | Book Illustrations, Book Covers, Visual Stories | карточки проектов |
| book-covers.html | «Book Covers» | 2026, 2025, 2024, Commission a Cover | нет |
| book-illustrations.html | «Book Illustrations» | **нет** | нет |
| visual-stories.html | «Visual Stories» | Series, Standalone, Living Illustrations | карточки серий |

**book-illustrations** — самая плоская структура (нет h2).

---

## 8. Выявленные проблемы для SEO

### Критические
1. **Нет footer-ссылок на 6 из 8 хабов** — `index.html`, `book-illustrations.html`, `about.html`, `contact.html`, `reviews.html`, `living-illustrations.html` (EN) не имеют внутренних ссылок в футере. Только `visual-stories.html` и `book-covers.html` их имеют.
2. **Sitemap содержит мёртвые URL** — `comic.html`, `bookcover.html`, `case-study-hoebeke.html` 301-редрят, но всё ещё перечислены.
3. **project/art/* не в sitemap** — десятки отдельных артов (каждый мог бы ранжироваться по long-tail запросам).
4. **book-illustrations.html без h2** — Google не видит иерархии контента.

### Средние
5. **Две системы навигации** — современные хабы (7 пунктов) vs. наследие (`personal.html`, `comic.html`, `bookcover.html`, `living-illustrations.html`) со старым меню (ссылки на `index.html#`).
6. **Дублирование sitemap** — `/sitemap.xml` уже включает все RU URL, отдельный `/ru/sitemap.xml` избыточен.
7. **Living Illustrations в `ru/sitemap.xml`** — хотя страница noindex.
8. **Нет `<meta name="robots">`** — reliance только на `X-Robots-Tag` в Vercel headers.

### Низкие
9. **OG-изображения** — на некоторых project/art страницах пути вида `../../thumbnails/...` — могут не резолвиться.
10. **JS-переключатель языка** — использует `replace()` а не универсальную карту; может сломаться на нестандартных путях.
11. **Отдельные interactive-страницы** (`living-illustrations/pilot/index.html` и `after-picasso/index.html`) — без hreflang, без canonical (могут индексироваться).

---

## 9. Технический стек

- **Хостинг**: Vercel (static SPA, auto-deploy из master)
- **Локальная разработка**: Python http.server на порту 8000
- **CSS**: `style.css` (один файл, ~2237 строк)
- **JS**: инлайн (переключатель меню, языковой switcher)
- **Фильтры**: жанровые табы на visual-stories.html (Selenium-протестированы)
