"""Convert Blog markdown articles to HTML pages matching vimark.art template."""

import re
import json
import html as html_mod
from datetime import datetime
from site_frame import site_frame

SITE_URL = "https://vimark.art"
HERO_NAME = "Max Mitenkov"
HERO_NAME_RU = "Максим Митенков"

article_meta = {
    "blog_common_mistakes_bilingual": {
        "slug": "common-mistakes-when-hiring-illustrator",
        "slug_ru": "chastye-oshibki-pri-vybore-illyustratora",
        "title_en": "10 Common Mistakes Authors Make When Hiring a Book Cover Illustrator",
        "title_ru": "10 частых ошибок авторов при выборе иллюстратора обложки",
        "desc_en": "Real mistakes authors make when commissioning book cover art, with real cases and practical advice from a professional illustrator with 71 Reedsy reviews.",
        "desc_ru": "Реальные ошибки авторов при заказе обложек: реальные случаи из практики иллюстратора с 71 отзывом на Reedsy.",
        "reading_min": 10,
        "date": "2026-06-16"
    },
    "blog_from_brief_to_final_bilingual": {
        "slug": "from-brief-to-final-art-process",
        "slug_ru": "ot-brifa-do-finalnogo-arta-protsess",
        "title_en": "From Brief to Final Art: My Book Cover Design Process",
        "title_ru": "От брифа до финального арта: мой процесс создания обложки",
        "desc_en": "A complete walkthrough of my professional book cover design process, from first contact and brief to file handover. No surprises, only transparency.",
        "desc_ru": "Полная карта процесса работы над обложкой от первого сообщения до готовых файлов. Прозрачно, понятно, без сюрпризов.",
        "reading_min": 10,
        "date": "2026-06-16"
    },
    "blog_how_to_choose_illustrator_bilingual": {
        "slug": "how-to-choose-book-cover-illustrator",
        "slug_ru": "kak-vybrat-illyustratora-oblozhki",
        "title_en": "How to Choose a Book Cover Illustrator: Step-by-Step Guide",
        "title_ru": "Как выбрать иллюстратора для обложки книги: пошаговое руководство",
        "desc_en": "A step-by-step guide to choosing the right book cover illustrator, with portfolio checks, red flags, pricing breakdown, and a 10-point checklist.",
        "desc_ru": "Пошаговое руководство по выбору иллюстратора обложки: как проверять портфолио, красные флаги, разбор цен и чек-лист на 10 пунктов.",
        "reading_min": 12,
        "date": "2026-06-16"
    },
    "Cover Design Trends 2026": {
        "slug": "book-cover-design-trends-2026",
        "slug_ru": "trendy-dizaina-oblozhek-2026",
        "title_en": "Book Cover Design Trends 2026: What Publishers Look For",
        "title_ru": "Тренды дизайна обложек 2026: что ищут издательства",
        "desc_en": "Explore the top book cover design trends of 2026: naive design, tactility, bold minimalism, retro-futurism, cinematic covers, AR, and sustainability.",
        "desc_ru": "Главные тренды дизайна обложек 2026: наивный дизайн, тактильность, смелый минимализм, ретро-футуризм, кинематографичность, AR и экологичность.",
        "reading_min": 8,
        "date": "2026-06-16"
    },
    "How Much Does a Book Cover Cost": {
        "slug": "how-much-does-a-book-cover-cost",
        "slug_ru": "skolko-stoit-oblozhka-knigi",
        "title_en": "How Much Does a Book Cover Cost? (2026 Pricing Guide)",
        "title_ru": "Сколько стоит обложка книги? (гид по ценам 2026)",
        "desc_en": "A complete guide to book cover pricing in 2026: average costs by genre, what affects the price, budget vs premium tiers, and tips from a pro illustrator.",
        "desc_ru": "Полный гид по ценам на обложки книг в 2026: средняя стоимость по жанрам, что влияет на цену, бюджетный и премиум-сегменты, советы профессионала.",
        "reading_min": 8,
        "date": "2026-06-16"
    }
}

