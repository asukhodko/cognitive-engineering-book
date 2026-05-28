# EPUB export

Эта папка содержит воспроизводимый EPUB-экспорт reader edition учебника.

## Основные артефакты

- `Когнитивное инженерство.epub` - готовая EPUB 3.2 книга.
- `Когнитивное инженерство - epub source.md` - Markdown, где Mermaid-блоки заменены на PNG-диаграммы.
- `assets/diagrams/` - исходные `.mmd` и отрендеренные `.png` диаграммы.
- `epub-build-manifest.json` - машинный манифест сборки.
- `epub-build-report.md` - отчет последней сборки и проверок.

## Сборка

Из корня vault:

```bash
python3 "Прооекты/Когнитивное инженерство/Учебник/Инструменты/build_epub.py"
```

Полный повторный рендер всех диаграмм:

```bash
python3 "Прооекты/Когнитивное инженерство/Учебник/Инструменты/build_epub.py" --force-diagrams
```

## Проверка

```bash
python3 "Прооекты/Когнитивное инженерство/Учебник/Инструменты/check_epub_export.py"
java -jar /usr/share/java/epubcheck.jar "Прооекты/Когнитивное инженерство/Учебник/Экспорт/epub/Когнитивное инженерство.epub"
```

`/usr/bin/epubcheck` в некоторых sandbox-сессиях может не запускаться через системный wrapper, поэтому проверка использует `java -jar /usr/share/java/epubcheck.jar`.
