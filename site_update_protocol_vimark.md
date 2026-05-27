# SOP: Обновление сайта vimark.art — Протокол добавления новых работ

**Версия:** 1.0  
**Дата:** 2026-05-27  
**Автор:** Maxim Mitenkov  
**Исполнитель:** Kimi Code (VS Code)  
**Цель:** Стандартизировать процесс публикации новых артов с полным SEO и автоматической интеграцией Pinterest API

---

## 1. Общий принцип

Каждый новый арт = отдельная страница проекта (Single) + запись в портфолио + Pinterest-пин.

**Золотое правило:** Ни один арт не публикуется без заполнения ВСЕХ обязательных полей. Пропуск хотя бы одного пункта = отклонение задачи.

---

## 2. Структура папок и файлов

```
/project/
  /shadow-over-innsmouth/
    index.html              # Страница проекта
    og-image.jpg            # 1200×630, < 200KB
    /images/
      cover.webp            # Основное изображение, 1920×1080 или вертикальное
      detail-1.webp         # Детали/процесс (опционально)
      detail-2.webp
    /thumbs/
      thumb-600.webp        # Превью 600×400
      thumb-300.webp        # Превью 300×200 (lazy loading)

/data/
  projects.json             # Реестр всех проектов для генерации портфолио

/pinterest/
  pins.json                 # Реестр запланированных/опубликованных пинов
```

**Именование папок:** kebab-case, только латиница, цифры, дефисы.  
**Пример:** `the-nameless-city`, `endymion-cover`, `board-game-characters-2026`

---

## 3. Обязательные поля нового проекта (SEO + контент)

### 3.1 Базовые метаданные

| Поле | Формат | Пример | Обязательно |
|------|--------|--------|-------------|
| **project_id** | kebab-case | `shadow-over-innsmouth` | Да |
| **title** | Название + тип работы | `The Shadow over Innsmouth — Book Cover Illustration` | Да |
| **meta_description** | 150–160 символов | `Book cover illustration for H.P. Lovecraft adaptation. Cosmic horror, architectural decay, digital painting by Maxim Mitenkov.` | Да |
| **year** | Год создания | `2024` | Да |
| **category** | Тип работы | `Book Cover` / `Illustration` / `Character Design` / `Board Game` / `Matte Painting` | Да |
| **client** | Клиент/издательство | `Private commission` / `HarperCollins` / `McGraw-Hill` | Да |
| **medium** | Техника | `Digital painting, Photoshop` / `3D base in Blender, overpaint in Photoshop` | Да |
| **concept** | 2–4 предложения о задаче | `The client needed a cover that conveyed cosmic dread without clichés. We focused on architectural decay and impossible geometry.` | Да |
| **result** | Итог/достижение | `Used for limited edition hardcover. Became one of the most shared covers in publisher's 2024 catalog.` | Нет, но желательно |
| **review_quote** | Цитата клиента (если есть) | `Maxim perfectly captured the atmosphere...` | Нет |
| **review_author** | Имя клиента | `Sarah Chen` | Если есть review_quote |
| **review_source** | Источник отзыва | `Reedsy` / `Direct email` | Если есть review_quote |

### 3.2 Изображения

| Поле | Требования | Обязательно |
|------|-----------|-------------|
| **main_image** | WebP, макс. 1500px по длинной стороне, < 500KB | Да |
| **thumb_image** | WebP, 600×400px, < 100KB | Да |
| **og_image** | JPG, 1200×630px, < 200KB | Да |
| **alt_text** | `[Что] · [Для чего] · [Стиль] · by Maxim Mitenkov` | Да |
| **pinterest_image** | Вертикальное 2:3, мин. 1000×1500px, < 800KB | Да |

**Правило alt_text:**  
`Book cover illustration for The Shadow over Innsmouth — cosmic horror, architectural decay, digital painting by Maxim Mitenkov`

### 3.3 Schema.org (JSON-LD)

На каждой странице проекта обязательно в `<head>`:

```json
{
  "@context": "https://schema.org",
  "@type": "VisualArtwork",
  "name": "{title}",
  "image": "https://www.vimark.art/project/{project_id}/images/cover.webp",
  "creator": {
    "@type": "Person",
    "name": "Maxim Mitenkov",
    "url": "https://www.vimark.art"
  },
  "artMedium": "{medium}",
  "artform": "{category}",
  "dateCreated": "{year}",
  "description": "{concept}",
  "url": "https://www.vimark.art/project/{project_id}/"
}
```

