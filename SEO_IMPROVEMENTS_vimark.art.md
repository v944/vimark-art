# План улучшения SEO и производительности сайта vimark.art

> **Дата:** 2026-05-28  
> **Сайт:** https://vimark.art  
> **Цель:** повышение позиций в поиске, ускорение загрузки, рост конверсии

---

## 1. Высокий приоритет (критично для SEO и доверия)

### 1.1 Исправить несоответствие количества отзывов

- **Проблема:** На сайте заявлено «71 verified review», но в `Reedsy/reviews.json` — 23 отзыва, в `reviews.md` — 22. `Schema.org` `AggregateRating` содержит `reviewCount: 71`.
- **Риск:** Поисковые системы могут посчитать данные противоречивыми, что снизит доверие к рейтингу.
- **Решение:**
  - Добавить недостающие отзывы в `reviews.json` до 71 (лучше импортировать их из Reedsy).
  - Или исправить текстовые упоминания и `reviewCount` на 23 (менее предпочтительно, т.к. теряется социальное доказательство).

### 1.2 Внедрить адаптивные изображения (AVIF + srcset)

- **Проблема:** На страницах проектов оригиналы (PNG/JPG) загружаются в полном размере на всех устройствах. Нет `<picture>` или `srcset`.
- **Влияние:** Медленная загрузка на мобильных, плохие Core Web Vitals (LCP, CLS).
- **Решение:**
  - Модифицировать `generate_site.py` для создания AVIF (качество 75–80%) из оригиналов.
  - Генерировать 3 размера: `640w`, `1024w`, `1400w`.
  - Использовать `<picture>` с fallback на WebP и оригинал.
  - Пример кода для шаблона:
    ```html
    <picture>
      <source srcset="image-640.avif 640w, image-1024.avif 1024w"
              sizes="(max-width: 800px) 90vw, 50vw"
              type="image/avif">
      <source srcset="image-640.webp 640w, image-1024.webp 1024w"
              sizes="(max-width: 800px) 90vw, 50vw"
              type="image/webp">
      <img src="image-original.jpg"
           loading="lazy" width="800" height="600" alt="...">
    </picture>
    ```

### 1.3 Включить автоматическую публикацию в Pinterest

- **Проблема:** GitHub Action отключён (`.github/workflows/pinterest.yml.disabled`), хотя все пины и изображения готовы (`pinterest/`).
- **Выгода:** Бесплатный трафик, автоматическое обновление досок при добавлении проектов.
- **Решение:**
  1. Переименовать файл в `pinterest.yml`.
  2. Добавить в GitHub Secrets: `PINTEREST_ACCESS_TOKEN`, `PINTEREST_REFRESH_TOKEN`, `PINTEREST_CLIENT_ID`, `PINTEREST_CLIENT_SECRET`.
  3. Создать доски в Pinterest и сверить маппинг в `pinterest/config.json`.

### 1.4 Исправить Open Graph для русской версии

- **Проблема:** На странице `/ru/index.html` `og:url` указывает на `https://vimark.art/` вместо `/ru/`.
- **Последствия:** Социальные сети могут неправильно индексировать языковую версию.
- **Решение:** В генераторе для всех RU-страниц прописать `og:url` с префиксом `/ru/` (аналогично каноническому URL).

---

## 2. Средний приоритет (улучшение производительности и UX)

### 2.1 Автоматизировать генерацию сайта через GitHub Actions

- **Проблема:** `generate_site.py` запускается вручную локально. Часто забывают выполнить перед push.
- **Решение:** Создать workflow `.github/workflows/build.yml`:
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

### 2.2 Добавить preload для критических ресурсов

- **Проблема:** Отсутствует preload для CSS и основного hero-изображения. LCP может тормозить.
- **Решение:** Добавить в `<head>` всех страниц:
  ```html
  <link rel="preload" href="/style.css" as="style">
  <link rel="preload" href="/STRONG/hero-default.webp" as="image" fetchpriority="high">
  ```

### 2.3 Улучшить alt-тексты по формуле

- **Проблема:** Alt-тексты часто берутся из имени файла (например, `dragon_01.jpg` → `dragon_01`).
- **SEO-эффект:** Более релевантные alt-тексты повышают трафик из Google Images.
- **Рекомендуемый формат:**
  ```
  [Что изображено] · [Проект/книга] · [Техника/стиль] · by Maxim Mitenkov
  ```
- **Реализация:** Модифицировать генератор, чтобы он формировал alt из `projects.ini` + `captions.txt`, либо доработать `captions.txt`.

### 2.4 Добавить микроразметку Offer для услуг

