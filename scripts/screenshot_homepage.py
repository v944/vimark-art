#!/usr/bin/env python3
"""Take a screenshot of the homepage showing the randomized cards."""
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PORT = 8767


def start_server():
    os.chdir(ROOT)
    server = HTTPServer(("127.0.0.1", PORT), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main():
    start_server()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1200})
        page.goto(f"http://127.0.0.1:{PORT}/index.html")
        page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, document.getElementById('book-illustrations').offsetTop - 80)")
        page.wait_for_timeout(500)
        screenshot_path = ROOT / "homepage_random_cards.png"
        page.screenshot(path=str(screenshot_path), full_page=False)
        browser.close()
        print(screenshot_path)


if __name__ == "__main__":
    main()
