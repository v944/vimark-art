# План доработки сайта vimark.art по требованиям v2.0

> Составлен на основе аудита `site_requirements_vimark_v2.md` и текущего состояния кодовой базы.
> Статус: `[✅]` — уже реализовано, `[⚠️]` — частично, `[❌]` — отсутствует.

---

## Аудит текущего состояния

### Блок 1. Техническое SEO и индексация

| Пункт | Статус | Примечание |
|-------|--------|------------|
| Семантическая вёрстка | ⚠️ | Есть `<main>`, `<section>`, `<aside>`, `<nav>`. Нет `<article>`, `<header>`, `<footer>` (site-footer — div). На главной нет `<h1>`. Иерархия заголовков нарушена. |
| ЧПУ-адреса | ⚠️ | URL читаемые (`/project/book-illustrations-endymion.html`), но есть `.html` в конце. Нет параметров. |
| Mobile First / Responsive | ⚠️ | Только 1 breakpoint (800px). Нет точек 320/768/1024/1440+. |
| Core Web Vitals | ⚠️ | Lazy loading есть. Нет blur-up placeholder, явной оптимизации LCP/CLS. |
| robots.txt | ⚠️ | Базовый, не запрещает чувствительные пути. |
| XML Sitemap | ⚠️ | Есть, но приоритеты не различаются (все 0.8/1.0). Нет `image-sitemap.xml`. |
| Микроразметка Schema.org | ⚠️ | Есть `Person` на главной. Нет `VisualArtwork`/`ImageObject` для работ. Нет `BreadcrumbList`. |
| SSR / статическая генерация | ✅ | Полностью статический HTML. |
| hreflang | ❌ | Русская версия в `/ru/`, но теги `hreflang` отсутствуют на всех страницах. |
| Канонические теги | ⚠️ | Есть, но `ru/index.html` указывает canonical на `/` вместо `/ru/`. |

### Блок 2. Изображения

| Пункт | Статус | Примечание |
|-------|--------|------------|
| alt | ⚠️ | Заполнены кратко («Martyn, 2025»). Нет техники и ключевых слов. |
| figcaption | ❌ | Подписи только в lightbox-caption (div). Нет семантического `<figcaption>`. |
| Имена файлов | ❌ | `__0000_E1_Martyn.jpg.jpg`, `crush_by_vimark_dkkvjah-pre.jpg` — не осмысленные. |
| Оптимизация веса | ⚠️ | Thumbnails в WebP, оригиналы в JPG. Нет AVIF. |
| Ленивая загрузка | ✅ | `loading="lazy"` везде кроме hero. |
| CDN | ❌ | Все ресурсы с `vimark.art`. |

### Блок 3. UX/UI

| Пункт | Статус | Примечание |
|-------|--------|------------|
| Hero-секция | ⚠️ | Есть fullscreen изображение. Нет имени/специализации/CTA на первом экране. |
| Галерея | ❌ | `aspect-ratio: 1 / 1` — обрезает изображения. Требуется Masonry или Grid с сохранением пропорций. |
| Вайтспейс | ⚠️ | gap 8px в галерее слишком мал. В проектах 24px — ок. |
| Меню | ⚠️ | Desktop: fixed sidebar (не sticky top). Mobile: бургер — ок. |
| Тёмная тема | ✅ | `#111` фон по умолчанию. Light mode — нет. |
| Микроанимация | ⚠️ | Есть `scale(1.03)` на hover. Нет оверлея с названием/годом/техникой. |
| Эффекты скролла | ✅ | Fade hero при скролле. Без параллакса. |
| Прелоадер / Placeholder | ❌ | Отсутствует blur-up / dominant color. |

### Блок 4. Навигация и структура

| Пункт | Статус | Примечание |
|-------|--------|------------|
| Фильтр по категориям | ❌ | Только якорные ссылки на секции. |
| Страница проекта (single page) | ⚠️ | Есть URL, но нет описания задачи, инструментов, сроков, CTA. |
| Lightbox | ✅ | Есть оверлей, стрелки, Escape, swipe. |
| WIP / Process | ❌ | Нет этапов работы на страницах проектов. |
| Пагинация / «Загрузить ещё» | ❌ | Не используется (всё на одной странице). |
| Кнопка «Наверх» | ❌ | Отсутствует. |
| Кастомная 404 | ❌ | Нет `404.html`. |

### Блок 5. Конверсия и контакты

| Пункт | Статус | Примечание |
|-------|--------|------------|
| Форма обратной связи | ⚠️ | Есть (web3forms). Нет поля «Тип проекта», honeypot-защиты. |
| Sticky-кнопка «Связаться» | ❌ | Нет Telegram/WhatsApp в углу. |
| Commissions Status | ❌ | Нет индикатора статуса заказов. |
| Ориентир по цене | ❌ | Нет проектных рейтов. |
| Социальное доказательство | ❌ | Нет отзывов. |
| CTA на странице проекта | ❌ | Нет кнопки «Заказать похожее». |
| Подписка на обновления | ❌ | Нет email-формы. |
| Скачиваемое CV | ✅ | Есть кнопка в About. |

