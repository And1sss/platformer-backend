from sqlalchemy import text


def create_level_attempt(session, user_id: int, level_code: str, client_version=None):
    sql = text("""
        INSERT INTO level_attempts (user_id, level_code, client_version)
        VALUES (:user_id, :level_code, :client_version)
    """)
    result = session.execute(sql, {
        "user_id": user_id,
        "level_code": level_code,
        "client_version": client_version
    })
    return result.lastrowid


def get_level_attempt_by_id(session, attempt_id: int):
    sql = text("""
        SELECT id, user_id, level_code, status, started_at, ended_at, client_version
        FROM level_attempts
        WHERE id = :attempt_id
        LIMIT 1
    """)
    return session.execute(sql, {"attempt_id": attempt_id}).mappings().first()


def finish_level_attempt(session, attempt_id: int):
    sql = text("""
        UPDATE level_attempts
        SET status = 'finished',
            ended_at = NOW(3)
        WHERE id = :attempt_id
    """)
    session.execute(sql, {"attempt_id": attempt_id})


def insert_level_result(
    session,
    attempt_id: int,
    is_completed: bool,
    score: int,
    duration_seconds: int,
    coins_collected: int,
    enemies_defeated: int,
    deaths_count: int = 0
):
    sql = text("""
        INSERT INTO level_results
        (attempt_id, is_completed, score, duration_seconds, coins_collected, enemies_defeated, deaths_count)
        VALUES
        (:attempt_id, :is_completed, :score, :duration_seconds, :coins_collected, :enemies_defeated, :deaths_count)
    """)
    session.execute(sql, {
        "attempt_id": attempt_id,
        "is_completed": int(is_completed),
        "score": score,
        "duration_seconds": duration_seconds,
        "coins_collected": coins_collected,
        "enemies_defeated": enemies_defeated,
        "deaths_count": deaths_count
    })