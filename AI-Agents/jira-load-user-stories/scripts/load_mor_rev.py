#!/usr/bin/env python3
"""Carga Morosidad/Reversiones desde MD validado → Jira (Fase 1 + payload Fase 2)."""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO = SCRIPT_DIR.parents[2]
sys.path.insert(0, str(SCRIPT_DIR))

from jira_rest import JiraError, JiraRest  # noqa: E402

MD_PATH = REPO / "AI-Outputs/po-expert-user-stories/po-historias-usuario-2026-08-25-morosidad-reversiones.md"
OUT_DIR = REPO / "AI-Outputs/jira-load-user-stories"
SLUG = "2026-08-26-morosidad-reversiones"
EPIC_MOR = "MAGIA-350"
EPIC_REV = "MAGIA-547"
EXCLUDE = {"T-01"}
PLACEHOLDER = "Pendiente de descripción."

HEADING_RE = re.compile(r"^### (MOR-[A-Z0-9-]+|REV-[A-Z0-9-]+) — (.+)$")
TEMP_REF_RE = re.compile(
    r"\b(MOR-HT-\d+|REV-HT-\d+|MOR-\d+|REV-\d+|T-\d+)\b"
)


def epic_for(temp_id: str) -> str:
    if temp_id.startswith("REV"):
        return EPIC_REV
    return EPIC_MOR


def issue_type_for(temp_id: str, tipo_line: str | None) -> str:
    if "HT" in temp_id or temp_id.startswith("T-"):
        return "Task"
    if tipo_line and "HT" in tipo_line:
        return "Task"
    return "Historia"


def parse_md(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?=^### (?:MOR|REV)-)", text, flags=re.MULTILINE)
    items: list[dict] = []
    for part in parts:
        m = HEADING_RE.match(part.strip().splitlines()[0] if part.strip() else "")
        if not m:
            continue
        temp_id, title = m.group(1), m.group(2).strip()
        if temp_id in EXCLUDE:
            continue
        tipo = None
        for line in part.splitlines()[:20]:
            if "**Tipo**" in line:
                tipo = line
                break
        body = extract_body(part)
        items.append(
            {
                "temp_id": temp_id,
                "summary": title,
                "issue_type": issue_type_for(temp_id, tipo),
                "epic_key": epic_for(temp_id),
                "description": body,
            }
        )

    # T-02 from section 8 (no ### heading)
    if "T-02" not in EXCLUDE:
        items.append(
            {
                "temp_id": "T-02",
                "summary": "Mock contrato API Prestamos",
                "issue_type": "Task",
                "epic_key": EPIC_MOR,
                "description": (
                    "Objetivo técnico: JSON de ejemplo alineado a MOR-HT-01 para FE/BFF/POC.\n\n"
                    "Criterios de aceptación:\n"
                    "1. Ejemplos AL_DIA y EN_MORA con diasMora\n"
                    "2. Campos documentados (estado, diasMora, fuente)\n"
                    "3. Publicado en repo o AI-Outputs\n\n"
                    "Notas / preguntas abiertas:\n"
                    "- Sustituir por contrato real Banco cuando exista"
                ),
            }
        )
    return items


def extract_body(part: str) -> str:
    lines = part.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("#### Historia") or line.startswith("#### Objetivo técnico"):
            start = i + 1
            break
    if start == 0:
        return ""
    out: list[str] = []
    skip_invest = False
    for line in lines[start:]:
        if line.startswith("### "):
            break
        if line.startswith("#### Chequeo INVEST"):
            skip_invest = True
            continue
        if skip_invest:
            if line.startswith("#### ") or line.startswith("---"):
                skip_invest = False
            else:
                continue
        if line.startswith("| | |") or line.startswith("|---|---|"):
            continue
        if line.startswith("| **Tipo**") or line.startswith("| **Épica**"):
            continue
        if re.match(r"^\| \*\*", line):
            continue
        out.append(line)
    # strip leading metadata table remnants and code fence wrappers for historia
    body = "\n".join(out).strip()
    body = re.sub(r"^```\n", "", body)
    body = re.sub(r"\n```$", "", body)
    # normalize historia block
    body = body.replace("```gherkin", "```gherkin\n").replace("```text", "```text\n")
    return body.strip()


def create_issue(client: JiraRest, item: dict) -> tuple[str, str]:
    fields = {
        "project": {"key": "MAGIA"},
        "issuetype": {"name": item["issue_type"]},
        "summary": item["summary"],
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": PLACEHOLDER}],
                }
            ],
        },
        "parent": {"key": item["epic_key"]},
        "customfield_10014": item["epic_key"],
    }
    try:
        data = client._request("POST", "/rest/api/3/issue", {"fields": fields})
        return data["key"], "ok"
    except JiraError as exc:
        fields.pop("parent", None)
        try:
            data = client._request("POST", "/rest/api/3/issue", {"fields": fields})
            return data["key"], f"ok_epic_link_only ({str(exc)[:80]})"
        except JiraError:
            raise


