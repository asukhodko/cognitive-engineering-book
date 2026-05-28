#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import uuid
from dataclasses import dataclass
from datetime import date
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = BOOK_ROOT / "Инструменты"
EXPORT_DIR = BOOK_ROOT / "Экспорт"
EPUB_DIR = EXPORT_DIR / "epub"
ASSETS_DIR = EPUB_DIR / "assets"
DIAGRAMS_DIR = ASSETS_DIR / "diagrams"

READER_EDITION = EXPORT_DIR / "Когнитивное инженерство - reader edition.md"
EPUB_SOURCE = EPUB_DIR / "Когнитивное инженерство - epub source.md"
EPUB_OUTPUT = EPUB_DIR / "Когнитивное инженерство.epub"
METADATA_FILE = EPUB_DIR / "metadata.yaml"
MANIFEST_FILE = EPUB_DIR / "epub-build-manifest.json"
REPORT_FILE = EPUB_DIR / "epub-build-report.md"
PUPPETEER_CONFIG = EPUB_DIR / "puppeteer.json"

CSS_FILE = TOOLS_DIR / "epub.css"
MERMAID_CONFIG = TOOLS_DIR / "epub_mermaid_config.json"
COVER_FILE = TOOLS_DIR / "epub_cover.svg"

BOOK_TITLE = "Когнитивное инженерство"
BOOK_SUBTITLE = (
    "Учебник о том, как проектировать мышление, действие, среду, "
    "восстановление и работу с инструментами"
)


@dataclass
class Diagram:
    index: int
    caption: str
    source_path: Path
    output_path: Path
    output_rel: str
    sha: str
    rendered: bool


def run(command: list[str], *, cwd: Path = BOOK_ROOT, env: dict[str, str] | None = None, quiet: bool = False) -> subprocess.CompletedProcess[str]:
    if not quiet:
        print("+ " + " ".join(str(part) for part in command))
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        if error.stdout:
            print(error.stdout, file=sys.stderr)
        raise


def find_first_existing(candidates: list[Path]) -> Path | None:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def find_mmdc() -> Path:
    env_path = os.environ.get("MMDC_BIN")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    found = shutil.which("mmdc")
    if found:
        return Path(found)

    nvm_bins = sorted(Path.home().glob(".nvm/versions/node/*/bin/mmdc"), key=lambda path: path.stat().st_mtime, reverse=True)
    candidate = find_first_existing(nvm_bins)
    if candidate:
        return candidate

    raise RuntimeError("mmdc not found. Install @mermaid-js/mermaid-cli or set MMDC_BIN.")


