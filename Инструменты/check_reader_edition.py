#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
READER_EDITION = BOOK_ROOT / "Экспорт" / "Когнитивное инженерство - reader edition.md"

EXPECTED_CHAPTERS = 36
EXPECTED_H1_COUNT = 38

FORBIDDEN_PATTERNS: list[tuple[str, str]] = [
    (r"\[\[", "Obsidian wiki-link"),
    (r"/home/asukh", "local absolute path"),
    (r"Прооекты/", "vault project path"),
    (r"Психология, нейрофизиология", "internal vault area"),
    (r"Темы/", "internal vault area"),
    (r"source packet", "production source-packet wording"),
    (r"source packets", "production source-packet wording"),
    (r"Проверенный пакет", "production source-packet wording"),
    (r"Источниковая опора", "chapter source-tail section"),
    (r"ready-for-review", "production status"),
    (r"Ревизия блока", "production revision section"),
    (r"turn[0-9]", "search pseudo-citation"),
    (r"cite", "search pseudo-citation"),
    (r"to-verify", "metadata verification marker"),
    (r"metadata to verify", "metadata verification marker"),
    (r"keep this note", "production note"),
    (r"Статус самой книги", "production-facing status section"),
    (r"первый полный черновик", "draft-facing wording"),
    (r"полный черновик", "draft-facing wording"),
    (r"`done`", "production status literal"),
    (r"ИИ-воды", "production editing vocabulary"),
    (r"гладких пустых переходов", "production editing vocabulary"),
]


@dataclass
class Heading:
    line_no: int
    level: int
    text: str


def iter_lines_with_fence_state(text: str):
    in_fence = False
    fence_marker = ""

    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        toggles_fence = stripped.startswith(("```", "~~~"))
        if toggles_fence:
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""

        yield line_no, line, in_fence

    if in_fence:
        yield -1, f"UNCLOSED_FENCE:{fence_marker}", True


def headings_outside_fences(text: str) -> tuple[list[Heading], list[str]]:
    headings: list[Heading] = []
    errors: list[str] = []

    for line_no, line, in_fence in iter_lines_with_fence_state(text):
        if line_no == -1:
            errors.append("unclosed fenced block")
            continue
        if in_fence:
            continue

        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.append(Heading(line_no, len(match.group(1)), match.group(2)))

    return headings, errors


def chapter_sections(text: str) -> list[tuple[int, str, str]]:
    matches = list(re.finditer(r"(?m)^# Глава (\d+)\. .*$", text))
    sections: list[tuple[int, str, str]] = []
    bibliography_start = text.find("\n# Список литературы")
    if bibliography_start == -1:
        bibliography_start = len(text)

    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else bibliography_start
        sections.append((int(match.group(1)), match.group(0), text[start:end]))

    return sections


def check_forbidden_patterns(text: str) -> list[str]:
    errors: list[str] = []
    for pattern, label in FORBIDDEN_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            line_no = text.count("\n", 0, match.start()) + 1
            errors.append(f"forbidden pattern at line {line_no}: {label} / {pattern}")
    return errors


def check_headings(text: str) -> list[str]:
    errors: list[str] = []
    headings, heading_errors = headings_outside_fences(text)
    errors.extend(heading_errors)

    h1 = [h for h in headings if h.level == 1]
    if len(h1) != EXPECTED_H1_COUNT:
        errors.append(f"expected {EXPECTED_H1_COUNT} outside-fence H1 headings, found {len(h1)}")

    expected_h1 = ["Когнитивное инженерство"]
    expected_h1.extend(f"Глава {n}." for n in range(1, EXPECTED_CHAPTERS + 1))
    expected_h1.append("Список литературы")

    for idx, expected in enumerate(expected_h1):
        if idx >= len(h1):
            errors.append(f"missing H1: {expected}")
            continue
        actual = h1[idx].text
        if expected.endswith("."):
            if not actual.startswith(expected):
                errors.append(f"H1 #{idx + 1} expected prefix {expected!r}, got {actual!r}")
        elif actual != expected:
            errors.append(f"H1 #{idx + 1} expected {expected!r}, got {actual!r}")

    previous_level = 0
    for heading in headings:
        if previous_level and heading.level > previous_level + 1:
            errors.append(
                f"heading jump at line {heading.line_no}: H{previous_level} -> H{heading.level} {heading.text!r}"
            )
        previous_level = heading.level

    return errors


def check_chapters(text: str) -> list[str]:
    errors: list[str] = []
    chapters = chapter_sections(text)

    if len(chapters) != EXPECTED_CHAPTERS:
        errors.append(f"expected {EXPECTED_CHAPTERS} chapters, found {len(chapters)}")

    numbers = [number for number, _, _ in chapters]
    expected_numbers = list(range(1, EXPECTED_CHAPTERS + 1))
    if numbers != expected_numbers:
        errors.append(f"chapter numbering mismatch: {numbers}")

    for number, title, body in chapters:
        chapter_errors: list[str] = []
        if "```mermaid" not in body:
            chapter_errors.append("no mermaid block")
        if not any(line.startswith("| ") for line in body.splitlines()):
            chapter_errors.append("no markdown table")
        if "## Короткое резюме" not in body:
            chapter_errors.append("no short summary")
        if "## Вопросы для самопроверки" not in body:
            chapter_errors.append("no self-check questions")
        if "## Мини-практика" not in body:
            chapter_errors.append("no mini-practice")
        if re.search(r"(?m)^## (Источниковая опора|Статус|Ревизия блока)\s*$", body):
            chapter_errors.append("production section leaked")

        if chapter_errors:
            errors.append(f"chapter {number:02d} failed: {', '.join(chapter_errors)} / {title}")

    return errors


def check_bibliography(text: str) -> list[str]:
    errors: list[str] = []
    if "\n# Список литературы\n" not in text:
        errors.append("missing bibliography H1")
        bibliography = ""
    else:
        bibliography = text.split("\n# Список литературы\n", 1)[1]

    for number in range(1, 9):
        if not re.search(rf"(?m)^## {number}\. ", bibliography):
            errors.append(f"missing public bibliography section {number}")

    if re.search(r"(?m)^## 9\. ", bibliography) or "Авторские и внутренние материалы" in bibliography:
        errors.append("internal bibliography section leaked into reader edition")

    return errors


def main() -> int:
    if not READER_EDITION.exists():
        print(f"missing reader edition: {READER_EDITION}", file=sys.stderr)
        return 1

    text = READER_EDITION.read_text(encoding="utf-8")
    errors: list[str] = []
    errors.extend(check_forbidden_patterns(text))
    errors.extend(check_headings(text))
    errors.extend(check_chapters(text))
    errors.extend(check_bibliography(text))

    if errors:
        print("reader edition check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    chapters = chapter_sections(text)
    print("reader edition check passed")
    print(f"chapters: {len(chapters)}")
    print(f"bytes: {READER_EDITION.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
