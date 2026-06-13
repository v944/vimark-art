# vimark.art — SEO-ревизия и полный обзор сайта

> **Дата:** 2026-06-13  
> **Сайт:** https://vimark.art  
> **Русская версия:** https://vimark.art/ru/  
> **Владелец:** Max Mitenkov / Максим Митенков  
> **Назначение документа:** передать человеку без доступа к коду актуальное состояние сайта, реализованные SEO-механики для людей и для поисковых агентов, а также общую структуру и процесс обновления.

---

## 1. Краткое резюме

Сайт — статическое двуязычное портфолио иллюстратора / концепт-художника. Контент генерируется кастомным Python-скриптом (`generate_site.py`) из папок с изображениями, метаданных проектов и локализации. Сайт развёрнут на Vercel, деплой происходит автоматически при push в ветку `master` GitHub.

**Последние доработки (вошли в пуш 2026-06-13):**

- Подключена единая система типографики `vimark_typography_system.css` (размеры, межстрочные, контраст).
- Во всём сайте обновлено главное меню до единого набора пунктов.
- Настроен генератор так, чтобы он больше не перезаписывал кастомные landing-страницы (Book Illustrations, Book Covers, Visual Stories, Reviews и т.д.).
- Восстановлены кастомные landing-страницы, которые генератор ранее затёр шаблонными.
- Добавлены страницы отдельных артворков для кейса `images/case-study/` (Creatures, Planètes).

---

## 2. Общие характеристики

| Параметр | Значение |
|----------|----------|
| **Тип сайта** | Статический HTML/CSS/JS |
| **Языки** | English (основной), Russian (`/ru/`) |
| **Хостинг / деплой** | Vercel, автодеплой из GitHub `master` |
| **SSL** | ✅ Vercel по умолчанию |
| **CMS / бэкенд** | Нет |
| **Фреймворки** | Нет, ванильный HTML/CSS/JS |
| **Генератор** | `generate_site.py` (Python + Pillow) |
| **Всего HTML-страниц** | ~403 |
| **Всего изображений** | ~630 (оригиналы + thumbnails + Pinterest + иконки) |

### Объём портфолио

| Категория | Проектов | Примерные страницы |
|-----------|----------|-------------------|
| Book Illustrations | 5 серий | 20 000 Leagues Under the Sea, Endymion, The Shadow over Innsmouth, The Nameless City, Winter’s Twins, Vegetation |
| Book Covers | 3 года | 2024, 2025, 2026 |
| Visual Stories (Comic) | 7 серий | Biological Deviations, Faceless, Geologyst, Nemirum, The Symbol of Faith, Wanderer, Winter |
| Personal | 3 периода | Early Work, Professional Growth, Recent Work |
| Case Studies | 1 публикация | Hoëbeke Sci-Fi Series + артворки Creatures / Planètes |

---

## 3. Архитектура и генератор

### 3.1 Основные файлы

| Файл | Назначение |
|------|------------|
| `generate_site.py` | Генератор сайта: сканирование папок, создание thumbnails, HTML-страниц, sitemap, Pinterest-ассетов |
| `style.css` | Основная таблица стилей (layout, компоненты, адаптив) |
| `vimark_typography_system.css` | Единая типографика (размеры, интерлиньяж, контраст) |
| `script.js` | Интерактивность: фильтры, lightbox, тема, языковой переключатель |
| `projects.ini` | Метаданные проектов (title, year, client, description) |
| `captions.txt` | Подписи и alt-тексты к изображениям |
| `locale.ini` | Строки локализации EN / RU |
| `Reedsy/reviews.json` | Отзывы клиентов (источник для `reviews.html`) |

### 3.2 Что делает генератор

При запуске `python generate_site.py`:

1. Сканирует папки с работами (`Book Illustrations/`, `BookCover/`, `comic/`, `Personal/`, `images/`, `STRONG/`, `HERO2/`).
2. Создаёт thumbnails WebP 600×600 (качество 85%).
3. Создаёт Pinterest-ассеты 1200×1800 и `pinterest/pins.json`.
4. Генерирует `/project/{id}.html` и `/project/art/{slug}.html` для всех языков.
5. **Больше не перезаписывает** кастомные landing-страницы (`index.html`, `book-illustrations.html`, `book-covers.html`, `visual-stories.html`, `reviews.html` и их `ru/` версии).

