#!/usr/bin/env python3
"""Delete old Vercel deployments to free up Deployment Storage.

Every push to vimark.art creates a deployment of ~1.1 GB, and the free
tier keeps all of them until they are deleted. This script keeps the
newest N deployments plus the current production deployment, and
deletes the rest. Deleting old deployments never affects the live site.

Usage:
    export VERCEL_TOKEN=...   # create at https://vercel.com/account/tokens
    python scripts/cleanup_vercel_deployments.py            # dry run
    python scripts/cleanup_vercel_deployments.py --apply    # delete
    python scripts/cleanup_vercel_deployments.py --keep 5 --apply
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://api.vercel.com"


def api(method: str, path: str, token: str, params: dict | None = None) -> dict:
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300]
        raise RuntimeError(f"{method} {path} -> HTTP {exc.code}: {detail}") from None


def dep_id(dep: dict) -> str:
    return dep.get("uid") or dep.get("id") or ""


def created_ms(dep: dict) -> int:
    c = dep.get("created")
    if isinstance(c, (int, float)):
        return int(c)
    try:
        dt = datetime.fromisoformat(dep.get("createdAt", "").replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)
    except ValueError:
        return 0


def fmt_date(dep: dict) -> str:
    ms = created_ms(dep)
    if not ms:
        return "unknown date      "
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")


def find_team(token: str, slug: str | None) -> dict:
    teams = api("GET", "/v2/teams", token).get("teams", [])
    if slug:
        for t in teams:
            if slug in (t.get("slug"), t.get("name"), t.get("id")):
                return t
        sys.exit(f"Team '{slug}' not found. Available: {', '.join(t.get('slug', '?') for t in teams) or '(none)'}")
    if len(teams) == 1:
        return teams[0]
    sys.exit("Token has access to several teams; pass --team. Available: "
             + ", ".join(t.get("slug", "?") for t in teams))


def find_project(token: str, team_id: str, name: str | None) -> dict:
    projects = api("GET", "/v9/projects", token,
                   {"teamId": team_id, "limit": 100}).get("projects", [])
    if name:
        for p in projects:
            if name in (p.get("name"), p.get("id")):
                return p
        sys.exit(f"Project '{name}' not found in team. Available: "
                 + ", ".join(p.get("name", "?") for p in projects) or "(none)")
    if len(projects) == 1:
        return projects[0]
    sys.exit("Team has several projects; pass --project. Available: "
             + ", ".join(p.get("name", "?") for p in projects))


def list_deployments(token: str, team_id: str, project_id: str) -> list[dict]:
    deployments, seen, until = [], set(), None
    while True:
        params = {"teamId": team_id, "projectId": project_id, "limit": 100}
        if until is not None:
            params["until"] = until
        batch = api("GET", "/v6/deployments", token, params).get("deployments", [])
        batch = [d for d in batch if dep_id(d) not in seen]
        if not batch:
            break
        deployments.extend(batch)
        seen.update(dep_id(d) for d in batch)
        last = max(created_ms(d) for d in batch)
        if until is not None and last >= until or len(batch) < 100:
            break
        until = last
    return deployments


def delete_deployment(token: str, team_id: str, dep: dict) -> None:
    params = {"teamId": team_id}
    url = (dep.get("url") or "").removeprefix("https://").removeprefix("http://")
    if url:
        params["url"] = url
    api("DELETE", f"/v13/deployments/{dep_id(dep)}", token, params)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--token", default=os.environ.get("VERCEL_TOKEN"),
                    help="Vercel API token (or env VERCEL_TOKEN)")
    ap.add_argument("--team", help="Team slug (default: only team the token sees)")
    ap.add_argument("--project", help="Project name (default: only project in the team)")
    ap.add_argument("--keep", type=int, default=3,
                    help="How many of the newest deployments to keep (default: 3)")
    ap.add_argument("--apply", action="store_true",
                    help="Actually delete (default: dry run, deletes nothing)")
    args = ap.parse_args()

    if not args.token:
        sys.exit("No token: set VERCEL_TOKEN or pass --token "
                 "(create one at https://vercel.com/account/tokens)")

    try:
        team = find_team(args.token, args.team)
        project = find_project(args.token, team["id"], args.project)
        deployments = sorted(list_deployments(args.token, team["id"], project["id"]),
                             key=created_ms, reverse=True)
    except RuntimeError as exc:
        sys.exit(f"API error: {exc}")
    if not deployments:
        sys.exit("No deployments found.")

    protected = {dep_id(d) for d in deployments[: args.keep]}
    production = next((d for d in deployments
                       if d.get("target") == "production" and d.get("state") == "READY"), None)
    if production is not None:
        protected.add(dep_id(production))
    to_delete = [d for d in deployments if dep_id(d) not in protected]

    print(f"Team: {team.get('name') or team.get('slug')} | Project: {project.get('name')}")
    print(f"Deployments: {len(deployments)} total, "
          f"{len(deployments) - len(to_delete)} kept, {len(to_delete)} to delete\n")
    for d in deployments:
        mark = "KEEP" if dep_id(d) in protected else "DEL "
        print(f"{mark}  {fmt_date(d)}  {d.get('state', '?'):<7} "
              f"{d.get('target') or '-':<10}  {d.get('url')}")

    if not to_delete:
        print("\nNothing to delete.")
        return
    if not args.apply:
        print(f"\nDry run: re-run with --apply to delete {len(to_delete)} deployments.")
        return

    print(f"\nDeleting {len(to_delete)} deployments...")
    ok = failed = 0
    for d in to_delete:
        try:
            delete_deployment(args.token, team["id"], d)
            ok += 1
            print(f"  deleted {d.get('url')}")
        except RuntimeError as exc:
            failed += 1
            print(f"  FAILED {d.get('url')}: {exc}", file=sys.stderr)
        time.sleep(0.25)
    print(f"\nDone: {ok} deleted, {failed} failed.")


if __name__ == "__main__":
    main()
