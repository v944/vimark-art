# vimark.art — Текущее состояние сайта

> Документ описывает актуальную структуру, процессы и выполненные работы по SEO и GEO.
> Дата: 20 июня 2026

---

## 1. Общая архитектура

**Тип сайта:** полностью статический, одностраничный (SPA-подобная навигация) + отдельные страницы для проектов/артов/блога.

**Генератор:** самописный на Python (`generate_site.py` ~2500 строк + `site_frame.py` ~165 строк + `blog_convert.py` ~418 строк).

**Деплой:** Vercel (static deployment, без билд-команды — файлы отдаются как есть).

**Домен:** `vimark.art` → редирект с `www.vimark.art`.

**Автор:** Max Mitenkov (Maksim Mitenkov), иллюстратор и концепт-художник.

---

## 2. Структура файлов и каталогов

### Корень сайта (`D:\Concept_work\Vimark_art\`)

#### Страницы (HTML, сгенерированные)

| Файл | Описание |
|------|----------|
| `index.html` | Главная — портфолио-лента, герой, фильтр, проекты |
| `404.html` | Страница 404 |
| `about.html` | Об авторе |
| `book-covers.html` | Галерея обложек книг |
| `book-illustrations.html` | Галерея иллюстраций к книгам |
| `bookcover.html` | Альтернативная страница обложек (редиректится на book-covers.html) |
| `case-studies/hoebeke-sci-fi-series.html` | Кейс: научно-фантастическая серия Hoebeke |
| `comic.html` | Страница комиксов (редиректится на visual-stories.html) |
| `contact.html` | Контакты (форма Web3Forms) |
| `faq.html` | Часто задаваемые вопросы |
| `living-illustrations.html` | «Живые иллюстрации» — **noindex** |
| `personal.html` | Персональные работы |
| `privacy.html` | Политика конфиденциальности |
| `reviews.html` | 71 отзыв с Reedsy, AggregateRating JSON-LD |
| `services.html` | Услуги и цены |
| `thanks.html` | Спасибо после отправки формы |
| `visual-stories.html` | Визуальные истории (комиксы) |

#### Страницы проектов (`project/`)

- `project/art/` — ~100+ HTML-страниц отдельных артов (каждый арт — отдельная страница с JSON-LD VisualArtwork + ImageObject)
- `project/book-illustrations-*.html` — страницы проектов книжных иллюстраций
- `project/bookcover-*.html` — страницы проектов обложек
- `project/comic-*.html` — страницы комикс-проектов
- `project/personal-*.html` — страницы персональных проектов
- `project/images-case-study.html` — изображения к кейсам

#### Русская версия (`ru/`)

Полное зеркало английской версии:
- `ru/index.html`, `ru/about.html`, `ru/services.html`, `ru/contact.html`, `ru/reviews.html`, `ru/faq.html`, `ru/book-covers.html`, `ru/book-illustrations.html`, `ru/comic.html`, `ru/personal.html`, `ru/living-illustrations.html`, `ru/visual-stories.html`
- `ru/project/art/` — русские версии страниц артов
- `ru/case-studies/hoebeke-sci-fi-series.html`
- `ru/blog/` — русские статьи блога
- `ru/sitemap.xml`

#### Блог (`blog/`)

- `blog/index.html` — список статей
- 5 статей на английском (HTML)
- 5 исходников на Markdown (билингва — EN + RU в одном файле)

#### CSS

| Файл | Строк | Назначение |
|------|-------|------------|
| `style.css` | 2560 | Основной: лейаут, галерея, герой, сайдбар, лайтбокс, отзывы, адаптивность, темы |
| `vimark_typography_system.css` | 341 | Типографика: переменные, H1–H4, FAQ, статьи, отзывы, мобильные |
| `blog.css` | 44 | Блог: индекс, статья, чеклисты |

#### JavaScript

| Файл | Строк | Назначение |
|------|-------|------------|
| `script.js` | 572 | Лайтбокс, темы (светлая/тёмная), мобильное меню, навигация, фильтр категорий, спин-спам контактной формы, трекинг GA4 + Я.Метрика |

#### Исходники изображений (непубликуемые, кроме STRONG)

