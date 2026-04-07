# 3 Жанровая адаптация (раздел 3)

**ФИО:** <Аксаков Андрей Валерьевич>  
**Группа:** <ДКИП-401гдрми>  
**Проект:** 2D Platformer Game Support System  
**Жанр:** 2D-платформер  
**Клиент:** Unity 2D  
**Backend:** Flask + MySQL  
**Дата:** <07.04.26>

---

## 3.1. Жанр

В рамках данного проекта выбрана жанровая адаптация под компьютерную игру в жанре 2D-платформер. Игрок управляет персонажем, проходит уровни, преодолевает препятствия, избегает ловушек, собирает игровые предметы, достигает контрольных точек и завершает уровень.

---

## 3.2. Единица процесса

- **Единица процесса:** `level_attempt`
- **Назначение:** единица процесса `level_attempt` представляет собой одну попытку прохождения уровня. Она необходима для фиксации старта и завершения уровня, записи результата, расчёта наград, обновления прогресса, статистики и лидерборда.
- **Ключевые endpoint'ы:**
  - `POST /api/v1/events`
  - `POST /api/v1/level/start`
  - `POST /api/v1/level/finish`
  - `GET /api/v1/profile`
- **Что является истиной на сервере:** клиент не должен присылать готовые значения наград, опыта, валюты и обновлённого прогресса как подтверждённый результат. Клиент передаёт только факты прохождения уровня, а сервер самостоятельно рассчитывает награды, обновляет прогресс и таблицу лидеров.

### 3.2.1. Связь с архитектурой
Игровой процесс проходит по контуру `Client → API → Auth → Business Logic → DB`.

Клиент Unity отправляет запрос на начало попытки прохождения уровня. Сервер создаёт запись о попытке в таблице `level_attempts` и при необходимости фиксирует событие в `game_events`.

Во время прохождения уровня клиент отправляет игровые события, например достижение чекпоинта, сбор монеты или гибель персонажа. Эти события записываются в `game_events`.

При завершении уровня клиент вызывает `POST /api/v1/level/finish`, сервер фиксирует итог прохождения, записывает результат в жанровые таблицы, рассчитывает награды, обновляет `player_progress`, `statistics_daily` и `leaderboard_scores`.

---

## 3.3. Жанровые таблицы (5)

### 1 `level_attempts` — попытки прохождения уровня
- **PK:** `id BIGINT AUTO_INCREMENT PRIMARY KEY`
- **Ключевые поля:**
  - `id`
  - `user_id`
  - `level_code`
  - `status`
  - `started_at`
  - `ended_at`
  - `client_version`
- **FK:**
  - `user_id → users.id`
- **Индексы и уникальности:**
  - `INDEX (user_id, started_at)`
  - `INDEX (level_code)`
  - `INDEX (status)`
- **CHECK/правила:**
  - `status` принимает значения `started`, `finished`, `failed`, `abandoned`

### 2 `level_results` — результаты прохождения уровня
- **PK:** `attempt_id BIGINT PRIMARY KEY`
- **Ключевые поля:**
  - `attempt_id`
  - `is_completed`
  - `score`
  - `duration_seconds`
  - `coins_collected`
  - `enemies_defeated`
  - `deaths_count`
- **FK:**
  - `attempt_id → level_attempts.id`
- **Индексы и уникальности:**
  - `PRIMARY KEY (attempt_id)`
  - `INDEX (score)`
- **CHECK/правила:**
  - `score >= 0`
  - `duration_seconds >= 0`
  - `coins_collected >= 0`
  - `enemies_defeated >= 0`
  - `deaths_count >= 0`

### 3 `level_checkpoints` — чекпоинты внутри попытки
- **PK:** `id BIGINT AUTO_INCREMENT PRIMARY KEY`
- **Ключевые поля:**
  - `id`
  - `attempt_id`
  - `checkpoint_code`
  - `reached_at_second`
  - `created_at`
- **FK:**
  - `attempt_id → level_attempts.id`
- **Индексы и уникальности:**
  - `INDEX (attempt_id)`
  - `INDEX (checkpoint_code)`
- **CHECK/правила:**
  - `reached_at_second >= 0`

