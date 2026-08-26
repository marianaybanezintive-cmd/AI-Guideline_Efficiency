"""Publica épicas y HUs de MAGIA-346/347/348/349 en Confluence.

- Épicas: actualiza páginas bajo Documentación Funcional y Documentación Técnica.
- HUs (tipo Historia, título que no empieza con QA): subpáginas solo bajo Funcional.
- Copia la descripción ADF (tablas, listas, imágenes); omite texto tachado.
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import time
import uuid
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "AI-Agents" / "sm-mass-clone" / "scripts"))
from jira_client import JiraClient, JiraError, load_user_env_fallback  # noqa: E402

SPACE_KEY = "~5ffedd6764208901414b0121"
JIRA_BROWSE = "https://bancoatlaspy.atlassian.net/browse"
STORY_TYPES = ("Historia", "Historia de Usuario", "Story")

EPICS = [
    {
        "key": "MAGIA-346",
        "title": "Confirming",
        "funcional_id": "1625687845",
        "tecnica_id": "1625688617",
        "tecnica_title": "Confirming — Técnica",
    },
    {
        "key": "MAGIA-347",
        "title": "Gestión de Facturas",
        "funcional_id": "1625687859",
        "tecnica_id": "1625688631",
        "tecnica_title": "Gestión de Facturas — Técnica",
    },
    {
        "key": "MAGIA-348",
        "title": "Simulación de Adelantos",
        "funcional_id": "1625687873",
        "tecnica_id": "1625688645",
        "tecnica_title": "Simulación de Adelantos — Técnica",
    },
    {
        "key": "MAGIA-349",
        "title": "Desembolso",
        "funcional_id": "1625687887",
        "tecnica_id": "1625688659",
        "tecnica_title": "Desembolso — Técnica",
    },
    {
        "key": "MAGIA-350",
        "title": "Morosidad",
        "funcional_id": "1625687901",
        "tecnica_id": "1625688673",
        "tecnica_title": "Morosidad — Técnica",
        "tecnica_child_types": ("Tarea", "Task"),
    },
    {
        "key": "MAGIA-547",
        "title": "Reversiones",
        "funcional_id": "1669431297",
        "tecnica_id": "1669693441",
        "tecnica_parent_id": "1625687929",
        "tecnica_title": "Reversiones — Técnica",
        "tecnica_child_types": ("Tarea", "Task"),
    },
]


def xml_esc(text: str) -> str:
    return escape(text or "", quote=True)


def has_strike(node: dict) -> bool:
    return any(m.get("type") == "strike" for m in (node.get("marks") or []))


def convert_text(node: dict) -> str:
    if has_strike(node):
        return ""
    text = xml_esc(node.get("text") or "")
    href = None
    color = None
    types = []
    for mark in node.get("marks") or []:
        mtype = mark.get("type")
        attrs = mark.get("attrs") or {}
        if mtype == "link":
            href = attrs.get("href")
        elif mtype == "textColor":
            color = attrs.get("color")
        elif mtype in {"strong", "em", "code", "underline"}:
            types.append(mtype)
    if "code" in types:
        text = f"<code>{text}</code>"
    if "strong" in types:
        text = f"<strong>{text}</strong>"
    if "em" in types:
        text = f"<em>{text}</em>"
    if "underline" in types:
        text = f"<u>{text}</u>"
    if color:
        text = f'<span style="color: {xml_esc(color)};">{text}</span>'
    if href:
        text = f'<a href="{xml_esc(href)}">{text}</a>'
    return text


def convert_nodes(nodes, media_files: list) -> str:
    if not nodes:
        return ""
    return "".join(convert_node(n, media_files) for n in nodes)


def convert_node(node, media_files: list) -> str:
    if node is None:
        return ""
    if isinstance(node, list):
        return convert_nodes(node, media_files)
    if not isinstance(node, dict):
        return xml_esc(str(node))

    ntype = node.get("type")
    attrs = node.get("attrs") or {}
    content = node.get("content")

    if ntype == "text":
        return convert_text(node)
    if ntype == "hardBreak":
        return "<br />"
    if ntype == "paragraph":
        inner = convert_nodes(content, media_files)
        return f"<p>{inner}</p>" if inner else "<p />"
    if ntype == "heading":
        level = min(max(int(attrs.get("level") or 2), 1), 6)
        inner = convert_nodes(content, media_files)
        return f"<h{level}>{inner}</h{level}>"
    if ntype == "blockquote":
        return f"<blockquote>{convert_nodes(content, media_files)}</blockquote>"
    if ntype == "rule":
        return "<hr />"
    if ntype == "bulletList":
        return f"<ul>{convert_nodes(content, media_files)}</ul>"
    if ntype == "orderedList":
        return f"<ol>{convert_nodes(content, media_files)}</ol>"
    if ntype == "listItem":
        return f"<li>{convert_nodes(content, media_files)}</li>"
    if ntype == "table":
        return f"<table><tbody>{convert_nodes(content, media_files)}</tbody></table>"
    if ntype == "tableRow":
        return f"<tr>{convert_nodes(content, media_files)}</tr>"
    if ntype in {"tableHeader", "tableCell"}:
        tag = "th" if ntype == "tableHeader" else "td"
        extra = []
        colspan = attrs.get("colspan")
        rowspan = attrs.get("rowspan")
        if colspan and int(colspan) > 1:
            extra.append(f' colspan="{int(colspan)}"')
        if rowspan and int(rowspan) > 1:
            extra.append(f' rowspan="{int(rowspan)}"')
        bg = attrs.get("background")
        if bg:
            extra.append(f' style="background-color: {xml_esc(str(bg))};"')
        return f"<{tag}{''.join(extra)}>{convert_nodes(content, media_files)}</{tag}>"
    if ntype == "codeBlock":
        lang = attrs.get("language") or ""
        code_text = "".join(
            (n.get("text") or "") if isinstance(n, dict) else str(n) for n in (content or [])
        )
        code_text = code_text.replace("]]>", "]]]]><![CDATA[>")
        lang_param = (
            f'<ac:parameter ac:name="language">{xml_esc(lang)}</ac:parameter>' if lang else ""
        )
        return (
            f'<ac:structured-macro ac:name="code">'
            f"{lang_param}"
            f"<ac:plain-text-body><![CDATA[{code_text}]]></ac:plain-text-body>"
            f"</ac:structured-macro>"
        )
    if ntype in {"mediaSingle", "mediaGroup"}:
        return convert_nodes(content, media_files)
    if ntype in {"media", "mediaInline"}:
        filename = attrs.get("alt") or f"{attrs.get('id') or 'image'}.png"
        width = attrs.get("width")
        token = f"MEDIA::{filename}::{width or ''}::{attrs.get('id') or ''}"
        media_files.append(
            {
                "filename": filename,
                "id": attrs.get("id"),
                "width": width,
                "token": token,
            }
        )
        return f"<p>__{xml_esc(token)}__</p>"
    if ntype == "inlineCard":
        url = attrs.get("url") or (attrs.get("data") or {}).get("url") or ""
        if not url:
            return ""
        return f'<a href="{xml_esc(url)}">{xml_esc(url)}</a>'
    if ntype == "emoji":
        return xml_esc(attrs.get("text") or attrs.get("shortName") or "")
    if ntype == "mention":
        return xml_esc(attrs.get("text") or "")
    if ntype == "date":
        return xml_esc(str(attrs.get("timestamp") or ""))
    if ntype == "doc":
        return convert_nodes(content, media_files)
    return convert_nodes(content, media_files)


def wrap_epic_body(issue_key: str, description_html: str) -> str:
    url = f"{JIRA_BROWSE}/{issue_key}"
    return (
        f'<p>JIRA = <a href="{xml_esc(url)}">{xml_esc(url)}</a></p>'
        f"{description_html}"
    )


def wrap_hu_body(issue_key: str, description_html: str) -> str:
    url = f"{JIRA_BROWSE}/{issue_key}"
    return (
        f'<p>JIRA: <a href="{xml_esc(url)}">{xml_esc(url)}</a></p>'
        f"<p />"
        f"{description_html}"
    )


def replace_media_tokens(html: str, uploaded: dict) -> str:
    """uploaded: token -> filename already attached on the page."""
    for token, filename in uploaded.items():
        needle = f"<p>__{xml_esc(token)}__</p>"
        width = ""
        parts = token.split("::")
        if len(parts) >= 3 and parts[2]:
            try:
                w = int(float(parts[2]))
                width = f' ac:width="{min(w, 900)}"'
            except ValueError:
                width = ""
        replacement = (
            f"<ac:image{width}><ri:attachment ri:filename=\"{xml_esc(filename)}\" /></ac:image>"
        )
        html = html.replace(needle, replacement)
    return html


def validate_storage(html: str) -> None:
    wrapped = (
        '<root xmlns:ac="http://atlassian.com/content" '
        'xmlns:ri="http://atlassian.com/resource/identifier">'
        f"{html}</root>"
    )
    ET.fromstring(wrapped)


class WikiClient:
    def __init__(self, jira: JiraClient):
        self.jira = jira
        self.base = jira.base_url
        self.headers = dict(jira._headers)
        self.headers["X-Atlassian-Token"] = "no-check"
        self.ssl = jira._ssl_context
        self.timeout = jira.timeout

    def _request(self, method: str, path: str, body=None, headers=None, raw=False):
        url = path if path.startswith("http") else f"{self.base}{path}"
        hdrs = dict(self.headers)
        if headers:
            hdrs.update(headers)
        data = None
        if body is not None and not isinstance(body, (bytes, bytearray)):
            data = json.dumps(body).encode("utf-8")
        elif isinstance(body, (bytes, bytearray)):
            data = body
        last_error = None
        for attempt in range(4):
            req = Request(url, data=data, headers=hdrs, method=method)
            try:
                with urlopen(req, timeout=self.timeout, context=self.ssl) as resp:
                    payload = resp.read()
                    if raw:
                        return resp.status, payload, resp.headers
                    if not payload:
                        return resp.status, None, resp.headers
                    return resp.status, json.loads(payload.decode("utf-8")), resp.headers
            except HTTPError as exc:
                err_body = exc.read().decode("utf-8", errors="replace")[:1200]
                if exc.code in (429,) or exc.code >= 500:
                    time.sleep(float(exc.headers.get("Retry-After") or 2 ** attempt))
                    last_error = JiraError(f"HTTP {exc.code} {method} {url}: {err_body}")
                    continue
                raise JiraError(f"HTTP {exc.code} {method} {url}: {err_body}") from exc
            except (URLError, TimeoutError) as exc:
                last_error = JiraError(f"Red {method} {url}: {exc}")
                time.sleep(2 ** attempt)
        raise last_error or JiraError(f"Fallo {method} {url}")

    def get_page(self, page_id: str) -> dict:
        _, data, _ = self._request(
            "GET",
            f"/wiki/rest/api/content/{page_id}?expand=version,space,ancestors,body.storage",
        )
        return data

    def list_children(self, page_id: str) -> list:
        results = []
        start = 0
        while True:
            _, data, _ = self._request(
                "GET",
                f"/wiki/rest/api/content/{page_id}/child/page?limit=50&start={start}",
            )
            batch = (data or {}).get("results") or []
            results.extend(batch)
            if not batch or len(batch) < 50:
                break
            start += len(batch)
        return results

    def create_page(self, title: str, parent_id: str, html: str) -> dict:
        body = {
            "type": "page",
            "title": title[:255],
            "space": {"key": SPACE_KEY},
            "ancestors": [{"id": str(parent_id)}],
            "body": {"storage": {"value": html, "representation": "storage"}},
        }
        _, data, _ = self._request("POST", "/wiki/rest/api/content", body=body)
        return data

    def update_page(self, page_id: str, title: str, html: str, version: int) -> dict:
        body = {
            "type": "page",
            "title": title[:255],
            "version": {"number": version + 1, "minorEdit": True},
            "body": {"storage": {"value": html, "representation": "storage"}},
        }
        _, data, _ = self._request("PUT", f"/wiki/rest/api/content/{page_id}", body=body)
        return data

    def delete_page(self, page_id: str) -> None:
        self._request("DELETE", f"/wiki/rest/api/content/{page_id}")

    def download_bytes(self, url: str) -> bytes:
        _, payload, _ = self._request("GET", url, raw=True)
        return payload

    def upload_attachment(self, page_id: str, filename: str, content: bytes, mime: str) -> None:
        boundary = uuid.uuid4().hex
        safe_name = filename.replace('"', "_")
        preamble = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{safe_name}"\r\n'
            f"Content-Type: {mime or 'application/octet-stream'}\r\n\r\n"
        ).encode("utf-8")
        closing = f"\r\n--{boundary}--\r\n".encode("utf-8")
        body = preamble + content + closing
        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "X-Atlassian-Token": "no-check",
        }
        try:
            self._request(
                "POST",
                f"/wiki/rest/api/content/{page_id}/child/attachment",
                body=body,
                headers=headers,
            )
        except JiraError as exc:
            if "already exists" in str(exc).lower() or "HTTP 409" in str(exc):
                return
            raise


def is_qa_title(summary: str) -> bool:
    return summary.strip().upper().startswith("QA")


def page_webui(page: dict) -> str:
    links = page.get("_links") or {}
    webui = links.get("webui") or ""
    if webui.startswith("http"):
        return webui
    return f"https://bancoatlaspy.atlassian.net/wiki{webui}"


def match_attachment(media: dict, attachments: list) -> dict | None:
    filename = media.get("filename")
    for att in attachments:
        if att.get("filename") == filename:
            return att
    if len(attachments) == 1:
        return attachments[0]
    return None


def publish_body(wiki: WikiClient, page: dict, title: str, html: str, media_files: list, attachments: list) -> dict:
    uploaded_map = {}
    if media_files:
        for media in media_files:
            att = match_attachment(media, attachments)
            if not att:
                continue
            raw = wiki.download_bytes(att["content"])
            wiki.upload_attachment(page["id"], att["filename"], raw, att.get("mimeType"))
            uploaded_map[media["token"]] = att["filename"]
        html = replace_media_tokens(html, uploaded_map)
        page = wiki.get_page(page["id"])
        wiki.update_page(page["id"], title, html, page["version"]["number"])
        return wiki.get_page(page["id"])
    return page


def upsert_page(wiki: WikiClient, parent_id: str, title: str, html: str, existing: dict | None) -> dict:
    if existing:
        current = wiki.get_page(existing["id"])
        return wiki.update_page(current["id"], title, html, current["version"]["number"])
    try:
        return wiki.create_page(title, parent_id, html)
    except JiraError as exc:
        if "already exists" not in str(exc).lower() and "HTTP 400" not in str(exc):
            raise
        fallback = f"{title[:200]}"
        raise


def publish_issues_under_parent(
    wiki: WikiClient,
    jira: JiraClient,
    epic: dict,
    parent_id: str,
    issue_types: tuple[str, ...],
    report: dict,
    report_bucket: str,
    label: str,
) -> None:
    children = wiki.list_children(parent_id)
    by_title = {c.get("title"): c for c in children}
    for child in children:
        title = child.get("title") or ""
        if is_qa_title(title):
            try:
                wiki.delete_page(child["id"])
                print(f"  DELETED QA page ({label}) {title}")
                report["deleted_qa"].append({"title": title, "id": child["id"], "parent": label})
            except Exception as exc:
                report["errors"].append(f"delete QA {title}: {exc}")

    types_jql = ", ".join(f'"{t}"' for t in issue_types)
    jql = (
        f'project = MAGIA AND (parent = {epic["key"]} OR "Epic Link" = {epic["key"]}) '
        f"AND issuetype in ({types_jql}) ORDER BY key ASC"
    )
    issues = jira.search_jql(
        jql, fields=["summary", "description", "attachment", "issuetype"], max_results=100
    )
    kept = [s for s in issues if not is_qa_title(s["fields"]["summary"])]
    print(f"  {label} a publicar: {len(kept)} (omitidas QA: {len(issues) - len(kept)})")

    used_titles = set(by_title.keys())
    for item in kept:
        key = item["key"]
        summary = item["fields"]["summary"].strip()
        title = summary[:255]
        media_files = []
        desc_html = convert_node(item["fields"].get("description"), media_files)
        html = wrap_hu_body(key, desc_html)
        try:
            validate_storage(html)
        except ET.ParseError as exc:
            report["errors"].append(f"{key} XML inválido: {exc}")
            print(f"  XML INVALID {key}: {exc}")
            continue

        existing = by_title.get(title)
        page_title = title
        try:
            if existing:
                current = wiki.get_page(existing["id"])
                page = wiki.update_page(existing["id"], page_title, html, current["version"]["number"])
                action = "updated"
            else:
                try:
                    page = wiki.create_page(page_title, parent_id, html)
                except JiraError as exc:
                    if "already exists" in str(exc).lower() or "HTTP 400" in str(exc):
                        page_title = f"{key} — {title}"[:255]
                        page = wiki.create_page(page_title, parent_id, html)
                    else:
                        raise
                action = "created"
                used_titles.add(page_title)

            attachments = item["fields"].get("attachment") or []
            if media_files:
                page = publish_body(wiki, page, page_title, html, media_files, attachments)

            url = page_webui(page)
            print(f"  {action.upper()} {key} {page_title[:70]} ({label})")
            report[report_bucket].append(
                {
                    "key": key,
                    "epic": epic["key"],
                    "title": page_title,
                    "url": url,
                    "action": action,
                    "images": len(media_files),
                    "section": label,
                }
            )
        except Exception as exc:
            print(f"  ERROR {key}: {exc}")
            report["errors"].append(f"{key}: {exc}")


def main(only_keys=None):
    load_user_env_fallback()
    jira = JiraClient()
    wiki = WikiClient(jira)
    report = {
        "epics": [],
        "stories": [],
        "tasks": [],
        "deleted_qa": [],
        "errors": [],
    }
    epics = EPICS
    if only_keys:
        wanted = {k.strip().upper() for k in only_keys}
        epics = [e for e in EPICS if e["key"] in wanted]
        if not epics:
            raise SystemExit(f"No hay épicas configuradas para: {sorted(wanted)}")

    for epic in epics:
        print(f"\n=== {epic['key']} {epic['title']} ===")
        issue = jira.get(
            f"/rest/api/3/issue/{epic['key']}",
            params={"fields": "summary,description,attachment"},
        )
        media_files = []
        desc_html = convert_node(issue["fields"].get("description"), media_files)
        html = wrap_epic_body(epic["key"], desc_html)
        try:
            validate_storage(html)
        except ET.ParseError as exc:
            report["errors"].append(f"{epic['key']} XML inválido: {exc}")
            print("XML INVALID", epic["key"], exc)
            continue

        tecnica_id = epic.get("tecnica_id")
        if not tecnica_id and epic.get("tecnica_parent_id"):
            parent_id = epic["tecnica_parent_id"]
            tecnica_title = epic["tecnica_title"]
            siblings = wiki.list_children(parent_id)
            match = next((c for c in siblings if c.get("title") == tecnica_title), None)
            if match:
                tecnica_id = match["id"]
            else:
                created = wiki.create_page(tecnica_title, parent_id, html)
                tecnica_id = created["id"]
                url = page_webui(created)
                print(f"  CREATED {tecnica_title} -> {url}")
                report["epics"].append(
                    {"key": epic["key"], "title": tecnica_title, "url": url, "action": "created"}
                )

        pages = [(epic["funcional_id"], epic["title"])]
        if tecnica_id:
            pages.append((tecnica_id, epic["tecnica_title"]))
        for page_id, title in pages:
            try:
                current = wiki.get_page(page_id)
                updated = wiki.update_page(page_id, title, html, current["version"]["number"])
                url = page_webui(updated)
                print(f"  UPDATED {title} -> {url}")
                report["epics"].append({"key": epic["key"], "title": title, "url": url, "action": "updated"})
            except Exception as exc:
                print(f"  ERROR epic page {title}: {exc}")
                report["errors"].append(f"{epic['key']} {title}: {exc}")

        publish_issues_under_parent(
            wiki,
            jira,
            epic,
            epic["funcional_id"],
            STORY_TYPES,
            report,
            "stories",
            "HUs",
        )

        child_types = epic.get("tecnica_child_types")
        if child_types and tecnica_id:
            publish_issues_under_parent(
                wiki,
                jira,
                epic,
                tecnica_id,
                child_types,
                report,
                "tasks",
                "Tareas técnicas",
            )

    suffix = "-".join(e["key"] for e in epics) if only_keys else ""
    name = f"publish-report-{suffix}.json" if suffix else "publish-report.json"
    out = Path(__file__).resolve().parent / name
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReporte: {out}")
    print(
        f"Épicas: {len(report['epics'])} | HUs: {len(report['stories'])} | "
        f"Tareas: {len(report['tasks'])} | QA borradas: {len(report['deleted_qa'])} | "
        f"Errores: {len(report['errors'])}"
    )
    if report["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--only",
        nargs="+",
        help="Claves de épica a publicar, p. ej. MAGIA-349",
    )
    args = parser.parse_args()
    main(only_keys=args.only)
