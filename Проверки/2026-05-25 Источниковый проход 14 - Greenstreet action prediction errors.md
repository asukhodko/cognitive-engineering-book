# Источниковый проход 14 - Greenstreet action prediction errors

Дата проверки: `2026-05-25`.

## Что проверялось

Фронт из источникового пакета главы 14: строка Greenstreet et al. (2025) была оставлена как `to-verify`, потому что в пакете не был раскрыт полный список авторов и не была зафиксирована точная библиографическая запись.

Источник нужен для узкой роли:

```text
dopamine heterogeneity
-> movement-related action prediction error
-> value-free teaching signal
-> bridge to action associations / habit learning
```

Он не должен становиться общим доказательством тезисов про человеческие привычки, мотивацию или практические интервенции.

## Проверено

| Источник | Проверенная библиография | Решение для учебника |
| --- | --- | --- |
| Greenstreet et al. (2025) | Greenstreet, F., Martinez Vergara, H., Johansson, Y., Pati, S., Schwarz, L., Lenzi, S. C., Geerts, J. P., Wisdom, M., Gubanova, A., Rollik, L. B., Kaur, J., Moskovitz, T., Cohen, J., Thompson, E., Margrie, T. W., Clopath, C., & Stephenson-Jones, M. (2025). "Dopaminergic Action Prediction Errors Serve as a Value-Free Teaching Signal." _Nature_, 643, 1333-1342. DOI: `10.1038/s41586-025-09008-9`. | Перевести из `to-verify` в `verified; checked 2026-05-25`. Использовать как свежий animal/circuit-level source for action prediction errors and stable sound-action associations, not as standalone human-intervention evidence. |

## Редакционная граница

В главе 14 источник поддерживает только ограниченный тезис:

```text
часть dopaminergic teaching signals may support action prediction errors
and value-free repetition of state-action associations in a specific circuit/task setting
```

В учебнике нельзя расширять это до формул:

- "дофамин формирует привычки";
- "дофамин можно настроить, чтобы закреплять действия";
- "человеческие привычки объясняются одним action-prediction-error контуром";
- "нейрохимический вывод сразу дает практическую технику".

## Обновленные файлы

- [[../Источники/2026-05-24 Пакет источников для главы 14]]
- [[../Источники/00-Реестр-библиографии]]
- [[../Главы/14-Нейромедиаторы-и-гормоны]]
- [[2026-05-25 Библиографическое применение - главы 12-15]]
- [[2026-05-25 Общий финальный аудит учебника]]

## Проверки

| Проверка | Результат |
| --- | --- |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --check` | pass |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --cached --check` | pass |
| `rg -n '[ \t]+$' /home/asukh/dalamar81/obsidian-vault/Прооекты/Когнитивное\ инженерство/Учебник` | no findings |
| Search for stale `Greenstreet ... to-verify` in source packets and chapter files | no findings |
| Raw citation scan outside saved research packet | only existing check-file mentions of `turn...` / `cite`, no raw citations in touched chapter/source files |

## Статус

`checked`