### 3.3 Статичные vs генерируемые страницы

| Страница | Тип | Комментарий |
|----------|-----|-------------|
| `index.html`, `ru/index.html` | Статичная | Кастомный дизайн главной, фильтры, CTA |
| `book-illustrations.html`, `book-covers.html`, `visual-stories.html`, `reviews.html`, `about.html`, `contact.html`, `faq.html`, `privacy.html`, `404.html`, `thanks.html` и `ru/` версии | Статичная | Редактируются вручную |
| `case-studies/hoebeke-sci-fi-series.html` | Статичная | Детальный кейс для издательства |
| `project/*.html`, `project/art/*.html` | Автогенерируемые | Пересоздаются при каждом запуске генератора |
| `sitemap.xml`, `image-sitemap.xml` | Статичные | Больше не перезаписываются генератором |

---

## 4. SEO для людей (UX, контент, доступность)

### 4.1 Навигация

Единое главное меню на всех страницах:

- Book Covers
- Book Illustrations
- Case Studies
- Visual Stories
- About
- Contact
- Reviews
- FAQ

В русской версии пункты локализованы:

- Обложки книг
- Иллюстрации к книгам
- Кейсы
- Визуальные истории
- Обо мне
- Контакты
- Отзывы
- FAQ

Ссылки на разделы, у которых нет отдельной русской страницы, ведут на английские версии (`../book-covers.html`, `../case-studies/...`, `../visual-stories.html`).

### 4.2 Типографика и читаемость

- Подключена система типографики `vimark_typography_system.css`.
- Размерная шкала: H1 24px → H2 18px → body 15px.
- Цвета текста с учётом контраста на тёмном фоне.
- Увеличены размеры шрифтов в блоке `about-content` для лучшей читаемости.

### 4.3 Структура страниц

- Семантическая вёрстка: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<figure>`, `<figcaption>`, `<footer>`, `<aside>`.
- Каждая страница имеет понятный H1, описательный lead/intro, CTA.
- Страницы проектов содержат: hero-изображение, мета-информацию (title, year, client, description), галерею, хлебные крошки, ссылки на соседние работы.

### 4.4 Социальное доказательство

- `reviews.html` — 71 verified review с Reedsy.
- `case-studies/hoebeke-sci-fi-series.html` — детальный кейс для издательства Hoëbeke / Hachette Livre.
- На главной и в проектах есть призывы к действию (CTA).

### 4.5 Контакт и конверсия

- Форма обратной связи на `contact.html` через Web3Forms.
- Email, Telegram, WhatsApp — в боковом меню и sticky-блоке.
- Страница `thanks.html` после отправки формы.

### 4.6 Мобильная версия

- Responsive layout: боковое меню превращается в кнопку «Menu» на ≤800px.
- Grid карточек адаптируется к ширине экрана.
- Hero-изображения сохраняют пропорции.

### 4.7 Доступность

- `alt`-тексты у изображений.
- `aria-label` у иконок соцсетей и кнопок.
- `loading="lazy"` для галерей.

---

## 5. SEO для агентов (техническое SEO)

### 5.1 Базовые метатеги

- `<title>` — уникальный на каждой странице.
- `<meta name="description">` — уникальный, описывает контент.
- `<meta charset="UTF-8">`, `<meta name="viewport">`.
- `<meta name="robots" content="index, follow">` на статичных landing-страницах.

### 5.2 Canonical и hreflang

- Каждая страница имеет `<link rel="canonical">`.
- Для двуязычных страниц прописаны `hreflang="en"`, `hreflang="ru"`, `hreflang="x-default"`.
- Пример: на `https://vimark.art/project/book-illustrations-endymion.html` указаны EN, RU и x-default версии.

### 5.3 Open Graph и Twitter Cards

