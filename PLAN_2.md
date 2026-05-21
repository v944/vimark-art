# PLAN 2: Пошаговый план исправлений vimark.art

> Составлен на основе аудита ТЗ. Идём от критического к долгосрочному.

---

## 🔴 High Priority — Исправить в первую очередь

### Шаг 1. Обновить `sitemap.xml` (устаревшие URL после редизайна)

**Проблема:** В `sitemap.xml` до сих пор старые URL с `single-*`, хотя папки переименованы в `Personal`.

**Файл:** `sitemap.xml`

**Что заменить:**
```xml
<!-- Было: -->
<loc>https://vimark.art/project/single-early-work.html</loc>
<loc>https://vimark.art/project/single-professional-growth.html</loc>
<loc>https://vimark.art/project/single-recent-work.html</loc>

<!-- Стало: -->
<loc>https://vimark.art/project/personal-early-work.html</loc>
<loc>https://vimark.art/project/personal-professional-growth.html</loc>
<loc>https://vimark.art/project/personal-recent-work.html</loc>
```

**Проверка:** Открыть `https://vimark.art/sitemap.xml` в браузере и убедиться, что все 3 URL начинаются с `personal-`.

---

### Шаг 2. Исправить `image-sitemap.xml`

**Проблемы:**
1. URL с пробелами (`Book Illustrations/Winter's Twins/...`) — пробелы должны быть `%20`.
2. Дублирующиеся `<image:title>` (например, «Entrance» встречается 2 раза).
3. Двойные расширения `.jpg.jpg`.

**Файл:** `image-sitemap.xml`

**Действия:**
1. Пробелы в путях заменить на `%20` или убрать пробелы из имён папок (предпочтительнее — переименовать папки без пробелов).
2. Дубли title сделать уникальными: добавить год или номер (`Entrance #1`, `Entrance #2`).
3. Убрать двойные `.jpg.jpg` в именах файлов и в XML.

**Проверка:** Загрузить `image-sitemap.xml` в Google Search Console → Sitemaps, проверить на ошибки.

---

### Шаг 3. Добавить `loading="lazy"` на изображения галереи

**Проблема:** Все изображения на страницах загружаются сразу, даже те, что ниже первого экрана.

**Файлы:**
- `generate_site.py` — в шаблон галереи (искать `<img` в функции генерации project-страниц)
- Либо вручную во всех `project/*.html` и `index.html`

**Действие:**
Добавить атрибут `loading="lazy"` ко всем `<img>` в галереях, кроме первого изображения (hero).

**Пример:**
```html
<!-- Было -->
<img src="..." alt="...">

<!-- Стало -->
<img src="..." alt="..." loading="lazy">
```

**Примечание:** Если править `generate_site.py` — после изменений нужно перегенерировать все страницы командой:
```bash
python generate_site.py
```

**Проверка:** Lighthouse → Performance → «Defer offscreen images» должен исчезнуть.

---

### Шаг 4. Исправить «Single» → «Personal» в навигации

**Проблема:** В `contact.html` и возможно в других статичных файлах до сих пор пункт меню «Single».

**Файлы:**
- `contact.html`
- `404.html`
- Проверить `ru/index.html`

**Что заменить:**
```html
<!-- Было -->
<li><a href="index.html" data-category="single">Single</a></li>

<!-- Стало -->
<li><a href="index.html" data-category="personal">Personal</a></li>
```

**Проверка:** Открыть `https://vimark.art/contact.html` и убедиться, что в меню написано «Personal».

---

### Шаг 5. Исправить апостроф в «Winter'S Twins»

**Проблема:** В `contact.html` написано `Winter'S Twins` (апостроф после S). Правильно: `Winter’s Twins` (типографический апостроф `'` перед S).

**Файл:** `contact.html` (строка 23)

**Что заменить:**
```html
<!-- Было -->
<li><a href="..." data-subcategory="winters-twins">Winter'S Twins</a></li>

<!-- Стало -->
<li><a href="..." data-subcategory="winters-twins">Winter's Twins</a></li>
```

