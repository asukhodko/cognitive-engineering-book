# Источниковый проход 9-14 - dopamine cost-benefit avoidance gradient

Дата проверки: `2026-05-25`.

## Что проверялось

Фронт из общего [[../Источники/00-Реестр-библиографии]] по строкам:

- `Michael Frank (2025)`;
- `Tsutsui-Kimura et al. (2025)`;
- `Mohebi et al. (2024)`;
- `Ben-Zion et al. (2025)`.

Задача прохода: закрыть связанный `to-verify`-долг для глав 9-14 и уточнить границы использования свежих работ о striatal dopamine, cost-benefit control, threat-reward avoidance, reward time horizons and anticipated reward/punishment.

## Проверено

| Источник | Проверенная библиография | Решение для учебника |
| --- | --- | --- |
| Frank (2025) | Frank, M. J. (2025). "Adaptive Cost-Benefit Control Fueled by Striatal Dopamine." _Annual Review of Neuroscience_, 48, 1-22. DOI: `10.1146/annurev-neuro-112723-025228`. | Перевести в `verified; checked 2026-05-25`. Использовать как computational overview for adaptive cost-benefit control, not as dopamine reductionism. |
| Tsutsui-Kimura et al. (2025) | Tsutsui-Kimura, I., Tian, Z. M., Amo, R., Zhuo, Y., Li, Y., Campbell, M. G., Uchida, N., & Watabe-Uchida, M. (2025). "Dopamine in the Tail of the Striatum Facilitates Avoidance in Threat-Reward Conflicts." _Nature Neuroscience_, 28, 1243-1257. DOI: `10.1038/s41593-025-01902-9`. | Перевести в `verified; checked 2026-05-25`. Использовать как animal/circuit-level source for active avoidance policy in threat-reward conflict. |
| Mohebi et al. (2024) | Mohebi, A., Wei, W., Pelattini, L., Kim, C. K., & Berke, J. D. (2024). "Dopamine Transients Follow a Striatal Gradient of Reward Time Horizons." _Nature Neuroscience_, 27, 796-804. DOI: `10.1038/s41593-023-01566-3`. | Перевести в `verified; checked 2026-05-25`. Использовать как fresh circuit-level source for striatal dopamine heterogeneity and reward time horizons. |
| Ben-Zion & Levy (2025) | Ben-Zion, Z., & Levy, I. (2025). "Representation of Anticipated Rewards and Punishments in the Human Brain." _Annual Review of Psychology_, 76, 601-624. DOI: `10.1146/annurev-psych-022324-042614`. | Перевести в `verified; checked 2026-05-25`. Использовать как human-brain review for anticipated rewards and punishments, not as a single reward/punishment map. |

## Редакционная граница

Этот блок поддерживает более точный язык:

```text
action selection depends on expected value, cost, time horizon, threat and learning signals;
dopamine signals are heterogeneous and circuit-dependent;
avoidance can be an active action policy under threat-reward conflict
```

В учебнике нельзя расширять этот блок до формул:

- "дофамин управляет мотивацией";
- "стресс или угроза всегда включает избегание";
- "избегание у человека объясняется одной зоной хвостатого стриатума";
- "можно напрямую настроить дофамин практиками продуктивности";
- "fresh animal/circuit-level evidence сразу доказывает бытовые техники саморегуляции".

## Обновленные файлы

- [[../Источники/00-Реестр-библиографии]]
- [[../Источники/2026-05-24 Пакет источников для главы 9]]
- [[../Источники/2026-05-24 Пакет источников для главы 11]]
- [[../Источники/2026-05-24 Пакет источников для главы 13]]
- [[../Источники/2026-05-24 Пакет источников для главы 14]]
- [[../Главы/09-Приближение-и-избегание]]
- [[../Главы/11-Цена-усилия-усталость-и-ощущаемая-энергия]]
- [[../Главы/13-Контуры-действия]]
- [[../Главы/14-Нейромедиаторы-и-гормоны]]

## Проверки

| Проверка | Результат |
| --- | --- |
| Search for stale `Michael Frank (2025) ... to-verify` in source registry | no findings |
| Search for stale `Tsutsui-Kimura et al. (2025) ... to-verify` in source registry | no findings |
| Search for stale `Mohebi et al. (2024) ... to-verify` in source registry | no findings |
| Search for stale `Ben-Zion ... to-verify` in source registry | no findings |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --check` | pass |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --cached --check` | pass |
| `rg -n '[ \t]+$' /home/asukh/dalamar81/obsidian-vault/Прооекты/Когнитивное\ инженерство/Учебник` | no findings |

## Статус

`checked`
