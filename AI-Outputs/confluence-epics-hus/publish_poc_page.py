"""Publica el resumen funcional de la POC en Confluence (página 1664876548).

El MCP de Confluence limita `content` a 1000 caracteres; este script usa la API REST.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "AI-Agents" / "sm-mass-clone" / "scripts"))
from jira_client import JiraClient, load_user_env_fallback  # noqa: E402

from publish_pages import WikiClient, validate_storage  # noqa: E402

PAGE_ID = "1664876548"
TITLE = "POC - Atlas Trade"
MD_PATH = Path(__file__).with_name("poc-atlas-trade-resumen-funcional.md")


def inline_md(text: str) -> str:
    links: list[tuple[str, str]] = []

    def _hold_link(match: re.Match) -> str:
        links.append((match.group(1), match.group(2)))
        return f"@@LINK{len(links) - 1}@@"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _hold_link, text)
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    for idx, (label, url) in enumerate(links):
        text = text.replace(
            f"@@LINK{idx}@@",
            f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>',
        )
    return text


def cell_html(text: str, header: bool) -> str:
    tag = "th" if header else "td"
    inner = inline_md(text.strip()) or "&nbsp;"
    return f"<{tag}><p>{inner}</p></{tag}>"


def convert_markdown(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    def flush_para(buf: list[str]) -> None:
        if not buf:
            return
        cleaned = [s.strip() for s in buf if s.strip()]
        if cleaned and all(re.match(r"^\*\*[^*]+:\*\*", s) for s in cleaned):
            for s in cleaned:
                out.append(f"<p>{inline_md(s)}</p>")
            buf.clear()
            return
        para = " ".join(cleaned)
        if para:
            out.append(f"<p>{inline_md(para)}</p>")
        buf.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            out.append("<hr />")
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            level = min(len(heading.group(1)), 6)
            out.append(f"<h{level}>{inline_md(heading.group(2))}</h{level}>")
            i += 1
            continue

        if stripped.startswith("```"):
            fence = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                fence.append(html.escape(lines[i]))
                i += 1
            if i < n:
                i += 1
            out.append(f"<pre><code>{chr(10).join(fence)}</code></pre>")
            continue

        if stripped.startswith("> "):
            quote_lines = []
            while i < n and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            inner = " ".join(quote_lines)
            out.append(
                '<ac:structured-macro ac:name="info" ac:schema-version="1">'
                f"<ac:rich-text-body><p>{inline_md(inner)}</p></ac:rich-text-body>"
                "</ac:structured-macro>"
            )
            continue

        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|?\s*-+", lines[i + 1].strip()):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                if re.match(r"^\|?\s*-+", row):
                    i += 1
                    continue
                cells = [c.strip() for c in row.strip("|").split("|")]
                rows.append(cells)
                i += 1
            if rows:
                header, *body = rows
                thead = "<tr>" + "".join(cell_html(c, True) for c in header) + "</tr>"
                tbody = "".join(
                    "<tr>" + "".join(cell_html(c, False) for c in row) + "</tr>" for row in body
                )
                out.append(
                    '<table data-layout="wide"><colgroup></colgroup>'
                    f"<thead>{thead}</thead><tbody>{tbody}</tbody></table>"
                )
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < n and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(lines[i].strip()[2:])
                i += 1
                while i < n and lines[i].startswith("   ") and lines[i].strip().startswith("- "):
                    items[-1] += " " + lines[i].strip()[2:]
                    i += 1
            lis = "".join(f"<li>{inline_md(item)}</li>" for item in items)
            out.append(f"<ul>{lis}</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            lis = "".join(f"<li>{inline_md(item)}</li>" for item in items)
            out.append(f"<ol>{lis}</ol>")
            continue

        buf = [stripped]
        i += 1
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            if (
                not ns
                or ns == "---"
                or ns.startswith("#")
                or ns.startswith("> ")
                or ns.startswith("|")
                or ns.startswith("- ")
                or ns.startswith("* ")
                or ns.startswith("```")
                or re.match(r"^\d+\.\s+", ns)
            ):
                break
            buf.append(ns)
            i += 1
        flush_para(buf)

    return "".join(out)


def main() -> None:
    load_user_env_fallback()
    md = MD_PATH.read_text(encoding="utf-8")
    storage = convert_markdown(md)
    validate_storage(storage)

    jira = JiraClient()
    wiki = WikiClient(jira)
    current = wiki.get_page(PAGE_ID)
    version = current["version"]["number"]
    updated = wiki.update_page(PAGE_ID, TITLE, storage, version)
    webui = updated.get("_links", {}).get("webui", "")
    print(f"OK página {PAGE_ID} v{updated['version']['number']}")
    print(f"https://bancoatlaspy.atlassian.net/wiki{webui}")


if __name__ == "__main__":
    main()
