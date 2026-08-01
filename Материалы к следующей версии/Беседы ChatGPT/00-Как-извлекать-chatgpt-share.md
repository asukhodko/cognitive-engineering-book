# Как извлекать материалы из ChatGPT Share

## Каноническая команда

Для публичной ссылки вида `https://chatgpt.com/share/<share-id>` использовать штатный CLI из корня репозитория:

```bash
python3 "Инструменты/extract_chatgpt_share.py" \
  "https://chatgpt.com/share/<share-id>"
```

Короткий вариант через Makefile:

```bash
make extract-chatgpt CHATGPT_SHARE_URL="https://chatgpt.com/share/<share-id>"
```

Системный браузер, Chromium, Puppeteer и исполнение JavaScript не требуются.

## Как работает извлечение

Утилита последовательно использует два публичных представления одной беседы:

1. `https://chatgpt.com/backend-api/share/<share-id>` - готовый JSON, если endpoint доступен.
2. HTML shared-страницы - fallback при `403` backend API. Из HTML извлекаются строки `window.__reactRouterContext.streamController.enqueue(...)`, JSON-декодируется RSC reference pool и восстанавливается объект беседы.

Режим `--proxy auto` перебирает:

1. маршруты из переменной `CHATGPT_SHARE_PROXIES`;
2. direct-доступ без environment proxy;
3. локальный proxy-кандидат `http://127.0.0.1:8899`.

Адреса сетевых gateway не зашиваются в публичный репозиторий. Их следует задавать через `CHATGPT_SHARE_PROXIES` или повторяемый параметр `--proxy`.

Маршрут можно задать явно и повторить параметр для собственного fallback-порядка:

```bash
python3 "Инструменты/extract_chatgpt_share.py" \
  "https://chatgpt.com/share/<share-id>" \
  --proxy direct \
  --proxy "http://proxy-host:8897"
```

Учетные данные proxy, если они присутствуют в URL, маскируются в manifest и консольном выводе.

Для повторной выгрузки в тот же каталог нужен осознанный `--force`; через Make ему соответствует `CHATGPT_SHARE_FORCE=1`.

## Что создается

По умолчанию экспорт лежит в `chatgpt-share-exports/<share-id>/` и не попадает в Git:

```text
conversation.md
conversation.json
links.md
links.json
research/
  001-report.md
  001-report-metadata.json
  001-sources.md
files/
files.json
manifest.json
```

- `conversation.*` содержит только видимые ходы `user` и `assistant`.
- `research/` содержит финальные Deep Research reports из `widget_state.report_message`, если они публично сериализованы.
- `links.*` сохраняет `safe_urls`, `content_references` и ссылки из видимого текста как технические кандидаты, а не готовую библиографию.
- `files.json` фиксирует явные attachment/file локаторы и результат каждой попытки скачивания.
- `manifest.json` хранит способ доступа, маршрут, счетчики, ограничения и SHA-256 созданных артефактов.

`--save-raw` сохраняет исходный HTML или backend JSON в `raw/`. Это нужно только для диагностики: raw payload может содержать временные websocket/download URL и не должен автоматически коммититься.

## Research и созданные файлы

Research-результат может находиться не в обычном assistant-сообщении, а внутри JSON-строки `metadata.chatgpt_sdk.widget_state`. Утилита разбирает ее отдельно, сохраняет `report_message` и карту `content_references`.

Автоскачивание применяется только к явным file-признакам:

- `asset_pointer`, `file_id`, `download_url` и attachment metadata;
- `file-service://...`, `sandbox:/...` и сходным локаторам;
- файловым HTTP(S)-ссылкам непосредственно в видимом сообщении.

Research PDF из `content_references` остаются в `links.*` и не скачиваются массово. Для HTTP-загрузок запрещены localhost и literal private-address targets, действует лимит размера, а неполные ответы не сохраняются как готовые файлы. `sandbox:/...` без публичного download URL отмечается как недоступный, но не теряется из manifest.

## Границы полноты

- Скрытые `system`, `tool`, `code`, `thoughts`, `reasoning` и visually-hidden узлы не переносятся в `conversation.md`.
- Заглушка `The output of this plugin was redacted.` не считается research-результатом.
- Если финальный report отсутствует и заменен заглушкой, его нельзя восстановить из одной shared-ссылки: нужен пользовательский export или вложение.
- `safe_urls` и citation metadata требуют проверки по первоисточникам перед использованием в книге.
- Удаленная, закрытая или переставшая быть публичной share-ссылка не может быть извлечена без авторизованного источника.

## Перенос в материалы книги

После проверки выгрузки создать или дополнить dossier в `Беседы ChatGPT/YYYY-MM-DD - Краткое название/`: сохранить карточку материала, видимую беседу, research-файлы, выжимку, карту источников и состояние сохранения. Затем добавить отдельную строку в `../../01-Реестр-материалов.md`.
