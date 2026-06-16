# SEO/GEO план vimark.art — 2026

Сводный план на основе `deepseek_markdown_20260616_0f72f8.md` и `vimark_seo_geo_2026-06-16.md`. Исключены дубликаты, расставлены приоритеты. ✅ = уже сделано.

---

## P0 — Быстрые технические победы (2–3 дня)

| # | Задача | Статус | Описание |
|---|--------|--------|----------|
| 1 | **WebSite + SearchAction schema** | ✅ | index.html, about.html, ru/about.html, generate_site.py |
| 2 | **Organization schema** | ✅ | Отдельная `Organization` на index.html, about.html, ru/about.html, generate_site.py |
| 3 | **ImageObject width/height** | ✅ | `QuantitativeValue` в ImageObject JSON-LD (generate_site.py) |
| 4 | **areaServed: Worldwide → список стран** | ✅ | 7 стран (US, UK, CA, AU, RU, DE, FR) |
| 5 | **Eager loading: первые 4 галереи** | ✅ | Счётчик в gallery_html + project_gallery_html; первые 4 `eager`, остальные `lazy` |

✅ **Уже реализовано:** hero-изображения (`eager` + `fetchpriority="high"`), srcset/sizes на всех thumbnails, Related Works, lazy loading на всех не-hero.

---

## P0 — Контент и GEO (2–4 недели)

| # | Задача | Статус | Описание |
|---|--------|--------|----------|
| 6 | **Создать `/blog/` и `/ru/blog/`** | ✅ | Индексные страницы, единый сайт-фрейм (site_frame.py) |
| 7 | **Опубликовать 5 статей EN + 5 RU** | ✅ | Article JSON-LD, OG/Twitter, hreflang, blog.css |
| 8 | **Детализировать кейс Hoëbeke** | ⬜ | Скетчи, процесс, результат, отзыв издателя |
| 9 | **Создать страницу Press/As Seen In** | ❌ | `/press.html` + `/ru/press.html`: публикации, награды, Reedsy, выставки |

---

## P1 — Локальное SEO и коммерческие лендинги (2–3 недели)

| # | Задача | Статус | Описание |
|---|--------|--------|----------|
| 10 | **Гео-упоминания на EN + RU** | ⬜ | «Работаю удаленно», «Минск», города РФ. Сейчас только «Based in Belarus» |
| 11 | **Профили на локальных площадках** | ❌ | Kwork, YouDo, Profiles.ru; Яндекс.Бизнес (если есть ИП) |
| 12 | **Коммерческие лендинги (EN + RU):** | ❌ | Каждый с H1=запрос, галерея, отзывы, FAQ, CTA |
| 12a | `/book-cover-design-cost.html` | ❌ | Стоимость дизайна обложки — таблица/калькулятор |
| 12b | `/fantasy-book-illustrator.html` | ❌ | Иллюстратор фэнтези |
| 12c | `/sci-fi-cover-artist.html` | ❌ | Художник sci-fi обложек |
| 12d | `/horror-book-illustrator.html` | ❌ | Иллюстратор хоррора |
| 13 | **Доп. кейсы (HarperCollins, self-pub, horror)** | ❌ | Отдельные страницы `/case-studies/` с `Article`, before/after, CTA |

---

## P1 — Техническое SEO (1 неделя)

| # | Задача | Статус | Описание |
|---|--------|--------|----------|
| 14 | **Regional hreflang** | ✅ | Решено оставить `en`/`ru` (международный сайт) |
| 15 | **Локальные ключевые в RU** | ✅ | Title/Description обновлены: «иллюстратор книжных обложек», «художник обложек на заказ», «заказать обложку книги» |
| 16 | **Security headers (vercel.json)** | ✅ | X-Content-Type-Options, X-Frame-Options, Referrer-Policy, HSTS, Permissions-Policy, CSP |
| 17 | **PWA manifest.json** | ✅ | `manifest.json`, icon-192.png, icon-512.png, `<link rel="manifest">` на всех страницах |

---

## P2 — E-E-A-T и перелинковка (2–3 недели, параллельно)

| # | Задача | Статус | Описание |
|---|--------|--------|----------|
| 18 | **Видео + VideoObject schema** | ❌ | Записать 2–3 time-lapse → YouTube → встроить на сайт |
| 19 | **Контекстная перелинковка в projects.ini** | ⬜ | HTML-ссылки между проектами в описаниях |
| 20 | **Каталоги и ассоциации** | ⬜ | AOI, Coroflot, Dribbble, Illustration Age |
| 21 | **Outreach / PR** | ❌ | Гостевые посты, интервью, конкурсы обложек |

---

## P3 — Оптимизация (по возможности)

| # | Задача | Статус | Описание |
|---|--------|--------|----------|
| 22 | **AVIF формат** | ❌ | Генерация `.avif`, `<picture>` с source |
| 23 | **Core Web Vitals (PageSpeed)** | ⬜ | Проверить LCP/CLS после внедрения, оптимизировать при необходимости |
| 24 | **Аналитика: цели в Я.Метрике и GA4** | ❌ | События: глубина чтения, клики по ссылкам, просмотр >1 страницы |

---

✅ **Дополнительно:** Blog добавлен в боковое меню и футер на всех страницах; Blog → blog redirect (Linux case-sensitivity); полный hreflang-маппинг на всех страницах.

---

## Чек-лист

### P0 — Сделать сейчас

- [x] 1. WebSite + SearchAction schema (index.html, about.html, generate_site.py)
- [x] 2. Organization schema (index.html, about.html)
- [x] 3. ImageObject width/height (generate_site.py)
- [x] 4. areaServed: Worldwide → [US, UK, CA, AU, RU, DE, FR]
- [x] 5. Eager loading: первые 4 изображения галереи, остальные lazy
- [x] 6. Структура `/blog/` и `/ru/blog/`
- [x] 7. 5 статей EN + 5 RU (первая партия)
- [ ] 8. Детализировать кейс Hoëbeke
- [ ] 9. Страница Press/As Seen In

### P1 — Следом

- [ ] 10. Гео-упоминания (удаленная работа, города)
- [ ] 11. Профили: Kwork, YouDo, Яндекс.Бизнес
- [ ] 12. Лендинги: cost, fantasy, sci-fi, horror (EN + RU)
- [ ] 13. Доп. кейсы (HarperCollins, self-pub, horror)
- [x] 14. Regional hreflang (оставлено en/ru)
- [x] 15. Локальные ключевые в RU Title/Description
- [x] 16. Security headers в vercel.json
- [x] 17. PWA manifest.json

### P2 — Параллельно

- [ ] 18. Видео + VideoObject schema
- [ ] 19. Перелинковка в projects.ini
- [ ] 20. Каталоги: AOI, Coroflot, Dribbble
- [ ] 21. Outreach: гостевые посты, интервью

### P3 — По возможности

- [ ] 22. AVIF
- [ ] 23. Core Web Vitals (проверка PageSpeed)
- [ ] 24. Аналитика: цели, события
