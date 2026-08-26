#!/usr/bin/env python3
"""Restaura Description en clones QA desde el issue original (ADF)."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[2]
sys.path.insert(0, str(SCRIPT_DIR))

from clone_issues import update_description  # noqa: E402
from jira_client import JiraClient, load_user_env_fallback  # noqa: E402


def main() -> int:
    load_user_env_fallback()
    last_run = REPO / "AI-Outputs/sm-mass-clone/last-run.json"
    data = json.loads(last_run.read_text(encoding="utf-8"))
    pairs = [
        (r["original_key"], r["clone_key"])
        for r in data.get("results", [])
        if r.get("ok") and r.get("clone_key")
    ]
    client = JiraClient()
    ok = fail = 0
    for orig, clone in pairs:
        try:
            issue = client.get(f"/rest/api/3/issue/{orig}", {"fields": "description"})
            desc = (issue.get("fields") or {}).get("description")
            if not desc:
                print(f"SKIP {clone}: original {orig} sin descripción")
                fail += 1
                continue
            update_description(client, clone, desc)
            print(f"OK  {clone} <- {orig}")
            ok += 1
            time.sleep(0.2)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {clone} <- {orig}: {exc}")
            fail += 1
    print(f"\nListo: {ok} ok, {fail} fail")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
