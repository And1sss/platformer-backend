from sqlalchemy import text


def get_user_by_email(session, email: str):
    sql = text("""
        SELECT id, email, password, nickname, created_at, last_login_at, is_banned
        FROM users
        WHERE email = :email
        LIMIT 1
    """)
    return session.execute(sql, {"email": email}).mappings().first()


def create_user(session, email: str, password_hash: str, nickname: str):
    sql = text("""
        INSERT INTO users (email, password, nickname)
        VALUES (:email, :password, :nickname)
    """)
    result = session.execute(sql, {
        "email": email,
        "password": password_hash,
        "nickname": nickname
    })
    return result.lastrowid


def update_last_login(session, user_id: int):
    sql = text("""
        UPDATE users
        SET last_login_at = NOW(3)
        WHERE id = :user_id
    """)
    session.execute(sql, {"user_id": user_id})


def get_user_by_id(session, user_id: int):
    sql = text("""
        SELECT id, email, nickname, created_at, last_login_at, is_banned
        FROM users
        WHERE id = :user_id
        LIMIT 1
    """)
    return session.execute(sql, {"user_id": user_id}).mappings().first()