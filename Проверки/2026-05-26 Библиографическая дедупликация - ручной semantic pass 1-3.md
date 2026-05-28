# Библиографическая дедупликация - ручной semantic pass 1-3

Дата: `2026-05-26`.

Статус: `manual-semantic-dedup-1-3-done`.

## Область прохода

Проверен рабочий черновик единой публикационной библиографии:

`Источники/03-Единая-публикационная-библиография-рабочий-черновик.md`

Область ручной проверки:

- раздел 1: когнитивный контроль, память и внешняя когниция;
- раздел 2: мотивация, потребности, самоэффективность и управляемость;
- раздел 3: нейрофизиология действия, усилия, стресса и аллостаза.

Проверка дополняет механические DOI/title/key passes. Ее цель - поймать не буквальные дубли, а случаи, где разные записи могут оказаться версиями одной публикации, разными изданиями одной книги, смешанными записями или неудачно разведенными тематическими пересечениями.

## Проверенные семантические пары

1. `Norman (1991)` и `Norman (1993)` оставлены как две разные записи.

   `Cognitive Artifacts` - глава/текст о когнитивных артефактах. _Things That Make Us Smart_ - отдельная книга о внешних представлениях и человеко-машинной среде. В учебнике они работают рядом, но не заменяют друг друга.

2. `Hutchins (1995)` оставлен как отдельная book-level запись без попытки слить его с Norman/Scaife/Risko.

   Это фундамент distributed cognition, а не просто еще один источник про external cognition.

3. `Gilbert (2015a)` и `Gilbert (2015b)` подтверждены как разные публикации.

   Первая запись про offloading delayed intentions, вторая - про strategic reminders and metacognitive confidence. Буквенные суффиксы нужны и сохраняются.

4. `Bandura (1977)` и `Bandura (1997)` оставлены как статья и монография.

   Статья вводит self-efficacy как теоретический мост к поведенческим изменениям; книга дает полный аппарат exercise of control и источники самоэффективности.

5. `McClelland (1961)` и `McClelland (1987)` оставлены как разные источники.

   _The Achieving Society_ нужен для культурно-исторического слоя мотива достижения. _Human Motivation_ - операционная карта мотивов achievement, affiliation, power and avoidance. Финальное стилевое решение закрыто в style-note pass: запись оставлена как `1987/1988`, потому что Cambridge Core фиксирует original publication in 1987 and print publication date 1988.

6. SDT-блок не является дублем.

   `Deci & Ryan (2000)` и `Ryan & Deci (2000)` - разные статьи 2000 года; `Ryan & Deci (2017)` - книга; `Ryan & Deci (2020)` - позднее уточнение intrinsic/extrinsic motivation; `Ryan (Ed.) (2023)` - handbook. Раздел 7 отдельно хранит рабоче-организационные SDT-источники.

7. Линия controllability/learned helplessness оставлена развернутой.

   `Seligman & Maier (1967)`, `Amat et al. (2005)`, `Maier & Seligman (2016)`, `Baratta et al. (2023)`, `Limbachia et al. (2021)` и `Tafet & Ortiz Alonso (2025)` покрывают разные уровни: исходный эксперимент, животный механизм mPFC/DRN, обзор learned helplessness at fifty, обзор resilience/controllability, human neuroimaging и свежую перспективу. Это тематическая цепочка, не дубли.

8. Нейромодуляторные и стрессовые источники раздела 3 оставлены как отдельный уровень механизма.

   `Arnsten (2009)`, `Robbins & Arnsten (2009)` и `Cools & Arnsten (2022)` не сливаются: стрессовые пути PFC, fronto-executive monoaminergic modulation and modern PFC neuromodulation review имеют разные роли.

9. Аллостаз и интероцепция оставлены несколькими записями.

   `McEwen (1998)` и `McEwen & Wingfield (2003)` разводят stress mediators/allostatic load и концепт allostasis. `Barrett & Simmons (2015)`, `Barrett (2017)`, `Seth (2013)`, `Seth & Friston (2016)` и `Zhang et al. (2025)` дают разные уровни interoceptive predictions, active inference and allostatic-interoceptive mapping.

10. Блок дофамина, усилия и выбора действия в разделе 3 не является дублированием мотивационного раздела.

    `Salamone & Correa (2024)`, `Treadway et al. (2009, 2012)`, `Frank (2025)`, `Lee et al. (2024)`, `Mohebi et al. (2024)`, `Greenstreet et al. (2025)` и `Tsutsui-Kimura et al. (2025)` оставлены как разные empirical/review/computational/circuit-level sources. Они должны использоваться с разными evidence labels.

## Принятые решения

- Разделы 1-3 оставлены тематическими, а не превращены в строго алфавитный единый список.
- В разделе 3 добавлена явная навигационная пометка: пересечение с разделами 1-2 допустимо, если источник добавляет нейросхемный, нейромодуляторный, аллостатический или интероцептивный уровень объяснения.
- `Следующий библиографический проход` обновлен: закрытый пункт по разделам 1-3 вынесен в контрольную строку, следующие открытые пункты начинаются с раздела 4.
- Новых дублей для удаления в разделах 1-3 не найдено.

## Что остается открытым

- Раздел 4: сверить intervention sources с разделами 1-3.
- Раздел 5: сверить sleep/exercise/recovery sources с разделами 3-4.
- Раздел 7: сверить organizational/work-design sources с разделами 1, 2, 5 и 6.
- Общая нормализация style notes перед reader edition.
- Финальная current-version проверка official/guideline resources перед публикацией.
