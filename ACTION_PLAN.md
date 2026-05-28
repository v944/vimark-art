# План действий по улучшению vimark.art

> **Составлен на основе аудита от 2026-05-28**  
> **Проверка:** ручной анализ кода + скрипты

---

## Сводка: что уже работает (не трогать)

| Функция | Статус | Где проверено |
|---------|--------|---------------|
| Google Analytics 4 | ✅ | `G-6RBP7X7H88` на всех страницах |
| Яндекс.Метрика | ✅ | `109279162`, вебвизор + цели |
| Schema.org (Person, BreadcrumbList, AggregateRating, VisualArtwork) | ✅ | Все типы на месте |
| Open Graph / Twitter Cards | ✅ | На всех страницах |
| hreflang (en/ru/x-default) | ✅ | На всех основных страницах |
| Canonical URLs | ✅ | Корректны |
| Sitemap + Image Sitemap | ✅ | `sitemap.xml`, `image-sitemap.xml` |
| robots.txt | ✅ | Базовый, но рабочий |
| WebP thumbnails | ✅ | `thumbnails/` |
| Lazy loading | ✅ | `loading="lazy"` на 638+ изображениях |
| Theme toggle (светлая/тёмная) | ✅ | `localStorage` |
| Lang switch (EN/RU) | ✅ | На всех страницах |
| Scroll to Top | ✅ | Есть |
| Lightbox | ✅ | С навигацией и счётчиком |
| Sticky Contact (Telegram/WhatsApp) | ✅ | С трекингом |
| Commissions Status | ✅ | 🟢 "Open for commissions" |
| **Форма — выбор типа проекта** | ✅ | `contact.html` и `ru/contact.html` уже имеют `<select id="project-type">` |
| Pinterest Rich Pins meta | ✅ | На страницах проектов |

---

## 🔴 Высокий приоритет (критичные ошибки)

### 1. Включить автопубликацию в Pinterest

**Проверка:**
```bash
$ ls -la .github/workflows/
pinterest.yml.disabled   ← файл отключён
```

**Действие:**
1. Переименовать `.github/workflows/pinterest.yml.disabled` → `pinterest.yml`
2. Получить токены Pinterest API v5:
   - `PINTEREST_ACCESS_TOKEN`
   - `PINTEREST_REFRESH_TOKEN`
   - `PINTEREST_CLIENT_ID`
   - `PINTEREST_CLIENT_SECRET`
3. Добавить их в GitHub Secrets (Settings → Secrets and variables → Actions)
4. Создать доски в Pinterest и сверить с `pinterest/config.json`
5. Запушить изменение — workflow сработает автоматически

---

### 2. Исправить Open Graph для русской версии

**Проверка:**
```bash
$ grep 'og:url' ru/index.html
<meta property="og:url" content="https://vimark.art/">   ← должно быть /ru/
```

**Действие:**
1. В `generate_site.py` найти шаблон OG для RU-страниц
2. Исправить `og:url` с `https://vimark.art/` на `https://vimark.art/ru/`
3. Перегенерировать сайт

---

### 3. Добавить AVIF + srcset для изображений

**Проверка:**
```bash
$ find . -name '*.avif' | wc -l
0

$ grep 'srcset\|<picture' project/bookcover-2026.html
# ничего не найдено
```

**Действие:**
1. Установить библиотеку для AVIF (если Pillow не поддерживает напрямую — использовать `pillow-avif` или вызывать `avifenc`/`ffmpeg`)
2. В `generate_site.py` добавить генерацию AVIF для каждого оригинала:
   - 3 размера: `640w`, `1024w`, `1400w`
   - Качество: 75–80%
3. Изменить HTML-шаблон изображений:
   ```html
   <picture>
     <source srcset="img-640.avif 640w, img-1024.avif 1024w"
             sizes="(max-width: 800px) 90vw, 50vw"
             type="image/avif">
     <source srcset="img-640.webp 640w, img-1024.webp 1024w"
             sizes="(max-width: 800px) 90vw, 50vw"
             type="image/webp">
     <img src="img-original.jpg" loading="lazy" width="800" height="600" alt="...">
   </picture>
   ```
4. Перегенерировать сайт

---

### 4. Добавить preload для критических ресурсов

**Проверка:**
```bash
$ grep 'rel="preload"' index.html
# ничего не найдено
```

**Действие:**
1. В `generate_site.py` добавить в `<head>` всех страниц:
   ```html
   <link rel="preload" href="/style.css" as="style">
   <link rel="preload" href="/script.js" as="script">
   ```
2. Для главной и страниц проектов добавить:
   ```html
   <link rel="preload" href="{hero_image}" as="image" fetchpriority="high">
   ```
3. Перегенерировать сайт

---

## 🟠 Средний приоритет (улучшение UX и автоматизации)

### 6. Автоматизировать генерацию через GitHub Actions

**Проверка:**
```bash
$ ls .github/workflows/
pinterest.yml.disabled   ← нет build workflow
```

**Действие:**
1. Создать `.github/workflows/build.yml`:
   ```yaml
   name: Build Site
   on:
     push:
       branches: [ master ]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
           with:
             python-version: '3.12'
         - run: pip install pillow
         - run: python generate_site.py
         - run: |
             git config user.name "github-actions[bot]"
             git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
             git add .
             git diff --quiet && git diff --staged --quiet || git commit -m "ci: auto-generate site"
             git push
   ```
2. Запушить — workflow активируется

---

### 7. Добавить honeypot в контактную форму

**Проверка:**
```bash
$ grep '_honey\|honeypot' contact.html ru/contact.html
# ничего не найдено
```

**Действие:**
1. В `generate_site.py` в шаблон формы добавить:
   ```html
   <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
   ```
