# Полный обзор сайта portfolio — vimark.art

> Документ составлен на основе аудита кодовой базы, конфигурационных файлов и рабочих планов.  
> **Дата аудита:** 2026-05-28  
> **Владелец:** Max Mitenkov / Максим Митенков  
> **Домен:** https://vimark.art

---

## 1. Общие характеристики

| Параметр | Значение |
|----------|----------|
| **Тип сайта** | Статический портфолио (HTML/CSS/JS) |
| **Тематика** | Иллюстрация, концепт-арт, обложки книг, комиксы |
| **Целевая аудитория** | Издатели, авторы книг, геймдев-студии, арт-директора |
| **Языки** | English (основной), Russian (`/ru/`) |
| **Хостинг** | Vercel (статический хостинг из GitHub) |
| **Деплой** | Автоматический при push в ветку `master` |
| **SSL** | ✅ (Vercel по умолчанию) |
| **CMS / Бэкенд** | Отсутствует — чистый статический сайт |
| **Фреймворки** | Нет — ванильный HTML/CSS/JS |

### Объем контента

| Категория | Проектов | Изображений |
|-----------|----------|-------------|
| Book Illustrations | 5 | 43 |
| Book Cover | 3 | 18 |
| Comic | 7 | 49 |
| Personal | 3 | 35 |
| **Итого** | **18** | **145** |

---

## 2. Архитектура и технологии

### 2.1 Генератор сайта

Сайт полностью генерируется кастомным Python-скриптом. Не используется Jekyll, Hugo, 11ty или другой SSG.

| Файл | Назначение |
|------|------------|
| `generate_site.py` (~1 722 строк) | Основной генератор. Сканирует папки с изображениями, создает thumbnails, пишет все HTML-страницы, sitemap, Pinterest-ассеты |
| `pinterest_publish.py` | Публикация пинов через Pinterest API v5 |
| `projects.ini` | Метаданные проектов (title, year, client, description) |
| `captions.txt` | Ручные подписи к изображениям (fallback — авто из имени файла) |
| `locale.ini` | Строки локализации EN / RU |
| `Reedsy/reviews.json` | 23 отзыва (источник для генерации `reviews.html`) |

### 2.2 Что делает генератор

При запуске `python generate_site.py`:

1. **Сканирует** папки с работами: `Book Illustrations/`, `BookCover/`, `comic/`, `Personal/`, `STRONG/`, `HERO2/`
2. **Генерирует thumbnails** (`thumbnails/`) — WebP, 600×600, качество 85% (Pillow)
3. **Генерирует Pinterest-ассеты** — вертикальные изображения 2:3 (`pinterest/images/*.webp`, 1200×1800) + `pinterest/pins.json`
4. **Собирает две языковые версии** (`build_lang('en')`, `build_lang('ru')`):
   - `index.html` / `ru/index.html` — главная
   - `project/{id}.html` / `ru/project/{id}.html` — 18 страниц проектов
   - `{category}.html` / `ru/{category}.html` — лендинги категорий
   - `reviews.html` / `ru/reviews.html` — страница отзывов
   - `sitemap.xml` / `ru/sitemap.xml` — карты сайта
   - `image-sitemap.xml` — карта изображений

> ⚠️ Важно: все файлы в `project/*.html` и `ru/project/*.html` **перезаписываются** при каждом запуске генератора. Ручные правки в них будут потеряны.

### 2.3 Фронтенд-стек

