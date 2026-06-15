# SEO-оптимизация vimark.art — полное руководство

> Документ описывает текущее состояние SEO-оптимизации сайта `vimark.art`, механику его работы и порядок обновления контента. Предназначен для передачи другому специалисту без предварительного доступа к сайту.

---

## 1. Общая информация

**Сайт:** https://vimark.art  
**Хостинг:** Vercel (автоматический деплой из ветки `master` репозитория GitHub)  
**Тип сайта:** статический HTML (без CMS), двуязычный  
**Языки:** английский (основной, `/`) и русский (`/ru/`)  
**Назначение:** портфолио иллюстратора / дизайнера обложек Максима Митенкова (vimark) с возможностью заказа услуг.

### Цель SEO-оптимизации

Сайт продаёт услуги (обложки книг, иллюстрации, концепт-арт). Основной трафик должен приходить по запросам:
- «book cover illustrator» / «иллюстратор обложек книг»
- «sci-fi book cover design» / «дизайн обложки фэнтези"
- «dark fantasy illustration" / «тёмное фэнтези иллюстрация»
- и по long-tail запросам отдельных работ, жанров, книг.

Поэтому важны:
- **техническая чистота** (правильная индексация, отсутствие дублей и мёртвых URL);
- **структура и перелинковка** (все страницы доступны из sitemap и меню);
- **качество title/description/h1** (релевантность запросам);
- **микроразметка Schema.org** (понимание контента поисковыми системами);
- **мультиязычность** (hreflang, правильные canonical).

---

## 2. Архитектура сайта

### 2.1. Типы страниц

| Тип | Путь | Как создаётся | Примеры |
|-----|------|---------------|---------|
| **Статические страницы (хабы)** | `/index.html`, `/book-covers.html`, `/book-illustrations.html`, `/visual-stories.html`, `/about.html`, `/contact.html`, `/reviews.html`, `/faq.html`, `/case-studies/...`, `/living-illustrations.html` | Редактируются вручную | Главная, галереи обложек и иллюстраций, о себе, контакты |
| **Страницы проектов** | `/project/{project}.html` | Генерируются `generate_site.py` | `/project/book-illustrations-endymion.html` |
| **Страницы отдельных артов** | `/project/art/{slug}.html` | Генерируются `generate_site.py` | `/project/art/martyn.html` |
| **Служебные** | `/privacy.html`, `/thanks.html`, `/404.html`, `/yandex_*.html` | Редактируются вручную | Приватность, 404, верификация Яндекса |
| **Ресурсы** | `/style.css`, `/script.js`, изображения | Редактируются вручную | Стили, скрипты, картинки |

### 2.2. Мультиязычность

- Английская версия находится в корне: `/index.html`, `/book-covers.html`, `/project/...`.
- Русская версия находится в `/ru/`: `/ru/index.html`, `/ru/book-covers.html`, `/ru/project/...`.
- На каждой странице есть `hreflang`:
  ```html
  <link rel="alternate" hreflang="en" href="https://vimark.art/..." />
  <link rel="alternate" hreflang="ru" href="https://vimark.art/ru/..." />
  <link rel="alternate" hreflang="x-default" href="https://vimark.art/..." />
  ```
- `canonical` указывает на соответствующую языковую версию.

### 2.3. Наследие и редиректы

В `vercel.json` настроены 301-редиректы:
- `/comic.html` → `/visual-stories.html`
- `/bookcover.html` → `/book-covers.html`
- `/case-study-hoebeke.html` → `/case-studies/hoebeke-sci-fi-series.html`
- `www.vimark.art/*` → `vimark.art/*`
- старые slugs артов (`/project/art/carib.html`) → новые (`/project/art/1-carib.html`).

Эти старые URL исключены из `sitemap.xml`, чтобы не тратить краулинговый бюджет.

---

## 3. Генерация сайта

### 3.1. Основной инструмент — `generate_site.py`

Файл `generate_site.py` — это Python-скрипт, который:
1. Сканирует папки с изображениями (`Book Illustrations`, `BookCover`, `comic`, `Personal`, `images`).
2. Генерирует страницы проектов и отдельных артов.
3. Создаёт `sitemap.xml`, `ru/sitemap.xml` и `image-sitemap.xml`.
4. Создаёт thumbnails для изображений.

### 3.2. Какие файлы отвечают за контент