- `og:type`, `og:url`, `og:title`, `og:description`, `og:image`, `og:image:width`, `og:image:height`.
- `twitter:card="summary_large_image"` + аналогичные поля.
- `image_src` для старых агрегаторов.
- Изображения OG берутся из thumbnails WebP.

### 5.4 Schema.org

- **Person** — на главной: имя, alternateName, jobTitle, description, knowsAbout, sameAs (соцсети), makesOffer.
- **BreadcrumbList** — на страницах проектов и артворков.
- **AggregateRating** — на `reviews.html` (ratingValue 5.0, reviewCount 71).
- **CollectionPage** — ранее использовался на страницах проектов.

### 5.5 Карты сайта

- `robots.txt` разрешает индексацию и указывает `Sitemap: https://vimark.art/sitemap.xml`.
- `sitemap.xml` — карта страниц.
- `image-sitemap.xml` — карта изображений.
- Текущие карты являются статичными (генератор больше их не перезаписывает).

### 5.6 robots.txt и noindex

```
User-agent: *
Allow: /
Allow: /images/
Allow: /uploads/
Disallow: /admin
Disallow: /.env
Disallow: /cgi-bin
Disallow: /wp-config
Sitemap: https://vimark.art/sitemap.xml
```

Через `vercel.json` настроены `X-Robots-Tag: noindex` для:

- `/living-illustrations.html`
- `/ru/living-illustrations.html`
- `/living-illustrations/:path*`

### 5.7 Редиректы (vercel.json)

- `www` → `non-www` (301).
- `/bookcover.html` → `/book-covers.html`.
- `/ru/bookcover.html` → `/ru/book-covers.html`.
- `/case-study-hoebeke.html` → `/case-studies/hoebeke-sci-fi-series.html`.
- `/comic.html` → `/visual-stories.html` (и ru-версия).
- `/case-studies/` → `/case-studies/hoebeke-sci-fi-series.html` (302).

### 5.8 Изображения

- Thumbnails генерируются в WebP, 600×600, качество 85%.
- Оригиналы хранятся в JPG/PNG.
- У всех изображений есть `alt`.
- Галереи используют `loading="lazy"`.
- Pinterest-ассеты 1200×1800 для Rich Pins.

### 5.9 Pinterest Rich Pins

- На страницах проектов прописаны:
  - `pinterest-rich-pin = true`
  - `article:published_time`

### 5.10 Аналитика

- **Google Analytics 4** — `G-6RBP7X7H88`.
- **Yandex.Metrika** — счётчик `109279162` с вебвизором, картами кликов, целями.

### 5.11 Структура URL

- ЧПУ: `/book-illustrations.html`, `/project/book-illustrations-endymion.html`, `/project/art/the-giant-squid.html`.
- Иерархия: `/ru/` для русской версии.
- Нет query-параметров, динамических сессий и т.п.

---

## 6. Структура сайта

### 6.1 Корневые страницы (English)

| URL | Title | Назначение |
|-----|-------|------------|
| `/` | Max Mitenkov · Illustrator · Concept Artist | Главная |
| `/book-covers.html` | Book Covers · Max Mitenkov | Лендинг обложек |
| `/book-illustrations.html` | Book Illustrations · Max Mitenkov | Лендинг иллюстраций |
| `/visual-stories.html` | Visual Stories · Max Mitenkov | Лендинг визуальных историй (бывший Comic) |
| `/case-studies/hoebeke-sci-fi-series.html` | Case Study: Hoëbeke Sci-Fi Covers · Max Mitenkov | Кейс издательства |
| `/about.html` | About vimark · Book Cover Illustrator & Designer | О художнике |
| `/contact.html` | Contact · Max Mitenkov | Форма связи |
| `/reviews.html` | 71 Verified Reedsy Reviews · Max Mitenkov | Отзывы |
| `/faq.html` | FAQ — Commissioning a Book Cover · Max Mitenkov | Частые вопросы |
| `/privacy.html` | Privacy Policy · vimark.art | Политика конфиденциальности |
| `/thanks.html` | Thank You · Max Mitenkov | Страница благодарности |
| `/404.html` | Page Not Found · Max Mitenkov | 404 |

