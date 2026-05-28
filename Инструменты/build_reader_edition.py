#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = BOOK_ROOT / "Главы"
BIBLIOGRAPHY = BOOK_ROOT / "Источники" / "03-Единая-публикационная-библиография-рабочий-черновик.md"
FINAL_OUTPUT = BOOK_ROOT / "Экспорт" / "Когнитивное инженерство - reader edition.md"
LEGACY_DRAFT_OUTPUT = BOOK_ROOT / "Экспорт" / "Когнитивное инженерство - reader edition draft.md"

PRODUCTION_SECTIONS = {
    "Источниковая опора",
    "Статус",
    "Ревизия блока",
}

FRONT_MATTER = """# Когнитивное инженерство

Учебник о том, как проектировать мышление, действие, среду, восстановление и работу с инструментами так, чтобы сложные задачи становились понятнее, управляемее и честнее по своей цене.

## Коротко о книге

"Когнитивное инженерство" - это учебник о человеке как работающей системе: внимании, памяти, мотивации, телесном состоянии, среде, инструментах, команде и обратной связи.

Книга ведет читателя от простой проблемы - человек теряет состояние мысли и не может войти в задачу - к более сложной модели: как ценность, угроза, цена усилия, управляемость, восстановление, ИИ, лидерство и доказательная дисциплина связаны в один контур действия.

Главная идея учебника: трудность не нужно объяснять только ленью, слабой волей или нехваткой мотивации. Часто действие становится недоступным из-за цены входа, тумана, угрозы, перегруза, отсутствия внешнего состояния, плохой обратной связи, неудачного контура работы или системной границы.

## Для кого

Учебник рассчитан на разработчиков и инженеров, которые работают с туманными задачами и большим контекстом; тимлидов и инженерных руководителей; людей, которые учатся сложному; пользователей ИИ, которым важно не потерять собственное мышление, навык и ответственность; всех, кто хочет говорить о продуктивности, мотивации, усталости и восстановлении без самообмана и нейромифов.

## Чем книга не является

Это не медицинский справочник, не психотерапевтический протокол, не инструкция по фармакологии, гормонам, БАДам, биохакингу или лечению. Это не HR-рецепт и не набор техник продуктивности.

Это учебник о проектировании условий действия. Там, где вопрос выходит в здоровье, клиническое состояние, психотерапию, юридическую ответственность, организационную власть или безопасность, книга помогает увидеть границу и перейти к соответствующему уровню помощи или решения.
"""

BIBLIOGRAPHY_NOTE = """## Примечание к источникам

Быстро меняющиеся источники по ИИ, software engineering, официальным классификациям и живым ресурсам требуют повторной проверки перед публичным выпуском. Внутренние авторские материалы в этот reader edition draft не включены как библиографический раздел: их нужно либо санитаризировать как авторские примеры, либо исключить из публичной версии.
"""


def iter_markdown_lines(text: str):
    in_fence = False
    fence_marker = ""

    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""

        yield line, in_fence


def heading_match(line: str) -> re.Match[str] | None:
    return re.match(r"^(#{1,6})\s+(.+?)\s*$", line)


def first_h1(text: str) -> str:
    for line, in_fence in iter_markdown_lines(text):
        if in_fence:
            continue
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("chapter has no H1 heading")


def strip_production_sections(text: str) -> str:
    out: list[str] = []
    skip_level: int | None = None

    for line, in_fence in iter_markdown_lines(text):
        if not in_fence:
            match = heading_match(line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()

                if skip_level is not None and level <= skip_level:
                    skip_level = None

                if skip_level is None and level == 2 and title in PRODUCTION_SECTIONS:
                    skip_level = level
                    continue

        if skip_level is None:
            out.append(line)

    return "\n".join(out).strip()


def chapter_files() -> list[Path]:
    files = sorted(CHAPTERS_DIR.glob("[0-9][0-9]-*.md"))
    if len(files) != 36:
        raise ValueError(f"expected 36 chapter files, found {len(files)}")
    return files


def build_toc(chapters: list[Path]) -> str:
    lines = ["## Оглавление", ""]
    for path in chapters:
        title = first_h1(path.read_text(encoding="utf-8"))
        lines.append(f"- {title}")
    return "\n".join(lines)


def public_bibliography() -> str:
    text = BIBLIOGRAPHY.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("## 1. "))
    end = next(i for i, line in enumerate(lines) if line.startswith("## 9. "))

    public_lines = []
    for line in lines[start:end]:
        public_lines.append(line)

    return "\n".join(public_lines).strip()


def build_reader_edition() -> str:
    chapters = chapter_files()
    parts = [
        FRONT_MATTER.strip(),
        "---",
        build_toc(chapters),
        "---",
    ]

    for path in chapters:
        parts.append(strip_production_sections(path.read_text(encoding="utf-8")))
        parts.append("---")

    parts.extend(
        [
            "# Список литературы",
            public_bibliography(),
            BIBLIOGRAPHY_NOTE.strip(),
        ]
    )

    return "\n\n".join(parts).rstrip() + "\n"


def main() -> None:
    FINAL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    content = build_reader_edition()
    FINAL_OUTPUT.write_text(content, encoding="utf-8")
    LEGACY_DRAFT_OUTPUT.write_text(content, encoding="utf-8")

    lines = content.count("\n")
    size = FINAL_OUTPUT.stat().st_size
    print(f"wrote: {FINAL_OUTPUT}")
    print(f"wrote legacy draft copy: {LEGACY_DRAFT_OUTPUT}")
    print(f"chapters: {len(chapter_files())}")
    print(f"lines: {lines}")
    print(f"bytes: {size}")


if __name__ == "__main__":
    main()
