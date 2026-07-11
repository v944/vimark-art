#!/usr/bin/env python3
"""Build data-cover-pool attributes for project cards on the home page.

Parses project pages, extracts gallery images, and injects a data-cover-pool
attribute into the matching project cards on index.html and ru/index.html.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT / "project"

# Mapping: homepage card href -> project page file name
CARD_TO_PROJECT = {
    # Book Illustrations
    "project/book-illustrations-endymion.html": "book-illustrations-endymion.html",
    "project/book-illustrations-insmoot.html": "book-illustrations-insmoot.html",
    "project/book-illustrations-nameless-city.html": "book-illustrations-nameless-city.html",
    "project/book-illustrations-planetes.html": "book-illustrations-planetes.html",
    "project/book-illustrations-creatures.html": "book-illustrations-creatures.html",
    "project/book-illustrations-20000-leagues-under-the-sea.html": "book-illustrations-20000-leagues-under-the-sea.html",
    "project/book-illustrations-vegetation.html": "book-illustrations-vegetation.html",
    "project/book-illustrations-winters-twins.html": "book-illustrations-winters-twins.html",
    # Visual Stories
    "project/comic-faceless.html": "comic-faceless.html",
    "project/comic-geologyst.html": "comic-geologyst.html",
    "project/comic-nemirum.html": "comic-nemirum.html",
    "project/comic-biological-deviations.html": "comic-biological-deviations.html",
    "project/comic-the-symbol-of-faith.html": "comic-the-symbol-of-faith.html",
    "project/comic-wanderer.html": "comic-wanderer.html",
    "project/comic-winter.html": "comic-winter.html",
}


def extract_pool(project_file: Path) -> list[dict]:
    """Extract image pool from a project page gallery."""
    soup = BeautifulSoup(project_file.read_text(encoding="utf-8"), "html.parser")
    pool = []
    for item in soup.select(".gallery-item"):
        img = item.find("img")
        if not img or not img.get("src"):
            continue
        thumb_src = img["src"]
        # Derive full-size path: thumbnails/.../file.webp -> .../file.jpg
        # Project pages use ../thumbnails/... so strip ../ and thumbnails/
        if thumb_src.startswith("../thumbnails/"):
            full_src = thumb_src.replace("../thumbnails/", "../", 1)
        elif thumb_src.startswith("thumbnails/"):
            full_src = thumb_src.replace("thumbnails/", "", 1)
        else:
            full_src = thumb_src
        # Replace .webp with .jpg for the full-size image
        full_src = re.sub(r"\.webp$", ".jpg", full_src, flags=re.IGNORECASE)
        alt = img.get("alt", "")
        pool.append({"thumb": thumb_src, "full": full_src, "alt": alt})
    return pool


def build_pools() -> dict[str, list[dict]]:
    pools = {}
    for card_href, project_name in CARD_TO_PROJECT.items():
        project_file = PROJECT_DIR / project_name
        if not project_file.exists():
            print(f"Warning: project file not found: {project_file}")
            continue
        pools[card_href] = extract_pool(project_file)
        print(f"{card_href}: {len(pools[card_href])} images")
    return pools


def to_home_paths(pool: list[dict], prefix: str = "") -> list[dict]:
    """Convert project-relative paths to homepage-relative paths."""
    result = []
    for item in pool:
        thumb = item["thumb"]
        full = item["full"]
        if thumb.startswith("../"):
            thumb = thumb[3:]
        if full.startswith("../"):
            full = full[3:]
        if prefix:
            thumb = prefix + thumb
            full = prefix + full
        result.append({"thumb": thumb, "full": full, "alt": item["alt"]})
    return result


def _find_opening_tag_end(html: str, start: int) -> int:
    """Return the index of the '>' that closes the opening tag starting at start."""
    i = start
    in_quote = None
    while i < len(html):
        ch = html[i]
        if in_quote:
            if ch == in_quote and html[i - 1] != "\\":
                in_quote = None
        elif ch in ('"', "'"):
            in_quote = ch
        elif ch == ">":
            return i
        i += 1
    return -1


def _remove_attribute(tag: str, attr_name: str) -> str:
    """Remove an attribute from an opening tag, handling unescaped quotes."""
    pattern = re.compile(
        rf"\s+{re.escape(attr_name)}=(['\"])(.*?)\\1",
        re.IGNORECASE | re.DOTALL,
    )
    # The regex above matches correctly-quoted attributes. If a malformed
    # single-quoted attribute contains a literal quote, we fall back to
    # scanning for the attribute and removing everything up to the next
    # quote followed by a space or '>'.
    new_tag, count = pattern.subn("", tag)
    if count == 0:
        # Fallback for malformed single-quoted attributes.
        start = tag.lower().find(f" {attr_name.lower()}='")
        if start == -1:
            start = tag.lower().find(f" {attr_name.lower()}=\"")
        if start != -1:
            eq = tag.find("=", start)
            quote = tag[eq + 1]
            i = eq + 2
            while i < len(tag):
                if tag[i] == quote:
                    # Check if this quote is followed by space or '>'
                    if i + 1 < len(tag) and tag[i + 1] in (" ", ">"):
                        new_tag = tag[:start] + tag[i + 1:]
                        break
                i += 1
    return new_tag


def update_index(index_path: Path, pools: dict[str, list[dict]], prefix: str = ""):
    text = index_path.read_text(encoding="utf-8")
    for card_href, pool in pools.items():
        home_pool = to_home_paths(pool, prefix)
        if len(home_pool) < 4:
            print(f"Skipping {card_href}: only {len(home_pool)} images")
            continue
        json_pool = json.dumps(home_pool, ensure_ascii=False)
        # The attribute is single-quoted, so escape any single quotes inside
        # the JSON (e.g. apostrophes in alt text) as an HTML entity.
        json_pool = json_pool.replace("'", "&#39;")

        # Find the card opening tag and add/replace data-cover-pool.
        # Russian index uses ../project/... paths.
        ru_card_href = "../" + card_href
        href_pattern = re.compile(
            rf'<a\s+[^>]*href="(?:{re.escape(card_href)}|{re.escape(ru_card_href)})"',
            re.IGNORECASE,
        )

        match = href_pattern.search(text)
        if not match:
            print(f"Warning: card not found in {index_path}: {card_href}")
            continue

        tag_start = match.start()
        tag_end = _find_opening_tag_end(text, tag_start)
        if tag_end == -1:
            print(f"Warning: could not parse opening tag for {card_href}")
            continue

        old_tag = text[tag_start:tag_end + 1]
        # Remove an existing data-cover-pool attribute (even malformed ones).
        new_tag = _remove_attribute(old_tag, "data-cover-pool")
        # Insert the new attribute just before the closing '>'.
        new_tag = new_tag[:-1] + f" data-cover-pool='{json_pool}'" + ">"

        text = text[:tag_start] + new_tag + text[tag_end + 1:]
        print(f"Updated {card_href} in {index_path}")
    index_path.write_text(text, encoding="utf-8")


def main():
    pools = build_pools()
    update_index(ROOT / "index.html", pools, prefix="")
    update_index(ROOT / "ru" / "index.html", pools, prefix="../")


if __name__ == "__main__":
    main()
