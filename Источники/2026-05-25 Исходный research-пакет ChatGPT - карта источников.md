# Исходный research-пакет ChatGPT - карта источников

## Статус материала

Дата фиксации: `2026-05-25`.

Источник: пользователь передал результат исследования, выполненного через ChatGPT по существующим материалам направления "Когнитивное инженерство".

Роль: сырой входной материал для учебника. Эта заметка сохраняет исходную карту источников, тем, подтем и редакционных принципов. Рабочая переработанная карта лежит в [[2026-05-24 Карта источников для большого учебника]], а учет проверки источников ведется в [[00-Реестр-библиографии]].

Важное ограничение: ссылки вида `turn...` в исходном тексте являются следами внешнего поиска ChatGPT, а не проверенными библиографическими ссылками внутри vault. Их нельзя переносить в учебник как источники. Перед использованием нужно найти первоисточник, проверить авторов, год, название, место публикации и уровень доказательности.

Решение по использованию: материал принят в работу как источниковый backlog и как управляющая карта переработки первоисточников для большого многоглавного, потенциально многотомного учебника.

## Исходный текст research-пакета

# Карта источников для большого учебника по когнитивному инженерству

## Как ваши текущие тексты складываются в цельный учебник

По приложенным черновикам уже видна не россыпь отдельных статей, а довольно стройная линия: от произвольного внимания, прокрастинации и саморегуляции — к мотивации как многослойной системе; дальше — к управляемости действия, привычкам, усталости и восстановлению; затем — к воспитанию способности делать трудное; и, наконец, к прикладному уровню знания-работы разработчика, где в игру входят внешняя память, прерывания, контекст, неопределённость и ИИ.

Из этого хорошо собирается не просто цикл статей, а самодостаточный учебник по **когнитивному инженерству** как дисциплине о том, как человек проектирует свои действия, рабочую среду, инструменты и режимы, чтобы мозг чаще выбирал нужную политику действия: сосредоточение, усилие, выдерживание неопределённости, восстановление, а не избегание, распад контекста и пассивное потребление. Для такого учебника особенно важна явная связка между теорией, механизмом и техникой вмешательства: от описания мотивации и саморегуляции — к инженерным приёмам изменения среды, ритмов, интерфейсов и привычек. Современные обзоры по behavior change и по “boosting” как подходу, усиливающему агентность, а не просто “подталкивающему” поведение, дают для этого хорошую надстройку. citeturn26search5turn26search10turn16search14

Ниже — список источников не “вообще по теме”, а именно в том ключе, который поможет превратить текущий корпус в большой учебник.

## Фундаментальная рамка, на которой стоит строить весь учебник

Здесь нужны работы, которые задают **язык** учебника: что такое мотив, что такое саморегуляция, как соотносятся мозг, тело, среда и действие, и почему любое поведение стоит рассматривать не как “силу воли”, а как результат работы нескольких конкурирующих систем.

**David C. McClelland, _Human Motivation_ (1987).** Для вашего корпуса это один из самых точных “стержневых” источников, потому что Макклелланд разбирает не только achievement, affiliation и power, но и avoidance как отдельную мотивационную систему. Именно отсюда удобно строить первую часть учебника — не как популярную типологию, а как рабочую карту мотивов, которые по-разному организуют внимание, оценку успеха, выбор среды и переживание угрозы. citeturn5search0turn5search16

**David C. McClelland, _The Achieving Society_ (1961).** Это уже не “операционная карта”, а культурно-историческая рамка: как achievement motive связывается с достижением, институтами и развитием. Для учебника это полезно как источник для главы о том, почему общество, воспитание и экономическая среда меняют не только поведение, но и структуру желаемого. citeturn5search1turn5search18

**Richard Ryan & Edward Deci, “The ‘What’ and ‘Why’ of Goal Pursuits” (2000); “Self-Determination Theory and the Facilitation of Intrinsic Motivation...” (2000); Ryan & Deci (2020, 2022).** Эти тексты нужны не как замена Макклелланду, а как вторая ось: autonomy, competence, relatedness как условия устойчивой, нераспадающейся мотивации. В вашем учебнике SDT особенно полезна в главах о воспитании самостоятельности, о поддержке мотивации в обучении и о том, как строить рабочую среду так, чтобы не ломать автономию и компетентность. citeturn4search10turn4search0turn4search6turn4search18turn4search12

**Roy Baumeister & Mark Leary, “The Need to Belong” (1995).** Этот источник стоит использовать как фундамент для разделов о принадлежности, одиночестве, социальной регуляции и “цене” изоляции. Он позволяет показать, что принадлежность — не мягкая факультативная надстройка, а базовый мотив, который меняет эмоции, внимание и поведение. citeturn24search3turn24search0