### Блок 6. Open Graph и соцсети

| Пункт | Статус | Примечание |
|-------|--------|------------|
| Open Graph | ⚠️ | Есть, но `og:image` на проектах может быть не 1200×630. |
| Twitter Cards | ✅ | `summary_large_image` настроен. |
| Мультиязычность | ⚠️ | EN по умолчанию, `/ru/` — ок. Но `ru/index.html` имеет `lang="en"`. |

### Блок 7. Аналитика

| Пункт | Статус | Примечание |
|-------|--------|------------|
| GA4 + Я.Метрика | ✅ | Установлены. |
| GSC + Я.Вебмастер | ⚠️ | Sitemap есть, но неизвестно, добавлены ли в консоли. |
| LinkedIn Insight Tag | ❌ | Нет. |
| Meta Pixel | ❌ | Нет. |
| Пиксель ВКонтакте | ❌ | Нет. |

---

## План действий по этапам

### Этап 1. Критичные SEO-исправления (неделя 1)

Цель: устранить факторы, мешающие индексации и мультиязычности.

1. **Исправить семантическую вёрстку**
   - Добавить `<h1>` на главную (в hero: имя + специализация).
   - Обернуть site-footer в `<footer>`, sidebar-header в `<header>`.
   - Добавить `<article>` вокруг каждой работы в галерее.
   - Проверить иерархию `<h2>` → `<h3>`.

2. **Добавить hreflang**
   - На главной (`index.html`) и каждой странице проекта добавить:
     ```html
     <link rel="alternate" hreflang="en" href="https://vimark.art/..." />
     <link rel="alternate" hreflang="ru" href="https://vimark.art/ru/..." />
     <link rel="alternate" hreflang="x-default" href="https://vimark.art/..." />
     ```
   - Прописать правильные canonical для `/ru/` версий.

3. **Исправить canonical на ru-версии**
   - `ru/index.html` → `canonical: https://vimark.art/ru/`
   - `ru/project/...` → `canonical: https://vimark.art/ru/project/...`

4. **Доработать robots.txt**
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

5. **Доработать sitemap.xml**
   - Проекты: `priority = 0.9`
   - Категории (главная): `priority = 0.7`
   - About/Contact: `priority = 0.5`
   - Добавить `image-sitemap.xml` или `<image:image>` внутри основного sitemap.

6. **Исправить `lang` на ru-страницах**
   - `ru/index.html` и все `ru/project/*.html` должны иметь `<html lang="ru">`.

---

### Этап 2. Микроразметка и изображения (неделя 1–2)

1. **Добавить Schema.org `VisualArtwork`**
   - Для каждой иллюстрации в галерее вставить JSON-LD или микроданные:
     ```json
     {
       "@context": "https://schema.org",
       "@type": "VisualArtwork",
       "name": "Martyn",
       "artist": { "@type": "Person", "name": "Max Mitenkov" },
       "dateCreated": "2025",
       "artMedium": "Digital painting",
       "image": "https://vimark.art/..."
     }
     ```

2. **Добавить `BreadcrumbList`**
   - На страницах проектов:
     ```json
     {
       "@context": "https://schema.org",
       "@type": "BreadcrumbList",
       "itemListElement": [
         { "@type": "ListItem", "position": 1, "name": "Portfolio", "item": "https://vimark.art/" },
         { "@type": "ListItem", "position": 2, "name": "Book Illustrations", "item": "https://vimark.art/#book-illustrations" },
         { "@type": "ListItem", "position": 3, "name": "Endymion", "item": "https://vimark.art/project/book-illustrations-endymion.html" }
       ]
     }
     ```

3. **Улучшить `alt`-тексты**
   - Формат: `Описание сцены — техника — ключевые слова`.
   - Пример: `Martyn character portrait — digital painting, Photoshop — fantasy book illustration, 2025`.
   - Обновить в `captions.txt` и перегенерировать сайт.

4. **Добавить `<figcaption>`**
   - Оборачивать каждую работу в `<figure>` с `<figcaption>`: название, техника, год, теги.

5. **Убрать обрезку изображений в галерее**
   - Заменить `aspect-ratio: 1 / 1` на сохранение оригинальных пропорций (Masonry или `object-fit: contain` + разные размеры ячеек).

6. **Увеличить вайтспейс**
   - gap в галерее: 24–32px вместо 8px.

---

### Этап 3. UX/UI и навигация (неделя 2–3)

1. **Доработать Hero-секцию**
   - Добавить overlay с текстом:
     - `<h1>Max Mitenkov</h1>`
     - Подзаголовок: `Illustrator · Concept Artist`
     - CTA-кнопка: `View Portfolio` / `Get in Touch`

2. **Добавить фильтр по категориям**
   - Горизонтальная панель над сеткой проектов: All, Book Covers, Illustrations, Comics, Concept Art, etc.
   - Фильтрация на JS без перезагрузки.

3. **Добавить оверлей на карточки проектов**
   - При hover: затемнение + overlay с названием, годом, техникой.
   - Анимация 200–300ms ease-out.

4. **Добавить кнопку «Наверх»**
   - Появляется после 1 экрана прокрутки.
   - Плавный скролл.

