#!/usr/bin/env python3
"""Import 6th Tirumurai Tamil text from thiruarutpa.org into content/ folders."""

from __future__ import annotations

import html
import json
import re
import ssl
import time
import urllib.request
from pathlib import Path

BASE = "https://www.thiruarutpa.org"
INDEX_URL = f"{BASE}/Thirumurai/sixth/tm"
CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
CATALOG_PATH = Path(__file__).resolve().parent.parent / "catalogue.json"

INDEX_PATTERN = re.compile(
    r'<a href="(/thirumurai/v/[^"]+)">\s*([^<]+?)\s*<br />\s*'
    r'<span class="meriendaFont">([^<]+)</span>',
    re.S,
)
SUP_PATTERN = re.compile(r"<sup>[^<]*</sup>")
TAG_PATTERN = re.compile(r"<[^>]+>")


def fetch(url: str) -> str:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "6th-tirumurai-telugu-blog/1.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def slug_from_href(href: str) -> str:
    return href.rstrip("/").split("/")[-1]


def strip_tags(text: str) -> str:
    text = SUP_PATTERN.sub("", text)
    text = TAG_PATTERN.sub("", text)
    return html.unescape(text).strip()


def parse_index(page_html: str) -> list[dict]:
    items: list[dict] = []
    for number, match in enumerate(INDEX_PATTERN.finditer(page_html), start=1):
        href, title_tamil, title_roman = match.groups()
        slug = slug_from_href(href)
        items.append(
            {
                "number": number,
                "slug": slug,
                "title_tamil": strip_tags(title_tamil),
                "title_roman": strip_tags(title_roman),
                "source_url": f"{BASE}{href}",
                "folder": f"{number:03d}_{slug}",
            }
        )
    return items


def parse_hymn_body(page_html: str) -> str:
    body_match = re.search(r'<div class="arutpaLyricsBody">(.*?</ul>)', page_html, re.S)
    if not body_match:
        return ""

    body = body_match.group(1)
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.I)
    body = re.sub(r"</h5>", "\n\n", body, flags=re.I)
    body = re.sub(r"</li>", "\n\n", body, flags=re.I)
    body = strip_tags(body)

    lines: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        lines.append(line)

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def write_page(entry: dict, tamil_text: str) -> None:
    folder = CONTENT_DIR / entry["folder"]
    folder.mkdir(parents=True, exist_ok=True)

    meta = {
        "title": f"{entry['number']:03d}. {entry['title_tamil']}",
        "title_tamil": entry["title_tamil"],
        "title_roman": entry["title_roman"],
        "title_telugu": "",
        "path_number": entry["number"],
        "source_url": entry["source_url"],
        "notes": "Tamil source: thiruarutpa.org. Add Telugu pronunciation and translation.",
    }
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "tamil.md").write_text(tamil_text + ("\n" if tamil_text else ""), encoding="utf-8")

    for name, placeholder in {
        "pronunciation.md": "_Add Tamil pronunciation in Telugu script._\n",
        "telugu.md": "_Add Telugu translation._\n",
    }.items():
        path = folder / name
        if not path.exists() or path.read_text(encoding="utf-8").strip().startswith("("):
            path.write_text(placeholder, encoding="utf-8")


def main() -> None:
    print(f"Fetching index: {INDEX_URL}")
    index_html = fetch(INDEX_URL)
    catalogue = parse_index(index_html)
    print(f"Found {len(catalogue)} hymns")

    for entry in catalogue:
        folder = CONTENT_DIR / entry["folder"]
        tamil_path = folder / "tamil.md"
        if tamil_path.exists() and len(tamil_path.read_text(encoding="utf-8").strip()) > 80:
            print(f"Skip {entry['folder']} (already imported)")
            continue

        print(f"Import {entry['number']:03d}: {entry['title_tamil']}")
        page_html = fetch(entry["source_url"])
        tamil_text = parse_hymn_body(page_html)
        if not tamil_text:
            print(f"  Warning: no Tamil text parsed for {entry['source_url']}")
        write_page(entry, tamil_text)
        time.sleep(0.35)

    CATALOG_PATH.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote catalogue to {CATALOG_PATH}")


if __name__ == "__main__":
    main()