**Albert Bandura, “Self-Efficacy: Toward a Unifying Theory of Behavioral Change” (1977) и _Self-Efficacy: The Exercise of Control_ (1997).** Если Макклелланд отвечает на вопрос “чего человек хочет”, то Бандура отвечает на вопрос “верит ли он, что способен это сделать”. Для вашего учебника это критично: именно self-efficacy связывает мотивацию, управляемость действия и опыт преодоления. Особенно важны четыре источника самоэффективности: mastery experiences, vicarious experiences, verbal persuasion, physiological/affective states. citeturn3search2turn3search0turn3search17

**A. Pfitzner-Eden et al. (2016) и V. Egele et al. (2025).** Эти более поздние работы нужны как мост от теории Бандуры к современным данным: они подтверждают структуру источников самоэффективности, а mastery experience снова и снова оказывается наиболее весомым. Для вашей главы “Опыт преодоления” это почти обязательный эмпирический каркас. citeturn2search4turn2search7turn3search18

**Marlon Quirin et al., “Dynamics of Personality: The Zurich Model of Social Motivation” (2023).** Это не канонический стержень учебника, а хороший дополнительный теоретический источник, если вы захотите глубже проработать различие социальных мотивов — привязанности, статуса, власти, защиты — и связать их с личностной динамикой. citeturn6search0turn24search13

**David Badre, “Cognitive Control” (2025).** Это современный большой обзор того, как исследователи понимают когнитивный контроль сегодня. Он нужен вам, чтобы всю линию про волю, внимание и управляемость действия не строить на старых клише, а опереться на актуальный язык cognitive control. citeturn8search5turn16search0

**Adele Diamond, “Executive Functions” (2013).** Это один из лучших обзорных текстов для главы о произвольности: рабочая память, торможение, когнитивная гибкость, а также их значение для обучения, адаптации и поведения. В учебнике его стоит использовать как “вход” в тему ещё до нейронных схем. citeturn11search1turn27search8

**Roshan Cools & Amy Arnsten, “Neuromodulation of Prefrontal Cortex Cognitive Function in Health and Disease” (2022).** Нужен для того, чтобы язык “воли” и “внимания” был связан с действительной ролью дофамина, норадреналина и префронтальной коры, а не с популярными упрощениями. Это хороший опорный обзор для глав о состоянии, контроле и уязвимости при стрессе. citeturn2search11

**Bruce McEwen: “Stress, Adaptation, and Disease: Allostasis and Allostatic Load” (1998), “The Concept of Allostasis in Biology and Biomedicine” (2003), последующие обзоры.** Это база для одной из важнейших ваших идей — объяснять поведение через “цену состояния”. Аллостатическая нагрузка даёт учебнику язык, на котором можно связывать стресс, истощение, восстановление, хроническое напряжение и снижение управляемости. citeturn7search0turn7search11turn7search17turn7search19

**Lisa Feldman Barrett & W. Kyle Simmons, “Interoceptive Predictions in the Brain” (2015), Barrett (2016) и Seth & Friston / Seth (2016).** Эти тексты нужны, если вы хотите сделать учебник не только психологическим, но и по-настоящему мозго-телесным: как мозг предсказывает состояние тела, как интероцепция влияет на субъективную “стоимость” действия, и как из этого вырастают fatigue, avoidance, urgency и perceived effort. citeturn7search1turn34search3turn34search2

**J. Zhang et al., “Cortical and Subcortical Mapping of the Human Allostatic–Interoceptive System” (2025).** Это уже не базовая теория, а очень сильный современный материал для иллюстрации вашей системной схемы: сеть allostasis/interoception реально картируется и связывает salience network, default mode, cingulate, insula, brainstem. Очень полезно для зрелой, поздней редакции учебника. citeturn34search1

## Внимание, прокрастинация, воля и саморегуляция

Здесь нужен корпус, который позволяет показать: прокрастинация — это не “лень”, а специфический режим саморегуляционного сбоя; внимание — не прожектор по команде, а функция конкурирующих систем; а то, что в быту зовут “силой воли”, лучше объяснять через контроль, приоритизацию и организацию среды.

**Fuschia Sirois & Timothy Pychyl, “Procrastination and the Priority of Short-Term Mood Regulation” (2013), плюс Fuschia Sirois, “Procrastination and Stress” (2023).** Эти тексты почти обязательны для вашей первой линии статей. Они позволяют показать, что прокрастинация часто выступает как дешёвая регуляция неприятных эмоций “здесь и сейчас”, а в стрессовых контекстах риск прокрастинации возрастает из-за истощения coping resources и снижения терпимости к негативным состояниям. citeturn22search0turn19search16

