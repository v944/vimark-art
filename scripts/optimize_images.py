#!/usr/bin/env python3
"""Convert full-size JPG/PNG to WebP and rewrite site references.

The lightboxes use full-size originals (up to ~6400 px, ~950 MB total),
while the site never displays more than ~2560 px. This script backs the
originals up outside the repo, converts them to WebP (q90, max edge
2560), generates small JPEG previews for og:image, rewrites references
in html/css/js/xml, and removes the originals from the working tree.

Usage:
    python scripts/optimize_images.py            # dry run: full report, no writes
    python scripts/optimize_images.py --apply    # backup + convert + rewrite + delete
    python scripts/optimize_images.py --verify   # check every local image reference
"""
from __future__ import annotations

import argparse
import io
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
BACKUP = Path(r"D:\Concept_work\Vimark_art_originals")
SITE = "https://vimark.art/"
MAX_EDGE = 2560
OG_EDGE = 1200
MIN_SIZE = 100 * 1024
EXCLUDE_PREFIXES = ("thumbnails/", "HERO/", "__UE_web/", "Reedsy/")
EXCLUDE_FILES = {"icon-192.png", "icon-512.png", "favicon.png"}
EXT_PATTERNS = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG")
TEXT_GLOBS = ("*.html", "*.css", "*.js", "*.xml")

OG_RES = [
    re.compile(r'property="og:image"[^>]*?content="([^"]+)"'),
    re.compile(r'content="([^"]+)"[^>]*?property="og:image"'),
]
OG_TAG_RE = re.compile(r'<meta[^>]*og:image[^>]*>')
CONTENT_RE = re.compile(r'content="([^"]+)"')
REF_RES = [
    re.compile(r'(?:src|href|data-full|data-src)="([^"]+\.(?:jpg|jpeg|png|webp|gif))"', re.I),
    re.compile(r'url\(["\']?([^"\')]+\.(?:jpg|jpeg|png|webp))["\']?\)', re.I),
]


def tracked_images() -> list[Path]:
    res = subprocess.run(["git", "ls-files", "-z", *EXT_PATTERNS],
                         capture_output=True, check=True, cwd=ROOT)
    out = []
    for s in res.stdout.decode().split("\0"):
        if not s or s.startswith(EXCLUDE_PREFIXES) or s in EXCLUDE_FILES:
            continue
        f = ROOT / s
        if f.is_file() and f.stat().st_size > MIN_SIZE:
            out.append(Path(s))
    return out


def ext_case_variants(p: str) -> set[str]:
    stem, _, ext = p.rpartition(".")
    return {p, f"{stem}.{ext.swapcase()}"}


def ref_variants(rel: str) -> set[str]:
    variants = set()
    for v in ext_case_variants(rel):
        variants.add(v)
        variants.add(urllib.parse.quote(v))
        variants.add(SITE + v)
        variants.add(SITE + urllib.parse.quote(v))
    return variants


def build_mapping(pairs: list[tuple[str, str]]) -> dict[str, str]:
    mapping = {}
    for old_rel, new_rel in pairs:
        for variant in ref_variants(old_rel):
            mapping[variant] = replacement(variant, new_rel)
    return mapping


def replacement(variant: str, new_rel: str) -> str:
    prefix = ""
    body = variant
    if variant.startswith(SITE):
        prefix, body = SITE, variant[len(SITE):]
    return prefix + (urllib.parse.quote(new_rel) if "%" in body else new_rel)


def load_prepared(path: Path) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    if max(img.size) > MAX_EDGE:
        scale = MAX_EDGE / max(img.size)
        img = img.resize((round(img.size[0] * scale), round(img.size[1] * scale)),
                         Image.LANCZOS)
    return img


def has_alpha(img: Image.Image) -> bool:
    return img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)


def encode_webp(img: Image.Image) -> bytes:
    if has_alpha(img):
        if img.mode == "P":
            img = img.convert("RGBA")
        buf_l, buf_q = io.BytesIO(), io.BytesIO()
        img.save(buf_l, "WEBP", lossless=True, method=6)
        img.save(buf_q, "WEBP", quality=90, method=6)
        return buf_l.getvalue() if buf_l.tell() <= buf_q.tell() else buf_q.getvalue()
    if img.mode != "RGB":
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=90, method=6)
    return buf.getvalue()


