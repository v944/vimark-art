#!/usr/bin/env python3
"""Publish ready pins to Pinterest via API v5.

Environment variables (set via GitHub Secrets or local env):
  PINTEREST_ACCESS_TOKEN  — active access token (preferred)
  PINTEREST_REFRESH_TOKEN — refresh token (used if access token missing)
  PINTEREST_CLIENT_ID     — Pinterest App ID
  PINTEREST_CLIENT_SECRET — Pinterest App Secret

Usage:
  python pinterest_publish.py
"""
import os
import json
import sys
import datetime
from pathlib import Path

import requests

PINTEREST_API = "https://api.pinterest.com/v5"
CONFIG_PATH = Path("pinterest/config.json")
PINS_PATH = Path("pinterest/pins.json")


def get_access_token():
    """Return active access token, refreshing if necessary."""
    access_token = os.environ.get("PINTEREST_ACCESS_TOKEN", "").strip()
    if access_token:
        # Quick validation
        headers = {"Authorization": f"Bearer {access_token}"}
        resp = requests.get(f"{PINTEREST_API}/user_account", headers=headers, timeout=30)
        if resp.status_code == 200:
            return access_token
        print("Access token expired or invalid, attempting refresh...")

    refresh_token = os.environ.get("PINTEREST_REFRESH_TOKEN", "").strip()
    client_id = os.environ.get("PINTEREST_CLIENT_ID", "").strip()
    client_secret = os.environ.get("PINTEREST_CLIENT_SECRET", "").strip()

    if refresh_token and client_id and client_secret:
        resp = requests.post(
            f"{PINTEREST_API}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            new_token = data.get("access_token")
            if new_token:
                print("Successfully refreshed access token.")
                return new_token
        print(f"Token refresh failed: {resp.status_code} {resp.text}")
    return None


def get_board_id(board_name, access_token):
    """Lookup board ID by exact name via Pinterest API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["bookmark"] = cursor
        resp = requests.get(
            f"{PINTEREST_API}/boards",
            headers=headers,
            params=params,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        for b in data.get("items", []):
            if b.get("name") == board_name:
                return b.get("id")
        cursor = data.get("bookmark")
        if not cursor:
            break
    return None


def create_pin(pin, access_token, board_id):
    """Create a single pin via Pinterest API."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "title": pin["title"][:100],
        "description": pin["description"][:500],
        "link": pin["link"],
        "board_id": board_id,
        "alt_text": pin.get("alt_text", "")[:500],
        "media_source": {
            "source_type": "image_url",
            "url": pin["image_url"],
        },
    }
    return requests.post(
        f"{PINTEREST_API}/pins",
        headers=headers,
        json=payload,
        timeout=60,
    )


def main():
    if not PINS_PATH.exists():
        print("No pinterest/pins.json found. Nothing to publish.")
        return

    pins = json.loads(PINS_PATH.read_text(encoding="utf-8"))
    config = {}
    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    access_token = get_access_token()
    if not access_token:
        print("ERROR: No valid Pinterest access token available.")
        print("Set PINTEREST_ACCESS_TOKEN or PINTEREST_REFRESH_TOKEN + CLIENT_ID + CLIENT_SECRET.")
        sys.exit(1)

    mapping = config.get("board_mapping", {})
    default_board = config.get("default_board", "Maxim Mitenkov Portfolio")
    board_cache = {}
    published = 0
    failed = 0
    skipped = 0

    for pin in pins:
        status = pin.get("status", "")
        if status == "published":
            skipped += 1
            continue
        if status != "ready_to_publish":
            continue

        board_name = pin.get("board", default_board)
        # Resolve mapped name
        resolved_name = mapping.get(board_name, board_name)

        if resolved_name not in board_cache:
            board_id = get_board_id(resolved_name, access_token)
            board_cache[resolved_name] = board_id

        board_id = board_cache.get(resolved_name)
        if not board_id:
            print(f"WARNING: Board '{resolved_name}' not found. Skipping pin {pin['pin_id']}.")
            pin["status"] = "failed"
            failed += 1
            continue

        print(f"Publishing pin: {pin['pin_id']} → board '{resolved_name}' ...")
        resp = create_pin(pin, access_token, board_id)
        if resp.status_code in (200, 201):
            data = resp.json()
            pin["status"] = "published"
            pin["date_published"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            pin["pinterest_pin_id"] = data.get("id")
            published += 1
            print(f"  OK: pinterest_pin_id={data.get('id')}")
        else:
            print(f"  FAILED: HTTP {resp.status_code} — {resp.text}")
            pin["status"] = "failed"
            failed += 1

    PINS_PATH.write_text(json.dumps(pins, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSummary: {published} published, {failed} failed, {skipped} already published.")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