**Piers Steel, “The Nature of Procrastination” (2007).** Классический метааналитический и теоретический обзор. Очень полезен как источник для глав, где вы хотите аккуратно свести вместе импульсивность, временную дисконтировку, self-regulatory failure и индивидуальные различия. citeturn22search2

**Shlomo Zacks & Meirav Hen, “Academic Interventions for Academic Procrastination” (2018).** Нужен не как теория, а как обзор практик: он показывает, что эффективные вмешательства должны работать и с ситуацией, и с дефицитами саморегуляции, а не только с уговариванием. Хороший источник для главы о практиках преодоления прокрастинации. citeturn22search4

**Daniel Gustavson & Akira Miyake, “Academic Procrastination and Goal Accomplishment” (2017).** Полезен именно тем, что показывает: простые SMART-goals и implementation intentions не всегда автоматически решают проблему, хотя исходный уровень прокрастинации хорошо предсказывает провал в достижении целей. Это важное противоядие против упрощённых рецептов. citeturn22search1

**Sheng Zhang et al., “To Do It Now or Later” (2019).** Хороший связующий источник между нейроэкономикой, прокрастинацией и мотивацией избегания: помогает объяснить, почему при откладывании асимметрично меняются мотивация действовать и мотивация избегать. citeturn22search5turn23search7

**Peter Gollwitzer, Paschal Sheeran и др.: современная линия по if-then planning / implementation intentions, включая “Psychology of Planning” (2025) и мета-анализ 2024.** Эти работы особенно нужны для вашего учебника, потому что они переводят волю в инженерный язык: не “постарайся”, а “если X, то Y”; не общая мотивация, а, по сути, прошивка переключений внимания и поведения. Важно, что современные обзоры связывают if-then planning не только с поведением, но и с attention control, prospective memory, executive functions и decision making. citeturn26search18turn26search13turn26search2

**Amitai/various chapters in _The Handbook of Behavior Change_ (planning, action phases, SDT, habits).** Этот сборник нужен как практический “мост” между психологической теорией и инженерным конструированием вмешательств. Для учебника он полезен не целиком, а как библиотека техник и терминов. citeturn26search5turn26search2turn17search18turn26search20

**Nash Unsworth, “A Locus Coeruleus–Norepinephrine Account of Individual Differences in Working Memory Capacity and Attention Control” (2017); Sara (2012); Aston-Jones & Cohen (классическая теория adaptive gain).** Этот блок нужен для вашей нейрофизиологии фокуса: он помогает объяснить, почему внимание и устойчивость контроля зависят не только от “лобных долей”, но и от LC-NE systems, arousal и режима neural gain. citeturn19search5turn31search1turn31search7turn31search12

**Michael Kane et al., “For Whom the Mind Wanders, and When” (2007), и Mooneyham & Schooler, “The Costs and Benefits of Mind-Wandering” (2013).** Нужны для аккуратной главы о рассеянии: mind wandering нельзя описывать только как дефект, но и романтизировать его нельзя. Эти источники хорошо поддерживают мысль, что рабочая память и executive attention особенно важны там, где задача требует усилия и удержания контекста. citeturn19search9turn19search12

**Adele Diamond (2013) + Best (2010).** В связке это хороший учебный блок о том, как развиваются executive functions и почему “воля” — это не единая субстанция, а сочетание торможения, рабочей памяти и гибкости, которые ещё и меняются по возрасту. citeturn27search0turn27search8

**Интервенции: exercise, mindfulness, sleep, стимуляторы, БАДы.** Здесь учебнику нужен не один источник, а иерархия доказательств. Физическая активность имеет довольно устойчивую поддержку на уровне мета-анализов по когнитивным функциям и executive function, тогда как mindfulness показывает полезные эффекты, но гораздо более гетерогенно, в зависимости от дизайна, выборки и исхода. По omega-3 выводы пока смешанные и не тянут на универсальную рекомендацию; по caffeine эффекты на alertness и attention вполне реальны, но контекст-зависимы и особенно заметны при усталости и недосыпе. Для вашей линии про “нейротренировку” это означает: главу об интервенциях лучше строить по шкале прочности доказательств, а не по яркости обещаний. citeturn28search4turn28search0turn28search1turn28search5turn28search2turn28search14turn28search3turn28search11turn28search19

## Мотивация, усилие, избегание, истощение и восстановление

Это, судя по вашим файлам, уже центральное ядро проекта. Здесь стоит собрать источники, которые помогут показать, что мотивация — это не “желание” вообще, а вычисление ценности, усилия, риска, контролируемости, состояния тела и социальных последствий.