| Файл | Назначение |
|------|------------|
| `generate_site.py` | Генератор всех project/art страниц, sitemap, thumbnails |
| `locale.ini` | Переводы интерфейса, title-суффиксы, alt-суффиксы, meta-описания |
| `captions.txt` | Caption для каждого изображения. Отсюда берутся **slug URL** и **fallback-название** для арта |
| `display_titles.txt` | Переопределение отображаемого названия арта **без смены URL**. Поддерживает секции `[en]` и `[ru]` |
| `projects.ini` | Описания проектов: title, year, client, description, thumbnail |
| `art_reviews.ini` | Отзывы к конкретным артам |
| `style.css` | Стили |
| `script.js` | Скрипты |

### 3.3. Как запустить генерацию

```bash
cd d:\Concept_work\Vimark_art
python3 generate_site.py
```

После этого:
- обновятся `/project/*.html` (23 en + 23 ru);
- обновятся `/project/art/*.html` (192 en + 192 ru);
- обновятся `/sitemap.xml`, `/ru/sitemap.xml`, `/image-sitemap.xml`;
- обновятся thumbnails (если появились новые изображения).

**Важно:** статические страницы (`index.html`, `book-covers.html`, `book-illustrations.html`, `visual-stories.html`, `about.html`, `contact.html`, `reviews.html`, `faq.html`) `generate_site.py` **не перезаписывает** (вызов `build_lang(skip_landing_pages=True)`). Их нужно редактировать вручную.

### 3.4. Процесс деплоя

1. Внести изменения в файлы.
2. Запустить `python3 generate_site.py`.
3. Проверить локально (`python3 -m http.server 8000`).
4. Закоммитить и запушить:
   ```bash
   git add -A
   git commit -m "описание изменений"
   git push origin master
   ```
5. Vercel автоматически задеплоит из `master`.

---

## 4. Что было сделано по SEO

### 4.1. Sitemap

**Что было:**
- В `sitemap.xml` были URL, которые 301-редиректят (`comic.html`, `bookcover.html`, `case-study-hoebeke.html`).
- В sitemap были `404.html` и `living-illustrations.html` (noindex).
- В sitemap не было всех `project/art/*.html` (192 страницы).
- В `ru/sitemap.xml` был legacy-проект `living-illustrations-after-picasso`.

**Что сделано:**
- Убраны мёртвые и noindex-URL.
- Добавлены все `project/art/*.html` (EN + RU).
- Удалён `living-illustrations-after-picasso` из `projects.ini` и с диска.
- Приоритеты расставлены:
  - главная — 1.0;
  - хабы и кейс — 0.9;
  - визуальные разделы — 0.8;
  - project pages — 0.8;
  - art pages — 0.6.

**Зачем:** поисковый робот не должен тратить краулинговый бюджет на редиректы и noindex-страницы. Все целевые страницы должны быть в sitemap для быстрой индексации.

### 4.2. Robots.txt

**Что сделано:** добавлена ссылка на `/ru/sitemap.xml`:
```
Sitemap: https://vimark.art/sitemap.xml
Sitemap: https://vimark.art/ru/sitemap.xml
Sitemap: https://vimark.art/image-sitemap.xml
```

**Зачем:** Яндекс и Google должны находить оба языковых sitemap и image-sitemap.

### 4.3. Meta robots

**Что сделано:** на `/living-illustrations.html` и `/ru/living-illustrations.html` добавлен:
```html
<meta name="robots" content="noindex, nofollow">
```

**Зачем:** это интерактивные WebGL-работы, не предназначенные для поиска. Раньше noindex был только через HTTP-заголовок `X-Robots-Tag` в `vercel.json`. Дублирование в `<meta>` делает запрет надёжнее.

### 4.4. Hreflang и canonical

Были настроены ранее, сохранены и проверены:
- `canonical` на каждой странице;
- `hreflang="en"`, `hreflang="ru"`, `hreflang="x-default"`;
- RU-версии указывают canonical на `/ru/...`.

**Зачем:** исключить дублирование контента между языками и помочь поисковикам показывать правильную языковую версию.

### 4.5. Иерархия заголовков

**Что было:**
- `book-illustrations.html`: `<h1>` → карточки без `<h2>`.
- `book-covers.html`: `<h1>` → `<h2>` (2026/2025/2024) → карточки без `<h3>`.

**Что сделано:**
- `book-illustrations.html`: названия проектов стали `<h2>`.
- `book-covers.html`: названия обложек стали `<h3>` (внутри секций `<h2>`).
- `generate_site.py` теперь генерирует карточки категорий с `<h2>` автоматически.

**Зачем:** правильная иерархия заголовков помогает Яндексу и Google понимать структуру страницы. Пропуск уровня (`h1` → `h3`) сигнализирует о плохой структуре.

### 4.6. Title и description для art-страниц