| Каталог | Описание |
|----------|----------|
| `Book Illustrations/` | ~80+ JPG исходников по проектам (Endymion, Innsmouth, Nameless City, Planetes и др.) |
| `BookCover/` | ~30+ JPG обложек (2024, 2025, 2026, Planetes) |
| `comic/` | ~60+ JPG комиксов (Faceless, Geologyst, Nemirum, Winter, Wanderer и др.) |
| `Personal/` | ~30+ JPG (Early Work, Professional Growth, Recent Work) |
| `STRONG/` | 7 лучших работ для героя и OG-изображений |
| `HERO/` | 8 устаревших JPG для героя |
| `HERO2/` | 6 текущих PNG для героя |
| `images/case-study/` | 5 скриншотов для кейсов |
| `images/logos/` | 4 SVG-логотипа (HarperCollins, Hachette, Reedsy, Amazon) |
| `__UE_web/` | Ассеты Unreal Engine WebGL (сцена + текстуры) |
| `Reedsy/` | 4 PNG-графика отзывов (professionalism, quality, value, responsiveness) |
| `thumbnails/` | **Автоматически сгенерированные** WebP превью (600×600, 400×400) для всех изображений |

#### Конфигурация и данные

| Файл | Формат | Назначение |
|------|--------|------------|
| `locale.ini` | INI | ~70 ключей перевода EN + RU |
| `projects.ini` | INI | Метаданные 26+ проектов (название, год, клиент, описание) |
| `art_reviews.ini` | INI | Привязка артов к отзывам (~15 записей) |
| `captions.txt` | TXT | Переопределение подписей к изображениям (путь=подпись) |
| `display_titles.txt` | TXT | Переопределение отображаемых названий (`[en]` / `[ru]`) |
| `Reedsy/reviews.json` | JSON | 23 отзыва с Reedsy (имя, дата, фото, текст, рейтинг) |
| `pinterest/pins.json` | JSON | Реестр пинов для Pinterest (статус: ready/published) |
| `vercel.json` | JSON | 44 редиректа + security headers (CSP, HSTS, X-Frame-Options и др.) |
| `manifest.json` | JSON | PWA-манифест |
| `BingSiteAuth.xml` | XML | Верификация Bing Webmaster Tools |
| `yandex_7042082dca4f98fb.html` | HTML | Верификация Яндекс.Вебмастер |

#### Служебные каталоги

| Каталог | Описание |
|----------|----------|
| `To_update/` | **Drop-папка** для новых изображений (в `.gitignore`, не коммитится) |
| `_scenes/desert-giants/` | Тестовый 3D-проект (Node.js, не относится к сайту) |
| `_UE_web/` | Unreal Engine WebGL эксперименты |
| `.github/workflows/pinterest.yml.disabled` | CI Pinterest (отключён) |
| `pinterest/images/` | Автосгенерированные 2:3 изображения для Pinterest (1200×1800) |

---

## 3. Процесс обновления сайта

### 3.1 Добавление новых работ

1. Исходники кладутся в соответствующую папку:
   - `Book Illustrations/<project_name>/`
   - `BookCover/<year>/` или `BookCover/planetes/`
   - `comic/<series_name>/`
   - `Personal/<period>/`
2. Если проект новый — добавляется секция в `projects.ini`.
3. Если нужны переопределения — правятся `captions.txt`, `display_titles.txt`.
4. Запускается генератор:
   ```
   python generate_site.py
   ```
   Что делает:
   - Сканирует все папки с исходниками
   - Читает `projects.ini`, `locale.ini`, `captions.txt`, `display_titles.txt`
   - Генерирует WebP превью (600×600, 400×400)
   - Генерирует 2:3 изображения для Pinterest (1200×1800)
   - Строит/перестраивает все страницы: index, категории, проекты, арты, отзывы
   - Генерирует `sitemap.xml`, `ru/sitemap.xml`, `image-sitemap.xml`
   - Обновляет `pinterest/pins.json`

### 3.2 Обновление блога

1. Пишется билингва Markdown-файл в `blog/`.
2. Запускается:
   ```
   python blog_convert.py
   ```
   - Разделяет EN/RU по маркерам `## 🇬🇧 English version` / `## 🇷🇺 Русская версия`
   - Генерирует HTML для EN и RU через `site_frame.py`
   - Обновляет `blog/index.html`

### 3.3 Деплой