**Ryan & Deci (2000, 2020, 2022) + Morris et al., “On What Motivates Us” (2022).** Этот набор нужен для главы, где вы разводите intrinsic/extrinsic motivation и показываете, что мотивация — не единый континуум. Morris et al. особенно полезна как современная обзорная статья по концептуализации, измерению и нейробиологии внутренней мотивации. citeturn4search0turn4search6turn4search18turn4search5

**John Salamone & Mercè Correa, “The Neurobiology of Activational Aspects of Motivation” (2024).** Это один из самых важных источников для ваших частей II–III. Он помогает очень точно объяснить, что дофамин важен не как “вещество удовольствия”, а как часть систем, связанных с effort expenditure, effort-based decision making и готовностью платить цену за результат. На нём хорошо строить главу о различии между “хочу награду” и “готов двигаться к награде”. citeturn9search2turn9search5turn9search8

**Michael Treadway: EEfRT (2009), effort-based decision making in depression (2012), translational review (2013).** Эти работы нужны для связывания лабораторной модели усилия с everyday self-regulation. Они особенно хороши, если вы хотите показать, что утрата мотивации часто выражается не как отсутствие ценности самой награды, а как завышенная субъективная цена достижения. citeturn16search4turn16search1turn16search7

**Masud Husain & Michael Browning/Roiser, “Neuroscience of Apathy and Anhedonia” (2018); Costello, Husain & Roiser (2024).** Эти тексты полезны для зрелой, медицински аккуратной главы о состояниях, где распадается activational component of motivation. Они хорошо защищают ваш проект от бытового морализма: иногда проблема не в “слабом характере”, а в сломанной экономике усилия. citeturn16search2turn9search17turn9search19

**Michael Frank, “Adaptive Cost-Benefit Control Fueled by Striatal Dopamine” (2025).** Это сильный современный обзор, который полезен, если вы хотите превратить ваши схемы из популярного объяснения в серьёзную computationally informed рамку. Особенно ценен для глав о выборе между усилием, привычкой, контролем и уходом. citeturn8search8turn16search11

**Rachel Lee, Yotam Sagiv & Nathaniel Daw, “A Feature-Specific Prediction Error Model Explains Dopaminergic Heterogeneity” (2024).** Этот текст нужен вам как защита от упрощения “дофамин = один общий сигнал”. Если учебник претендует на серьёзность, стоит прямо показывать, что допаминергические сигналы гетерогенны и кодируют не одну-единственную “ценность”. citeturn20search0turn20search2

**Francesca Greenstreet et al., “Dopaminergic Action Prediction Errors Serve as a Value-Free Teaching Signal” (2025).** Это важный источник для главы о привычках: он показывает, что часть допаминергического обучения может усиливать повторение действия как такового, а не только обучение ценности результата. Для вашей темы “управляемости действия” это очень сильный аргумент. citeturn20search1turn20search5turn20search12

**Iku Tsutsui-Kimura et al., “Dopamine in the Tail of the Striatum Facilitates Avoidance in Threat–Reward Conflicts” (2025).** Очень релевантная работа для вашей линии про угрозу, избегание и конфликт “цель–опасность”. Она особенно полезна для уточнения, что avoidance — не просто отсутствие approach, а отдельная активная политика действия с собственной нейронной архитектурой. citeturn8search1turn8search7

**Antonio Mohebi et al., “Dopamine Transients Follow a Striatal Gradient...” (2024).** Полезно для более продвинутой редакции главы о стриатуме: разные зоны стриатума работают на разных временных горизонтах оценки. Это хорошо стыкуется с вашей идеей про привычку, быстрые реакции и долгий контроль. citeturn20search17

**Z. Ben-Zion et al., “Representation of Anticipated Rewards and Punishments in the Human Brain” (2025).** Это хороший обзор для соединения reward/ punishment/ anticipated cost в одной рамке. Особенно полезен, если вы захотите написать сильную синтезирующую главу о том, как мозг кодирует ожидаемые выгоды и потери до действия. citeturn9search11turn16search9

**Tobias Müller et al., “Neural and Computational Mechanisms of Momentary Fatigue” (2021).** Для вашей идеи “истощения” это почти идеальный источник: он различает recoverable fatigue и slower unrecoverable fatigue, обе из которых снижают готовность вкладывать усилие. Это даёт учебнику очень хороший язык для разговора о коротком отдыхе, накоплении усталости и ложных моральных интерпретациях. citeturn9search0turn10search16

**WHO: burnout as an occupational phenomenon, ICD-11; Sonnentag et al., “Recovery from Work” (2022).** На этом блоке удобно строить раздел о выгорании и восстановлении. Важно, что ВОЗ определяет burnout как occupational phenomenon, а не как общую болезнь “от жизни”; это помогает не растягивать термин на всё подряд. Sonnentag даёт сильную научную опору для разговора о work breaks, detachment, evenings, weekends, vacations и режиме восстановления. citeturn21search4turn9search4turn21search3turn35search8