**Что было:**
```html
<title>Martyn · Max Mitenkov</title>
<meta name="description" content="Martyn — Endymion by Max Mitenkov">
```

**Что стало:**
```html
<title>Martyn · Endymion · Max Mitenkov</title>
<meta name="description" content="Martyn — Endymion by Max Mitenkov. Book Illustrations Digital painting and illustration for sci-fi, fantasy, horror and literary fiction publishing.">
```

**Зачем:** улучшена релевантность по жанровым и коммерческим запросам. Добавлено название проекта и категория.

### 4.7. Отображаемые названия без смены URL

**Проблема:** caption в `captions.txt` используется одновременно для **URL/slug** и для **отображаемого названия**. Если исправить название (`Prizraki` → `The ghosts of the old cemetery`), меняется URL.

**Решение:** создан файл `display_titles.txt` с секциями `[en]` и `[ru]`:
```ini
[en]
BookCover/2026/__0004_Prizraki_2026.jpg = The ghosts of the old cemetery

[ru]
BookCover/2026/__0004_Prizraki_2026.jpg = Призраки старого кладбища
```

- `captions.txt` отвечает за **slug/URL**.
- `display_titles.txt` отвечает за **отображаемое название** в title, h1, description, OG, хлебных крошках.

**Зачем:** стабильные URL важны для SEO (не теряется индексация, ссылки, sitemap). При этом на странице может быть правильное человеческое название.

### 4.8. Alt-тексты изображений

**Что сделано:**
- Добавлена функция `get_alt(img)` в `generate_site.py`.
- Alt формируется по шаблону: `{caption} — {suffix}`.
- Суффикс зависит от категории:
  - `bookcover` → «book cover design by Max Mitenkov» / «дизайн обложки книги, художник Максим Митенков»
  - `book-illustrations` → «book illustration by Max Mitenkov» / «иллюстрация к книге, художник Максим Митенков»
  - `comic` → «comic art by Max Mitenkov» / «комикс-арт, художник Максим Митенков»
  - остальное → «artwork by Max Mitenkov» / «арт, художник Максим Митенков»

**Пример:**
```html
<img src="..." alt="Martyn — book illustration by Max Mitenkov">
```

**Зачем:** поисковики не видят изображения, но видят alt. Ключевые слова в alt улучшают ранжирование по изображениям и общую тематику страницы.

### 4.9. Footer-links

**Что сделано:** меню `.footer-links` добавлено на все основные хабы (`index.html`, `book-covers.html`, `book-illustrations.html`, `visual-stories.html`, `about.html`, `contact.html`, `reviews.html`, `faq.html`) в EN и RU.

**Зачем:** равномерная внутренняя перелинковка распределяет ссылочный вес и помогает роботу находить все важные страницы.

### 4.10. Микроразметка Schema.org

#### 4.10.1. `BreadcrumbList`

Добавлена на:
- все art-страницы (`/project/art/*.html`);
- все project-страницы (`/project/*.html`);
- категории (book-covers, book-illustrations, visual-stories и др.).

**Пример для art-страницы:**
```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"position": 1, "name": "Portfolio", "item": "https://vimark.art/"},
    {"position": 2, "name": "Book Illustrations", "item": "https://vimark.art/book-illustrations.html"},
    {"position": 3, "name": "Endymion", "item": "https://vimark.art/project/book-illustrations-endymion.html"},
    {"position": 4, "name": "Martyn", "item": "https://vimark.art/project/art/martyn.html"}
  ]
}
```

**Зачем:** Яндекс и Google используют хлебные крошки в сниппетах. Раньше ссылка на категорию вела на `/#book-illustrations` (якорь), что было битой. Теперь ведёт на реальную страницу категории.

#### 4.10.2. `VisualArtwork`

Добавлен JSON-LD `VisualArtwork`:
- на каждую art-страницу (одна работа);
- на каждую project-страницу (`ItemList` из `VisualArtwork` для всех артов проекта).

**Пример для одного арта:**
```json
{
  "@type": "VisualArtwork",
  "name": "Martyn",
  "image": "https://vimark.art/Book Illustrations/Endymion/__0000_E1_Martyn.jpg",
  "url": "https://vimark.art/project/art/martyn.html",
  "artist": {"@type": "Person", "name": "Max Mitenkov", "url": "https://vimark.art/"},
  "dateCreated": "2025",
  "artMedium": "Digital painting",
  "genre": "Book Illustrations",
  "isPartOf": {"@type": "CreativeWork", "name": "Endymion", "url": "https://vimark.art/project/book-illustrations-endymion.html"}
}
```

