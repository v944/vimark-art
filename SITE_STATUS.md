# vimark.art — Текущее состояние проекта

**Дата:** 2026-05-27  
**Версия генератора:** generate_site.py (Python 3 + Pillow)  
**Языки:** English (основной), Russian (`/ru/`)  
**Хостинг:** Vercel (статический сайт из GitHub)  

---

## 1. Архитектура сайта

### Генератор
- **Файл:** `generate_site.py`
- **Принцип:** Сканирует папки с изображениями (`Book Illustrations/`, `BookCover/`, `comic/`, `Personal/`, `STRONG/`, `HERO2/`) и генерирует:
  - Главную страницу с галереей (`index.html` / `ru/index.html`)
  - Страницы категорий (`book-illustrations.html`, `bookcover.html` и т.д.)
  - Страницы проектов (`project/{id}.html`) — отдельная страница для каждой подпапки
  - Thumbnails (`thumbnails/`) — WebP, 600×600, качество 85%
  - Sitemap (`sitemap.xml`) + Image Sitemap (`image-sitemap.xml`)
  - Pinterest-ассеты (`pinterest/images/*.webp` + `pinterest/pins.json`)

### Структура страниц
| Страница | Назначение |
|----------|------------|
| `index.html` | Главная: hero, фильтры по категориям, карточки проектов, about, contact |
| `project/{id}.html` | Single-страница проекта: hero, meta, галерея, CTA |
| `{category}.html` | Landing категории: карточки проектов |
| `reviews.html` | 71 отзыв с Reedsy + AggregateRating schema |
| `contact.html` | Форма обратной связи (Web3Forms) |
| `privacy.html` | Политика конфиденциальности (для Pinterest Developer) |
| `404.html` | Кастомная страница 404 |

---

## 2. SEO и микроразметка

### Реализовано
- [x] **Open Graph** — `og:title`, `og:description`, `og:image`, `og:image:width/height` на всех страницах
- [x] **Twitter Cards** — `summary_large_image` на всех страницах
- [x] **Schema.org / JSON-LD:**
  - `Person` — на главной (creator info)
  - `VisualArtwork` — на карточках изображений в галерее
  - `BreadcrumbList` — на всех project- и category-страницах
  - `AggregateRating` — на странице отзывов (5/5, 71 review)
- [x] **Canonical + hreflang** — `en` / `ru` / `x-default` на всех страницах
- [x] **Sitemap** — `sitemap.xml` (для поисковиков)
- [x] **Image Sitemap** — `image-sitemap.xml` (145 изображений)
- [x] **Preconnect** — `googletagmanager.com`, `mc.yandex.ru`
- [x] **Alt-тексты** — для всех изображений (из `captions.txt` или авто из имени файла)

### Чеклист SEO (из протокола)
| Критерий | Статус |
|----------|--------|
| Уникальный `<title>` 50–60 символов | ✅ |
| Уникальный `<meta name="description">` 150–160 символов | ✅ |
| JSON-LD на каждой странице | ✅ |
| Open Graph + Twitter Cards | ✅ |
| Canonical + hreflang | ✅ |
| Alt_text содержит "by Maxim Mitenkov" | ✅ (частично, авто-генерация) |
| Sitemap + Image Sitemap | ✅ |

---

## 3. Pinterest-интеграция (новое — 2026-05-27)

### Реализовано
- [x] **Pinterest Rich Pins meta-теги** — на каждой странице проекта (`<meta name="pinterest-rich-pin" content="true">`)
- [x] **Вертикальные изображения 2:3** — автоматически генерируются в `pinterest/images/{project_id}.webp` (1200×1800)
- [x] **`pinterest/pins.json`** — реестр из 18 пинов с:
  - `title`, `description`, `alt_text`, `tags`
  - `board` (маппинг категорий)
  - `image_url`, `link`
  - `status`: `ready_to_publish` / `published`
- [x] **`pinterest/config.json`** — маппинг категорий → досок Pinterest
- [x] **`pinterest_publish.py`** — скрипт публикации через Pinterest API v5
- [x] **`privacy.html`** — страница политики (требование Pinterest Developer)
- [x] **GitHub Action** — `.github/workflows/pinterest.yml.disabled` (отключена до получения API-ключа)

### Статус
> ⚠️ **Заглушка активна.** Автопубликация отключена (workflow переименован в `.disabled`). Все данные для Pinterest генерируются и хранятся — при получении API-ключа достаточно:
> 1. Переименовать файл обратно в `.yml`
> 2. Добавить токены в GitHub Secrets
> 3. Создать доски на Pinterest

---

## 4. UI / UX

