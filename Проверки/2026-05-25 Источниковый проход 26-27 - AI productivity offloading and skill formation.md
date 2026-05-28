# Источниковый проход 26-27 - AI productivity offloading and skill formation

Дата проверки: `2026-05-25`.

## Что проверялось

Фронт из общего аудита: быстро меняющаяся база для глав [[../Главы/26-ИИ-как-усилитель-и-как-обход-мышления]] и [[../Главы/27-Как-работать-с-ИИ-не-отдавая-ему-субъектность]].

Проверялись четыре вопроса:

- можно ли писать, что ИИ ускоряет разработчиков;
- как обновить METR-линейку после RCT early-2025;
- можно ли перевести Lee et al. (2025) из `to-verify`;
- какие источники годятся для осторожного блока про AI offloading, hollowing-out, deskilling and skill formation.

## Проверенные источники

| Блок | Источник | Решение для учебника |
| --- | --- | --- |
| AI coding productivity, RCT / field studies | Peng et al. (2023); Cui et al. (2026); Qian & Wexler (2024); Butler et al. (2025); METR (2025/2026). | Оставить тезис "эффект возможен, но неоднороден"; не писать "ИИ ускоряет разработчиков" как общий закон. |
| Updated METR evidence | METR (2026-02-24), "We are Changing our Developer Productivity Experiment Design"; METR (2026-05-11), "Measuring the Self-Reported Impact of Early-2026 AI on Technical Worker Productivity"; METR (2026-05-19), "Frontier Risk Report." | Заменить старую рабочую строку про несуществующий January update на реальные обновления. Указывать, что selection effects, self-report and study design matter. |
| Meta-analysis preprint | Maier et al. (2026), "A Meta-Analysis of the Effect of Generative AI on Productivity and Learning in Programming", arXiv: `2605.04779`. | Добавить как свежий synthesis candidate: moderate positive productivity effect with heterogeneity; no statistically significant learning effect. Статус: preprint, not final verdict. |
| Critical thinking | Lee et al. (2025), CHI '25, DOI `10.1145/3706598.3713778`. | Перевести из `to-verify` в `verified; emerging`; использовать как survey/self-report, не как causal proof of deskilling. |
| AI-era cognitive offloading | Jose et al. (2025), _Frontiers in Psychology_, DOI `10.3389/fpsyg.2025.1645237`. | Использовать как opinion/conceptual map of risks, not strong evidence. |
| Foundational knowledge | Klein & Klein (2025), _Frontiers in Artificial Intelligence_, DOI `10.3389/frai.2025.1719019`. | Использовать как hypothesis/theory warning: внутреннее знание нужно для проверки, переноса и устойчивого обучения. |
| Skill formation | Shen & Tamkin (2026), "How AI Impacts Skill Formation", arXiv: `2601.20245`. | Добавить как preprint experiment candidate for skill-maintenance section; не строить на нем окончательные практические claims без дальнейшего чтения. |

## Редакционное решение

Главы 26-27 должны писать об ИИ в трехслойной рамке:

```text
productivity evidence
-> cognitive offloading / trust calibration
-> skill maintenance and learning boundary
```

Ключевой вывод:

```text
ИИ может снижать цену входа и ускорять отдельные рабочие циклы,
но это не доказывает автоматического роста понимания,
субъектности,
навыка
или качества решения.
```

Поэтому практическая рекомендация остается прежней, но теперь лучше подкреплена:

```text
до ИИ: свой trace, критерий, гипотеза
во время ИИ: явная роль инструмента
после ИИ: проверка, объяснение своими словами, тест или контрпример, след решения
```

## Что обновлено

- [[../Источники/2026-05-25 Пакет источников для главы 26]]: исправлена строка Cui et al.; добавлены Butler et al. (2025), обновления METR 2026 года, Maier et al. (2026), Jose et al. (2025), Klein & Klein (2025), Shen & Tamkin (2026); Lee et al. (2025) зафиксирован как `verified; emerging`.
- [[../Источники/2026-05-25 Пакет источников для главы 27]]: обновлены строки AI productivity и Critical thinking / AI offloading.
- [[../Источники/00-Реестр-библиографии]]: fast-moving AI-блоки теперь отражают дату проверки и разные типы evidence.
- [[../05-Реестр-глав]]: последний закрытый источниковый фронт обновлен.

## Оставшиеся ограничения

- Maier et al. (2026) and Shen & Tamkin (2026) остаются preprint-level sources.
- Jose et al. (2025) and Klein & Klein (2025) полезны как conceptual / opinion / hypothesis-theory sources, not strong empirical evidence.
- AI productivity evidence нужно обновлять перед переводом глав 26-27 в `done`, потому что поколение инструментов и способы измерения меняются слишком быстро.

## Статус

`checked`