### 4 `player_level_progress` — прогресс игрока по уровням
- **PK:** `id BIGINT AUTO_INCREMENT PRIMARY KEY`
- **Ключевые поля:**
  - `id`
  - `user_id`
  - `level_code`
  - `is_unlocked`
  - `is_completed`
  - `best_score`
  - `best_time_seconds`
  - `updated_at`
- **FK:**
  - `user_id → users.id`
- **Индексы и уникальности:**
  - `UNIQUE (user_id, level_code)`
  - `INDEX (user_id)`
- **CHECK/правила:**
  - `best_score >= 0`
  - `best_time_seconds >= 0`

### 5 `processed_events` — дедупликация событий
- **PK:** `id BIGINT AUTO_INCREMENT PRIMARY KEY`
- **Ключевые поля:**
  - `id`
  - `user_id`
  - `event_id`
  - `event_type`
  - `processed_at`
- **FK:**
  - `user_id → users.id`
- **Индексы и уникальности:**
  - `UNIQUE (user_id, event_id)`
  - `INDEX (user_id)`
  - `INDEX (event_type)`
- **CHECK/правила:**
  - `event_id` должен быть уникальным в пределах пользователя

---

## 3.4. События (6 event_type) + payload

> События записываются в `game_events` в полях `event_type` и `payload_json`.  
> В payload обязательно должен присутствовать идентификатор процесса, то есть `attemptId`.

### 1 event_type: `level_start` — начало попытки прохождения уровня
```json id="ce4dd2"
{
  "attemptId": 15,
  "levelCode": "level_01",
  "clientVersion": "1.0.0"
}

2) event_type: checkpoint_reached — достижение контрольной точки
{
  "attemptId": 15,
  "checkpointCode": "cp_02",
  "atSecond": 48
}

3) event_type: coin_collected — сбор монеты или игрового предмета
{
  "attemptId": 15,
  "coinId": "coin_18",
  "totalCoinsCollected": 12,
  "atSecond": 63
}

4) event_type: enemy_defeated — победа над врагом
{
  "attemptId": 15,
  "enemyCode": "slime",
  "totalEnemiesDefeated": 3,
  "atSecond": 80
}

5) event_type: player_death — гибель персонажа
{
  "attemptId": 15,
  "reason": "spikes",
  "checkpointCode": "cp_02",
  "atSecond": 97
}

6) event_type: level_finish — завершение попытки прохождения уровня
{
  "attemptId": 15,
  "isCompleted": true,
  "score": 1850,
  "durationSeconds": 142,
  "coinsCollected": 18,
  "enemiesDefeated": 6,
  "deathsCount": 1
}

3.5. Связка с ядром (обязательно)

В рамках жанровой адаптации 2D-платформера используются следующие таблицы ядра:

game_events — хранит все ключевые действия игрока во время прохождения уровня
processed_events — используется для защиты от повторной обработки одного и того же события
player_progress — хранит итоговое состояние игрока после завершения уровня
leaderboard_scores — используется для записи лучшего результата игрока в таблицу лидеров
statistics_daily — содержит агрегированную статистику игрока за день
Какие данные пишутся в player_progress при завершении процесса
xp — увеличивается на величину серверной награды
soft_currency — увеличивается на величину серверной награды
hard_currency — не изменяется в базовом сценарии
level — может быть увеличен при накоплении достаточного количества опыта
Как обновляется leaderboard_scores
board_code: platformer_score
season: 1
score: лучший результат игрока по очкам на уровне или в рамках сезона
Какие поля обновляются в statistics_daily
events_count
playtime_seconds
wins
losses
score_sum
3.6. Транзакция "итог → награда → прогресс → рейтинг"

При вызове POST /api/v1/level/finish сервер должен выполнять все критически важные действия атомарно в одной транзакции. Сначала проверяется существование попытки прохождения уровня, её принадлежность пользователю и статус started. Затем попытка переводится в состояние завершённой, а результат записывается в таблицу level_results.

После этого сервер рассчитывает награды и обновляет player_progress. Далее выполняется upsert в statistics_daily и leaderboard_scores. Только после успешного выполнения всех операций транзакция фиксируется. Если на любом этапе происходит ошибка, транзакция отменяется полностью.