def replace_refs(text: str, id_map: dict[str, str]) -> str:
    def repl(match: re.Match) -> str:
        tid = match.group(1)
        return id_map.get(tid, tid)

    return TEMP_REF_RE.sub(repl, text)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    items = parse_md(MD_PATH)
    print(f"Parsed {len(items)} items from {MD_PATH.name}")

    client = JiraRest()
    id_map: dict[str, str] = {}
    create_results = []

    for i, item in enumerate(items, 1):
        tid = item["temp_id"]
        try:
            key, status = create_issue(client, item)
            id_map[tid] = key
            print(f"OK  [{i}/{len(items)}] {tid} -> {key} ({item['epic_key']}) [{status}]")
            create_results.append({**item, "issue_key": key, "fase1": status, "error": None})
        except JiraError as exc:
            print(f"FAIL [{i}/{len(items)}] {tid}: {exc}")
            create_results.append({**item, "issue_key": None, "fase1": "fail", "error": str(exc)[:500]})
        time.sleep(0.35)

    payload_issues = []
    for item in create_results:
        key = item.get("issue_key")
        if not key:
            continue
        desc = replace_refs(item["description"], id_map)
        payload_issues.append(
            {
                "issue_key": key,
                "temp_id": item["temp_id"],
                "epic_key": item["epic_key"],
                "issue_type": item["issue_type"],
                "summary": item["summary"],
                "description": desc,
            }
        )

    payload = {
        "source_md": str(MD_PATH.relative_to(REPO)).replace("\\", "/"),
        "created_at": date.today().isoformat(),
        "epics": {"MOR": EPIC_MOR, "REV": EPIC_REV},
        "excluded": sorted(EXCLUDE),
        "id_map": id_map,
        "issues": payload_issues,
    }
    payload_path = OUT_DIR / f"jira-load-{SLUG}-payload.json"
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    map_path = OUT_DIR / f"jira-load-{SLUG}-map.json"
    map_path.write_text(json.dumps({"results": create_results}, ensure_ascii=False, indent=2), encoding="utf-8")

    # report md
    report_lines = [
        f"# Jira Load — Morosidad & Reversiones ({date.today().isoformat()})",
        "",
        f"**Fuente:** `{MD_PATH.name}`",
        f"**Épicas:** Morosidad → [{EPIC_MOR}](https://bancoatlaspy.atlassian.net/browse/{EPIC_MOR}) · "
        f"Reversiones → [{EPIC_REV}](https://bancoatlaspy.atlassian.net/browse/{EPIC_REV})",
        f"**Excluido:** {', '.join(sorted(EXCLUDE))}",
        "",
        "## Mapeo temp_id → Issue Key",
        "",
        "| temp_id | Issue Key | Tipo | Épica | Fase 1 | Summary |",
        "|---------|-----------|------|-------|--------|---------|",
    ]
    for r in create_results:
        key = r.get("issue_key") or "—"
        link = f"[{key}](https://bancoatlaspy.atlassian.net/browse/{key})" if r.get("issue_key") else "—"
        report_lines.append(
            f"| {r['temp_id']} | {link} | {r['issue_type']} | {r['epic_key']} | {r['fase1']} | {r['summary'][:60]} |"
        )
    report_path = OUT_DIR / f"jira-load-{SLUG}.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    ok = sum(1 for r in create_results if r.get("issue_key"))
    print(f"\nFase 1: {ok}/{len(items)} creadas")
    print(f"Payload: {payload_path}")
    print(f"Informe: {report_path}")
    return 0 if ok == len(items) else 1


if __name__ == "__main__":
    raise SystemExit(main())