**Sleep / circadian / cognition: Cao et al. (2025), Cajochen & Schmidt (2025), Wüst et al. (2024), Killgore (2010).** Эти источники нужны для главы, где вы хотите доказательно показать, что снижение сна бьёт по working memory, inhibitory control, sustained attention и cognitive flexibility, а циркадная организация влияет на когнитивную эффективность не менее серьёзно, чем “мотивация”. Для вашего проекта это важно ещё и потому, что “не могу собраться” часто маскирует банальную state problem. citeturn11search9turn31search6turn11search13turn11search17turn11search21

**HRV / neurovisceral integration: Thayer & Lane (2000), Smith et al. (2017), Magnon et al. (2022), Tinello et al. (2022).** Это хороший комплект, если вы хотите аккуратно включить автономную регуляцию в учебник. Он помогает показать, как vagal control, prefrontal function, emotion regulation и executive functioning связаны друг с другом, и где HRV действительно полезен как индикатор, а где начинаются уже маркетинговые перегибы. citeturn12search1turn12search9turn12search3turn12search20turn12search17

**McEwen + Barrett + Zhang (allostasis/interoception).** Для вашего термина “аллостатический бюджет” этого набора достаточно: аллостатическая нагрузка — это кумулятивная цена постоянной адаптации; интероцептивные модели помогают объяснить, почему цена состояния чувствуется до осознанного решения; а современные карты allostatic-interoceptive system позволяют вывести это из разряда метафоры в разряд объяснительной модели. citeturn7search0turn7search11turn7search13turn7search1turn34search3turn34search1

## Управляемость, привычки, самоэффективность и опыт преодоления

Этот блок особенно важен для того, чтобы ваш учебник не свалился в популярную “мотивационную” литературу. Здесь требуется показать, как человек становится способным делать трудное: не лозунгами, а через контролируемость, опыт успеха, формирование привычек, ко-регуляцию и возрастно-адекватную поддержку.

**Albert Bandura (1977, 1997) + эмпирические источники по источникам self-efficacy.** Ваша глава “Опыт преодоления” практически просит построить её на Бандуре. Делать трудное человек учится прежде всего через mastery experiences; остальные факторы работают, но слабее и чаще как поддержка. Это стоит сделать центральной идеей раздела о выращивании способности к усилию. citeturn3search2turn3search0turn2search4turn2search7

**Mark Baratta et al., “From Helplessness to Controllability” (2023), Limbachia et al. (2021), Tafet & Nemeroff (2025).** Этот набор нужен для вашей части III и для всей линии про управляемость. Он помогает показать, что не только uncontrollable stress делает helplessness-подобные последствия, но и сам опыт контроля активным образом защищает систему, уменьшая threat-related responses, включая anterior insula и BNST. Это сильная нейробиологическая опора для тезиса, что человеку нужен опыт реального воздействия на ситуацию. citeturn2search3turn2search5turn2search6

**Wendy Wood: “A New Look at Habits and the Habit–Goal Interface” (2007), “Psychology of Habit” (2016), “Habit in Personality and Social Psychology” (2017).** Для вашего учебника это must-read. У Вуд привычка — не просто “бессознательная рутина”, а особый режим контроля, который опирается на стабильные cue-behavior associations и тесно переплетён с целями. Это идеальный материал для разведения goal-directed action и habit. citeturn26search8turn26search1turn26search4

**Tom Smeets et al., “Does Stress Consistently Favor Habits over Goal-Directed Control?” (2023).** Очень важный корректирующий источник. В популярном изложении легко сказать: “стресс переводит человека в привычки”. Этот обзор показывает, что картина сложнее и эффект не столь универсален. Для учебника это ценно как защита от соблазна объяснять всё одной формулой. citeturn8search0

**S. Nebe et al., “Characterizing Human Habits in the Lab” (2024).** Полезно для раздела о том, почему привычки трудно чисто измерять у людей и почему человеческие привычки не всегда сводятся к животным моделям. Это делает главу о привычках методологически зрелой. citeturn8search12

**Robert & Elizabeth Bjork: “Creating Desirable Difficulties...” (2011), “Desirable Difficulties in Theory and Practice” (2020), Nelson et al. (2023), Soderstrom & Bjork (2015).** Это база для вашей главы о тренировке преодоления. Суть, которую стоит взять: трудность полезна не сама по себе, а когда она запускает процессы кодирования и извлечения, поддерживающие долговременное обучение. В учебнике это удобно конвертировать в принцип “дозированного трения”: препятствие должно быть не парализующим, а развивающим. citeturn18search0turn18search4turn18search2turn17search4turn18search5