Если есть отзыв — добавить блок `review` (см. раздел 3.1 полей).

### 3.4 Open Graph

```html
<meta property="og:title" content="{title} | Maxim Mitenkov">
<meta property="og:description" content="{meta_description}">
<meta property="og:image" content="https://www.vimark.art/project/{project_id}/og-image.jpg">
<meta property="og:type" content="article">
<meta property="og:url" content="https://www.vimark.art/project/{project_id}/">
<meta property="article:published_time" content="{year}-01-01">
<meta property="article:author" content="Maxim Mitenkov">
```

---

## 4. Pinterest-протокол (автоматическое обновление)

### 4.1 Структура данных для Pinterest

При добавлении нового арта Kimi Code должен автоматически сгенерировать запись в `/pinterest/pins.json`:

```json
{
  "pin_id": "{project_id}-pinterest",
  "status": "ready_to_publish",
  "board": "Book Cover Design",
  "image_path": "/project/{project_id}/images/pinterest.webp",
  "link": "https://www.vimark.art/project/{project_id}/",
  "title": "{title}",
  "description": "{pinterest_description}",
  "alt_text": "{alt_text}",
  "tags": ["{tag1}", "{tag2}", "..."],
  "date_created": "2026-05-27",
  "date_published": null
}
```

### 4.2 Правила описания для Pinterest

**Формула:**
```
[Тип работы] for [название/клиент]. [Краткое описание стиля/атмосферы]. [Техника]. By Maxim Mitenkov.

#bookcover #illustration #[стиль] #[жанр] #digitalpainting #coverdesign #artwork #[доп. тег]
```

**Пример:**
```
Book cover illustration for a dark fantasy novel. Cosmic horror atmosphere with architectural decay and surreal geometry. Digital painting by Maxim Mitenkov.

#bookcover #illustration #darkart #surrealism #cosmichorror #digitalpainting #coverdesign #bookillustration #maximmitenkov #vimarkart
```

**Правила:**
- Описание: 300–500 символов (включая хештеги)
- Хештеги: 5–10 штук, на английском, смешанные популярные и нишевые
- Не использовать русские хештеги (алгоритм Pinterest хуже их индексирует)
- Всегда включать: `#bookcover` или `#illustration`, `#digitalpainting`, `#maximmitenkov`, `#vimarkart`

### 4.3 Доски (Boards) — выбор по категории

| Категория проекта | Доска Pinterest |
|-------------------|-----------------|
| Book Cover | Book Cover Design |
| Illustration | Dark Fantasy Illustration |
| Illustration (сюрреализм) | Surreal Fantasy Illustration |
| Character Design | Character Design & Concept Art |
| Board Game / Video Game | Game Art & Illustration |
| Matte Painting | Environment & Matte Painting |
| Любой / Все | Maxim Mitenkov Portfolio |

### 4.4 Размеры изображений для Pinterest

- **Соотношение:** 2:3 (вертикальное)
- **Минимум:** 1000×1500px
- **Оптимум:** 1200×1800px
- **Формат:** WebP
- **Макс. размер:** 800KB
- **Путь на сайте:** `pinterest/images/{project_id}.webp`

**Примечание:** Pinterest плохо обрезает горизонтальные изображения. Генератор сайта автоматически создаёт вертикальный 2:3 crop из первого изображения проекта.

---

## 5. Пошаговый алгоритм для Kimi Code (VS Code)

### Шаг 0: Получение исходных данных от Maxim
Kimi Code получает:
- Исходное изображение (макс. качество)
- Файл `project.txt` (Способ A) или сообщение в чат (Способ B)
- Категорию проекта
- Год создания

### Шаг 1: Подготовка изображений
- [ ] Создать папку `/project/{project_id}/`
- [ ] Сгенерировать `cover.webp` (основное, 1920px по длинной стороне)
- [ ] Сгенерировать `thumb-600.webp` и `thumb-300.webp`
- [ ] Сгенерировать `og-image.jpg` (1200×630)
- [ ] Сгенерировать `pinterest.webp` (вертикальный 2:3, 1200×1800)
- [ ] Проверить размеры всех файлов (не превышают лимиты)
- [ ] Прописать alt_text для всех изображений

