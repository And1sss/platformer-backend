from sqlalchemy import text


def get_progress_by_user_id(session, user_id: int):
    sql = text("""
        SELECT user_id, level, xp, soft_currency, hard_currency, updated_at
        FROM player_progress
        WHERE user_id = :user_id
        LIMIT 1
    """)
    return session.execute(sql, {"user_id": user_id}).mappings().first()


def ensure_progress_row(session, user_id: int):
    sql = text("""
        INSERT IGNORE INTO player_progress (user_id)
        VALUES (:user_id)
    """)
    session.execute(sql, {"user_id": user_id})


def add_progress_rewards(session, user_id: int, xp: int, soft_currency: int):
    sql = text("""
        UPDATE player_progress
        SET xp = xp + :xp,
            soft_currency = soft_currency + :soft_currency
        WHERE user_id = :user_id
    """)
    session.execute(sql, {
        "xp": xp,
        "soft_currency": soft_currency,
        "user_id": user_id
    })


def lock_progress_row(session, user_id: int):
    sql = text("""
        SELECT user_id
        FROM player_progress
        WHERE user_id = :user_id
        FOR UPDATE
    """)
    return session.execute(sql, {"user_id": user_id}).first()