**Roediger & Butler, “The Critical Role of Retrieval Practice in Long-Term Retention” (2011).** Очень нужен, если вы хотите сделать раздел о формировании устойчивых навыков и преодоления практичным. Retrieval practice — один из самых надёжных механизмов перевода хрупкого знания в рабочую компетентность. citeturn17search8

**Stress inoculation training: Meichenbaum line; Saunders et al. (1996) и обзоры.** Для подростков и взрослых это важная связка: учить преодолению не через “брось себя в холодную воду”, а через контролируемую, пошаговую экспозицию к напряжению с навыками переработки. Для вашего учебника это может стать мостом между нейрофизиологией угрозы и реальной психологической тренировкой. citeturn17search5turn17search1

**Развитие self-regulation у детей и подростков: Best (2010), Duckworth & Carlson (глава о school success), Obradović et al. (2021), Blair (2008), co-regulation review (2023).** На этом наборе удобно строить возрастную арку вашей статьи “Опыт преодоления”: в раннем возрасте нужны scaffolded routines, responsive parenting и co-regulation; позже — автономная практика, постепенный перенос контроля внутрь и поддержка competence. Важно, что сильная поддержка не равна гиперопеке: данные показывают, что parental over-engagement может ухудшать self-regulation. citeturn27search0turn27search2turn27search3turn27search16turn27search7

**Ryan & Deci по autonomy support в семье и школе.** Нужны, чтобы developmental chapter не превратился в чисто executive-function account. Воспитание способности делать трудное — это не только тренировка inhibition, но и поддержка автономии, связности, смысла и отношений. citeturn17search3turn17search7turn17search12turn17search18

**Growth mindset meta-analyses (Burnette et al., 2020; 2023).** Эти источники можно включить, но не как стержень, а как дополнительный раздел о belief-level interventions. Их лучше подавать осторожно: mindset имеет эффект, но не должен замещать chapters про mastery, controllability и structured practice. citeturn17search9turn17search13turn17search6

## Внешняя когниция, работа разработчика, прерывания, контекст и ИИ

Это та часть, которая может сделать ваш учебник действительно оригинальным: не просто пересказ когнитивной науки, а перенос её на knowledge work и инженерную деятельность.

**Edwin Hutchins, _Cognition in the Wild_ (1995).** Это фундамент для всей вашей идеи “рабочего журнала как внешней памяти”. Хатчинс позволяет вывести мышление за пределы черепа и показать, что когнитивная система включает людей, артефакты, записи, процедуры и среду. Для вашего проекта это один из важнейших источников. citeturn14search0turn14search20

**Donald Norman, _Things That Make Us Smart_ и текст о cognitive artifacts.** Норман нужен там, где вы переходите от психологии к дизайну. Его идея проста и мощна: хорошие внешние представления не просто хранят информацию, они меняют сложность задачи. Это прямо ложится на ваши идеи о рабочем журнале, структуре заметок, шаблонах входа в задачу и дефолтных интерфейсах. citeturn14search2turn14search6

**Mary Scaife & Yvonne Rogers, “External Cognition: How Do Graphical Representations Work?” (1996).** Очень полезный источник для объяснения, почему диаграммы, схемы, чек-листы, таймлайны и карты задач действительно помогают думать, а не просто “украшают” мысль. Хороший теоретический каркас для главы о внешних представлениях. citeturn14search1turn14search9turn14search21

**Evan Risko & Sam Gilbert, “Cognitive Offloading” (2016).** Это ключевой обзор для всех ваших прикладных глав. Он даёт и определение, и структуру вопроса: когда человек выгружает когнитивную работу наружу, какие механизмы запускают это решение, и каковы последствия offloading. citeturn13search0

**Sam Gilbert: “Strategic Offloading of Delayed Intentions...” (2015), “Optimal Use of Reminders” (2020), “Outsourcing Memory to External Tools” (2023), свежие работы о metacognitive training (2026).** Это почти готовая научная база под ваши идеи о TODO, рабочем журнале, заметках-возобновителях и построении контекстов возвращения. Особенно ценно, что Gilbert показывает: offloading guided by metacognition, reminders highly effective, but people systematically use them suboptimally. Это очень “когнитивно-инженерный” материал. citeturn25search12turn25search3turn25search2turn25search24

**Altmann & Trafton tradition: interruption lag, memory for goals; Monk et al. (2008), Morgan et al. (2013), Foroughi et al. (2016).** Эти работы нужны для раздела о прерываниях и мучительном разогреве после паузы. They show, в сущности, что после interruption задача не “ждёт нас в памяти”, а требует повторного восстановления goal state, и что небольшой interruption lag или cueing может заметно помочь возобновлению. citeturn13search2turn13search9turn13search12

