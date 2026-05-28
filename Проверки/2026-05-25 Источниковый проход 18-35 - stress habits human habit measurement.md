# Источниковый проход 18-35 - stress habits human habit measurement

Дата проверки: `2026-05-25`.

## Что проверялось

Фронт из общего [[../Источники/00-Реестр-библиографии]] по строкам:

- `Smeets et al. (2023)`;
- `Nebe et al. (2024)`.

Задача прохода: закрыть `to-verify`-долг для блока привычек, стресса и методологии human habit measurement. Этот блок нужен главам 18, 23 and 35 как защита от слишком простой формулы:

```text
stress -> habits
```

## Проверено

| Источник | Проверенная библиография | Решение для учебника |
| --- | --- | --- |
| Smeets et al. (2023) | Smeets, T., Ashton, S. M., Roelands, S. J. A. A., & Quaedflieg, C. W. E. M. (2023). "Does Stress Consistently Favor Habits over Goal-Directed Behaviors? Data from Two Preregistered Exact Replication Studies." _Neurobiology of Stress_, 23, 100528. DOI: `10.1016/j.ynstr.2023.100528`. | Перевести в `verified; checked 2026-05-25`. Использовать как replication/boundary source: stress-induced habit claims require conditions and should not be stated universally. |
| Nebe et al. (2024) | Nebe, S., Kretzschmar, A., Brandt, M. C., & Tobler, P. N. (2024). "Characterizing Human Habits in the Lab." _Collabra: Psychology_, 10(1), 92949. DOI: `10.1525/collabra.92949`. | Перевести в `verified; checked 2026-05-25`. Использовать как methodological source: human habits are difficult to operationalize and measure in lab settings. |

## Редакционная граница

Этот блок поддерживает осторожный тезис:

```text
stress can interact with habit and goal-directed control,
but the claim is not universal;
human habits require careful operationalization before practical transfer
```

В учебнике нельзя расширять это до формул:

- "стресс всегда переводит человека в привычки";
- "все автоматические действия под стрессом являются привычками";
- "лабораторная habit task прямо равна бытовому автопилоту";
- "если человек прокрастинирует под стрессом, значит это доказанная habit-loop";
- "stress-habit evidence сразу дает практическую технику".

## Обновленные файлы

- [[../Источники/00-Реестр-библиографии]]
- [[../Источники/2026-05-24 Пакет источников для главы 18]]
- [[../Источники/2026-05-25 Пакет источников для главы 23]]
- [[../Источники/2026-05-25 Пакет источников для главы 35]]
- [[../Главы/18-Прокрастинация-как-конфликт-систем]]
- [[../Главы/23-Как-ломается-мотивационный-контур]]
- [[../Главы/35-Как-читать-исследования-и-не-построить-нейромиф]]

## Проверки

| Проверка | Результат |
| --- | --- |
| Search for stale `Smeets et al. (2023) ... to-verify` in source registry | no findings |
| Search for stale `Nebe et al. (2024) ... to-verify` in source registry | no findings |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --check` | pass |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --cached --check` | pass |
| `rg -n '[ \t]+$' /home/asukh/dalamar81/obsidian-vault/Прооекты/Когнитивное\ инженерство/Учебник` | no findings |

## Статус

`checked`
