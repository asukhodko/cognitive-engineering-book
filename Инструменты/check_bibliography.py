#!/usr/bin/env python3
from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
BIBLIOGRAPHY = BOOK_ROOT / "Источники" / "03-Единая-публикационная-библиография-рабочий-черновик.md"
CHAPTERS_DIR = BOOK_ROOT / "Главы"


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    return re.sub(r"\s+", " ", value)


def first_key(author_part: str) -> str:
    author = re.sub(r"\s+", " ", author_part.strip())
    if "," in author:
        author = author.split(",", 1)[0]
    else:
        author = re.sub(r"\.$", "", author)
    author = re.sub(r"\s+et al\.?$", "", author, flags=re.IGNORECASE)
    author = re.split(r"\s+&\s+", author, maxsplit=1)[0]
    return author.lower()


def year_token_from_record(record: str, year_pattern: re.Pattern[str]) -> str:
    match = year_pattern.search(record)
    if not match:
        raise ValueError(f"record has no year token: {record[:120]}")

    raw = match.group(0)[1:-1]
    if raw.startswith("n.d.-"):
        return raw.split(",", 1)[0]
    if raw.startswith("2016; updated"):
        return "2016; updated"

    slash = re.match(r"\d{4}[a-z]?/\d{4}[a-z]?", raw)
    if slash:
        return slash.group(0)

    year = re.match(r"\d{4}[a-z]?", raw)
    if not year:
        raise ValueError(f"unsupported year token: {raw}")
    return year.group(0)


def publication_records(text: str, year_pattern: re.Pattern[str]) -> list[str]:
    records: list[str] = []
    for line in (line.strip() for line in text.splitlines()):
        if not line or line.startswith(("#", "-", "`", "|")):
            continue
        if line.startswith("Нейросхемная") or line.startswith("Раздел "):
            continue
        if year_pattern.search(line):
            records.append(line)
    return records


def duplicate_dois(text: str) -> dict[str, list[str]]:
    doi_counts: dict[str, list[str]] = defaultdict(list)
    for match in re.finditer(r"https://doi\.org/([^\s)]+)", text):
        doi = match.group(1).rstrip(".,;]").lower()
        doi_counts[doi].append(doi)
    return {key: values for key, values in doi_counts.items() if len(values) > 1}


def duplicate_stable_urls(text: str) -> dict[str, list[str]]:
    url_counts: dict[str, list[str]] = defaultdict(list)
    for match in re.finditer(r"https?://[^\s)]+", text):
        url = match.group(0).rstrip(".,;]")
        if "doi.org" not in url:
            url_counts[url].append(url)
    return {key: values for key, values in url_counts.items() if len(values) > 1}


def duplicate_titles(records: list[str], year_pattern: re.Pattern[str]) -> dict[str, list[str]]:
    title_counts: dict[str, list[str]] = defaultdict(list)
    for record in records:
        match = year_pattern.search(record)
        if not match:
            continue
        after_year = record[match.end() :]
        title = None

        quoted = re.search(r'"([^"]{8,})"', after_year)
        if quoted:
            title = quoted.group(1)
        else:
            italic = re.search(r"_([^_]{8,})_", after_year)
            if italic:
                title = italic.group(1)

        if title:
            title_counts[normalize_title(title)].append(record)

    return {key: values for key, values in title_counts.items() if key and len(values) > 1}


def bibliography_keys(records: list[str], year_pattern: re.Pattern[str]) -> dict[tuple[str, str], list[str]]:
    author_years: dict[tuple[str, str], list[str]] = defaultdict(list)
    for record in records:
        match = year_pattern.search(record)
        if not match:
            continue
        key = (first_key(record[: match.start()]), year_token_from_record(record, year_pattern))
        author_years[key].append(record)
        if re.search(r"\breprint\b.*\b2003\b|\b2003\b.*\breprint\b", record, flags=re.IGNORECASE):
            author_years[(key[0], "2003")].append(record)
    return author_years