### Шаг 2: Создание страницы проекта
- [ ] Создать `/project/{project_id}/index.html`
- [ ] Вставить JSON-LD (VisualArtwork) в `<head>`
- [ ] Вставить Open Graph метатеги
- [ ] Заполнить `<title>` и `<meta name="description">`
- [ ] Добавить BreadcrumbList schema
- [ ] Разместить основное изображение с `loading="eager"`
- [ ] Добавить детали/процесс с `loading="lazy"` (если есть)
- [ ] Добавить блок отзыва (если есть)
- [ ] Добавить навигацию: ← Previous · Next →
- [ ] Добавить CTA: "Need a similar cover? Let's talk" → /contact

### Шаг 3: Обновление портфолио
- [ ] Добавить запись в `/data/projects.json`
- [ ] Проверить, что проект появился в нужной категории фильтра
- [ ] Обновить главную страницу (если проект попадает в featured)

### Шаг 4: SEO-чеклист
- [ ] Проверить `<title>` (50–60 символов)
- [ ] Проверить `<meta name="description">` (150–160 символов)
- [ ] Проверить alt_text всех изображений
- [ ] Проверить JSON-LD через validator.schema.org
- [ ] Проверить Open Graph через Facebook Sharing Debugger (опционально)
- [ ] Проверить, что URL доступен и нет 404
- [ ] Проверить мобильную версию (responsive)

### Шаг 5: Pinterest-протокол (автоматическая публикация через API)
- [ ] Запустить `generate_site.py` — он автоматически:
  - Сгенерирует вертикальные 2:3 изображения в `pinterest/images/`
  - Обновит `pinterest/pins.json` со статусом `ready_to_publish`
  - Добавит Pinterest Rich Pins meta-теги на страницы проектов
- [ ] Проверить `pinterest/pins.json`: description содержит 5–10 хештегов на английском, board выбрана правильно
- [ ] Закоммитить и запушить изменения — GitHub Action `Publish to Pinterest` выполнит публикацию автоматически
- [ ] Если публикация не прошла, проверить `PINTEREST_ACCESS_TOKEN` в GitHub Secrets