**Платформа:** Vercel
- Отсутствует build-команда (нет `package.json` в корне)
- Vercel просто отдаёт статику
- `vercel.json` содержит:
  - **44 редиректа** (www → non-www, старые URL → новые)
  - **Security headers**: CSP (Google Tag Manager, Yandex Metrika, Web3Forms), HSTS (2 года), X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy, Permissions-Policy
  - **Noindex** для `living-illustrations.html`

### 3.4 Pinterest (отключено)

GitHub Actions workflow `.github/workflows/pinterest.yml.disabled`:
- При пуше в main: устанавливает Python + Pillow + requests
- Запускает `pinterest_publish.py`
- Коммитит обновлённый `pins.json`
- Отключён — требуется ручной запуск или донастройка токенов.

---

## 4. SEO — выполненные работы

### 4.1 Техническое SEO

| Элемент | Статус | Детали |
|---------|--------|--------|
| robots.txt | ✅ | Разрешено всё, кроме /admin, /.env, /cgi-bin, /wp-config |
| Sitemap.xml | ✅ | **1365 URL**, changefreq weekly, lastmod 2026-06-17 |
| Sitemap RU | ✅ | Полное зеркало для русской версии |
| Image Sitemap | ✅ | **1350+ изображений** с `image:loc` и `image:title` |
| Canonical URLs | ✅ | На каждой странице — `rel="canonical"` |
| Мета-описания | ✅ | Главная, категории, проекты, арты, блог |
| Alt-тексты | ✅ | `caption + alt_suffix` из `locale.ini` (4 суффикса: bookcover, book-illustrations, comic, artwork) |
| ЧПУ (slug) | ✅ | `/project/art/<number>-<slug>.html`, `/ru/` |
| Redirects | ✅ | 44 редиректа со старых URL на новые |

### 4.2 Микроразметка (JSON-LD)

| Тип Schema | Где используется |
|------------|-----------------|
| `WebSite` | Главная (с SearchAction) |
| `Organization` | Главная |
| `Person` + `ProfessionalService` | Главная |
| `BreadcrumbList` | Категории (3 уровня), арты (4 уровня) |
| `VisualArtwork` | Каждый арт (размеры, формат, лицензия, копирайт) |
| `ImageObject` | Каждый арт |
| `ItemList` | Категории и проекты (все изображения) |
| `Article` | Блог |
| `AggregateRating` | Страница отзывов (5.0, 71 отзыв) |
| `SearchAction` | Главная (поиск по сайту) |

### 4.3 Open Graph / Twitter Cards

| Элемент | Статус |
|---------|--------|
| `og:type` | ✅ website / article |
| `og:title` | ✅ Уникальный на каждой странице |
| `og:description` | ✅ |
| `og:image` | ✅ Из `STRONG/` — превью через `/thumbnails/` |
| `og:image:width/height` | ✅ 600×300 |
| `twitter:card` | ✅ summary_large_image |
| `twitter:site` | ✅ @vimark_art |
| `twitter:creator` | ✅ @vimark_art |
| Pinterest Rich Pins | ✅ |

### 4.4 Ссылочное SEO

| Элемент | Статус |
|---------|--------|
| Внутренняя перелинковка | ✅ Хлебные крошки, сайдбар со всеми разделами, футер, «Похожие работы» |
| Навигация | ✅ Семантическая: `<nav>`, `<main>`, `<article>`, `<figure>` |
| Backlinks (известные) | Reedsy, Behance, ArtStation |

### 4.5 Производительность

- **Thumbnails WebP** — все изображения автоматически конвертируются в WebP (600×600, 400×400)
- **Lazy loading** — `loading="lazy"` на изображениях галереи
- **Preconnect** — Google Tag Manager, Yandex Metrika
- **DNS-prefetch** — Google Analytics
- **CSP** — строгий Content-Security-Policy заголовок

### 4.6 Верификация

- **Google Search Console** — не обнаружен явный HTML-файл, но GA4 присутствует
- **Яндекс.Вебмастер** — ✅ `yandex_7042082dca4f98fb.html`
- **Bing Webmaster Tools** — ✅ `BingSiteAuth.xml` + `<meta name="msvalidate.01">` на главной

### 4.7 Аналитика

