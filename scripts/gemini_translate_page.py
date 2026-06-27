#!/usr/bin/env python3
"""Generate Telugu pronunciation + translation for a content page using Google Gemini."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

PROMPT = """You are helping translate 6th Tirumurai (Thirunavukkarasar / Appar) hymns for Telugu readers.

Given Tamil hymn text, produce TWO outputs:

1. **Pronunciation**: Write how to pronounce the Tamil lines using Telugu script (తెలుగు లిపి). Keep the same line breaks and verse structure as the Tamil source. Do NOT translate meaning here — only represent Tamil sounds in Telugu letters.

2. **Telugu**: Provide a clear, devotional Telugu translation/meaning. Preserve verse numbers, section headers (temple name, meter names), and line breaks matching the Tamil structure.

Rules:
- Keep headers like temple names and meter names translated naturally to Telugu
- Preserve numbered verses (1., 2., etc.)
- Output plain markdown only — no code fences, no JSON
- Use respectful devotional tone

Format your response EXACTLY like this:

===PRONUNCIATION===
(pronunciation content here)

===TELUGU===
(telugu translation here)

Tamil source:
"""


def call_gemini(tamil_text: str, api_key: str, model: str = "gemini-2.0-flash") -> tuple[str, str]:
    try:
        from google import genai
    except ImportError as exc:
        raise SystemExit("Install google-genai: pip install google-genai") from exc

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=PROMPT + tamil_text,
    )
    text = response.text or ""
    if "===PRONUNCIATION===" not in text or "===TELUGU===" not in text:
        raise ValueError("Unexpected Gemini response format")

    _, rest = text.split("===PRONUNCIATION===", 1)
    pronunciation, telugu = rest.split("===TELUGU===", 1)
    return pronunciation.strip(), telugu.strip()


def translate_page(folder_name: str, api_key: str, force: bool = False) -> None:
    page_dir = CONTENT_DIR / folder_name
    tamil_path = page_dir / "tamil.md"
    if not tamil_path.exists():
        raise SystemExit(f"Missing {tamil_path}")

    tamil_text = tamil_path.read_text(encoding="utf-8").strip()
    if not tamil_text:
        raise SystemExit(f"No Tamil text in {folder_name}")

    pron_path = page_dir / "pronunciation.md"
    telugu_path = page_dir / "telugu.md"
    if not force and pron_path.exists():
        existing = pron_path.read_text(encoding="utf-8").strip()
        if existing and not existing.startswith("_Add"):
            print(f"Skip {folder_name} (pronunciation already filled; use --force)")
            return

    print(f"Translating {folder_name} via Gemini...")
    pronunciation, telugu = call_gemini(tamil_text, api_key)
    pron_path.write_text(pronunciation + "\n", encoding="utf-8")
    telugu_path.write_text(telugu + "\n", encoding="utf-8")
    print(f"  Wrote {pron_path.name} and {telugu_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gemini Telugu translation for one Tirumurai page")
    parser.add_argument("folders", nargs="+", help="Content folder names, e.g. 001_parasiva_vanakkam")
    parser.add_argument("--force", action="store_true", help="Overwrite existing translations")
    parser.add_argument("--model", default="gemini-2.0-flash")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable")

    for folder in args.folders:
        translate_page(folder, api_key, force=args.force)


if __name__ == "__main__":
    main()