**Требования к Pinterest API:**
1. Business-аккаунт на Pinterest
2. Приложение зарегистрировано на [developers.pinterest.com](https://developers.pinterest.com/)
3. Политика конфиденциальности размещена на сайте: `https://vimark.art/privacy.html`
4. OAuth-токены сохранены в GitHub Secrets:
   - `PINTEREST_ACCESS_TOKEN` (или `PINTEREST_REFRESH_TOKEN` + `PINTEREST_CLIENT_ID` + `PINTEREST_CLIENT_SECRET`)

### Шаг 6: Git commit и деплой
- [ ] Commit message: `feat: add project {project_id} — {title}`
- [ ] Push в GitHub
- [ ] Проверить деплой на Vercel
- [ ] Проверить живой URL: `https://www.vimark.art/project/{project_id}/`
- [ ] Проверить в Google Search Console (Request Indexing)

### Шаг 7: Пост-публикация
- [ ] Добавить URL в sitemap.xml
- [ ] Отправить sitemap в Google Search Console
- [ ] Обновить Pinterest pins.json статус на `published` + дата
- [ ] Уведомить Maxim о завершении

---

## 6. Передача данных нового проекта (2 способа)

### Способ A (рекомендуемый): Файл `project.txt`

Создайте папку проекта и положите рядом с исходником файл `project.txt`:

```
/project/shadow-over-innsmouth/
├── source-image.jpg          ← Исходник от Maxim
└── project.txt               ← Заполненные данные (обычный текст)
```

**Формат `project.txt`:**

```
project_id: shadow-over-innsmouth
title: The Shadow over Innsmouth
category: Book Cover
year: 2024
client: Private commission for independent publisher
medium: Digital painting, Photoshop, 3D base in Blender
concept: The client needed a cover that conveyed cosmic dread without relying on clichés. We focused on architectural decay and impossible geometry.
result: Used for limited edition hardcover. Became one of the most shared covers in publisher's 2024 catalog.
review_quote: Maxim perfectly captured the cosmic horror atmosphere. He was responsive, professional, and delivered beyond expectations.
review_author: Sarah Chen
review_source: Reedsy
```

**Правила заполнения:**
- Каждая строка: `ключ: значение`
- Ключи только из списка ниже — не добавлять свои
- Если данных нет — пропустите строку (не пишите ключ)
- Многострочный текст разрешён, пока следующая строка не начинается с нового ключа

**Kimi Code автоматически:**
1. Читает `project.txt` и извлекает все поля
2. Генерирует `meta_description`, `alt_text`, `pinterest_description` по шаблонам
3. Создаёт все изображения (WebP, OG, Pinterest)
4. Генерирует HTML-страницу с JSON-LD
5. Обновляет `projects.json` и `pins.json`

### Способ B: Сообщение в чат

Если файл создавать неудобно — просто скопируйте шаблон ниже и заполните в чате Kimi Code:

```
Новый проект:
project_id: [kebab-case]
title: [Title]
category: [Book Cover / Illustration / Character Design / ...]
year: [YYYY]
client: [Name / Private commission]
medium: [Digital painting, Photoshop...]
concept: [2-4 предложения]
result: [итог, если есть]
review_quote: [цитата]
review_author: [имя]
review_source: [Reedsy / Direct]
```

Kimi Code извлечёт данные и выполнит протокол по шагам.

---

## 7. Шаблоны для быстрого заполнения

### 6.1 Шаблон meta_description
```
[Category] for [Client/Book]. [Style/atmosphere]. [Technique] by Maxim Mitenkov.
```
**Пример:** `Book cover illustration for H.P. Lovecraft adaptation. Cosmic horror, architectural decay, digital painting by Maxim Mitenkov.`

### 6.2 Шаблон title
```
[Project Name] — [Category] | Maxim Mitenkov
```
**Пример:** `The Shadow over Innsmouth — Book Cover | Maxim Mitenkov`

### 6.3 Шаблон concept
```
The client needed [что]. We focused on [решение]. The result [итог].
```
**Пример:** `The client needed a cover that conveyed cosmic dread without relying on clichés. We focused on architectural decay and impossible geometry. The illustration was used for the limited edition hardcover.`

### 6.4 Шаблон Pinterest description
```
[Category] for [Project/Client]. [Atmosphere/style details]. [Technique] by Maxim Mitenkov.

#bookcover #illustration #[style] #[genre] #digitalpainting #coverdesign #maximmitenkov #vimarkart
```

---

## 8. Контроль качества (QA)

### 7.1 Автоматические проверки (Kimi Code должен выполнять)

```
□ Длина title: 50–60 символов
□ Длина meta_description: 150–160 символов
□ Все изображения в WebP (кроме og-image)
□ Размер og-image: ровно 1200×630
□ Pinterest image: вертикальное, 2:3 (1200×1800)
□ Pinterest pins.json обновлён со статусом ready_to_publish
□ Pinterest Rich Pins meta-теги присутствуют на странице проекта
□ JSON-LD валиден (проверка через schema.org validator — ментально)
□ Alt_text содержит "by Maxim Mitenkov"
□ Все обязательные поля из раздела 3.1 заполнены
□ URL проекта: /project/{kebab-case}.html
□ Ссылка на проект работает (нет битых ссылок)
```

### 7.2 Ручные проверки (Maxim)

- [ ] Визуальная проверка страницы проекта (дизайн, отступы, типографика)
- [ ] Проверка изображения на ретина-дисплеях
- [ ] Проверка Pinterest-пина (обрезка, читаемость текста на изображении)

---

## 9. Частые ошибки (Anti-patterns)

| Ошибка | Почему плохо | Как исправить |
|--------|-------------|---------------|
| Пропуск alt_text | Потеря SEO + Pinterest accessibility | Всегда заполнять по формуле |
| Горизонтальное изображение для Pinterest | Pinterest обрежет или покажет плохо | Всегда делать вертикальный 2:3 crop |
| Русские хештеги | Алгоритм Pinterest не индексирует | Только английские теги |
| Пустой review_author | Выглядит фейковым | Либо полное имя + источник, либо не добавлять отзыв |
| Пропуск year | Посетитель не понимает актуальность | Всегда указывать год создания |
| Одинаковые meta_description для всех проектов | Google считает дублированным контентом | Уникальный текст для каждого проекта |
| Нет JSON-LD | Потеря rich snippets в Google | Обязательно на каждой странице |

---

## 10. Пример полного заполнения (Reference)

```json
{
  "project_id": "shadow-over-innsmouth",
  "title": "The Shadow over Innsmouth — Book Cover Illustration",
  "meta_description": "Book cover illustration for H.P. Lovecraft adaptation. Cosmic horror, architectural decay, digital painting by Maxim Mitenkov.",
  "year": "2024",
  "category": "Book Cover",
  "client": "Private commission for independent publisher",
  "medium": "Digital painting, Photoshop, 3D base in Blender",
  "concept": "The client needed a cover that conveyed cosmic dread without relying on clichés. We focused on architectural decay and impossible geometry to create unease.",
  "result": "The illustration was used for the limited edition hardcover and became one of the most shared covers in the publisher's 2024 catalog.",
  "review_quote": "Maxim perfectly captured the cosmic horror atmosphere. He was responsive, professional, and delivered beyond expectations.",
  "review_author": "Sarah Chen",
  "review_source": "Reedsy",
  "alt_text": "Book cover illustration for The Shadow over Innsmouth — cosmic horror, architectural decay, digital painting by Maxim Mitenkov",
  "pinterest_description": "Book cover illustration for a Lovecraftian dark fantasy novel. Cosmic horror atmosphere with architectural decay and surreal geometry. Digital painting by Maxim Mitenkov.

#bookcover #illustration #darkart #cosmichorror #lovecraft #digitalpainting #coverdesign #surrealism #maximmitenkov #vimarkart",
  "pinterest_board": "Book Cover Design",
  "pinterest_tags": ["bookcover", "illustration", "darkart", "cosmichorror", "lovecraft", "digitalpainting", "coverdesign", "surrealism", "maximmitenkov", "vimarkart"]
}
```

---

## 11. Обновление протокола

- **Версионирование:** При изменении правил — обновлять версию в шапке документа.
- **Changelog:** Фиксировать изменения в конце документа.
- **Согласование:** Любые изменения в обязательных полях — только после согласования с Maxim.

---

## 12. Pinterest API: настройка автопубликации

### 12.1 Регистрация приложения
1. Перейти на [developers.pinterest.com](https://developers.pinterest.com/)
2. Создать приложение, указать:
   - **Name:** vimark.art Portfolio Publisher
   - **Privacy Policy URL:** `https://vimark.art/privacy.html`
   - **Redirect URI:** `https://vimark.art/` (или localhost для локального теста)
3. Получить **App ID** и **App Secret**

### 12.2 Получение токенов (OAuth)
1. Открыть в браузере:
   ```
   https://www.pinterest.com/oauth/?client_id=YOUR_APP_ID&redirect_uri=https://vimark.art/&response_type=code&scope=boards:read,pins:read,pins:write
   ```
2. Авторизовать приложение
3. Обменять `code` на `access_token` и `refresh_token` через POST `/v5/oauth/token`
4. Сохранить токены в **GitHub Secrets** репозитория:
   - `PINTEREST_ACCESS_TOKEN`
   - `PINTEREST_REFRESH_TOKEN`
   - `PINTEREST_CLIENT_ID`
   - `PINTEREST_CLIENT_SECRET`

### 12.3 Доски Pinterest
Доски должны быть созданы вручную в Pinterest. Имена досок указаны в `pinterest/config.json` и маппятся на категории сайта. Если доска не найдена, пин публикуется в `Maxim Mitenkov Portfolio`.

### 12.4 Локальный запуск публикации
Если нужно опубликовать пины вручную (без GitHub Action):
```bash
pip install requests Pillow
export PINTEREST_ACCESS_TOKEN="your_token"
python pinterest_publish.py
```

---

**Changelog:**
- v1.1 (2026-05-27) — Добавлена полная автоматизация Pinterest API: `pinterest_publish.py`, GitHub Action, генерация 2:3 изображений, Rich Pins meta-теги.
- v1.0 (2026-05-27) — Initial version. Covers SEO, Schema.org, Pinterest integration, and Kimi Code workflow.
