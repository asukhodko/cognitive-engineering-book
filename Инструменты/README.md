# Извлечение публичных ChatGPT Share

## Назначение

`extract_chatgpt_share.py` выгружает публичную shared-беседу ChatGPT в воспроизводимый локальный набор Markdown/JSON-артефактов. Системный браузер, Node.js, Chromium и аккаунт ChatGPT не нужны.

Точка входа:

```text
Инструменты/extract_chatgpt_share.py
```

Основная логика и повторно используемые функции:

```text
Инструменты/chatgpt_share_extractor.py
```

## Требования

- Linux, macOS или WSL;
- Python 3.10 или новее;
- Git и POSIX Make для быстрого старта; при прямом запуске Python-скрипта Make не нужен;
- доступ к `https://chatgpt.com` напрямую или через HTTP(S)-proxy;
- публичная ссылка вида `https://chatgpt.com/share/<share-id>`.

Утилита использует только стандартную библиотеку Python. Устанавливать Python-пакеты не нужно.

## Быстрый старт

```bash
git clone https://github.com/asukhodko/cognitive-engineering-book.git
cd cognitive-engineering-book
python3 --version
make test-share-extractor
make extract-chatgpt CHATGPT_SHARE_URL="https://chatgpt.com/share/<share-id>"
```

По умолчанию экспорт появится в:

```text
chatgpt-share-exports/<share-id>/
```

Этот каталог игнорируется Git.

## Настройка proxy

Если direct-доступ не работает, создайте локальный XDG-файл. Он не попадает в репозиторий:

```bash
config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/cognitive-engineering-book"
install -d -m 0700 "$config_dir"
printf '%s\n' 'http://proxy-host:8897' > "$config_dir/chatgpt-share-proxies"
chmod 0600 "$config_dir/chatgpt-share-proxies"
```

Формат файла: один `http://` или `https://` proxy URL на строку. Пустые строки и строки, начинающиеся с `#`, игнорируются. Можно задать несколько fallback-маршрутов:

```text
# preferred
http://proxy-one.example:8897
http://proxy-two.example:8080
```

В режиме `auto` маршруты пробуются в таком порядке:

1. `CHATGPT_SHARE_PROXIES`;
2. `${XDG_CONFIG_HOME:-$HOME/.config}/cognitive-engineering-book/chatgpt-share-proxies` или файл из `CHATGPT_SHARE_PROXY_FILE`;
3. `HTTPS_PROXY`, `ALL_PROXY`, `HTTP_PROXY` и их lowercase-варианты;
4. direct-доступ;
5. встроенные loopback-кандидаты.

Повторы удаляются с сохранением порядка. Credentials в proxy URL не печатаются в route labels и сетевой диагностике. Тем не менее файл с credentials нужно хранить с mode `0600`.

Разовый proxy можно передать без файла:

```bash
make extract-chatgpt \
  CHATGPT_SHARE_URL="https://chatgpt.com/share/<share-id>" \
  CHATGPT_SHARE_PROXY="http://proxy-host:8897"
```

Принудительно direct-маршрут:

```bash
make extract-chatgpt \
  CHATGPT_SHARE_URL="https://chatgpt.com/share/<share-id>" \
  CHATGPT_SHARE_PROXY=direct
```

SOCKS-proxy напрямую не поддерживаются. Используйте HTTP(S)-proxy или локальный HTTP bridge.

## Запуск без Make

```bash
python3 "Инструменты/extract_chatgpt_share.py" \
  "https://chatgpt.com/share/<share-id>" \
  --proxy auto \
  --output-dir "/tmp/chatgpt-share-export"
```

Полный список параметров:

```bash
python3 "Инструменты/extract_chatgpt_share.py" --help
```

Важные опции:

| Опция | Назначение |
| --- | --- |
| `--proxy auto` | Использовать автоматическую цепочку маршрутов. |
| `--proxy URL` | Явно задать HTTP(S)-proxy; опцию можно повторять. |
| `--output-dir PATH` | Задать точный выходной каталог. |
| `--force` | Заменить ранее созданный экспорт той же Share-ссылки. |
| `--save-raw` | Сохранить сырой backend JSON или HTML/RSC payload. |
| `--no-download-files` | Не пытаться скачивать найденные file-артефакты. |
| `--timeout SECONDS` | Задать timeout каждого HTTP-запроса; по умолчанию 45 секунд. |
| `--max-share-bytes N` | Ограничить размер ответа Share; по умолчанию 64 MiB. |
| `--max-file-bytes N` | Ограничить размер каждого file-артефакта; по умолчанию 100 MiB. |

