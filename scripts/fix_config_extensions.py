#!/usr/bin/env python3
"""Fix image-path keys in generator config files after the WebP conversion.

captions.txt, display_titles.txt and art_meta.ini still reference .jpg
paths while the originals on disk are now .webp. For every key that no
longer resolves to a real file, swap its extension to the sibling file
that actually exists. Keys that already resolve are left untouched;
keys that resolve to nothing are reported and kept as-is.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = [".webp", ".jpg", ".jpeg", ".png", ".gif"]

CAPTION_FILES = [ROOT / "captions.txt", ROOT / "display_titles.txt"]
INI_FILES = [ROOT / "art_meta.ini"]


def resolve(path_str):
    """Return the on-disk path for a config key, swapping extension if needed.

    String-based suffix swap: Path.with_suffix() would mangle stems that
    contain dots (e.g. __0000_Nam1.0001.jpg)."""
    if (ROOT / path_str).exists():
        return path_str, False
    m = re.match(r"^(.*)\.(?:jpg|jpeg|png|webp|gif)$", path_str, re.IGNORECASE)
    if not m:
        return None, False
    base = m.group(1)
    for ext in EXTENSIONS:
        candidate = base + ext
        if (ROOT / candidate).exists():
            return candidate, True
    return None, False


def fix_caption_file(path):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = unresolved = 0
    out = []
    for line in lines:
        body = line.rstrip("\r\n")
        ending = line[len(body):]
        stripped = body.strip()
        if not stripped or stripped.startswith("#") or "=" not in body:
            out.append(line)
            continue
        key = body.split("=", 1)[0].strip()
        new_key, was_changed = resolve(key)
        if new_key is None:
            print(f"  UNRESOLVED: {key}")
            unresolved += 1
            out.append(line)
        elif was_changed:
            out.append(body.replace(key, new_key, 1) + ending)
            changed += 1
        else:
            out.append(line)
    path.write_text("".join(out), encoding="utf-8")
    return changed, unresolved


def fix_ini_file(path):
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = unresolved = 0
    out = []
    for line in lines:
        body = line.rstrip("\r\n")
        ending = line[len(body):]
        m = re.match(r"^\[(.+)\]$", body.strip())
        if not m:
            out.append(line)
            continue
        key = m.group(1).strip()
        new_key, was_changed = resolve(key)
        if new_key is None:
            print(f"  UNRESOLVED: [{key}]")
            unresolved += 1
            out.append(line)
        elif was_changed:
            out.append(f"[{new_key}]" + ending)
            changed += 1
        else:
            out.append(line)
    path.write_text("".join(out), encoding="utf-8")
    return changed, unresolved


def main():
    total_changed = total_unresolved = 0
    for f in CAPTION_FILES:
        print(f"{f.name}:")
        changed, unresolved = fix_caption_file(f)
        print(f"  {changed} keys re-pointed, {unresolved} unresolved")
        total_changed += changed
        total_unresolved += unresolved
    for f in INI_FILES:
        print(f"{f.name}:")
        changed, unresolved = fix_ini_file(f)
        print(f"  {changed} sections re-pointed, {unresolved} unresolved")
        total_changed += changed
        total_unresolved += unresolved
    print(f"Done: {total_changed} fixed, {total_unresolved} unresolved.")
    return 1 if total_unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