**Зачем:** помогает поисковикам понимать, что страница — это произведение искусства/иллюстрация, с автором, годом, жанром. Улучшает шансы на попадание в «Картинки» и расширенные сниппеты.

#### 4.10.3. `ImageObject`

Добавлен JSON-LD `ImageObject` на каждую art-страницу (после `VisualArtwork`):

```json
{
  "@type": "ImageObject",
  "name": "1 carib",
  "author": {"@type": "Person", "name": "Max Mitenkov"},
  "description": "1 carib — book illustration by Max Mitenkov",
  "contentUrl": "https://vimark.art/Book Illustrations/Planetes/__0000_1_carib.jpg",
  "thumbnailUrl": "https://vimark.art/thumbnails/Book Illustrations/Planetes/__0000_1_carib.webp",
  "datePublished": "2024",
  "license": "https://vimark.art/privacy.html",
  "acquireLicensePage": "https://vimark.art/contact.html"
}
```

**Зачем:** Специфичный тип для Google Images / Pinterest. contentUrl + thumbnailUrl улучшают показ в поиске по картинкам.

#### 4.10.4. `ProfessionalService`

- `Person` → `["Person", "ProfessionalService"]` — на главной (`index.html`) и `about.html`.
- Добавлен `hasOfferCatalog` с перечнем услуг (Book Cover, Interior Illustration).
- Добавлены `areaServed: Worldwide` и расширенный `knowsAbout`.

#### 4.10.5. Другая микроразметка

- `Person` — на главной и в артах (artist).
- `Service` + `AggregateRating` — на странице отзывов (`/reviews.html`).
- `CollectionPage` — на `/book-covers.html` и `/visual-stories.html`.
- `Article` + `CreativeWork` — на кейс-странице.
- `Service` + `hasOfferCatalog` + `HowTo` + `FAQPage` — на `/services.html`.

### 4.11. Дополнительные meta-теги на art-страницах

- `article:published_time` — год создания работы (`YYYY-01-01`)
- `article:modified_time` — дата последней генерации страницы (ISO 8601)
- `twitter:site` / `twitter:creator` — `@vimark_art`

### 4.12. Блок «Related Works» на art-страницах

После секции WIP (Process) и перед CTA добавлена сетка до 6 похожих работ из того же проекта. Каждая — thumbnail + название, ссылка на `/project/art/{slug}.html`.

CSS классы: `.related-works`, `.related-grid`, `.related-item`, `.related-name`.

### 4.13. Визуальные хлебные крошки

**Что сделано:** на art-страницах добавлена визуальная навигация:
```
Portfolio › Book Illustrations › Endymion › Martyn
```

**Зачем:** улучшает UX, повышает глубину просмотра (пользователь может перейти на уровень проекта или категории), дополнительно сигнализирует поисковику о структуре.

### 4.12. Аналитика и цели конверсий

**Что сделано:**
- В код добавлены события для Яндекс.Метрики и Google Analytics 4:
  - `click_telegram`, `click_whatsapp` — клики по мессенджерам;
  - `submit_contact` — отправка формы контактов;
  - `download_cv` — скачивание CV;
  - `click_cta` — любая кнопка призыва к действию;
  - `click_email` — клик по email-ссылке;
  - `click_social_*` — клики по социальным профилям (Behance, ArtStation, Instagram, LinkedIn, Facebook, Pinterest, DeviantArt);
  - `click_reedsy` — переход на профиль Reedsy;
  - `click_project_card` — клик по карточке проекта;
  - `open_lightbox`, `gallery_view` — взаимодействие с лайтбоксом;
  - `scroll_contact` — прокрутка до контактной формы.
- Созданы соответствующие JavaScript-цели в интерфейсе Яндекс.Метрики (счётчик `109279162`).
- Добавлена инструкция по целям: `YANDEX_METRIKA_GOALS.md`.

**Зачем:** отслеживание конверсий позволяет понимать, какие источники и страницы приносят заказы, и оптимизировать сайт под реальные цели бизнеса, а не только трафик.

---

## 5. Как обновлять контент

### 5.1. Добавить новый проект

1. Создать папку с изображениями в нужной категории, например:
   ```
   Book Illustrations/New Project/
   ```
2. Добавить описание проекта в `projects.ini`:
   ```ini
   [book-illustrations-new-project]
   title = New Project
   year = 2026
   client = Author Name
   description = Description of the project.
   thumbnail = Book Illustrations/New Project/cover.jpg
   ```
3. Запустить `python3 generate_site.py`.
4. Проверить, что новый project page появился в `/project/`.
5. Проверить sitemap.
6. Закоммитить и запушить.