### 6.2 Корневые страницы (Russian)

| URL | Title |
|-----|-------|
| `/ru/` | Максим Митенков · Иллюстратор · Концепт-художник |
| `/ru/book-covers.html` | Обложки книг · Максим Митенков |
| `/ru/book-illustrations.html` | Иллюстрации к книгам · Максим Митенков |
| `/ru/visual-stories.html` | Визуальные истории · Максим Митенков |
| `/ru/case-studies/hoebeke-sci-fi-series.html` | Кейс: обложки Hoëbeke · Максим Митенков |
| `/ru/about.html` | О vimark · Иллюстратор и дизайнер книжных обложек |
| `/ru/contact.html` | Контакты · Максим Митенков |
| `/ru/reviews.html` | 71 проверенных отзыва на Reedsy · Максим Митенков |
| `/ru/faq.html` | FAQ — Заказ обложки для книги · Максим Митенков |

### 6.3 Страницы проектов

- `/project/{subcategory}.html` — hub страница серии (18+ страниц).
- `/project/art/{slug}.html` — страница отдельного артворка (300+ страниц).
- `ru/project/...` — русские версии тех же страниц.

---

## 7. Процесс обновления

```
1. Добавить новые изображения в папку проекта
   (например, Book Illustrations/NewProject/)

2. При необходимости обновить:
   - projects.ini   (метаданные проекта)
   - captions.txt   (подписи и alt-тексты)
   - locale.ini     (переводы)

3. Запустить генератор:
   python generate_site.py

4. Генератор обновит:
   - thumbnails/
   - pinterest/images/
   - project/*.html
   - project/art/*.html
   - ru/project/*.html
   - ru/project/art/*.html

5. Кастомные landing-страницы НЕ перезаписываются.
   Их нужно редактировать вручную.

6. Закоммитить и запушить:
   git add -A && git commit -m "..." && git push origin master
```

---

## 8. Что делать при реструктуризации

- **Добавить новый раздел:** создать папку в корне, добавить туда изображения, обновить `locale.ini` и `projects.ini`, запустить генератор, затем вручную создать/обновить статичный landing.
- **Изменить меню:** отредактировать `generate_site.py` (шаблоны `project_nav`, `cat_nav_lines`, `reviews_nav`, `nav_lines`) + вручную обновить статичные HTML.
- **Изменить дизайн landing:** редактировать соответствующий `.html` вручную.
- **Добавить отзывы:** пополнить `Reedsy/reviews.json` и перегенерировать `reviews.html` вручную (генератор его больше не трогает).

---

## 9. Известные нюансы и рекомендации

1. **Sitemap статичен.** После добавления новых проектов стоит обновить `sitemap.xml` и `image-sitemap.xml` вручную или временно включить их генерацию в `generate_site.py`.
2. **Pinterest workflow отключён.** Файл `.github/workflows/pinterest.yml.disabled` не публикует пины автоматически. Для автопубликации нужно переименовать в `.yml` и добавить секреты Pinterest.
3. **Количество отзывов.** На сайте заявлено 71 отзыв, в `Reedsy/reviews.json` меньше. Нужно либо импортировать недостающие, либо скорректировать цифру.
4. **Адаптивные изображения.** Пока нет `<picture>` / `srcset` / AVIF. Это средний приоритет для Core Web Vitals.
5. ** robots meta на generated-страницах.** В сгенерированных `project/` страницах отсутствует `<meta name="robots" content="index, follow">`. Поисковики по умолчанию индексируют, но для явности можно добавить в шаблон генератора.
6. **H1-H2 иерархия.** Последняя типографика задаёт размеры 24px / 18px / 15px, но `font-weight` и цвета разделов стоит сверить визуально, чтобы H1 всегда читался как главный.

---

## 10. Контакты и доступы

- **Репозиторий:** https://github.com/v944/vimark-art
- **Домен:** https://vimark.art
- **Хостинг:** Vercel (привязан к репозиторию)
- **Аналитика:** Google Analytics 4 `G-6RBP7X7H88`, Yandex.Metrika `109279162`