- **Google Analytics 4** (ID: `G-6RBP7X7H88`) — на всех страницах
- **Яндекс.Метрика** (ID: `109279162`) — на всех страницах, с Webvisor, clickmap, trackLinks, accurateTrackBounce
- **Кастомные цели** — через `reachGoal()` в `script.js`:
  - `click_cta`, `click_email`, `click_social_*`, `click_project_card`
  - `open_lightbox`, `gallery_view`, `scroll_contact`, `submit_contact`
  - `click_telegram`, `click_whatsapp`

### 4.8 PWA

✅ Манифест `manifest.json` с иконками 192×192 и 512×512, `display: standalone`, тёмная тема.

---

## 5. GEO — выполненные работы

### 5.1 Hreflang

На каждой странице присутствуют 3 тега:
```html
<link rel="alternate" hreflang="en" href="https://vimark.art/..." />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/..." />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/..." />
```

Охват: **все сгенерированные страницы** (главная, категории, проекты, арты).

### 5.2 Языковые версии

| Компонент | EN | RU |
|-----------|----|-----|
| `locale.ini` | ✅ ~70 ключей | ✅ ~75 ключей (больше — цены) |
| `display_titles.txt` | ✅ Секция `[en]` | ✅ Секция `[ru]` |
| Блог | ✅ 5 статей | ✅ 5 статей |
| Мета-описания | ✅ | ✅ |
| Alt-тексты | ✅ | ✅ (с героем «Максим Митенков») |
| Sitemap | ✅ `sitemap.xml` | ✅ `ru/sitemap.xml` |
| URL-структура | `/page.html` | `/ru/page.html` |

### 5.3 Языковой переключатель

- **На всех страницах** в футере (SVG-флаги UK / RU)
- **JavaScript** в футере: читает `location.pathname`, переключает между `/ru/` и `/` с маппингом путей
- Активный язык помечается `class="active"`

### 5.4 Таргетирование стран в Schema

В `Person + ProfessionalService` на главной:
```json
"areaServed": [
  { "@type": "Country", "name": "United States" },
  { "@type": "Country", "name": "United Kingdom" },
  { "@type": "Country", "name": "Canada" },
  { "@type": "Country", "name": "Australia" },
  { "@type": "Country", "name": "Russia" },
  { "@type": "Country", "name": "Germany" },
  { "@type": "Country", "name": "France" }
]
```

### 5.5 Доменные/гео-редиректы

- `www.vimark.art` → `vimark.art` (permanent)
- Все регионы ведут на единый домен без ccTLD

### 5.6 Дополнительно для RU

- **Яндекс.Метрика** вместо/вместе с GA4
- **Яндекс.Вебмастер** верификация
- Валюты и цены в `services.html` — отдельные для RU

---

## 6. Используемые сервисы и интеграции

| Сервис | Назначение |
|--------|------------|
| **Vercel** | Хостинг, редиректы, security headers |
| **Google Analytics 4** | Аналитика (ID: G-6RBP7X7H88) |
| **Яндекс.Метрика** | Аналитика для RU (ID: 109279162) |
| **Web3Forms** | Контактная форма (API key: 211a1ef5-25ea-4d59-9b9c-33b5f9126f21) |
| **Reedsy** | Отзывы и профиль фрилансера |
| **Behance / ArtStation / DeviantArt / Instagram / Pinterest** | Социальные сети и портфолио |
| **Pinterest API** | Автопубликация (отключена, требует настройки) |
| **Unreal Engine 5** | WebGL-эксперименты (отдельный проект `_UE_web/`) |

---

## 7. Ключевые метрики

- **1365** URL в английской sitemap
- **~150+** HTML-страниц всего
- **200+** исходных изображений
- **26** проектов в `projects.ini`
- **71** отзыв на Reedsy (рейтинг 5.0)
- **2** языка (EN, RU)
- **3** sitemap (основная EN, основная RU, image)
- **44** URL-редиректа
- **5** статей в блоге на каждом языке

---

## 8. Что ещё не реализовано / на паузе

| Задача | Статус |
|--------|--------|
| Google Search Console верификация (HTML-файл) | ❓ Не найден явный файл |
| Pinterest автопубликация | ⏸ Отключено (`.yml.disabled`) |
| Push-уведомления / Service Worker | ❌ Не реализовано |
| CDN для изображений | ❌ Всё через Vercel |
| Блог-комментарии | ❌ Не реализовано |