- **HTML5** — семантическая верстка (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<aside>`, `<figure>`, `<figcaption>`)
- **CSS3** — единый файл `style.css`, CSS-переменные для темной темы, responsive-дизайн
- **Vanilla JS** — единый файл `script.js`
- **Нет** jQuery, React, Vue, Bootstrap или других фреймворков

### 2.4 Структура страниц

| Страница | Назначение |
|----------|------------|
| `index.html` | Главная: hero, фильтры, карточки проектов, about, contact, pricing |
| `project/{id}.html` | Страница проекта: hero, мета, галерея, CTA |
| `{category}.html` | Лендинг категории (bookcover, book-illustrations, comic, personal) |
| `reviews.html` | 71 отзыв с Reedsy + AggregateRating Schema.org |
| `contact.html` | Форма обратной связи (Web3Forms) |
| `privacy.html` | Политика конфиденциальности (требование Pinterest Developer) |
| `thanks.html` | Страница "Спасибо" после отправки формы |
| `404.html` | Кастомная страница 404 |

---

## 3. Процесс обновления и деплоя

### 3.1 Как внести изменения

```
1. Добавить новые изображения в папку проекта
   (например, Book Illustrations/NewProject/)

2. При необходимости обновить:
   - projects.ini   (метаданные проекта)
   - captions.txt   (подписи к изображениям)

3. Запустить генератор локально:
   $ python generate_site.py

4. Проверить git diff — убедиться, что новые файлы появились

5. Закоммитить и запушить:
   $ git add . && git commit -m "feat: add project ..." && git push

6. Vercel автоматически деплоит из ветки master
```

### 3.2 CI/CD

| Компонент | Статус |
|-----------|--------|
| **Vercel Auto-Deploy** | ✅ При каждом push в `master` |
| **GitHub Actions — Build** | ❌ Нет (генерация локальная) |
| **GitHub Actions — Tests** | ❌ Нет |
| **GitHub Actions — Pinterest** | ⚠️ Есть, но **отключена** (`.github/workflows/pinterest.yml.disabled`) |

### 3.3 Обновление меню / общих блоков

Поскольку `project/*.html` генерируются автоматически, любые изменения в шаблонах меню, навигации, футера или SEO-метаданных нужно вносить **внутри `generate_site.py`** (в Python f-string шаблоны), а затем перегенерировать весь сайт.

---

## 4. SEO (Поисковая оптимизация)

### 4.1 Общая оценка

Сайт имеет **сильный SEO-фундамент** с полным покрытием базовых и продвинутых практик.

### 4.2 Мета-теги

На **каждой** странице присутствуют:

- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Уникальный `<title>` (50–60 символов)
- Уникальный `<meta name="description">` (150–160 символов)
- Favicon: `<link rel="icon" type="image/png" href="vimark_logo.png">`

**Примеры title:**
- Главная: `Max Mitenkov · Illustrator · Concept Artist`
- Отзывы: `71 Verified Reedsy Reviews · Max Mitenkov · Illustrator & Concept Artist`
- Проект: `{ProjectName} · Max Mitenkov`
- RU: `Максим Митенков · Иллюстратор · Концепт-художник`

### 4.3 Канонические URL

Канонические теги на всех страницах:

| Страница | Canonical |
|----------|-----------|
| `index.html` | `https://vimark.art/` |
| `ru/index.html` | `https://vimark.art/ru/` |
| `reviews.html` | `https://vimark.art/reviews.html` |
| `project/{id}.html` | `https://vimark.art/project/{id}.html` |
| `404.html` | `https://vimark.art/404.html` |

### 4.4 Hreflang (мультиязычность)

На всех основных страницах и 18 страницах проектов:

```html
<link rel="alternate" hreflang="en" href="https://vimark.art/..." />
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/..." />
<link rel="alternate" hreflang="x-default" href="https://vimark.art/..." />
```

> ⚠️ Служебные страницы (`privacy.html`, `thanks.html`, `404.html`) не имеют hreflang.

### 4.5 Open Graph (Facebook / LinkedIn)

Полная реализация на всех страницах:
- `og:type`, `og:url`, `og:title`, `og:description`
- `og:image`, `og:image:width`, `og:image:height`
- `<link rel="image_src">`

> ⚠️ На `ru/index.html` `og:url` указывает на корень `/` вместо `/ru/` — небольшая неточность.

### 4.6 Twitter Cards

- `twitter:card` = `summary_large_image`
- `twitter:url`, `twitter:title`, `twitter:description`, `twitter:image`

### 4.7 Schema.org / JSON-LD

| Тип | Где | Что содержит |
|-----|-----|--------------|
| `Person` | `index.html`, `ru/index.html` | Имя, должность, URL, фото, sameAs (5 соцсетей), описание |
| `BreadcrumbList` | Все project-страницы | Portfolio → Category → Project |
| `BreadcrumbList` | `reviews.html` | Portfolio → Reviews |
| `Service` + `AggregateRating` | `reviews.html` | 5★ рейтинг, 71 отзыв |
| `VisualArtwork` (microdata) | Галереи на project-страницах | `itemprop="image"`, `itemprop="name"`, `itemprop="dateCreated"` |

Всего ~1 525 вхождений микроразметки `VisualArtwork`.

### 4.8 Sitemap

| Файл | URL | Описание |
|------|-----|----------|
| `sitemap.xml` | 25 URL | EN-страницы |
| `ru/sitemap.xml` | 25 URL | RU-страницы |
| `image-sitemap.xml` | ~100+ изображений | Google Image Sitemap с `<image:image>` и `<image:title>` |

Все URL содержат `<lastmod>`, `<changefreq>weekly</changefreq>`, `<priority>`:
- Главная: 1.0
- Проекты: 0.9
- Категории: 0.8
- Отзывы: 0.7
- Контакт: 0.5

### 4.9 robots.txt

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
Sitemap: https://vimark.art/image-sitemap.xml
```

### 4.10 Оптимизация изображений

| Техника | Статус |
|---------|--------|
| **WebP thumbnails** | ✅ Все превью в `thumbnails/` — WebP |
| **Lazy loading** | ✅ `loading="lazy"` на 638+ изображениях |
| **Eager loading** | ✅ Hero-изображения — `loading="eager"` |
| **fetchpriority="high"** | ✅ 39 вхождений на hero-изображениях |
| **Width/Height** | ✅ Явные размеры для предотвращения CLS |
| **Preconnect** | ✅ `googletagmanager.com`, `mc.yandex.ru` |
| **Alt-тексты** | ✅ Заполнены для всех изображений |
| **AVIF** | ❌ Не используется |
| **CDN** | ❌ Все ресурсы с `vimark.art` |
| **srcset / <picture>** | ❌ Нет адаптивных форматов |

### 4.11 Pinterest Rich Pins

На страницах проектов:
```html
<meta name="pinterest-rich-pin" content="true">
<meta property="article:published_time" content="2025-01-01">
```

---

## 5. Аналитика и отслеживание

### 5.1 Google Analytics 4

| Параметр | Значение |
|----------|----------|
| **ID** | `G-6RBP7X7H88` |
| **Покрытие** | Все 36+ HTML-файлов |
| **Preconnect** | `https://www.googletagmanager.com` |
| **dns-prefetch** | `https://www.google-analytics.com` |

**Кастомные события (gtag):**

| Событие | Триггер |
|---------|---------|
| `submit_contact` | Отправка формы контактов |
| `click_telegram` | Клик по Telegram |
| `click_whatsapp` | Клик по WhatsApp |
| `download_cv` | Скачивание CV (PDF) |

### 5.2 Яндекс.Метрика

| Параметр | Значение |
|----------|----------|
| **ID счетчика** | `109279162` |
| **Вебвизор** | ✅ |
| **Карта кликов** | ✅ |
| **Ecommerce** | ✅ `dataLayer` |
| **Точный показатель отказов** | ✅ |
| **Внешние ссылки** | ✅ |
| **Fallback (noscript)** | ✅ |

**Цели (reachGoal):**

| Цель | Триггер |
|------|---------|
| `submit_contact` | Отправка формы |
| `click_telegram` | Клик по Telegram |
| `click_whatsapp` | Клик по WhatsApp |
| `download_cv` | Скачивание CV |

### 5.3 Другие трекеры

| Сервис | Статус |
|--------|--------|
| Facebook Pixel | ❌ Нет |
| LinkedIn Insight Tag | ❌ Нет |
| VK Pixel | ❌ Нет |
| Hotjar / Mixpanel / Amplitude | ❌ Нет |
| TikTok Pixel | ❌ Нет |

---

## 6. Маркетинг и продвижение

### 6.1 Социальные сети (присутствуют на каждой странице)

| Платформа | URL | Тип иконки |
|-----------|-----|------------|
| **Behance** | https://www.behance.net/vimark | PNG |
| **DeviantArt** | https://www.deviantart.com/vimark | PNG |
| **Instagram** | https://www.instagram.com/vimark_art/ | SVG |
| **Facebook** | https://www.facebook.com/maks.vimark/ | SVG |
| **LinkedIn** | https://www.linkedin.com/in/maxim-mitenkov-06192940/ | SVG |
| **Telegram** | https://t.me/MaxMitenkov | SVG (footer) |
| **WhatsApp** | https://wa.me/375296534382 | SVG (footer) |

- Telegram и WhatsApp имеют **двойной трекинг** (gtag + Yandex reachGoal) по onclick
- Все профили прописаны в Schema.org `sameAs`

### 6.2 Reedsy (социальное доказательство)

- **Страница:** `reviews.html` / `ru/reviews.html`
- **Профиль:** https://reedsy.com/freelancers/maxim-m
- **Заявлено:** 71 verified review
- **Рейтинг:** 5/5 звезд
- **Gauge-изображения:** Professionalism, Quality, Value, Responsiveness
- **Schema.org:** `AggregateRating` (ratingValue: 5, reviewCount: 71)
- **Источник данных:** `Reedsy/reviews.json` (23 отзыва в файле)
- **Reedsy logo:** Inline SVG (Georgia italic)

> ⚠️ Диссонанс: на сайте заявлено 71 отзыв, в `reviews.json` хранится 23 записи, в `reviews.md` указано "Total reviews (5★ only): 22".

### 6.3 Pinterest (автопубликация — в разработке)

| Компонент | Статус |
|-----------|--------|
| **Конфиг** | `pinterest/config.json` — маппинг категорий → доски |
| **Пины** | `pinterest/pins.json` — 18 пинов готовы к публикации |
| **Изображения** | `pinterest/images/*.webp` — вертикальные 2:3 |
| **Rich Pins** | ✅ Мета-теги на project-страницах |
| **API** | Pinterest API v5 |
| **GitHub Action** | ⚠️ Отключена (`.github/workflows/pinterest.yml.disabled`) |
| **Статус пинов** | `ready_to_publish`, `date_published: null` |

**Для активации нужно:**
1. Переименовать workflow в `.yml`
2. Добавить в GitHub Secrets: `PINTEREST_ACCESS_TOKEN`, `PINTEREST_REFRESH_TOKEN`, `PINTEREST_CLIENT_ID`, `PINTEREST_CLIENT_SECRET`
3. Создать доски на Pinterest

### 6.4 Контактная форма

- **Бэкенд:** Web3Forms (`api.web3forms.com/submit`)
- **Поля:** Name, Email, Subject, Message
- **Защита:** Нет honeypot, нет reCAPTCHA
- **Доп. поля:** Нет dropdown "Тип проекта"

### 6.5 Резюме / CV

- **Файл:** `2025_Resume_eng_concept.pdf`
- **Расположение:** Корень репозитория
- **Ссылка:** В разделе About на главной
- **Трекинг:** `gtag('event','download_cv')` + `ym(109279162,'reachGoal','download_cv')`

### 6.6 Чего нет (маркетинговые возможности)

| Функция | Статус |
|---------|--------|
| Рассылка / Newsletter | ❌ Нет |
| Email-capture / Lead magnet | ❌ Нет |
| Реклама (AdSense, баннеры) | ❌ Нет |
| Retargeting-пиксели (Meta, LinkedIn) | ❌ Нет |
| Партнерские ссылки | ❌ Нет |
| Гостевые посты / бэклинки | ❌ Только органические (Reedsy) |

---

## 7. UI/UX и функциональность

### 7.1 Компоненты интерфейса

| Компонент | Описание |
|-----------|----------|
| **Hero-баннер** | Случайное изображение из `STRONG/` или `HERO2/`, клиентская ротация |
| **Фильтры** | Кнопки "All" + по категориям, клиентская фильтрация на JS |
| **Карточки проектов** | Главное изображение + 3 thumbnail + оверлей с названием и количеством работ |
| **Галерея** | Сетка изображений с `loading="lazy"`, микроразметка `VisualArtwork` |
| **Lightbox** | Полноэкранный просмотр: стрелки ← →, Escape, свайп, счетчик, caption |
| **Sticky Contact** | Плавающие иконки Telegram + WhatsApp (справа внизу) |
| **Theme Toggle** | Переключатель светлая/тёмная тема, сохранение в `localStorage` |
| **Lang Switch** | Переключение EN/RU на всех страницах |
| **Scroll to Top** | Кнопка ↑ |
| **Reviews Bar** | 5 звезд + 4 gauge-изображения на главной и странице отзывов |
| **Commissions Status** | 🟢 "Open for commissions" в сайдбаре |

### 7.2 Адаптивность

- Mobile-first подход
- Sidebar → hamburger menu на мобильных
- **Только 1 breakpoint:** 800px
- Отсутствуют точки: 320, 768, 1024, 1440px

### 7.3 Темная тема

- Фон по умолчанию: `#111` (темный)
- Переключатель: ☀ / 🌙
- Сохранение предпочтения в `localStorage`

---

## 8. Мультиязычность

| Аспект | EN | RU |
|--------|-----|-----|
| **URL** | `/index.html`, `/project/...` | `/ru/index.html`, `/ru/project/...` |
| **HTML lang** | `lang="en"` | `lang="ru"` |
| **Контент** | Полный | Полный (зеркало) |
| **SEO-мета** | Уникальные | Локализованные |
| **hreflang** | `hreflang="en"` | `hreflang="ru"` |

Переключатель языка в футере: флаги UK / RU. Работает через JS, учитывает текущий путь.

---

## 9. Технический долг и планы (из PLAN.md)

### 9.1 Высокий приоритет

- [ ] Включить Pinterest автопубликацию (нужен API-ключ)
- [ ] Добавить поле `medium` в `projects.ini` (Digital painting, Photoshop и т.д.)
- [ ] Оптимизировать OG-image до 1200×630 (сейчас используется thumbnail 600×600)

### 9.2 Средний приоритет

- [ ] Pinterest Save Button на изображениях проектов
- [ ] Добавить отзывы на страницы конкретных проектов
- [ ] Улучшить alt_text до формата: `[Что] · [Для чего] · [Стиль] · by Maxim Mitenkov`
- [ ] Добавить preload для критического CSS / шрифтов / hero-изображений
- [ ] Добавить `<picture>` + srcset для адаптивных изображений

### 9.3 Низкий приоритет

- [ ] Добавить сайт в Google Search Console и отправить sitemap
- [ ] Проверить OG-разметку через Facebook Sharing Debugger
- [ ] Валидировать Pinterest Rich Pins

---

## 10. Безопасность и конфиденциальность

| Аспект | Статус |
|--------|--------|
| **Форма без бэкенда** | ✅ Web3Forms (внешний сервис, нет обработки на сервере) |
| **Политика конфиденциальности** | ✅ `privacy.html` (требование Pinterest) |
| **robots.txt** | ✅ Запрещает чувствительные пути |
| **Нет сессий / cookies** | ✅ Статический сайт |
| **reCAPTCHA / honeypot** | ❌ Нет защиты от ботов в форме |

---

## 11. Файловая структура (ключевое)

```
vimark.art/
├── generate_site.py              # Генератор сайта (~1722 строк)
├── pinterest_publish.py          # Публикация в Pinterest
├── projects.ini                  # Метаданные проектов
├── captions.txt                  # Подписи к изображениям
├── locale.ini                    # Локализация EN/RU
├── style.css                     # Стили
├── script.js                     # Логика (lightbox, фильтры, тема)
├── sitemap.xml                   # Карта сайта (EN)
├── image-sitemap.xml             # Карта изображений
├── robots.txt                    # Инструкции для роботов
├── 2025_Resume_eng_concept.pdf   # CV для скачивания
├── yandex_7042082dca4f98fb.html  # Подтверждение Яндекс.Вебмастер
│
├── .github/
│   └── workflows/
│       └── pinterest.yml.disabled    # Заглушка автопубликации
│
├── Book Illustrations/           # Исходные изображения
├── BookCover/
├── comic/
├── Personal/
├── STRONG/                       # OG / social изображения
├── HERO2/                        # Hero-баннеры
│
├── project/                      # Сгенерированные страницы проектов (18 шт.)
├── thumbnails/                   # WebP-превью (145 шт.)
├── pinterest/
│   ├── config.json               # Маппинг досок Pinterest
│   ├── pins.json                 # Реестр пинов (18 шт.)
│   └── images/                   # Вертикальные 2:3 изображения
├── Reedsy/
│   ├── reviews.json              # 23 отзыва
│   └── reviews.md                # Ручные заметки
│
├── ru/                           # Русская версия (зеркало)
│   ├── index.html
│   ├── project/                  # 18 RU-страниц проектов
│   └── sitemap.xml
│
└── ... (остальные HTML-страницы)
```

---

## 12. Итоговая сводка

| Категория | Оценка | Комментарий |
|-----------|--------|-------------|
| **SEO** | ⭐⭐⭐⭐☆ | Отличный фундамент: OG, Twitter Cards, Schema.org, sitemap, hreflang, canonical. Можно улучшить preload и srcset. |
| **Аналитика** | ⭐⭐⭐⭐☆ | GA4 + Я.Метрика с целями. Нет продвинутых пикселей (Meta, LinkedIn). |
| **Продвижение** | ⭐⭐⭐☆☆ | Сильная интеграция Reedsy, присутствие в 7 соцсетях, готовый Pinterest. Нет рассылки, рекламы, ретаргетинга. |
| **UX/UI** | ⭐⭐⭐⭐☆ | Темная тема, lightbox, фильтры, sticky-контакты. Нужно больше breakpoints и Masonry-галерея. |
| **Технологии** | ⭐⭐⭐⭐☆ | Кастомный генератор на Python — гибко, но требует ручного запуска. Нет CDN, AVIF. |
| **Обновляемость** | ⭐⭐⭐☆☆ | Добавление работ простое (скрипт), но любые правки шаблонов требуют перегенерации всего сайта. |

---

*Документ подготовлен на основе аудита кодовой базы vimark.art.  
Последнее обновление: 2026-05-28*
