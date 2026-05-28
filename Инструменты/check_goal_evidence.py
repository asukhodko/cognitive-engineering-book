#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CHAPTERS = 36

REQUIRED_DIR_COUNTS = {
    "Главы": EXPECTED_CHAPTERS,
    "Паспорта": EXPECTED_CHAPTERS,
    "Карты объяснения": EXPECTED_CHAPTERS,
}

REQUIRED_CHECKS = [
    "Проверки/2026-05-25 Общий финальный аудит учебника.md",
    "Проверки/2026-05-25 Сквозная учебная лестница 1-36 - понятия и переходы.md",
    "Проверки/2026-05-25 Export privacy pass 1-36 - главы и служебные слои.md",
    "Проверки/2026-05-26 Reader edition assembly pass.md",
    "Проверки/2026-05-26 Reader edition structural completeness pass.md",
    "Проверки/2026-05-26 Fast-moving AI software bibliography update.md",
    "Проверки/2026-05-26 Official guideline current-version check.md",
    "Проверки/2026-05-26 Библиография cosmetic reader-note pass.md",
    "Источники/03-Единая-публикационная-библиография-рабочий-черновик.md",
    "07-Публичный-front-matter-и-экспортная-рамка.md",
    "06-Реестр-визуальных-материалов.md",
    "05-Реестр-глав.md",
]

REQUIRED_BLOCK_CHECK_PREFIXES = [
    "Проверки/2026-05-25 Ревизия блока ",
    "Проверки/2026-05-25 Финальная языковая редактура ",
    "Проверки/2026-05-25 Визуальный quality-pass ",
    "Проверки/2026-05-25 Claims-vs-evidence audit ",
    "Проверки/2026-05-25 Библиографическое применение - главы ",
]


def markdown_count(relative_dir: str) -> int:
    return len(list((BOOK_ROOT / relative_dir).glob("*.md")))


def chapter_source_package_exists(chapter_number: int) -> bool:
    sources = BOOK_ROOT / "Источники"
    direct = list(sources.glob(f"2026-05-* Пакет источников для главы {chapter_number}.md"))
    if direct:
        return True

    # Chapters 7 and 8 intentionally use the shared motivation-block source package.
    if chapter_number in {7, 8}:
        return (sources / "2026-05-24 Пакет источников для мотивационного блока 7-11.md").exists()

    return False


def matching_files(prefix: str) -> list[Path]:
    return sorted(BOOK_ROOT.glob(prefix + "*.md"))


def run_reader_check() -> tuple[bool, str]:
    script = BOOK_ROOT / "Инструменты" / "check_reader_edition.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=BOOK_ROOT.parent.parent,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode == 0, result.stdout.strip()


def main() -> int:
    errors: list[str] = []
    report: list[str] = []

    for relative_dir, expected in REQUIRED_DIR_COUNTS.items():
        found = markdown_count(relative_dir)
        report.append(f"{relative_dir}: {found}")
        if found != expected:
            errors.append(f"{relative_dir}: expected {expected} markdown files, found {found}")

    missing_source_packages = [
        chapter_number
        for chapter_number in range(1, EXPECTED_CHAPTERS + 1)
        if not chapter_source_package_exists(chapter_number)
    ]
    if missing_source_packages:
        errors.append(f"missing source packages for chapters: {missing_source_packages}")
    else:
        report.append("source packages: covered for chapters 1-36")

    for relative_path in REQUIRED_CHECKS:
        if not (BOOK_ROOT / relative_path).exists():
            errors.append(f"missing required check/artifact: {relative_path}")

    for prefix in REQUIRED_BLOCK_CHECK_PREFIXES:
        found = matching_files(prefix)
        report.append(f"{prefix}: {len(found)}")
        if not found:
            errors.append(f"missing block check prefix: {prefix}")

    visual_registry = (BOOK_ROOT / "06-Реестр-визуальных-материалов.md").read_text(encoding="utf-8")
    visual_rows = [line for line in visual_registry.splitlines() if line.startswith("| ") and "`quality-pass`" in line]
    report.append(f"visual quality-pass rows: {len(visual_rows)}")
    if len(visual_rows) < EXPECTED_CHAPTERS:
        errors.append(f"expected at least {EXPECTED_CHAPTERS} chapter-level visual quality-pass rows, found {len(visual_rows)}")

    reader_ok, reader_output = run_reader_check()
    report.append(reader_output)
    if not reader_ok:
        errors.append("reader edition checker failed")

    bibliography = (BOOK_ROOT / "Источники" / "03-Единая-публикационная-библиография-рабочий-черновик.md").read_text(encoding="utf-8")
    for number in range(1, 9):
        if f"## {number}. " not in bibliography:
            errors.append(f"bibliography missing section {number}")

    if errors:
        print("goal evidence check failed:")
        for error in errors:
            print(f"- {error}")
        print("\npartial report:")
        for item in report:
            print(f"- {item}")
        return 1

    print("goal evidence check passed")
    for item in report:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
