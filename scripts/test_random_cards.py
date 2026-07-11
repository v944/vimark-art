#!/usr/bin/env python3
"""Quick smoke test for homepage project-card randomization."""
import json
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PORT = 8765


def start_server():
    os.chdir(ROOT)
    server = HTTPServer(("127.0.0.1", PORT), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def run_test():
    start_server()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page_errors = []
        page.on("pageerror", lambda e: page_errors.append(str(e)))

        for lang_path in ["index.html", "ru/index.html"]:
            print(f"\nTesting {lang_path}")
            page.goto(f"http://127.0.0.1:{PORT}/{lang_path}")
            page.wait_for_timeout(1500)
            print(f"  title: {page.title()}")

            # Scroll to ensure projects are visible
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)

            cards = page.query_selector_all('#book-illustrations .projects-grid > .project-card')
            print(f"  Visible Book Illustration cards: {len(cards)}")
            for card in cards:
                href = card.get_attribute('href')
                pool_attr = card.get_attribute('data-cover-pool')
                main = card.query_selector('.project-card-main')
                main_src = main.get_attribute('src') if main else None
                print(f"    {href}: pool={bool(pool_attr)}, main_src={main_src}")
                assert pool_attr, f"Missing data-cover-pool on {href}"
                pool = json.loads(pool_attr)
                assert any(item['thumb'] == main_src for item in pool), f"main_src not in pool for {href}"

            cards = page.query_selector_all('#comic .projects-grid > .project-card')
            print(f"  Visible Visual Stories cards: {len(cards)}")
            for card in cards:
                href = card.get_attribute('href')
                pool_attr = card.get_attribute('data-cover-pool')
                main = card.query_selector('.project-card-main')
                main_src = main.get_attribute('src') if main else None
                print(f"    {href}: pool={bool(pool_attr)}, main_src={main_src}")
                assert pool_attr, f"Missing data-cover-pool on {href}"
                pool = json.loads(pool_attr)
                assert any(item['thumb'] == main_src for item in pool), f"main_src not in pool for {href}"

        browser.close()

        if page_errors:
            print(f"\n{len(page_errors)} page error(s) detected:")
            for e in page_errors:
                print(f"  - {e}")
            raise SystemExit(1)
        print("\nAll checks passed.")


if __name__ == "__main__":
    run_test()