def reader_facing_forms(bib_keys: set[tuple[str, str]]) -> tuple[set[tuple[str, str]], list[tuple[str, str, str, str]]]:
    form_pattern = re.compile(
        r"([\wÀ-ÖØ-öø-ÿА-Яа-яЁё][\wÀ-ÖØ-öø-ÿА-Яа-яЁё0-9 .,&'’\-/]+?)\s*\(([^)]*(?:\d{4}|n\.d\.)[^)]*)\)"
    )
    year_extract = re.compile(
        r"n\.d\.-[a-z]|\d{4}[a-z]?/updated|\d{4}[a-z]?/\d{4}[a-z]?|\d{4}[a-z]?; updated|\d{4}[a-z]?"
    )

    effective_bib_keys = set(bib_keys)
    for author, year in list(effective_bib_keys):
        if author.startswith("task force"):
            effective_bib_keys.add(("task force", year))

    forms: set[tuple[str, str]] = set()
    misses: list[tuple[str, str, str, str]] = []

    for path in sorted(CHAPTERS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        if "## Источниковая опора" in content:
            content = content.split("## Источниковая опора", 1)[1]

        for line in content.splitlines():
            if not line.lstrip().startswith("-"):
                continue

            for match in form_pattern.finditer(line):
                author = match.group(1).strip(" -;:,.")
                if ";" in author:
                    author = author.rsplit(";", 1)[-1].strip()
                if ":" in author:
                    author = author.rsplit(":", 1)[-1].strip()

                years: list[str] = []
                for extracted in year_extract.findall(match.group(2)):
                    if "/updated" in extracted:
                        years.append(extracted.replace("/updated", "; updated"))
                    elif re.fullmatch(r"\d{4}[a-z]?/\d{4}[a-z]?", extracted):
                        slash_key = (first_key(author), extracted)
                        if slash_key in effective_bib_keys:
                            years.append(extracted)
                        else:
                            years.extend(extracted.split("/"))
                    else:
                        years.append(extracted)

                for year in years:
                    key = (first_key(author), year)
                    forms.add(key)
                    if key not in effective_bib_keys:
                        misses.append((path.name, author, year, line.strip()))

    return forms, misses


def print_duplicate_samples(prefix: str, duplicates: dict[object, list[str]]) -> None:
    for key, values in sorted(duplicates.items())[:20]:
        print(prefix, key, len(values))


def main() -> int:
    text = BIBLIOGRAPHY.read_text(encoding="utf-8")
    year_pattern = re.compile(r"\((?:\d{4}[a-z]?|\d{4}/\d{4}|\d{4}; updated|n\.d\.-[a-z])[^)]*\)")

    records = publication_records(text, year_pattern)
    doi_dups = duplicate_dois(text)
    url_dups = duplicate_stable_urls(text)
    title_dups = duplicate_titles(records, year_pattern)
    author_years = bibliography_keys(records, year_pattern)
    key_dups = {key: values for key, values in author_years.items() if len(values) > 1}
    forms, misses = reader_facing_forms(set(author_years))

    print(f"bibliographic records: {len(records)}")
    print(f"doi duplicates: {len(doi_dups)}")
    print_duplicate_samples("DOI_DUP", doi_dups)
    print(f"stable url duplicates: {len(url_dups)}")
    print_duplicate_samples("URL_DUP", url_dups)
    print(f"normalized-title duplicates: {len(title_dups)}")
    print_duplicate_samples("TITLE_DUP", title_dups)
    print(f"first-author/year key duplicates: {len(key_dups)}")
    print_duplicate_samples("KEY_DUP", key_dups)
    print(f"reader-facing author-year forms: {len(forms)}")
    print(f"potential first-author/year gaps: {len(misses)}")
    for item in misses[:40]:
        print("MISS", item[0], item[1], item[2], item[3])

    if doi_dups or url_dups or title_dups or key_dups or misses:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