### Компоненты
- **Hero-баннер** — случайное изображение из `STRONG/` или `HERO2/`, клиентская ротация (JS)
- **Фильтры** — кнопки "All" + по категориям, клиентская фильтрация
- **Карточки проектов** — главное изображение + 3 thumbnail + оверлей с названием и количеством работ
- **Галерея** — сетка изображений с `loading="lazy"`, `itemscope itemtype="https://schema.org/VisualArtwork"`
- **Lightbox** — полноэкранный просмотр с навигацией ← →, счётчик, caption
- **Sticky Contact** — плавающие иконки Telegram + WhatsApp
- **Theme Toggle** — переключатель светлая/тёмная тема (сохраняется в `localStorage`)
- **Lang Switch** — переключение EN/RU на всех страницах
- **Scroll to Top** — кнопка ↑
- **Reviews Bar** — 5 звёзд + 4 gauge-изображения на главной и странице отзывов

### Технологии фронтенда
- Чистый HTML/CSS/JS (без фреймворков)
- CSS-переменные для тёмной темы
- `loading="lazy"` + `fetchpriority="high"` для изображений
- Responsive дизайн (mobile-first, sidebar → hamburger menu)

---

## 5. Аналитика и отслеживание

| Сервис | ID / Статус |
|--------|-------------|
| Google Analytics 4 | `G-6RBP7X7H88` ✅ |
| Yandex.Metrika | `109279162` ✅ (вебвизор, карта кликов, ecommerce) |
| gtag события | `click_telegram`, `click_whatsapp`, `submit_contact`, `download_cv` |

---

## 6. Контент

### Категории и проекты
| Категория | Проектов | Изображений |
|-----------|----------|-------------|
| Book Illustrations | 5 | 43 |
| Book Cover | 3 | 18 |
| Comic | 7 | 49 |
| Personal | 3 | 35 |
| **Итого** | **18** | **145** |

### Данные проектов
- Хранятся в `projects.ini` (title, year, client, description)
- Подписи к изображениям — `captions.txt` (ручное переопределение или авто из имени файла)
- Локализация — `locale.ini` (EN + RU)

---

## 7. Формы и интеграции

- **Контактная форма** — Web3Forms (`access_key: 211a1ef5-...`)
- **Reedsy** — 71 отзыв подгружается из `Reedsy/reviews.json`
- **Социальные ссылки** — Email, Facebook, LinkedIn, Instagram, Behance, DeviantArt

---

## 8. Что осталось / TODO

### Высокий приоритет
- [ ] **Включить Pinterest автопубликацию** — получить API-ключ, создать доски, включить GitHub Action
- [ ] **Добавить medium в projects.ini** — поле `medium` (Digital painting, Photoshop и т.д.) для более точного Pinterest description
- [ ] **Оптимизация изображений** — проверить размеры OG-image (должно быть 1200×630, сейчас используется thumbnail 600×600)

### Средний приоритет
- [ ] **Pinterest Save Button** — кнопка «Save» прямо на изображениях проектов (для посетителей)
- [ ] **Добавить review на страницы проектов** — если отзыв связан с конкретным проектом
- [ ] **Улучшить alt_text** — гарантировать формат `[Что] · [Для чего] · [Стиль] · by Maxim Mitenkov`
- [ ] **Структурировать `/project/{id}/`** — сейчас страницы плоские (`project/{id}.html`), в протоколе предложена вложенная структура с `index.html` и подпапками

### Низкий приоритет
- [ ] **Google Search Console** — добавить и отправить sitemap (ручная операция)
- [ ] **Facebook Sharing Debugger** — проверить OG-разметку
- [ ] **Pinterest Rich Pins Validator** — валидировать после включения API

---

## 9. Файловая структура (ключевое)

```
vimark.art/
├── generate_site.py           # Генератор сайта
├── projects.ini               # Данные проектов
├── captions.txt               # Подписи к изображениям
├── locale.ini                 # Локализация EN/RU
├── privacy.html               # Политика конфиденциальности
├── pinterest/
│   ├── config.json            # Маппинг досок Pinterest
│   ├── pins.json              # Реестр пинов (18 шт.)
│   └── images/                # Вертикальные 2:3 изображения
├── .github/
│   └── workflows/
│       └── pinterest.yml.disabled   # Заглушка автопубликации
├── project/                   # Страницы проектов (18 шт.)
├── thumbnails/                # WebP-превью (145 шт.)
├── STRONG/                    # Изображения для OG/social
├── HERO2/                     # Hero-баннеры
├── Reedsy/
│   └── reviews.json           # Отзывы (71 шт.)
├── ru/                        # Русская версия (зеркало)
├── style.css                  # Стили
├── script.js                  # Логика (lightbox, фильтры, тема)
├── sitemap.xml                # Карта сайта
└── image-sitemap.xml          # Карта изображений
```

---

## 10. Как обновлять сайт (краткая инструкция)

1. Добавить новые изображения в соответствующую папку (`Book Illustrations/{project}/`)
2. При необходимости — обновить `projects.ini` и `captions.txt`
3. Запустить `python generate_site.py`
4. Проверить `git diff` — убедиться, что новые файлы появились
5. `git add . && git commit -m "feat: add project ..." && git push`
6. Vercel автоматически деплоит. Pinterest-публикация пока отключена.

---

*Документ подготовлен Kimi Code. Последнее обновление: 2026-05-27.*