2. Убедиться, что Web3Forms поддерживает honeypot (документация: поле `_honey`)
3. Перегенерировать сайт

---

### 8. Добавить микроразметку Offer для услуг

**Проверка:**
```bash
$ grep 'Offer\|priceSpecification' index.html contact.html
# ничего не найдено
```

**Действие:**
1. В `generate_site.py` добавить JSON-LD на страницу контактов или в блок Pricing на главной:
   ```json
   {
     "@context": "https://schema.org",
     "@type": "Offer",
     "itemOffered": {
       "@type": "Service",
       "name": "Book Cover Illustration",
       "description": "Custom book cover from $700"
     },
     "priceSpecification": {
       "@type": "UnitPriceSpecification",
       "price": 700,
       "priceCurrency": "USD"
     }
   }
   ```
2. Добавить для всех типов услуг (Illustration, Character design, Environment concept)
3. Перегенерировать сайт

---

### 9. Динамический lastmod в sitemap

**Проверка:**
```bash
$ grep 'lastmod' sitemap.xml | head -3
<lastmod>2026-05-27</lastmod>
<lastmod>2026-05-27</lastmod>
<lastmod>2026-05-27</lastmod>   ← все одинаковые
```

**Действие:**
1. В `generate_site.py` заменить фиксированную дату на дату последнего изменения папки проекта:
   ```python
   import subprocess
   lastmod = subprocess.check_output(
       ['git', 'log', '-1', '--format=%cd', '--date=short', '--', folder_path]
   ).decode().strip()
   ```
2. Для корневых страниц использовать дату изменения `projects.ini` или `generate_site.py`
3. Перегенерировать сайт

---

## 🟡 Низкий приоритет (конверсия и расширение)

### 10. Создать отдельную страницу «Pricing»

**Проверка:**
```bash
$ ls pricing.html ru/pricing.html
ls: cannot access 'pricing.html': No such file or directory
```

**Действие:**
1. В `generate_site.py` добавить генерацию `pricing.html` и `ru/pricing.html`
2. Вынести текущий блок цен из `index.html` на отдельную страницу с расширенным описанием
3. Добавить ссылку в меню (main-nav)
4. Перегенерировать сайт

---

### 11. Интегрировать Calendly для звонков

**Проверка:**
```bash
$ grep -i 'calendly\|book.a.call' index.html contact.html
# ничего не найдено
```

**Действие:**
1. Создать бесплатный аккаунт Calendly
2. Получить ссылку на страницу бронирования (например, `https://calendly.com/vimark/30min`)
3. Добавить кнопку «Book a call»:
   - Вариант A: в раздел Contact на главной
   - Вариант B: плавающая кнопка рядом с Telegram/WhatsApp
4. Добавить трекинг клика (gtag + Yandex reachGoal)

---

### 12. Добавить отзывы на страницы проектов

**Проверка:**
```bash
$ grep 'review' project/bookcover-2026.html | grep -v 'reviews.html'
# ничего не найдено
```

**Действие:**
1. В `projects.ini` добавить поле `reviews = ["review_id_1", "review_id_2"]`
2. В `generate_site.py` на странице проекта выводить 1–2 соответствующих отзыва внизу (после галереи)
3. Перегенерировать сайт

---

### 13. Улучшить alt-тексты

**Проверка:**
```bash
$ grep 'alt_text' generate_site.py
alt_text = f"{title} — {description[:120] if description else 'Digital painting'} by Maxim Mitenkov"
```

Текущая формула уже хорошая, но можно усилить:
1. Убедиться, что `captions.txt` содержит описания для всех ключевых работ
2. Добавить в `projects.ini` поле `medium` (Photoshop, Procreate, Blender и т.д.)
3. В `generate_site.py` обновить формулу:
   ```python
   alt_text = f"{title} — illustration for {project_name} — {medium} — fantasy art by Maxim Mitenkov"
   ```
4. Перегенерировать сайт

---

## 📋 Контрольный чек-лист

### Неделя 1
- [ ] Исправить `og:url` для RU в `generate_site.py`
- [ ] Перегенерировать сайт
- [ ] Запушить на Vercel

### Неделя 2
- [ ] Настроить Pinterest API и включить workflow
- [ ] Добавить AVIF-генерацию в `generate_site.py`
- [ ] Добавить `<picture>` + `srcset` в шаблоны
- [ ] Добавить `preload` в `<head>`

### Неделя 3
- [ ] Создать GitHub Action для автогенерации
- [ ] Добавить honeypot в форму
- [ ] Добавить `Offer` JSON-LD
- [ ] Исправить `lastmod` через git-log

### Неделя 4
- [ ] Создать страницу `pricing.html`
- [ ] Настроить Calendly и добавить кнопку
- [ ] Добавить отзывы на страницы проектов
- [ ] Улучшить alt-тексты

### Месяц 2
- [ ] Отправить sitemap в Google Search Console
- [ ] Проверить Core Web Vitals в PageSpeed Insights
- [ ] Валидировать Pinterest Rich Pins
- [ ] Настроить проверку битых ссылок (опционально)

---

## Итог

**Что требует немедленного вмешательства:**
1. Отключенный Pinterest — упускается бесплатный трафик
2. Нет AVIF/srcset — теряем скорость и позиции в Google Images
3. Неправильный `og:url` для русской версии

**Что уже работает отлично:**
- Аналитика (GA4 + Я.Метрика с целями)
- SEO-разметка (Schema.org, OG, hreflang)
- Мультиязычность
- Генератор и структура сайта

**Рекомендуемый порядок:** сначала исправить данные (отзывы, OG), затем добавить производительность (AVIF, preload), потом автоматизацию (CI/CD, Pinterest), и в последнюю очередь — расширение функционала (Pricing, Calendly).