def encode_og(path: Path) -> bytes:
    img = ImageOps.exif_transpose(Image.open(path))
    if max(img.size) > OG_EDGE:
        scale = OG_EDGE / max(img.size)
        img = img.resize((round(img.size[0] * scale), round(img.size[1] * scale)),
                         Image.LANCZOS)
    if img.mode != "RGB":
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return buf.getvalue()


def collect_og_targets() -> set[str]:
    """Repo-relative paths referenced by og:image (converted or not)."""
    targets = set()
    for f in ROOT.rglob("*.html"):
        if ".git" in f.parts:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        for rx in OG_RES:
            for url in rx.findall(text):
                if url.startswith(SITE):
                    rel = url[len(SITE):]
                elif url.startswith("/"):
                    rel = url[1:]
                elif url.startswith("http"):
                    continue
                else:
                    rel = (f.parent.relative_to(ROOT) / urllib.parse.unquote(url)).as_posix()
                targets.add(urllib.parse.unquote(rel))
    return targets


def cmd_dry_run() -> None:
    images = tracked_images()
    total_old = sum((ROOT / p).stat().st_size for p in images)
    total_new = 0
    rows = []
    for rel in images:
        old = (ROOT / rel).stat().st_size
        try:
            webp = encode_webp(load_prepared(ROOT / rel))
        except Exception as exc:
            print(f"  ERROR {rel}: {exc}")
            continue
        total_new += len(webp)
        rows.append((old, len(webp), rel.as_posix()))
    rows.sort(reverse=True)
    print(f"Files to convert: {len(rows)} (threshold {MIN_SIZE // 1024} KB)")
    for old, new, name in rows[:15]:
        print(f"  {old / 1048576:7.1f} -> {new / 1024:7.0f} KB  {name}")
    if len(rows) > 15:
        print(f"  ... and {len(rows) - 15} more")
    print(f"\nTotal: {total_old / 1048576:.0f} MB -> {total_new / 1048576:.0f} MB "
          f"(saves {(total_old - total_new) / 1048576:.0f} MB)")


def rewrite_text(text: str, og_map: dict[str, str], conv_map: dict[str, str]) -> str:
    def sub_og(m: re.Match) -> str:
        tag = m.group(0)
        for old_rel, new_rel in og_map.items():
            for variant in ref_variants(old_rel):
                if variant in tag:
                    tag = tag.replace(variant, replacement(variant, new_rel))
        return tag

    text = OG_TAG_RE.sub(sub_og, text)
    mapping = build_mapping(list(conv_map.items()))
    for old, new in mapping.items():
        if old in text:
            text = text.replace(old, new)
    return text


def cmd_apply() -> None:
    images = tracked_images()
    if not images:
        sys.exit("Nothing to convert.")

    conflicts = []
    for rel in images:
        dst = BACKUP / rel
        if dst.exists() and dst.stat().st_size != (ROOT / rel).stat().st_size:
            conflicts.append(rel.as_posix())
    if conflicts:
        sys.exit("Backup conflicts (file exists with different size):\n  "
                 + "\n  ".join(conflicts))

    print(f"Backing up {len(images)} originals to {BACKUP} ...")
    for rel in images:
        dst = BACKUP / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copy2(ROOT / rel, dst)

    og_targets = collect_og_targets()
    conv_map: dict[str, str] = {}
    og_map: dict[str, str] = {}
    total_old = total_new = 0
    print("Converting ...")
    for rel in images:
        src = ROOT / rel
        old = src.stat().st_size
        stem = rel.as_posix().rpartition(".")[0]
        new_rel = f"{stem}.webp"
        try:
            (ROOT / new_rel).write_bytes(encode_webp(load_prepared(src)))
            if rel.as_posix() in og_targets:
                og_rel = f"{stem}.og.jpg"
                (ROOT / og_rel).write_bytes(encode_og(src))
                og_map[rel.as_posix()] = og_rel
        except Exception as exc:
            print(f"  FAILED {rel}: {exc}")
            continue
        new = (ROOT / new_rel).stat().st_size
        total_old += old
        total_new += new
        conv_map[rel.as_posix()] = new_rel
        print(f"  {rel.as_posix()}: {old / 1048576:.1f} -> {new / 1024:.0f} KB")

    print("Rewriting references ...")
    changed = []
    for glob in TEXT_GLOBS:
        for f in ROOT.rglob(glob):
            if ".git" in f.parts:
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            new_text = rewrite_text(text, og_map, conv_map)
            if new_text != text:
                f.write_text(new_text, encoding="utf-8", newline="")
                changed.append(f.relative_to(ROOT).as_posix())
    print(f"  {len(changed)} files updated")

    print("Removing originals ...")
    for rel in conv_map:
        (ROOT / rel).unlink()
    print(f"\nDone: {len(conv_map)} converted, "
          f"{total_old / 1048576:.0f} MB -> {total_new / 1048576:.0f} MB, "
          f"{len(og_map)} og previews, {len(changed)} refs files.")