**Mary Czerwinski et al., “A Diary Study of Task Switching and Interruptions” (2004).** Хороший классический источник для общей главы о том, как knowledge workers реально перемежают задачи и почему переключение — это не безболезненный micro-event, а кумулятивный когнитивный расход. citeturn13search11

**Chris Parnin et al., “Resumption Strategies for Interrupted Programming Tasks” (2010) и “Evaluating Cues for Resuming Interrupted Programming Tasks” (2010).** Это прямые источники для вашей внешней статьи о разработчике. Они дают именно тот материал, который нужен: как разработчики возвращаются к незавершённой работе, какие cues помогают, и как можно проектировать better resumption support. citeturn25search1turn25search23

**A. Tregubov et al. (2017), “Impact of Task Switching and Work Interruptions on Software Development”; Y. Ma et al. (2024), “Breaking the Flow”; работы по focus support и interruptibility.** Это блок уже не про общую психологию, а про software engineering. Он позволяет связать ваш тезис про “туманные задачи” и “потерю контекста” с данными именно из мира разработки. citeturn13search1turn13search14turn13search5turn13search16turn25search11turn25search14

**Cognitive load in software development: Duran et al. (2022), Peitek et al. (2021), Fritz/Sharafi line, measurement reviews.** Эти источники нужны для главы о том, как код, сложность, лексика, архитектура и размер контекста бьют по рабочей памяти. Они помогают сделать ваш developer-focused раздел не просто житейским, а исследовательски обоснованным. citeturn13search7turn13search21turn25search0turn25search22turn25search8

**Risko/Gilbert + Hutchins/Norman + Gilbert reminder studies.** Это тот набор, на котором можно строить вашу центральную инженерную идею: рабочий журнал — это не “продуктивность ради продуктивности”, а deliberate externalization of state, goals, assumptions, next-entry cues and resumption anchors. citeturn13search0turn14search0turn14search2turn25search12turn25search3

**ИИ и разработка: Sida Peng et al. (2023) controlled experiment with Copilot; K. Cui et al. / MIT field experiments (2025); Google RCT on AI-enhanced code features (2024).** Эти работы нужны, чтобы писать об ИИ трезво. Controlled experiment with Copilot показал ускорение на лабораторной задаче, field experiments на тысячах разработчиков показали рост pull requests и других метрик в реальной работе, а Google RCT изучал enterprise-grade task with randomized access to tools. Это хороший минимум для главы “ИИ как внешний когнитивный контур”. citeturn29search4turn32search1turn32search11turn29search0

**Hou et al., “Large Language Models for Software Engineering” (2023) и Terragni et al., “The Future of AI-Driven Software Engineering” (2025).** Для учебника это полезно как обзорный и дорожный блок: что именно делает ИИ в software engineering today, где границы, какие классы задач затронуты, и какие новые роли остаются за человеком. citeturn29search6turn29search3turn29search17

**Dell’Acqua et al., “Navigating the Jagged Technological Frontier” (2023/2024).** Это один из лучших источников для вашей авторской мысли о том, что ИИ не просто “ускоряет всё”, а помогает вдоль неровной границы применимости: на одних задачах усиливает качество и скорость, на других — ухудшает результат. Для учебника это важнейший антиутопический и антинеоромантический баланс. citeturn33search6turn33search11turn33search17

**Parasuraman & Manzey (2010), Goddard et al. (2012), Lee & See (2004), Hoff & Bashir (2015).** Этот корпус нужен, чтобы раздел об ИИ не свёлся к “полезный/вредный”. Основная рамка здесь — automation bias, complacency, trust calibration, appropriate reliance. Для вашего учебника это особенно важно: когнитивное инженерство должно учить не просто пользоваться ИИ, а поддерживать skill maintenance и уровни проверки. citeturn15search0turn15search4turn30search0turn30search9turn15search8

**Дискуссия о offloading, hollowing-out и deskilling в эпоху ИИ: концептуальные работы 2025–2026.** Это не самый твёрдый эмпирический блок, но его стоит включить в конце как раздел “предупреждение и дизайн-принцип”. Современные обзоры уже обсуждают psychological costs of AI-era offloading, foundational knowledge erosion и risk of deskilling. В учебнике их лучше подавать как emerging concerns, а не как уже закрытый научный вердикт. citeturn15search1turn15search5turn15search13turn15search21turn30search14

## Как я бы расставил приоритеты чтения и переработки

Если цель — не просто накопить библиографию, а быстро собрать **большой цельный учебник**, я бы делал это в таком порядке.

