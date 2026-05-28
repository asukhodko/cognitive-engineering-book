PYTHON ?= python3
JAVA ?= java
EPUBCHECK_JAR ?= /usr/share/java/epubcheck.jar
EPUB_PATH := Экспорт/epub/Когнитивное инженерство.epub

.PHONY: help all reader check-reader evidence bibliography check epub epub-check whitespace status

help:
	@printf '%s\n' \
		'Targets:' \
		'  make reader        - rebuild Markdown reader edition' \
		'  make epub          - rebuild EPUB, render Mermaid diagrams, run EPUB checks' \
		'  make check         - run reader, evidence, bibliography and EPUB checks' \
		'  make bibliography  - run bibliography duplicate/coverage audit' \
		'  make whitespace    - run git whitespace checks' \
		'  make status        - show compact git status'

all: reader epub check

reader:
	$(PYTHON) "Инструменты/build_reader_edition.py"

check-reader:
	$(PYTHON) "Инструменты/check_reader_edition.py"

evidence:
	$(PYTHON) "Инструменты/check_goal_evidence.py"

bibliography:
	$(PYTHON) "Инструменты/check_bibliography.py"

check: check-reader evidence bibliography epub-check

epub:
	$(PYTHON) "Инструменты/build_epub.py"

epub-check:
	$(PYTHON) "Инструменты/check_epub_export.py"
	@if [ -f "$(EPUBCHECK_JAR)" ]; then \
		$(JAVA) -jar "$(EPUBCHECK_JAR)" "$(EPUB_PATH)"; \
	else \
		echo "skip EPUBCheck: $(EPUBCHECK_JAR) not found"; \
	fi

whitespace:
	git diff --check
	git diff --cached --check

status:
	git status --short --branch
