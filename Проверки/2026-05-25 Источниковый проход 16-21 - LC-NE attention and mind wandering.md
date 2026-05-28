# Источниковый проход 16-21 - LC-NE attention and mind wandering

Дата проверки: `2026-05-25`.

## Что проверялось

Фронт из общего [[../Источники/00-Реестр-библиографии]] по строкам:

- `Unsworth (2017); Sara (2012); Aston-Jones & Cohen`;
- `Kane et al. (2007); Mooneyham & Schooler (2013)`.

Задача прохода: закрыть `to-verify`-долг для блока attention control, LC-NE/arousal and mind wandering, а также уточнить границы claims для глав 16, 21 and 35.

## Проверено

| Источник | Проверенная библиография | Решение для учебника |
| --- | --- | --- |
| Unsworth & Robison (2017) | Unsworth, N., & Robison, M. K. (2017). "A Locus Coeruleus-Norepinephrine Account of Individual Differences in Working Memory Capacity and Attention Control." _Psychonomic Bulletin & Review_, 24, 1282-1311. DOI: `10.3758/s13423-016-1220-5`. | Перевести в `verified; checked 2026-05-25`. Использовать для attention-control/arousal framing, not as "willpower chemistry". |
| Sara & Bouret (2012) | Sara, S. J., & Bouret, S. (2012). "Orienting and Reorienting: The Locus Coeruleus Mediates Cognition through Arousal." _Neuron_, 76(1), 130-141. DOI: `10.1016/j.neuron.2012.09.011`. | Перевести в `verified; checked 2026-05-25`. Использовать для orienting/reorienting and arousal, not as "noradrenaline = attention". |
| Aston-Jones & Cohen (2005) | Aston-Jones, G., & Cohen, J. D. (2005). "An Integrative Theory of Locus Coeruleus-Norepinephrine Function: Adaptive Gain and Optimal Performance." _Annual Review of Neuroscience_, 28, 403-450. DOI: `10.1146/annurev.neuro.28.061604.135709`. | Уже проверен в пакете главы 14; в общем реестре зафиксировать как verified within LC-NE block. |
| Kane et al. (2007) | Kane, M. J., Brown, L. H., McVay, J. C., Silvia, P. J., Myin-Germeys, I., & Kwapil, T. R. (2007). "For Whom the Mind Wanders, and When: An Experience-Sampling Study of Working Memory and Executive Control in Daily Life." _Psychological Science_, 18(7), 614-621. DOI: `10.1111/j.1467-9280.2007.01948.x`. | Перевести в `verified; checked 2026-05-25`. Использовать как empirical source for mind wandering, WMC, concentration and executive control in daily life. |
| Mooneyham & Schooler (2013) | Mooneyham, B. W., & Schooler, J. W. (2013). "The Costs and Benefits of Mind-Wandering: A Review." _Canadian Journal of Experimental Psychology_, 67(1), 11-18. DOI: `10.1037/a0031569`. | Перевести в `verified; checked 2026-05-25`. Использовать как review boundary: mind wandering has costs and possible benefits. |

## Редакционная граница

Этот блок поддерживает осторожный тезис:

```text
attention control depends on working memory, task demand, arousal and LC-NE dynamics;
mind wandering can be costly or useful depending on task and outcome
```

В учебнике нельзя расширять это до формул:

- "внимание = норадреналин";
- "LC-NE объясняет всю концентрацию";
- "mind wandering всегда вреден";
- "mind wandering всегда творчески полезен";
- "чтобы сфокусироваться, нужно просто поднять arousal";
- "индивидуальные различия attention control являются фиксированным пределом".

## Обновленные файлы

- [[../Источники/00-Реестр-библиографии]]
- [[../Источники/2026-05-24 Пакет источников для главы 16]]
- [[../Источники/2026-05-25 Пакет источников для главы 21]]
- [[../Источники/2026-05-25 Пакет источников для главы 35]]
- [[../Главы/16-Как-строится-понимание]]
- [[../Главы/21-Фокус-WIP-и-переключения]]
- [[../Главы/35-Как-читать-исследования-и-не-построить-нейромиф]]

## Проверки

| Проверка | Результат |
| --- | --- |
| Search for stale `Unsworth ... to-verify` in source registry | no findings |
| Search for stale `Kane et al. (2007) ... to-verify` in source registry | no findings |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --check` | pass |
| `git -C /home/asukh/dalamar81/obsidian-vault diff --cached --check` | pass |
| `rg -n '[ \t]+$' /home/asukh/dalamar81/obsidian-vault/Прооекты/Когнитивное\ инженерство/Учебник` | no findings |

## Статус

`checked`
