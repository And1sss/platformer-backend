from app.extensions import db
from app.middleware.error_handler import AppError
from app.repositories.level_repo import (
    create_level_attempt,
    get_level_attempt_by_id,
    finish_level_attempt,
    insert_level_result
)
from app.repositories.progress_repo import (
    ensure_progress_row,
    lock_progress_row,
    add_progress_rewards
)
from app.repositories.stats_repo import upsert_daily_stats
from app.repositories.leaderboard_repo import upsert_leaderboard_score


def level_start_service(user_id: int, payload: dict) -> dict:
    user_id = int(user_id)

    level_code = payload["levelCode"]
    client_version = payload.get("clientVersion")

    attempt_id = create_level_attempt(
        db.session,
        user_id=user_id,
        level_code=level_code,
        client_version=client_version
    )
    db.session.commit()

    return {
        "attemptId": attempt_id,
        "status": "started"
    }


def level_finish_service(user_id: int, payload: dict) -> dict:
    user_id = int(user_id)

    attempt_id = payload["attemptId"]
    result = payload["result"]

    is_completed = result["isCompleted"]
    score = result["score"]
    duration_seconds = result["durationSeconds"]
    coins_collected = result["coinsCollected"]
    enemies_defeated = result["enemiesDefeated"]
    deaths_count = result.get("deathsCount", 0)

    attempt = get_level_attempt_by_id(db.session, attempt_id)
    if not attempt:
        raise AppError(
            code="NOT_FOUND",
            message="Level attempt not found",
            http_status=404
        )

    if int(attempt["user_id"]) != user_id:
        raise AppError(
            code="FORBIDDEN",
            message="Level attempt belongs to another user",
            http_status=403
        )

    if attempt["status"] != "started":
        raise AppError(
            code="CONFLICT",
            message="Level attempt is not in started state",
            http_status=409
        )

    xp_gained = 100 if is_completed else 25
    soft_currency_gained = 50 if is_completed else 10

    try:
        ensure_progress_row(db.session, user_id)
        lock_progress_row(db.session, user_id)

        finish_level_attempt(db.session, attempt_id)

        insert_level_result(
            db.session,
            attempt_id=attempt_id,
            is_completed=is_completed,
            score=score,
            duration_seconds=duration_seconds,
            coins_collected=coins_collected,
            enemies_defeated=enemies_defeated,
            deaths_count=deaths_count
        )

        add_progress_rewards(
            db.session,
            user_id=user_id,
            xp=xp_gained,
            soft_currency=soft_currency_gained
        )

        upsert_daily_stats(
            db.session,
            user_id=user_id,
            playtime_seconds=duration_seconds,
            is_win=is_completed,
            score=score
        )

        upsert_leaderboard_score(
            db.session,
            user_id=user_id,
            board_code="platformer_score",
            season=1,
            score=score
        )

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {
        "attemptId": attempt_id,
        "isCompleted": is_completed,
        "xpGained": xp_gained,
        "softCurrencyGained": soft_currency_gained
    }