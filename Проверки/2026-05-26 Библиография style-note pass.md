# Библиография style-note pass

Дата: `2026-05-26`.

Статус: `bibliography-style-note-pass-done`.

Повторная проверка после выравнивания reader-facing ссылок: `2026-05-26`. Форма `McClelland (1987/1988)` применена в источниковых блоках глав 7, 8, 29, 31, 33 и 36, а также в рабочих реестрах и пакетах глав. `python3 /tmp/cogeng_bib_audit.py` после правки: DOI duplicates `0`, stable URL duplicates `0`, normalized-title duplicates `0`, first-author/year key duplicates `0`, potential first-author/year gaps `0`.

## Область прохода

Проверен файл:

`Источники/03-Единая-публикационная-библиография-рабочий-черновик.md`

Цель прохода - убрать пометки, которые выглядели как незакрытая библиографическая неопределенность, и отделить их от нормальных evidence/status notes.

## Закрытые хвосты

1. `McClelland (1987/1988)`.

   Cambridge Core показывает _Human Motivation_ как книгу Cambridge University Press with online DOI `10.1017/CBO9781139878289`, print publication date `29 January 1988`, ISBN `9780521369510`, online ISBN `9781139878289`, while description states original publication in 1987. Поэтому в публикационной библиографии оставлена форма `1987/1988`, а старый хвост "решить стиль года" закрыт.

2. `Herzberg, Mausner & Snyderman (1959)`.

   Старый URL на Internet Archive вел к переизданию / edition metadata 2017 года и мог создавать ложное впечатление, что это источник самой записи 1959 года. Для публикационной библиографии оставлен original book-level record: New York: John Wiley & Sons, 1959, LCCN `59014119`, checked against Open Library / WorldCat records. Ссылка на 2017 archive edition убрана из единой публикационной записи.

## Что оставлено

Оставлены bracket notes, которые являются не ошибками, а полезными gates:

- `recent review`;
- `animal/circuit-level evidence`;
- `animal/mechanistic evidence`;
- `clinical boundary`;
- `domain-specific`;
- `preprint`;
- `emerging`;
- `official resource`;
- `recheck before publication`;
- notes about fast-moving AI/software sources.

## Что остается открытым

- Финальный cosmetic pass перед reader edition: решить, какие bracket notes оставить в публичной библиографии, а какие перенести в служебный apparatus.
- Повторный author-year audit после следующих reader-facing edits.
- Повторный current-version check official/guideline resources and fast-moving sources перед публичным выпуском, если выпуск будет позже текущих проверок.