### 5.2. Изменить caption (название + URL)

1. Открыть `captions.txt`.
2. Найти строку:
   ```
   Book Illustrations/Endymion/__0000_E1_Martyn.jpg = Martyn
   ```
3. Изменить значение после `=`.
4. **Важно:** при изменении caption меняется URL арта. Нужно:
   - проверить все ссылки на старый URL;
   - добавить 301-редирект в `vercel.json`;
   - запустить `python3 generate_site.py`.

### 5.3. Изменить отображаемое название без смены URL

1. Открыть `display_titles.txt`.
2. Добавить или изменить строку в нужной секции:
   ```ini
   [en]
   Book Illustrations/Endymion/__0000_E1_Martyn.jpg = New Display Title
   
   [ru]
   Book Illustrations/Endymion/__0000_E1_Martyn.jpg = Новое отображаемое название
   ```
3. Запустить `python3 generate_site.py`.

### 5.4. Добавить новое изображение

1. Положить файл в нужную папку.
2. При необходимости добавить caption в `captions.txt`.
3. При необходимости добавить display title в `display_titles.txt`.
4. Запустить `python3 generate_site.py`.

### 5.5. Обновить sitemap

Sitemap обновляется автоматически при запуске `generate_site.py`. Но если менялись статические страницы, нужно вручную убедиться, что:
- в `sitemap.xml` нет мёртвых URL;
- новые статические страницы добавлены в список `landing_pages` в `generate_site.py` (иначе они не попадут в sitemap).

---

## 6. Текущий статус и дальнейшие шаги

### 6.1. Что уже работает

- Техническое SEO: sitemap, robots, canonical, hreflang, meta robots, headings.
- Микроразметка: BreadcrumbList, VisualArtwork, ImageObject, ProfessionalService, Person, Service, AggregateRating, HowTo, FAQPage.
- Meta-теги: article:published_time, article:modified_time, twitter:site, twitter:creator, Open Graph, Pinterest Rich Pins.
- Блок «Related Works» на art-страницах (до 6 похожих работ из того же проекта).
- Контент страниц артов: title, description, alt, хлебные крошки.
- Sitemap отправлен в Яндекс.Вебмастер, находится в очереди на обработку (1–2 недели).

### 6.2. Что рекомендуется сделать дальше

1. **Коммерческий контент:**
   - [x] Создать `/services.html` и `/ru/services.html` с перечнем услуг, ценами и этапами работы.
   - [x] Расширить FAQ коммерческими вопросами.
2. **Микроразметка:**
   - [x] Добавить `ImageObject` JSON-LD на art-страницы (A.4).
   - [x] Расширить `Person` → `["Person", "ProfessionalService"]` на главной и about (C.2).
   - [x] Добавить `article:published_time` / `modified_time` на art-страницы (A.2).
   - [x] Добавить `twitter:site` / `twitter:creator` на art-страницы (A.3).
   - [x] Добавить блок «Related Works» на art-страницы (B.3).
   - [~] Отложено: создать `/series-cover-design.html` (D.3).
3. **Техническое SEO:**
   - [x] `og:image` — абсолютные URL (A.1 + A.5)
   - [x] Title/Description — коммерческие (E.1)
   - [x] Preconnect к внешним ресурсам (G.2)
   - [~] Lazy loading — частично: hero eager, галереи lazy (G.3)
   - [ ] `srcset` + `sizes` для thumbnails (G.1)
4. **Внешние ссылки:**
   - [x] Убедиться, что профили Reedsy, Behance, ArtStation, Instagram ссылаются на `vimark.art`.
   - [x] Bing Webmaster Tools — msvalidate + BingSiteAuth.xml
   - [ ] Получить упоминания в русскоязычных блогах/интервью.
5. **Яндекс.Вебмастер:**
   - [x] Цели в Метрике настроены (F.1)
   - [ ] После обработки sitemap проверить «Индексирование → Страницы в поиске».
   - [ ] Исправить ошибки, если появятся.
6. **Аналитика:**
   - [ ] Следить за поведенческими факторами (время, глубина, отказы) и конверсиями по настроенным целям.

---

## 7. Быстрые команды

```bash
# Локальный просмотр
cd d:\Concept_work\Vimark_art
python3 -m http.server 8000

# Генерация всех страниц
python3 generate_site.py

# Проверка sitemap
python3 -c "import xml.etree.ElementTree as ET; ET.parse('sitemap.xml'); print('OK')"

# Git
git add -A
git commit -m "описание"
git push origin master
```

---

*Документ актуален на 2026-06-15. При внесении изменений в SEO-логику необходимо обновлять этот файл.*
