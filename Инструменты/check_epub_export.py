#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
EPUB_DIR = BOOK_ROOT / "Экспорт" / "epub"
EPUB_PATH = EPUB_DIR / "Когнитивное инженерство.epub"
SOURCE_PATH = EPUB_DIR / "Когнитивное инженерство - epub source.md"
MANIFEST_PATH = EPUB_DIR / "epub-build-manifest.json"


def fail(message: str) -> int:
    print(f"epub export check failed: {message}", file=sys.stderr)
    return 1


def main() -> int:
    if not EPUB_PATH.exists():
        return fail(f"missing EPUB: {EPUB_PATH}")
    if not SOURCE_PATH.exists():
        return fail(f"missing EPUB source markdown: {SOURCE_PATH}")
    if not MANIFEST_PATH.exists():
        return fail(f"missing build manifest: {MANIFEST_PATH}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_diagrams = int(manifest.get("diagram_count", -1))
    if expected_diagrams <= 0:
        return fail("manifest has no rendered diagrams")

    source = SOURCE_PATH.read_text(encoding="utf-8")
    if re.search(r"(?m)^```mermaid|^~~~mermaid", source):
        return fail("EPUB source still contains raw mermaid fences")
    image_refs = re.findall(r"!\[[^\]]+\]\(assets/diagrams/diagram-[^)]+\.png\)", source)
    if len(image_refs) != expected_diagrams:
        return fail(f"expected {expected_diagrams} diagram image refs, found {len(image_refs)}")

    with zipfile.ZipFile(EPUB_PATH) as archive:
        names = archive.namelist()
        png_images = [name for name in names if name.lower().endswith(".png")]
        if len(png_images) != expected_diagrams:
            return fail(f"expected {expected_diagrams} PNG diagram images in EPUB, found {len(png_images)}")

        xhtml_names = [name for name in names if name.endswith((".xhtml", ".html"))]
        if not xhtml_names:
            return fail("EPUB contains no XHTML/HTML content")

        html_blob = "\n".join(
            archive.read(name).decode("utf-8", errors="replace")
            for name in xhtml_names
        )
        forbidden = [
            ("raw mermaid text", r"```mermaid|~~~mermaid"),
            ("Obsidian wikilink", r"\[\["),
            ("local vault path", r"/home/asukh|Прооекты/"),
            ("reader source status", r"ready-for-review|source packet|Проверенный пакет"),
        ]
        for label, pattern in forbidden:
            if re.search(pattern, html_blob, flags=re.IGNORECASE):
                return fail(f"{label} leaked into EPUB XHTML")

        image_tags = re.findall(r"<img\b[^>]+>", html_blob)
        diagram_tags = [tag for tag in image_tags if 'class="diagram"' in tag or "class='diagram'" in tag]
        diagram_captions = re.findall(r"Диаграмма\s+\d+\.", html_blob)
        if len(diagram_tags) != expected_diagrams:
            return fail(f"expected {expected_diagrams} diagram image tags, found {len(diagram_tags)}")
        if len(diagram_captions) < expected_diagrams:
            return fail(f"expected at least {expected_diagrams} diagram captions/alts, found {len(diagram_captions)}")

    print("epub export check passed")
    print(f"epub: {EPUB_PATH}")
    print(f"diagrams: {expected_diagrams}")
    print(f"bytes: {EPUB_PATH.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
