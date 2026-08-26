#!/usr/bin/env python3
"""Clona QA para épicas Morosidad (MAGIA-350) y Reversiones (MAGIA-547)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[2]
sys.path.insert(0, str(SCRIPT_DIR))

from clone_issues import clone_one, build_clone_summary, load_config  # noqa: E402
from jira_client import JiraClient, JiraError, load_user_env_fallback, resolve_field_id  # noqa: E402
from clone_issues import build_jql, resolve_alias, SPRINT_FIELD_NAMES  # noqa: E402

CONFIG = SCRIPT_DIR.parent / "config.json"
OUT_DIR = REPO / "AI-Outputs/sm-mass-clone"
PREFIX = "QA - "
TARGET_STATUS = "Relevamiento"
RUNS = [
    ("MAGIA-350", "Historia"),
    ("MAGIA-350", "Tarea"),
    ("MAGIA-547", "Historia"),
    ("MAGIA-547", "Tarea"),
]


def find_transition_id(client: JiraClient, issue_key: str, target_status: str) -> str | None:
    trans = client.get(f"/rest/api/3/issue/{issue_key}/transitions") or {}
    target_lower = target_status.lower()
    for t in trans.get("transitions", []):
        to_name = (t.get("to") or {}).get("name") or ""
        if to_name.lower() == target_lower:
            return t["id"]
    return None


def transition_issue(client: JiraClient, issue_key: str, transition_id: str) -> None:
    client.post(f"/rest/api/3/issue/{issue_key}/transitions", {"transition": {"id": transition_id}})


def main() -> int:
    load_user_env_fallback()
    config = load_config(str(CONFIG))
    client = JiraClient()
    field_map = client.discover_fields()
    sprint_field_id = resolve_field_id(field_map, SPRINT_FIELD_NAMES)

    all_results = []
    transition_cache: dict[str, str | None] = {}

    for epic, issue_type in RUNS:
        issue_types = resolve_alias(issue_type, config.get("issue_type_aliases") or {})
        jql = build_jql(config, "epica", epic, issue_types, [TARGET_STATUS])
        issues = client.search_jql(
            jql,
            fields=["summary", "description", "status", "issuetype", "parent", "assignee", sprint_field_id or "customfield_10020"],
        )
        candidates = [
            i
            for i in issues
            if not (i.get("fields") or {}).get("summary", "").lower().startswith(PREFIX.lower())
        ]
        print(f"\n=== {epic} / {issue_type}: {len(candidates)} candidatos ===", file=sys.stderr)

        for idx, issue in enumerate(candidates, 1):
            key = issue["key"]
            print(f"[{idx}/{len(candidates)}] Clonando {key}…", file=sys.stderr)
            row = clone_one(
                client,
                config,
                issue,
                PREFIX,
                None,
                None,
                sprint_field_id,
                "backlog",
            )
            clone_key = row.get("clone_key")
            if row.get("ok") and clone_key:
                status_name = None
                try:
                    if TARGET_STATUS not in transition_cache:
                        transition_cache[TARGET_STATUS] = find_transition_id(client, clone_key, TARGET_STATUS)
                    tid = transition_cache[TARGET_STATUS]
                    if not tid:
                        # probe transitions from clone and cache by from-status
                        tid = find_transition_id(client, clone_key, TARGET_STATUS)
                        transition_cache[TARGET_STATUS] = tid
                    if tid:
                        transition_issue(client, clone_key, tid)
                        detail = client.get(f"/rest/api/3/issue/{clone_key}", {"fields": "status"})
                        status_name = (detail.get("fields") or {}).get("status", {}).get("name")
                        row["target_status"] = status_name
                    else:
                        row["target_status"] = f"WARN: sin transición a {TARGET_STATUS}"
                except JiraError as exc:
                    row["target_status"] = f"WARN: transición falló: {exc}"
            row["epic"] = epic
            row["issue_type_filter"] = issue_type
            all_results.append(row)
            time.sleep(0.25)

    ok = sum(1 for r in all_results if r.get("ok"))
    fail = len(all_results) - ok
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": False,
        "filters": {
            "epics": ["MAGIA-350", "MAGIA-547"],
            "issue_types": ["Historia", "Tarea"],
            "status": TARGET_STATUS,
            "title_prefix": PREFIX,
            "assignee": None,
            "target_status": TARGET_STATUS,
            "target_placement": "backlog",
        },
        "counts": {"ok": ok, "fail": fail, "total": len(all_results)},
        "results": all_results,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    last_run = OUT_DIR / "last-run.json"
    last_run.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = OUT_DIR / f"{stamp}-clone-report-mor-rev-qa.md"
    subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "render_report.py"), str(last_run), "-o", str(report_path)],
        check=False,
    )

    print(f"\nOK: {ok}/{len(all_results)}", file=sys.stderr)
    print(f"Report: {report_path}", file=sys.stderr)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