5. **Создать кастомную 404.html**
   - Извинение, ссылки на главные разделы, случайная работа.

6. **Доработать responsive**
   - Добавить breakpoints: 320, 768, 1024, 1440px.
   - Оптимизировать галерею под мобильные.

---

### Этап 4. Страницы проектов и конверсия (неделя 3–4)

1. **Расширить страницу проекта**
   - Описание задачи (из `projects.ini`).
   - Использованные инструменты.
   - Сроки / год.
   - Кнопка CTA: «Discuss a project» / «Commission similar work».

2. **Добавить WIP / Process**
   - На странице проекта: 2–4 этапа (sketch → blocking → detail → final).
   - Требует отдельной папки/логики в генераторе.

3. **Добавить Commissions Status**
   - Видный блок в хедере или сайдбаре:
     - 🟢 `Open for commissions`
     - 🟡 `Waitlist: 2 weeks`
     - 🔴 `Closed`

4. **Добавить ориентир по ценам**
   - В About или отдельный раздел «Pricing»:
     - Character design from $800
     - Book cover from $500
     - Environment concept from $1200

5. **Добавить социальное доказательство**
   - 2–4 отзыва с аватарами, именами, должностями, ссылками.

6. **Добавить подписку на обновления**
   - Форма email в футере: «New works once a month».

7. **Доработать форму контактов**
   - Добавить dropdown «Project type» (Book cover, Illustration, Concept art, Other).
   - Добавить honeypot-поле для защиты от ботов.

8. **Добавить sticky-кнопку связи**
   - Фиксированная иконка Telegram/WhatsApp в правом нижнем углу.

---

### Этап 5. Аналитика и оптимизация (неделя 4)

1. **Добавить цели в GA4 и Я.Метрику**
   - Отправка формы.
   - Клик на Telegram/WhatsApp.
   - Скачивание CV.
   - Просмотр 3+ работ (событие `gallery_view`).

2. **Добавить пиксели**
   - LinkedIn Insight Tag (B2B-клиенты).
   - Meta Pixel (Instagram/Facebook ретаргетинг).
   - Пиксель VK (вторичный, если нужен РФ/Беларусь).

3. **Оптимизировать Core Web Vitals**
   - Добавить `fetchpriority="high"` для hero-изображения.
   - Установить явные `width`/`height` на все `<img>` (частично есть).
   - Рассмотреть CDN для изображений (Cloudflare/AWS CloudFront/BunnyCDN).

4. **Создать `image-sitemap.xml`**
   - Список всех иллюстраций с `<image:loc>`, `<image:title>`, `<image:caption>`.

---

### Этап 6. Дополнительные улучшения (по возможности)

1. **Light mode (тумблер)**
   - Переключатель тёмная/светлая тема.
   - Сохранение предпочтения в `localStorage`.

2. **Прелоадер / blur-up**
   - Для каждого изображения генерировать миниатюру 20×20px (LQIP) и показывать как placeholder.

3. **Пагинация или «Загрузить ещё»**
   - Для категорий с большим количеством работ (>20).

4. **Убрать `.html` из URL**
   - Настроить rewrite rules на сервере (Apache/Nginx) или перейти на чистые URL.

---

## Чек-лист для отслеживания прогресса

### Этап 1 — SEO-исправления
- [ ] `<h1>` на главной
- [ ] `<header>`, `<footer>`, `<article>`
- [ ] hreflang на всех страницах
- [ ] Правильные canonical для `/ru/`
- [ ] Доработать `robots.txt`
- [ ] Приоритеты в `sitemap.xml`
- [ ] `lang="ru"` на ru-страницах

### Этап 2 — Микроразметка и изображения
- [ ] Schema.org `VisualArtwork` для работ
- [ ] `BreadcrumbList`
- [ ] Улучшенные `alt`-тексты
- [ ] `<figcaption>`
- [ ] Галерея без обрезки (Masonry / Grid с пропорциями)
- [ ] Вайтспейс 24–32px

### Этап 3 — UX/UI
- [ ] Текст + CTA в Hero
- [ ] Фильтр по категориям (JS)
- [ ] Hover-оверлей на карточках
- [ ] Кнопка «Наверх»
- [ ] Кастомная `404.html`
- [ ] Breakpoints 320/768/1024/1440

### Этап 4 — Конверсия
- [ ] Расширенная страница проекта (описание, инструменты, CTA)
- [ ] WIP / Process
- [ ] Commissions Status
- [ ] Ориентир по ценам
- [ ] Отзывы
- [ ] Подписка на email
- [ ] Доработка формы (тип проекта, honeypot)
- [ ] Sticky-кнопка связи

### Этап 5 — Аналитика
- [ ] Цели GA4 / Я.Метрика
- [ ] LinkedIn Insight Tag
- [ ] Meta Pixel
- [ ] VK Pixel
- [ ] Core Web Vitals оптимизация
- [ ] `image-sitemap.xml`

### Этап 6 — Дополнительно
- [ ] Light mode
- [ ] Blur-up placeholder
- [ ] «Загрузить ещё» / пагинация
- [ ] Чистые URL без `.html`
