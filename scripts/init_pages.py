#!/usr/bin/env python3
"""Create empty page folders for the 500-page book."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
TOTAL_PAGES = 500


def write_page(page_num: int) -> None:
    folder = CONTENT_DIR / f"page_{page_num:03d}"
    folder.mkdir(parents=True, exist_ok=True)

    meta = {
        "book_page": page_num,
        "title": f"Page {page_num}",
        "notes": "",
    }
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    tamil = folder / "tamil.md"
    if not tamil.exists() or tamil.read_text(encoding="utf-8").strip().startswith("_Add"):
        tamil.write_text("_Add original Tamil from the book._\n", encoding="utf-8")

    pron = folder / "pronunciation.md"
    if not pron.exists() or pron.read_text(encoding="utf-8").strip().startswith("_Add"):
        pron.write_text("_Add Tamil pronunciation in Telugu script._\n", encoding="utf-8")

    telugu = folder / "telugu.md"
    if not telugu.exists() or telugu.read_text(encoding="utf-8").strip().startswith("_Add"):
        telugu.write_text("_Add Telugu meaning._\n", encoding="utf-8")


def main() -> None:
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    template = CONTENT_DIR / "_template"
    template.mkdir(exist_ok=True)
    (template / "meta.json").write_text(
        json.dumps({"book_page": 0, "title": "Template", "notes": ""}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (template / "tamil.md").write_text("_Add original Tamil from the book._\n", encoding="utf-8")
    (template / "pronunciation.md").write_text("_Add Tamil pronunciation in Telugu script._\n", encoding="utf-8")
    (template / "telugu.md").write_text("_Add Telugu meaning._\n", encoding="utf-8")

    for page_num in range(1, TOTAL_PAGES + 1):
        write_page(page_num)

    print(f"Created {TOTAL_PAGES} pages under {CONTENT_DIR}")


if __name__ == "__main__":
    main()