Сначала — **каркас понятий**. Для него я бы полноценно прочитал Макклелланда, Райана и Деси, Бандуру, Баумейстера и Лири, Макьюэна, Барретт/Сета и Badre/Diamond. Это даст общий язык: мотивы, потребности, self-efficacy, принадлежность, allostasis, executive control. Без этого дальнейшие главы рискуют остаться набором умных, но несвязанных тем. citeturn5search0turn4search10turn3search2turn24search3turn7search0turn34search3turn8search5turn27search8

Потом — **механика действия**. Здесь нужны Salamone, Treadway, Frank, Wood, Baratta/Maier, Sirois/Pychyl, Gollwitzer. Это уже даёт скелет глав о том, как мозг выбирает между усилием, избеганием, привычкой, контролем и восстановлением; почему прокрастинация возникает; что делает controllability; как планирование переводит намерение в действие. citeturn9search2turn16search1turn8search8turn26search1turn2search3turn22search0turn26search18

Третьим шагом я бы собрал **главы об интервенциях**, но только с явной градацией уверенности. Сильнее всего выглядят sleep/exercise/planning/retrieval practice/external reminders/work recovery; более смешанные зоны — mindfulness, HRV-biofeedback, omega-3 и особенно любые “нейротренинговые” обещания, если они выходят за пределы умеренных, проверяемых эффектов. Это место, где учебнику нужна не энциклопедия советов, а строгая редакционная политика по evidence quality. citeturn11search9turn28search4turn26search13turn17search8turn25search2turn21search3turn28search1turn28search2

После этого можно писать **прикладные тома или разделы**: “Опыт преодоления” и “Когнитивное инженерство разработчика”. Там научный материал уже будет не висеть в воздухе, а ляжет на понятную основу: controllability, self-efficacy, desirable difficulties, distributed cognition, interruption recovery, AI calibration. citeturn2search3turn3search2turn18search0turn14search0turn25search1turn30search0

Есть и несколько редакционных принципов, которые я бы сделал для всего учебника обязательными.

Во-первых, **не сводить сложные темы к одному медиатору**: “дофамин = мотивация”, “норадреналин = внимание”, “серотонин = настроение” — слишком грубо для книги вашего замысла. Современная литература показывает гетерогенность допаминергических сигналов и сложную роль стриатальных, префронтальных и интероцептивных систем. citeturn20search0turn20search1turn8search8turn9search2

Во-вторых, **разводить уровни объяснения**: motive structure, state variables, control policy, learning history, environment design. Это поможет не путать, например, “у человека высока потребность в достижении” с “сейчас у него низкая готовность платить effort cost” или с “он живёт в среде, которая рвёт контекст”. citeturn5search0turn9search2turn26search1turn13search11

В-третьих, **говорить о развитии способности делать трудное через опыт и среду, а не через проповедь**. Самый надёжный язык здесь — mastery, controllability, autonomy support, graded challenge, retrieval and practice. citeturn2search4turn2search3turn17search18turn18search0turn17search8

В-четвёртых, **писать об ИИ как об эргономике и распределении когнитивной работы**, а не как о спасителе или враге. Хорошая рамка здесь: productivity gains exist, but they are task-dependent; trust must be calibrated; offloading has benefits and costs; skill retention requires intentional design. citeturn29search4turn32search1turn33search6turn30search0turn15search21

## Открытые вопросы и ограничения

Не все темы, затронутые в ваших текстах, одинаково хорошо покрыты одинаково сильными данными. Самые надёжные блоки — motivation/effort, self-efficacy, habits, implementation intentions, recovery from work, cognitive offloading, interruptions, exercise/sleep. Более осторожно стоит писать о mindfulness как универсальной “починке”, о БАДах и нейродобавках, о HRV как прямом инструменте улучшения воли, а также о широких выводах про long-term deskilling from AI: здесь данные есть, но степень уверенности заметно ниже или сильнее зависит от контекста. citeturn28search1turn28search2turn12search20turn15search21turn30search14

Кроме того, литература по ИИ и software engineering меняется очень быстро, и часть сильных эмпирических источников пока существует в виде working papers, arXiv-препринтов или недавно вышедших ACM-статей. Для учебника это не проблема, если пометить такие разделы как быстро меняющиеся и обновляемые. citeturn32search1turn29search0turn29search6turn29search3

Главное же ограничение — не научное, а композиционное: ваш будущий учебник должен очень чётко различать, где он **объясняет**, где **оценивает доказательства**, а где **предлагает инженерные решения**. Если эту трёхслойную структуру выдержать, ваш корпус уже сейчас вполне тянет не на набор статей, а на большой и редкий по целостности учебник.
