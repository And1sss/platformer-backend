from sqlalchemy import text


def upsert_daily_stats(session, user_id: int, playtime_seconds: int, is_win: bool, score: int):
    wins = 1 if is_win else 0
    losses = 0 if is_win else 1

    sql = text("""
        INSERT INTO statistics_daily
        (user_id, day, sessions_count, events_count, playtime_seconds, wins, losses, score_sum)
        VALUES (:user_id, CURDATE(), 0, 1, :playtime_seconds, :wins, :losses, :score)
        ON DUPLICATE KEY UPDATE
            events_count = events_count + 1,
            playtime_seconds = playtime_seconds + VALUES(playtime_seconds),
            wins = wins + VALUES(wins),
            losses = losses + VALUES(losses),
            score_sum = score_sum + VALUES(score_sum)
    """)
    session.execute(sql, {
        "user_id": user_id,
        "playtime_seconds": playtime_seconds,
        "wins": wins,
        "losses": losses,
        "score": score
    })


def get_stats_range(session, user_id: int, date_from: str, date_to: str):
    sql = text("""
        SELECT
            day,
            sessions_count,
            events_count,
            playtime_seconds,
            wins,
            losses,
            score_sum
        FROM statistics_daily
        WHERE user_id = :user_id
          AND day BETWEEN :date_from AND :date_to
        ORDER BY day ASC
    """)
    return session.execute(sql, {
        "user_id": user_id,
        "date_from": date_from,
        "date_to": date_to
    }).mappings().all()