def cmd_rewrite_only() -> None:
    """Rewrite refs and drop originals; reuse already-encoded .webp/.og.jpg."""
    images = tracked_images()
    og_targets = collect_og_targets()
    conv_map: dict[str, str] = {}
    og_map: dict[str, str] = {}
    for rel in images:
        stem = rel.as_posix().rpartition(".")[0]
        new_rel = f"{stem}.webp"
        if not (ROOT / new_rel).is_file():
            (ROOT / new_rel).write_bytes(encode_webp(load_prepared(ROOT / rel)))
        conv_map[rel.as_posix()] = new_rel
        if rel.as_posix() in og_targets:
            og_rel = f"{stem}.og.jpg"
            if not (ROOT / og_rel).is_file():
                (ROOT / og_rel).write_bytes(encode_og(ROOT / rel))
            og_map[rel.as_posix()] = og_rel

    changed = []
    for glob in TEXT_GLOBS:
        for f in ROOT.rglob(glob):
            if ".git" in f.parts:
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            new_text = rewrite_text(text, og_map, conv_map)
            if new_text != text:
                f.write_text(new_text, encoding="utf-8", newline="")
                changed.append(f.relative_to(ROOT).as_posix())
    for rel in conv_map:
        (ROOT / rel).unlink()
    print(f"rewrite-only: {len(conv_map)} originals removed, "
          f"{len(og_map)} og refs, {len(changed)} files updated.")


def cmd_verify() -> int:
    actual = {}
    for pat in (*EXT_PATTERNS, "*.webp", "*.WEBP", "*.gif"):
        for f in ROOT.rglob(pat):
            if ".git" in f.parts:
                continue
            rel = f.relative_to(ROOT).as_posix()
            actual[rel.lower()] = rel

    missing, badcase, checked = set(), set(), 0

    def check(f: Path, url: str) -> None:
        nonlocal checked
        root_absolute = url.startswith("/") or url.startswith(SITE)
        if url.startswith(("http", "data:", "mailto:", "//")) and not url.startswith(SITE):
            return
        if url.startswith(SITE):
            url = url[len(SITE):]
        url = urllib.parse.unquote(url).lstrip("/")
        if not url or not re.search(r"[a-zA-Z]", url) or " " in url or "," in url:
            return
        rel = url if root_absolute else (f.parent.relative_to(ROOT) / url).as_posix()
        parts = []
        for part in Path(rel).parts:
            if part == ".." and parts:
                parts.pop()
            elif part != ".":
                parts.append(part)
        rel = Path(*parts).as_posix() if parts else rel
        checked += 1
        hit = actual.get(rel.lower())
        if hit is None:
            missing.add(f"{f.relative_to(ROOT).as_posix()} -> {url}")
        elif hit != rel:
            badcase.add(f"{f.relative_to(ROOT).as_posix()} -> {url} (actual: {hit})")

    for glob in TEXT_GLOBS:
        for f in ROOT.rglob(glob):
            if ".git" in f.parts:
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            for rx in REF_RES:
                for url in rx.findall(text):
                    check(f, url)
            for tag in OG_TAG_RE.findall(text):
                if 'property="og:image"' not in tag:
                    continue  # skip og:image:width/height and similar
                m = CONTENT_RE.search(tag)
                if m:
                    check(f, m.group(1))

    print(f"Checked {checked} local image references.")
    for m in sorted(missing):
        print(f"  MISSING  {m}")
    for b in sorted(badcase):
        print(f"  CASE     {b}")
    if not missing and not badcase:
        print("All references resolve.")
        return 0
    return 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true")
    g.add_argument("--rewrite-only", action="store_true")
    g.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    if args.apply:
        cmd_apply()
    elif args.rewrite_only:
        cmd_rewrite_only()
    elif args.verify:
        sys.exit(cmd_verify())
    else:
        cmd_dry_run()


if __name__ == "__main__":
    main()