- **Проблема:** Нет структурированных данных для коммерческих услуг (цены на иллюстрации).
- **Решение:** На странице контактов или в блоке Pricing добавить JSON-LD:
  ```json
  {
    "@context": "https://schema.org",
    "@type": "Offer",
    "itemOffered": {
      "@type": "Service",
      "name": "Book Cover Illustration",
      "description": "Custom book cover from $500"
    },
    "priceSpecification": {
      "@type": "UnitPriceSpecification",
      "price": 500,
      "priceCurrency": "USD"
    }
  }
  ```

### 2.5 Добавить honeypot в контактную форму

- **Проблема:** Форма через Web3Forms не имеет защиты от ботов.
- **Решение:** Добавить скрытое поле и проверку на стороне Web3Forms:
  ```html
  <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
  ```
  В `script.js` добавить валидацию, чтобы поле оставалось пустым.

---

## 3. Низкий приоритет (улучшение конверсии и удобства)

### 3.1 Создать отдельную страницу «Pricing»

- **Проблема:** Цены упомянуты в блоке на главной, но нет отдельной страницы. Это снижает SEO для коммерческих запросов («стоимость иллюстрации книги», «прайс концепт-арта»).
- **Решение:** Создать `pricing.html` и `/ru/pricing.html` с детальными ценами (Book Cover, Comic page, Character design). Добавить в меню.

### 3.2 Добавить выбор типа проекта в контактную форму

- **Проблема:** Поле Subject — текстовое. Клиенты редко указывают конкретную услугу.
- **Решение:** Заменить Subject на выпадающий список:
  ```html
  <select name="project_type" required>
    <option value="">Select project type</option>
    <option value="book_cover">Book Cover</option>
    <option value="book_illustrations">Book Illustrations</option>
    <option value="comic">Comic / Graphic Novel</option>
    <option value="concept_art">Concept Art</option>
    <option value="other">Other</option>
  </select>
  ```

### 3.3 Интегрировать виджет Calendly для звонков

- **Проблема:** Пользователь может написать в Telegram/WhatsApp, но это добавляет шаг.
- **Решение:** Добавить кнопку «Book a call» (плавающую или в разделе Contact) с ссылкой на Calendly (бесплатно).

### 3.4 Добавить отзывы на страницы конкретных проектов

- **Проблема:** Все отзывы собраны только на `/reviews.html`. Клиент, читая страницу проекта, не видит социального доказательства именно для этого типа работ.
- **Решение:** В `projects.ini` добавить поле `reviews = ["review_id_1", "review_id_2"]` и выводить 1–2 соответствующих отзыва внизу страницы проекта.

---

## 4. Техническое обслуживание и мониторинг

### 4.1 Отправить sitemap в Google Search Console

- **Действие:** Добавить домен `vimark.art` в GSC, загрузить `sitemap.xml` и `image-sitemap.xml`.

### 4.2 Валидировать Pinterest Rich Pins через Pinterest Debugger

- **Действие:** Пройти по адресу https://developers.pinterest.com/tools/url-debugger/ для главной и нескольких проектов.

### 4.3 Настроить ежедневную проверку битых ссылок

- **Решение:** Добавить в GitHub Actions шаг с `htmlproofer` или `blc`:
  ```yaml
  - name: Check broken links
    run: |
      pip install linkchecker
      linkchecker --threads 2 --ignore-url /telegram/,/whatsapp/ https://vimark.art
  ```

### 4.4 Обновить lastmod в sitemap на основе git-лога

- **Проблема:** Сейчас `lastmod` фиксируется при генерации. При изменении подписей дата не меняется.
- **Решение:** В `generate_site.py` для каждого проекта определять дату последнего изменения папки через `git log -1 --format=%cd -- <folder>`.

---

## 5. Контрольные точки (Roadmap)

| Срок | Задача |
|------|--------|
| **Неделя 1** | Исправить количество отзывов, включить Pinterest Action |
| **Неделя 2** | Внедрить AVIF + srcset, добавить preload |
| **Неделя 3** | Автоматизировать генерацию в CI, улучшить alt-тексты |
| **Неделя 4** | Создать страницу Pricing, добавить Calendly, honeypot |
| **Месяц 2** | Настроить GSC, проверить Core Web Vitals через PageSpeed Insights |

---

## Заключение

Сайт имеет прочную основу, но требует точечных улучшений в области производительности изображений, автоматизации и доверия к данным. После реализации предложенных изменений ожидается:

- **Ускорение LCP на 30–40%**
- **Увеличение органического трафика из Google Images**
- **Повышение CTR** за счёт качественных Rich Results (Offer, AggregateRating)
- **Снижение ручной работы** при обновлении портфолио
