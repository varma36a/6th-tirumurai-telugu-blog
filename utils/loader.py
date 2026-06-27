"""Load book page content from the content/ folder."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
PLACEHOLDER_PREFIX = "_Add "


@dataclass(frozen=True)
class PageMeta:
    id: str
    title: str
    book_page: int
    notes: str = ""


@dataclass(frozen=True)
class PageContent:
    meta: PageMeta
    tamil: str
    pronunciation: str
    telugu: str
    folder: Path


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _load_meta(page_dir: Path) -> PageMeta:
    data = json.loads((page_dir / "meta.json").read_text(encoding="utf-8"))
    return PageMeta(
        id=page_dir.name,
        title=data.get("title", page_dir.name),
        book_page=int(data["book_page"]),
        notes=data.get("notes", ""),
    )


def list_pages() -> list[PageMeta]:
    pages: list[PageMeta] = []
    if not CONTENT_DIR.exists():
        return pages

    for page_dir in CONTENT_DIR.iterdir():
        if not page_dir.is_dir() or page_dir.name.startswith("_"):
            continue
        if not (page_dir / "meta.json").exists():
            continue
        pages.append(_load_meta(page_dir))

    pages.sort(key=lambda p: p.book_page)
    return pages


def load_page(page_id: str) -> PageContent | None:
    page_dir = CONTENT_DIR / page_id
    if not page_dir.is_dir() or not (page_dir / "meta.json").exists():
        return None

    return PageContent(
        meta=_load_meta(page_dir),
        tamil=_read_text(page_dir / "tamil.md"),
        pronunciation=_read_text(page_dir / "pronunciation.md"),
        telugu=_read_text(page_dir / "telugu.md"),
        folder=page_dir,
    )


def is_filled(text: str) -> bool:
    text = text.strip()
    return bool(text) and not text.startswith(PLACEHOLDER_PREFIX)
