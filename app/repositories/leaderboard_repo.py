from sqlalchemy import text


def upsert_leaderboard_score(session, user_id: int, board_code: str, season: int, score: int):
    sql = text("""
        INSERT INTO leaderboard_scores (user_id, board_code, season, score)
        VALUES (:user_id, :board_code, :season, :score)
        ON DUPLICATE KEY UPDATE
            score = GREATEST(score, VALUES(score)),
            updated_at = CURRENT_TIMESTAMP(3)
    """)
    session.execute(sql, {
        "user_id": user_id,
        "board_code": board_code,
        "season": season,
        "score": score
    })


def get_leaderboard(session, board_code: str, season: int, limit: int):
    sql = text("""
        SELECT
            ls.user_id,
            u.nickname,
            ls.score
        FROM leaderboard_scores ls
        JOIN users u ON u.id = ls.user_id
        WHERE ls.board_code = :board_code
          AND ls.season = :season
        ORDER BY ls.score DESC, ls.updated_at ASC
        LIMIT :limit_value
    """)
    return session.execute(sql, {
        "board_code": board_code,
        "season": season,
        "limit_value": limit
    }).mappings().all()