# Источниковый проход 14 - Lee dopaminergic heterogeneity

Дата проверки: `2026-05-25`.

## Что проверялось

В общем [[../Источники/00-Реестр-библиографии]] оставалась строка `Lee, Sagiv & Daw (2024)` со статусом `to-verify`, хотя в [[../Источники/2026-05-24 Пакет источников для главы 14]] уже была зафиксирована полная проверенная запись Lee et al. (2024).

Цель прохода: убрать дублирующий статусный долг без расширения claims beyond source packet.

## Проверено

| Источник | Проверенная библиография | Решение для учебника |
| --- | --- | --- |
| Lee, Sagiv & Daw (2024) | Lee, R. S., Sagiv, Y., Engelhard, B., Witten, I. B., & Daw, N. D. (2024). "A Feature-Specific Prediction Error Model Explains Dopaminergic Heterogeneity." _Nature Neuroscience_, 27, 1574-1586. DOI: `10.1038/s41593-024-01689-1`. | В общем реестре перевести дублирующую строку из `to-verify` в `verified; checked in chapter 14 packet`. |

## Редакционная граница

Источник поддерживает узкий тезис:

```text
dopaminergic prediction errors are heterogeneous and can be modeled as feature-specific,
so dopamine should not be described as one single scalar signal for motivation, pleasure or learning
```

В учебнике нельзя расширять это до формул:

- "дофамин всегда кодирует все свойства будущего действия";
- "гетерогенность дофамина сама по себе объясняет мотивацию";
- "одна computational model закрывает весь разговор о нейромедиаторах";
- "нейрохимическая неоднородность сразу дает практическую технику саморегуляции".

## Обновленные файлы

- [[../Источники/00-Реестр-библиографии]]

## Проверки

| Проверка | Результат |
| --- | --- |
| Search for stale `Lee, Sagiv & Daw (2024) ... to-verify` in source registry | no findings |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --check` | pass |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --cached --check` | pass |
| `rg -n '[ \t]+$' /home/asukh/dalamar81/obsidian-vault/Прооекты/Когнитивное\ инженерство/Учебник` | no findings |

## Статус

`checked`