Для Make доступны `CHATGPT_SHARE_URL`, `CHATGPT_SHARE_OUTPUT`, `CHATGPT_SHARE_PROXY` и `CHATGPT_SHARE_FORCE=1`.

## Состав экспорта

| Путь | Содержимое |
| --- | --- |
| `conversation.md` | Видимые user/assistant-сообщения в Markdown. |
| `conversation.json` | Тот же диалог в структурированном JSON. |
| `research/NNN-report.md` | Embedded Deep Research report, если он есть в Share payload. |
| `research/NNN-report-metadata.json` | Metadata и контрольные хэши research report. |
| `research/NNN-sources.md` | Ссылки, найденные в metadata research report. |
| `links.md`, `links.json` | Техническая карта уникальных URL. |
| `files/`, `files.json` | Скачанные публичные file-артефакты и журнал попыток. |
| `manifest.json` | Метод, маршрут, счетчики, warnings, HTTP-попытки, размеры и SHA-256 артефактов. |
| `raw/` | Сырой ответ, только при `--save-raw`. |

В диалог не включаются скрытые `system`, `tool`, `reasoning`, `thoughts`, code-вызовы и служебные узлы. Списки ссылок и file-кандидатов нужно считать технической выгрузкой, а не проверенной библиографией.

## Повторный экспорт

Утилита не перезаписывает существующий каталог без явного разрешения:

```bash
make extract-chatgpt \
  CHATGPT_SHARE_URL="https://chatgpt.com/share/<share-id>" \
  CHATGPT_SHARE_FORCE=1
```

`--force` заменит только каталог, который по своему `manifest.json` является прежним экспортом той же Share-ссылки. Произвольный каталог утилита не удалит.

## Диагностика

| Симптом | Что проверить |
| --- | --- |
| `all ChatGPT Share routes failed` | Доступен ли `chatgpt.com`; верен ли proxy URL; не удалена ли Share-ссылка. В ошибке перечислены route/endpoint/status каждой попытки. |
| `backend-api: 403` | Это не обязательно сбой: утилита затем пробует HTML/RSC на том же маршруте. |
| `output directory already exists` | Передайте `--force` или `CHATGPT_SHARE_FORCE=1`, если нужно осознанно обновить этот экспорт. |
| `no embedded research report was found` | В данной беседе может не быть Deep Research report; сам диалог при этом может быть извлечен корректно. |
| File-кандидат не скачан | Временная ссылка могла истечь, публичный file-service может требовать авторизацию, а `sandbox:/mnt/data/...` вообще не содержит публичного URL. Подробности и HTTP status есть в `files.json`; embedded Research при этом часто уже сохранен отдельно. |
| `unsupported proxy URL` | Поддерживаются только `http://` и `https://`; проверьте файл и proxy-переменные. |

Для изолированной проверки одного маршрута задайте его явно через `--proxy`, не используя `auto`.

## Проверка изменений

```bash
make test-share-extractor
git diff --check
```

Тесты проверяют URL-нормализацию, proxy discovery и fallback, HTML/RSC и backend JSON, фильтрацию скрытых узлов, research report, file-кандидаты, manifest и безопасную замену прежнего экспорта.

## Границы

- Извлекаются только публичные ChatGPT Share, а не приватные чаты аккаунта.
- Локаторы `sandbox:/mnt/data/...` фиксируются как evidence отсутствующего производного артефакта, но не реконструируются и не выдаются за скачанный файл.
- HTML/RSC-формат управляется ChatGPT и может измениться; live-проверка нужна после изменений сайта.
- Raw payload может содержать временные служебные URL; не публикуйте `raw/` без проверки.
- Извлеченный текст и файлы могут быть защищены авторским правом; ответственность за их использование несет пользователь.
