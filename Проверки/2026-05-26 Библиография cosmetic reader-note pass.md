# Библиография cosmetic reader-note pass

Дата: `2026-05-26`.

Статус: `bibliography-cosmetic-reader-note-pass-done`.

## Область прохода

Проверен файл:

`Источники/03-Единая-публикационная-библиография-рабочий-черновик.md`

Цель прохода - приблизить рабочую публикационную библиографию к reader edition: убрать скобочные пометки, которые нужны только для внутренней проверки, но не помогают читателю понять тип источника, границу доказательности или необходимость повторной проверки перед публикацией.

## Что изменено

- Из стабильных академических записей убраны чисто служебные хвосты вида `recent review; checked`, `checked-only`, `bibliographic metadata checked`.
- Для McClelland (1987/1988) оставлена короткая читательская пометка про original publication 1987 и print publication 1988, без ссылки на внутренний ход проверки.
- Для Herzberg, Mausner & Snyderman (1959), Bjork & Bjork (2011), Kendler (2012), Mohebi et al. (2024), Nebe et al. (2024), Smeets et al. (2023), Cajochen & Schmidt (2025), Cao et al. (2025) и других стабильных записей служебные даты проверки вынесены в проверочные артефакты и больше не шумят в самой записи.
- Для animal/mechanistic, clinical/methodological, official-resource, preprint/report, emerging и fast-moving AI/software источников оставлены компактные reader-relevant gates.
- Для fast-moving AI/software блока явно добавлен `recheck before publication`, чтобы не потерять обязанность повторной проверки статуса, версии, метаданных и типа evidence перед публичным выпуском.

## Что не менялось

- Не менялись состав источников, структура разделов и авторско-годовые формы reader-facing глав.
- Не удалялись evidence/status gates, которые защищают текст от слишком сильных выводов: animal/circuit-level, clinical boundary, official living resource, preprint, emerging, context-dependent и similar notes.
- Не выполнялась новая интернет-перепроверка fast-moving источников: этот проход был косметическим и опирался на уже закрытые проверки от `2026-05-26`.
- Раздел `Авторские и внутренние материалы` остается отложенным до export sanitization.

## Проверки

После правки:

- `python3 /tmp/cogeng_bib_audit.py`: DOI duplicates `0`, stable URL duplicates `0`, normalized-title duplicates `0`, first-author/year key duplicates `0`, potential first-author/year gaps `0`.
- `git diff --check`: clean.

## Открыто

- Повторить author-year audit после следующих reader-facing правок.
- Повторить current-version check official/guideline resources перед публичным выпуском, если выпуск будет позже `2026-05-26`.
- Повторить fast-moving AI/software recheck на дату публичного выпуска.
- Выполнить export sanitization: решить, что происходит с production source tails, служебными слоями и внутренними авторскими материалами.