**Проверка:** Визуальная — текст в меню должен выглядеть корректно.

---

## 🟠 Medium Priority — Улучшит индексацию и UX

### Шаг 6. Создать landing-страницы категорий

**Проблема:** Нет отдельных URL для категорий (`/book-illustrations/`, `/comics/` и т.д.). Сейчас всё на главной со скроллом.

**Что создать:**
- `book-illustrations.html`
- `comics.html`
- `bookcover.html`
- `personal.html`

**Вариант А — через генератор:**
Добавить логику в `generate_site.py`, которая создаёт страницу-каталог для каждой верхнеуровневой папки.

**Вариант Б — вручную:**
Скопировать структуру `index.html`, оставив только одну категорию + H1 с описанием.

**SEO-требования к каждой странице:**
- Уникальный `<title>`: `Book Illustrations · Max Mitenkov`
- Уникальный `<meta name="description">`
- `<h1>` с названием категории
- BreadcrumbList (см. шаг 7)

**Проверка:**
1. Страницы открываются по URL (`/book-illustrations.html`).
2. Title и H1 уникальны.
3. Добавить URL в `sitemap.xml`.

---

### Шаг 7. Добавить хлебные крошки (BreadcrumbList) на project-страницы

**Файлы:** `project/*.html` (или шаблон в `generate_site.py`)

