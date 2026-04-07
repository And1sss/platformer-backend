from app.extensions import db
from app.repositories.leaderboard_repo import get_leaderboard


def get_leaderboard_service(board_code: str, season: int, limit: int) -> dict:
    rows = get_leaderboard(
        db.session,
        board_code=board_code,
        season=season,
        limit=limit
    )

    items = []
    rank = 1
    for row in rows:
        items.append({
            "rank": rank,
            "userId": row["user_id"],
            "nickname": row["nickname"],
            "score": row["score"]
        })
        rank += 1

    return {
        "boardCode": board_code,
        "season": season,
        "items": items
    }