def read_md(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text

def split_bilingual(text):
    """Split bilingual markdown into RU and EN sections."""
    # Try primary markers
    ru_match = re.search(r'##\s*🇷🇺\s*(?:Русская версия|Русская)', text)
    en_match = re.search(r'##\s*🇬🇧\s*(?:English version|English)', text)
    
    # Fallback markers
    if not ru_match:
        ru_match = re.search(r'##\s*Русская версия', text)
    if not en_match:
        en_match = re.search(r'##\s*English\s*Version', text)
    
    if ru_match and en_match:
        ru_start = ru_match.start()
        en_start = en_match.start()
        if ru_start < en_start:
            ru_text = text[ru_start:en_start]
            en_text = text[en_start:]
        else:
            en_text = text[en_start:ru_start]
            ru_text = text[ru_start:]
    else:
        return None, None
    
    return ru_text, en_text

def md_to_html_simple(md):
    """Convert a subset of markdown to HTML."""
    lines = md.split('\n')
    html_lines = []
    in_list = False
    in_table = False
    table_html = ""
    in_blockquote = False
    
    for line in lines:
        stripped = line.strip()
        
        # Blockquote
        if stripped.startswith('> '):
            content = stripped[2:]
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            html_lines.append(f'<p>{inline_md(content)}</p>')
            continue
        else:
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
        
        # Headers
        if stripped.startswith('### '):
            html_lines.append(f'<h3>{inline_md(stripped[4:])}</h3>')
        elif stripped.startswith('## '):
            html_lines.append(f'<h2>{inline_md(stripped[3:])}</h2>')
        elif stripped.startswith('# '):
            html_lines.append(f'<h1>{inline_md(stripped[2:])}</h1>')
        
        # Table
        elif '|' in stripped and stripped.startswith('|'):
            parts = [p.strip() for p in stripped.split('|')[1:-1]]
            if not in_table:
                table_html = '<table>\n'
                in_table = True
            elif re.match(r'^[\s\|:\-]+$', stripped):
                continue
            else:
                if not table_html.endswith('<tr>'):
                    table_html += '<tr>'
                table_html += '<tr>' + ''.join(f'<td>{inline_md(p)}</td>' for p in parts) + '</tr>\n'
        else:
            if in_table:
                table_html += '</table>'
                html_lines.append(table_html)
                in_table = False
                table_html = ""
        
        # Horizontal rule
        if stripped == '---' and not in_table:
            html_lines.append('<hr>')
        
        # List items
        elif re.match(r'^(\d+\.|-)\s', stripped) and not in_table:
            content = re.sub(r'^\d+\.\s*|-\s*', '', stripped)
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{inline_md(content)}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
        
        # Empty line = paragraph break
        if stripped == '' and not in_list and not in_table and not in_blockquote:
            pass
        elif stripped and not in_list and not in_table and not in_blockquote and not stripped.startswith(('#', '|', '-', '>', '---')) and not re.match(r'^\d+\.', stripped):
            # Check if it's a checkbox
            if stripped.startswith('- ['):
                continue
            html_lines.append(f'<p>{inline_md(stripped)}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        table_html += '</table>'
        html_lines.append(table_html)
    if in_blockquote:
        html_lines.append('</blockquote>')
    
    return '\n'.join(html_lines)

def inline_md(text):
    """Process inline markdown: bold, italic, links."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text

def extract_checklist(md):
    """Extract checklist items from markdown."""
    items = re.findall(r'- \[(.)\] (.+)', md)
    return items

def build_article_html(md_text, lang, meta, base):
    """Build full HTML page for a blog article."""
    is_ru = lang == 'ru'
    slug = meta[f'slug_ru'] if is_ru else meta['slug']
    title = meta[f'title_ru'] if is_ru else meta['title_en']
    desc = meta[f'desc_ru'] if is_ru else meta['desc_en']
    hero = HERO_NAME_RU if is_ru else HERO_NAME
    date_pub = meta['date']
    reading = meta['reading_min']
    
    page_url = f"{SITE_URL}/{lang}/blog/{slug}.html" if is_ru else f"{SITE_URL}/blog/{slug}.html"
    alt_url = f"{SITE_URL}/ru/blog/{slug}.html" if not is_ru else f"{SITE_URL}/blog/{slug}.html"
    hreflang_en = f"{SITE_URL}/blog/{slug}.html"
    hreflang_ru = f"{SITE_URL}/ru/blog/{slug}.html"
    
    # Full blog mapping for hreflang JS
    blog_pairs = [
        ('/blog/', '/ru/blog/'),
        ('/blog/common-mistakes-when-hiring-illustrator.html', '/ru/blog/chastye-oshibki-pri-vybore-illyustratora.html'),
        ('/blog/from-brief-to-final-art-process.html', '/ru/blog/ot-brifa-do-finalnogo-arta-protsess.html'),
        ('/blog/how-to-choose-book-cover-illustrator.html', '/ru/blog/kak-vybrat-illyustratora-oblozhki.html'),
        ('/blog/book-cover-design-trends-2026.html', '/ru/blog/trendy-dizaina-oblozhek-2026.html'),
        ('/blog/how-much-does-a-book-cover-cost.html', '/ru/blog/skolko-stoit-oblozhka-knigi.html'),
    ]
    all_pairs = list(blog_pairs) + [(r, e) for e, r in blog_pairs]
    blog_map_entries = ',\n    '.join(f'"{e}":"{r}"' for e, r in all_pairs)
    
    content_html = md_to_html_simple(md_text)
    
    # Extract checklist and convert to styled HTML
    checklist_items = extract_checklist(md_text)
    checklist_html = ""
    if checklist_items:
        items_html = ''.join(f'<label class="checklist-item"><input type="checkbox"> {html_mod.escape(desc)}</label>'
                           for checked, desc in checklist_items)
        checklist_html = f'<div class="checklist">{items_html}</div>'
        content_html = re.sub(r'<ul>.*?</ul>', '', content_html, flags=re.DOTALL)
    
    # Article schema
    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {
            "@type": "Person",
            "name": hero,
            "url": f"{SITE_URL}/about.html"
        },
        "datePublished": date_pub,
        "dateModified": date_pub,
        "publisher": {
            "@type": "Organization",
            "name": "vimark",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/vimark_logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": page_url
        }
    }, ensure_ascii=False)
    
    # Generate author info line
    author_line = f'by <a href="{base}about.html">{hero}</a>'
    if is_ru:
        author_line = f'<a href="{base}about.html">{hero}</a>'
    
    lang_switch_js = f'''(function(){{var p=location.pathname.replace(/\\\\/g,"/");var h=location.hash;if(p==="/"||p==="")p="/index.html";var i=p.indexOf("/ru/")!==-1;var e=document.getElementById("lang-en");var r=document.getElementById("lang-ru");var m={{{blog_map_entries}}};if(i){{e.href=(m[p]||p.replace("/ru/","/"))+h;r.href=p+h;}}else{{r.href=(m[p]||p.replace("/blog/","/ru/blog/"))+h;e.href=p+h;}}if(i){{r.classList.add("active");}}else{{e.classList.add("active");}}}})();'''

    head_html = f'''<title>{html_mod.escape(title)} | Max Mitenkov</title>
<meta name="description" content="{html_mod.escape(desc)}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="en" href="{hreflang_en}" />
<link rel="alternate" hreflang="ru" href="{hreflang_ru}" />
<link rel="alternate" hreflang="x-default" href="{hreflang_en}" />

<meta property="og:type" content="article">
<meta property="og:url" content="{page_url}">
<meta property="og:title" content="{html_mod.escape(title)}">
<meta property="og:description" content="{html_mod.escape(desc)}">
<meta property="og:image" content="{SITE_URL}/thumbnails/STRONG/faceless2.webp">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="300">

<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="{page_url}">
<meta property="twitter:title" content="{html_mod.escape(title)}">
<meta property="twitter:description" content="{html_mod.escape(desc)}">
<meta property="twitter:site" content="@vimark_art">
<meta property="twitter:creator" content="@vimark_art">
<meta property="article:published_time" content="{date_pub}">
<meta property="article:modified_time" content="{date_pub}">

<script type="application/ld+json">
{article_schema}
</script>'''

    main_html = f'''    <article class="blog-article">
      <header class="blog-header">
        <p class="blog-meta">{date_pub} · {reading} min read</p>
        <h1>{html_mod.escape(title)}</h1>
        <p class="blog-author">{author_line}</p>
      </header>
      
      <div class="blog-content">
{content_html}
      </div>
      
      <footer class="blog-footer">
        <hr>
        <p class="blog-cta">{'Ready to discuss your project?' if not is_ru else 'Готовы обсудить ваш проект?'}</p>
        <a href="{base}contact.html" class="cta-button">{'Get a Free Quote' if not is_ru else 'Обсудить проект'}</a>
        <p class="blog-updated">{'Last updated' if not is_ru else 'Последнее обновление'}: {date_pub}</p>
      </footer>
    </article>'''

    return site_frame(base, is_ru,
        {'head': head_html, 'main': main_html},
        lang_switch_js)


def build_index_html(lang, articles, base):
    """Build blog index page listing all articles."""
    is_ru = lang == 'ru'
    title = 'Blog' if not is_ru else 'Блог'
    desc = 'Articles about book cover design, illustration process, and tips for authors' if not is_ru else 'Статьи иллюстратора о дизайне обложек книг, процессе создания и советы авторам фэнтези и sci-fi'
    
    page_url = f"{SITE_URL}/{lang}/blog/" if is_ru else f"{SITE_URL}/blog/"
    hreflang_en = f"{SITE_URL}/blog/"
    hreflang_ru = f"{SITE_URL}/ru/blog/"
    
    items = []
    for a in articles:
        slug = a['slug_ru'] if is_ru else a['slug']
        title_a = a[f'title_ru'] if is_ru else a['title_en']
        desc_a = a[f'desc_ru'] if is_ru else a['desc_en']
        items.append(f'''    <article class="blog-card">
      <h2><a href="{slug}.html">{html_mod.escape(title_a)}</a></h2>
      <p class="blog-card-meta">{a['date']} · {a['reading_min']} min</p>
      <p>{html_mod.escape(desc_a)}</p>
    </article>''')
    
    items_html = '\n'.join(items)
    
    lang_switch_js = f'''(function(){{var p=location.pathname.replace(/\\\\/g,"/");var h=location.hash;if(p==="/"||p==="")p="/index.html";var i=p.indexOf("/ru/")!==-1;var e=document.getElementById("lang-en");var r=document.getElementById("lang-ru");var m={{"{base}blog/":"{base}ru/blog/","{base}ru/blog/":"{base}blog/"}};if(i){{e.href=(m[p]||p.replace("/ru/","/"))+h;r.href=p+h;}}else{{r.href=(m[p]||p.replace("/blog/","/ru/blog/"))+h;e.href=p+h;}}if(i){{r.classList.add("active");}}else{{e.classList.add("active");}}}})();'''

    head_html = f'''<title>{title} | Max Mitenkov</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{page_url}">
<link rel="alternate" hreflang="en" href="{hreflang_en}" />
<link rel="alternate" hreflang="ru" href="{hreflang_ru}" />
<link rel="alternate" hreflang="x-default" href="{hreflang_en}" />'''

    main_html = f'''    <section class="blog-index">
      <h1>{title}</h1>
      <p class="blog-index-desc">{desc}</p>
      <div class="blog-list">
{items_html}
      </div>
    </section>'''

    return site_frame(base, is_ru,
        {'head': head_html, 'main': main_html},
        lang_switch_js)


def main():
    blog_dir = 'D:/Concept_work/Vimark_art/blog'
    out_en = 'D:/Concept_work/Vimark_art/blog'
    out_ru = 'D:/Concept_work/Vimark_art/ru/blog'
    
    files = [
        'blog_common_mistakes_bilingual.md',
        'blog_from_brief_to_final_bilingual.md',
        'blog_how_to_choose_illustrator_bilingual.md',
        'Cover Design Trends 2026.md',
        'How Much Does a Book Cover Cost.md'
    ]
    
    articles = []
    
    for fname in files:
        key = fname.replace('.md', '')
        meta = article_meta[key]
        articles.append(meta)
        
        md_text = read_md(f'{blog_dir}/{fname}')
        ru_text, en_text = split_bilingual(md_text)
        
        if ru_text and en_text:
            en_html = build_article_html(en_text, 'en', meta, '../')
            ru_html = build_article_html(ru_text, 'ru', meta, '../../')
            
            with open(f'{out_en}/{meta["slug"]}.html', 'w', encoding='utf-8') as f:
                f.write(en_html)
            with open(f'{out_ru}/{meta["slug_ru"]}.html', 'w', encoding='utf-8') as f:
                f.write(ru_html)
            
            print(f'  {meta["slug"]}.html + {meta["slug_ru"]}.html')
    
    # Generate index pages
    en_index = build_index_html('en', articles, '../')
    ru_index = build_index_html('ru', articles, '../../')
    
    with open(f'{out_en}/index.html', 'w', encoding='utf-8') as f:
        f.write(en_index)
    with open(f'{out_ru}/index.html', 'w', encoding='utf-8') as f:
        f.write(ru_index)
    
    print('  index.html + ru/blog/index.html')
    print('Done!')


if __name__ == '__main__':
    main()