**Добавить в `<head>` каждой project-страницы:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://vimark.art/" },
    { "@type": "ListItem", "position": 2, "name": "Book Illustrations", "item": "https://vimark.art/#book-illustrations" },
    { "@type": "ListItem", "position": 3, "name": "Endymion", "item": "https://vimark.art/project/book-illustrations-endymion.html" }
  ]
}
</script>
```

**Проверка:** Google Rich Results Test — ввести URL страницы, убедиться что BreadcrumbList распознаётся.

---

### Шаг 8. Мобильный аудит

**Инструменты:**
- [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- Chrome DevTools → Lighthouse → Mobile
- Реальное устройство (iPhone/Samsung)

**Что проверить:**
- [ ] Меню читаемо (шрифт ≥16px)
- [ ] Нет горизонтальной прокрутки
- [ ] Кнопки/ссылки ≥44×44px для тапов
- [ ] Изображения не вылазят за экран

**Если найдены проблемы:**
- Горизонтальная прокрутка — обычно от `width: 100vw` или широких изображений. Исправить через `max-width: 100%` и `overflow-x: hidden`.
- Мелкий шрифт — увеличить в `@media (max-width: 768px)`.

---

### Шаг 9. Добавить canonical на RU-версии project-страниц

**Проблема:** RU-страницы (`ru/project/...`) должны иметь `canonical` на EN-версию или на себя + `hreflang`.

**Проверить:**
- Есть ли `<link rel="canonical">` на страницах `ru/project/*.html`?
- Есть ли `<link rel="alternate" hreflang="ru">` и `hreflang="en">`?

**Если нет — добавить в `<head>`:**
```html
<link rel="canonical" href="https://vimark.art/project/book-illustrations-endymion.html">
<link rel="alternate" hreflang="en" href="https://vimark.art/project/book-illustrations-endymion.html">
<link rel="alternate" hreflang="ru" href="https://vimark.art/ru/project/book-illustrations-endymion.html">
```

---

### Шаг 10. Добавить reCAPTCHA v3 в форму

**Файл:** `contact.html`

**Действие:**
1. Зарегистрировать сайт в [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin) (выбрать reCAPTCHA v3).
2. Получить `site key`.
3. Добавить перед закрывающим `</body>`:
```html
<script src="https://www.google.com/recaptcha/api.js?render=YOUR_SITE_KEY"></script>
<script>
  grecaptcha.ready(function() {
    grecaptcha.execute('YOUR_SITE_KEY', {action: 'submit'}).then(function(token) {
      // добавить token в форму перед отправкой
    });
  });
</script>
```
4. Либо использовать простую защиту — honeypot-поле (скрытое поле, которое боты заполнят, а люди нет).

**Проверка:** Отправить форму — сообщение должно приходить, спам должен фильтроваться.

---

## 🟡 Low Priority — Контент и аналитика (зависит от вас)

### Шаг 11. Создать страницу «Услуги и цены»

**URL:** `/prices.html` или `/services.html`

**Что указать:**
- Виды работ (обложки, иллюстрации, концепт-арт, комиксы)
- Примерные цены или диапазоны
- Сроки выполнения
- Формат исходников
- Правки (сколько включено)

**SEO:**
- Title: `Commission Prices · Max Mitenkov · Illustrator`
- Description: `Pricing for book covers, illustrations, concept art and comics. Contact for a custom quote.`

---

### Шаг 12. Добавить FAQ

**Варианты размещения:**
- На странице `/prices.html`
- На `contact.html`
- Отдельная страница `/faq.html`

**Примеры вопросов:**
- Как заказать иллюстрацию?
- Какие сроки выполнения?
- Сколько правок включено?
- В каком формате передаются исходники?
- Работаете ли вы по контракту?

**SEO:** FAQ микроразметка (`FAQPage` Schema.org) — повышает CTR в выдаче.

---

### Шаг 13. Написать 2–3 кейса

**Структура кейса:**
1. Задача клиента (что нужно было нарисовать)
2. Референсы и эскизы
3. Процесс работы
4. Финальный результат
5. Отзыв клиента (если есть)

**URL:** `/case/endymion.html` или раздел на главной.

**Цель:** Уникальный контент для индексации + повышение доверия.

---

### Шаг 14. Собрать 3–5 отзывов

**Что нужно:**
- Текст отзыва
- Имя клиента / компания
- Ссылка на проект (если публичный)
- Фото работы

**Размещение:**
- Блок на главной
- Отдельная страница `/testimonials.html`
- Schema.org `Review` + `AggregateRating`

---

### Шаг 15. Подключить Google Search Console и Яндекс.Вебмастер

**Google Search Console:**
1. Перейти на [search.google.com/search-console](https://search.google.com/search-console)
2. Добавить свойство `vimark.art`
3. Подтвердить через:
   - HTML-файл (загрузить в корень)
   - HTML-тег (добавить `<meta name="google-site-verification" content="...">` в `<head>`)
   - DNS-запись
4. Отправить `sitemap.xml`

**Яндекс.Вебмастер:**
1. [webmaster.yandex.ru](https://webmaster.yandex.ru)
2. Аналогично — подтвердить владение и отправить sitemap.

**Проверка:** Через 3–7 дней в панелях появятся данные об индексации.

---

### Шаг 16. Блог / статьи (долгосрочно)

**Идеи статей:**
- «How to commission a book illustration: a client's guide»
- «Concept art pipeline for indie games»
- «Cover design process: from sketch to final»

**URL:** `/blog/commission-guide.html`

**Цель:** Привлечь трафик по низкочастотным запросам.

---

## 📋 Отложенные задачи (делать позже или по необходимости)

| Задача | Почему отложена |
|--------|-----------------|
| Конвертация всех изображений в WebP | Требует обновления `generate_site.py`, генерации WebP-копий и изменения HTML. Большой объём. |
| Минификация CSS/JS | Vercel уже сжимает статику (gzip/brotli). Ручная минификация даст <5% прироста. |
| Расширенная Schema.org (ImageObject, CreativeWork) | Полезно, но не критично. Можно добавить при обновлении генератора. |
| Поддомен `en.vimark.art` | Текущая структура `/ru/` + hreflang уже корректна. Переезд на поддомен создаст лишние риски. |

---

## ✅ Чек-лист завершения High Priority

- [ ] `sitemap.xml` обновлён (`single-*` → `personal-*`)
- [ ] `image-sitemap.xml` без пробелов и дублей
- [ ] `loading="lazy"` на всех изображениях галереи
- [ ] «Single» исправлено на «Personal» в навигации
- [ ] Апостроф в «Winter's Twins» исправлен

После выполнения High Priority можно деплоить на Vercel и проверить через [Google Search Console](https://search.google.com/search-console) + [PageSpeed Insights](https://pagespeed.web.dev/).