def find_chrome() -> Path:
    env_path = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    candidates = sorted(
        Path.home().glob(".cache/puppeteer/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    candidate = find_first_existing(candidates)
    if candidate:
        return candidate

    for name in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return Path(found)

    raise RuntimeError("Chrome/Chromium not found. Install chromium or set PUPPETEER_EXECUTABLE_PATH.")


def command_env(mmdc: Path, chrome: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PATH"] = str(mmdc.parent) + os.pathsep + env.get("PATH", "")
    env["PUPPETEER_EXECUTABLE_PATH"] = str(chrome)
    env["PUPPETEER_SKIP_DOWNLOAD"] = "true"
    # WSL sessions can inherit Windows TEMP/TMP paths under /mnt/c. In sandboxed
    # runs those paths may be read-only, so force Chromium profiles into /tmp.
    env["TMPDIR"] = "/tmp"
    env["TMP"] = "/tmp"
    env["TEMP"] = "/tmp"
    return env


def write_puppeteer_config(chrome: Path) -> None:
    PUPPETEER_CONFIG.write_text(
        json.dumps(
            {
                "executablePath": str(chrome),
                "args": [
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--no-zygote",
                    "--single-process",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--user-data-dir=/tmp/cogeng-epub-chrome-profile",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def current_heading_from_line(line: str, previous: str) -> str:
    if line.startswith("# "):
        return line[2:].strip()
    return previous


def diagram_caption(index: int, current_h1: str, per_heading_count: int) -> str:
    heading = re.sub(r"\s+", " ", current_h1).strip()
    suffix = f" ({per_heading_count})" if per_heading_count > 1 else ""
    return f"Диаграмма {index}. {heading}{suffix}"


def render_diagram(diagram: Diagram, mmdc: Path, env: dict[str, str], width: int, height: int, scale: float, force: bool) -> bool:
    if diagram.output_path.exists() and not force:
        return False

    command = [
        str(mmdc),
        "-i",
        str(diagram.source_path),
        "-o",
        str(diagram.output_path),
        "-p",
        str(PUPPETEER_CONFIG),
        "-c",
        str(MERMAID_CONFIG),
        "-b",
        "white",
        "-w",
        str(width),
        "-H",
        str(height),
        "-s",
        str(scale),
        "-q",
    ]
    run(command, cwd=BOOK_ROOT, env=env, quiet=True)
    return True


def build_epub_source(text: str, mmdc: Path, env: dict[str, str], args: argparse.Namespace) -> tuple[str, list[Diagram]]:
    DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

    lines = text.splitlines()
    output: list[str] = []
    diagrams: list[Diagram] = []
    current_h1 = BOOK_TITLE
    per_heading_counts: dict[str, int] = {}

    in_mermaid = False
    fence_marker = ""
    block: list[str] = []

    for line in lines:
        stripped = line.strip()

        if not in_mermaid:
            current_h1 = current_heading_from_line(line, current_h1)
            if stripped.startswith("```mermaid") or stripped.startswith("~~~mermaid"):
                in_mermaid = True
                fence_marker = stripped[:3]
                block = []
                continue
            output.append(line)
            continue

        if stripped.startswith(fence_marker):
            mermaid_source = "\n".join(block).strip() + "\n"
            digest = hashlib.sha256(mermaid_source.encode("utf-8")).hexdigest()[:12]
            index = len(diagrams) + 1
            per_heading_counts[current_h1] = per_heading_counts.get(current_h1, 0) + 1
            caption = diagram_caption(index, current_h1, per_heading_counts[current_h1])
            basename = f"diagram-{index:03d}-{digest}"
            source_path = DIAGRAMS_DIR / f"{basename}.mmd"
            output_path = DIAGRAMS_DIR / f"{basename}.png"
            output_rel = f"assets/diagrams/{basename}.png"
            source_path.write_text(mermaid_source, encoding="utf-8")
            diagram = Diagram(index, caption, source_path, output_path, output_rel, digest, False)
            rendered = render_diagram(diagram, mmdc, env, args.diagram_width, args.diagram_height, args.diagram_scale, args.force_diagrams)
            diagrams.append(
                Diagram(index, caption, source_path, output_path, output_rel, digest, rendered)
            )
            output.append("")
            output.append(f"![{caption}]({output_rel}){{.diagram}}")
            output.append("")
            in_mermaid = False
            fence_marker = ""
            block = []
            continue

        block.append(line)

    if in_mermaid:
        raise RuntimeError("unclosed mermaid fenced block in reader edition")

    return "\n".join(output).rstrip() + "\n", diagrams


def write_metadata(reader_text: str) -> str:
    identifier = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, hashlib.sha256(reader_text.encode('utf-8')).hexdigest())}"
    author = os.environ.get("COGENG_EPUB_AUTHOR", "Александр Суходько")
    metadata = textwrap.dedent(
        f"""\
        ---
        title: "{BOOK_TITLE}"
        subtitle: "{BOOK_SUBTITLE}"
        author: "{author}"
        lang: "ru-RU"
        language: "ru-RU"
        date: "{date.today().isoformat()}"
        identifier: "{identifier}"
        rights: "Reader edition draft. Requires final publication review before public release."
        publisher: "dalamar81"
        ---
        """
    )
    METADATA_FILE.write_text(metadata, encoding="utf-8")
    return identifier


def write_manifest(diagrams: list[Diagram], mmdc: Path, chrome: Path, identifier: str) -> None:
    manifest = {
        "book": BOOK_TITLE,
        "identifier": identifier,
        "reader_edition": str(READER_EDITION.relative_to(BOOK_ROOT)),
        "epub_source": str(EPUB_SOURCE.relative_to(BOOK_ROOT)),
        "epub": str(EPUB_OUTPUT.relative_to(BOOK_ROOT)),
        "diagram_count": len(diagrams),
        "mmdc": str(mmdc),
        "chrome": str(chrome),
        "diagrams": [
            {
                "index": diagram.index,
                "caption": diagram.caption,
                "source": str(diagram.source_path.relative_to(EPUB_DIR)),
                "image": str(diagram.output_path.relative_to(EPUB_DIR)),
                "sha": diagram.sha,
                "rendered": diagram.rendered,
            }
            for diagram in diagrams
        ],
    }
    MANIFEST_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_report(diagrams: list[Diagram], epubcheck_output: str, check_output: str) -> None:
    rendered_count = sum(1 for diagram in diagrams if diagram.rendered)
    lines = [
        "# EPUB export report",
        "",
        f"Date: `{date.today().isoformat()}`",
        f"EPUB: `{EPUB_OUTPUT}`",
        f"EPUB source: `{EPUB_SOURCE}`",
        f"Diagrams: `{len(diagrams)}` total, `{rendered_count}` rendered this run, `{len(diagrams) - rendered_count}` reused from cache.",
        f"Size: `{EPUB_OUTPUT.stat().st_size}` bytes",
        "",
        "## Rebuild command",
        "",
        "```bash",
        'python3 "Прооекты/Когнитивное инженерство/Учебник/Инструменты/build_epub.py"',
        'python3 "Прооекты/Когнитивное инженерство/Учебник/Инструменты/build_epub.py" --force-diagrams',
        "```",
        "",
        "## EPUBCheck",
        "",
        "```text",
        epubcheck_output.strip(),
        "```",
        "",
        "## Internal EPUB Export Check",
        "",
        "```text",
        check_output.strip(),
        "```",
    ]
    REPORT_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_pandoc_command() -> list[str]:
    return [
        "pandoc",
        str(EPUB_SOURCE),
        "--from=markdown+smart+pipe_tables+implicit_figures+link_attributes",
        "--to=epub3",
        "--standalone",
        "--toc",
        "--toc-depth=2",
        "--split-level=1",
        "--metadata-file",
        str(METADATA_FILE),
        "--css",
        str(CSS_FILE),
        "--epub-cover-image",
        str(COVER_FILE),
        "--resource-path",
        str(EPUB_DIR),
        "-o",
        str(EPUB_OUTPUT),
    ]


def build_epubcheck_command() -> list[str]:
    jar = Path("/usr/share/java/epubcheck.jar")
    if jar.exists():
        return ["java", "-jar", str(jar), str(EPUB_OUTPUT)]
    return ["epubcheck", str(EPUB_OUTPUT)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Cognitive Engineering EPUB export.")
    parser.add_argument("--force-diagrams", action="store_true", help="rerender diagram PNG files even when cached")
    parser.add_argument("--diagram-width", type=int, default=1800, help="Mermaid render viewport width")
    parser.add_argument("--diagram-height", type=int, default=1400, help="Mermaid render viewport height")
    parser.add_argument("--diagram-scale", type=float, default=2.0, help="Mermaid/Puppeteer scale factor")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    EPUB_DIR.mkdir(parents=True, exist_ok=True)

    mmdc = find_mmdc()
    chrome = find_chrome()
    write_puppeteer_config(chrome)
    env = command_env(mmdc, chrome)

    run([sys.executable, str(TOOLS_DIR / "build_reader_edition.py")])
    run([sys.executable, str(TOOLS_DIR / "check_reader_edition.py")])

    reader_text = READER_EDITION.read_text(encoding="utf-8")
    epub_source, diagrams = build_epub_source(reader_text, mmdc, env, args)
    EPUB_SOURCE.write_text(epub_source, encoding="utf-8")

    identifier = write_metadata(reader_text)
    write_manifest(diagrams, mmdc, chrome, identifier)

    pandoc_result = run(build_pandoc_command())
    if pandoc_result.stdout.strip():
        print(pandoc_result.stdout)

    epubcheck_result = run(build_epubcheck_command())
    check_result = run([sys.executable, str(TOOLS_DIR / "check_epub_export.py")])
    write_report(diagrams, epubcheck_result.stdout, check_result.stdout)

    print("epub build passed")
    print(f"epub: {EPUB_OUTPUT}")
    print(f"diagrams: {len(diagrams)}")
    print(f"bytes: {EPUB_OUTPUT.stat().st_size}")
    print(f"report: {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
