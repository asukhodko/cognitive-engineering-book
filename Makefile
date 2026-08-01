PYTHON ?= python3
JAVA ?= java
EPUBCHECK_JAR ?= /usr/share/java/epubcheck.jar
EPUB_PATH := Экспорт/epub/Когнитивное инженерство.epub
CHATGPT_SHARE_URL ?=
CHATGPT_SHARE_OUTPUT ?=
CHATGPT_SHARE_PROXY ?= auto
CHATGPT_SHARE_FORCE ?=

.PHONY: help all reader check-reader evidence bibliography check epub epub-check extract-chatgpt test-share-extractor whitespace status

help:
	@printf '%s\n' \
		'Targets:' \
		'  make reader        - rebuild Markdown reader edition' \
		'  make epub          - rebuild EPUB, render Mermaid diagrams, run EPUB checks' \
		'  make check         - run reader, evidence, bibliography and EPUB checks' \
		'  make bibliography  - run bibliography duplicate/coverage audit' \
		'  make extract-chatgpt CHATGPT_SHARE_URL=... - export a public ChatGPT Share' \
		'  make test-share-extractor - run ChatGPT Share extractor tests' \
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

check: check-reader evidence bibliography test-share-extractor epub-check

epub:
	$(PYTHON) "Инструменты/build_epub.py"

epub-check:
	$(PYTHON) "Инструменты/check_epub_export.py"
	@if [ -f "$(EPUBCHECK_JAR)" ]; then \
		$(JAVA) -jar "$(EPUBCHECK_JAR)" "$(EPUB_PATH)"; \
	else \
		echo "skip EPUBCheck: $(EPUBCHECK_JAR) not found"; \
	fi

extract-chatgpt:
	@test -n "$(CHATGPT_SHARE_URL)" || { echo 'CHATGPT_SHARE_URL is required' >&2; exit 2; }
	$(PYTHON) "Инструменты/extract_chatgpt_share.py" "$(CHATGPT_SHARE_URL)" \
		--proxy "$(CHATGPT_SHARE_PROXY)" \
		$(if $(strip $(CHATGPT_SHARE_OUTPUT)),--output-dir "$(CHATGPT_SHARE_OUTPUT)",) \
		$(if $(filter 1 true yes,$(CHATGPT_SHARE_FORCE)),--force,)

test-share-extractor:
	$(PYTHON) -m unittest discover -s "Инструменты/tests" -p 'test_*.py'

whitespace:
	git diff --check
	git diff --cached --check

status:
	git status --short --branch
