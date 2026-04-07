from datetime import date, timedelta

from app.extensions import db
from app.repositories.stats_repo import get_stats_range


def get_stats_service(user_id: int, date_from: str | None, date_to: str | None) -> dict:
    user_id = int(user_id)

    if not date_to:
        date_to = date.today().isoformat()

    if not date_from:
        date_from = (date.today() - timedelta(days=30)).isoformat()

    rows = get_stats_range(
        db.session,
        user_id=user_id,
        date_from=date_from,
        date_to=date_to
    )

    daily = []
    summary = {
        "daysActive": 0,
        "eventsCount": 0,
        "playtimeSeconds": 0,
        "wins": 0,
        "losses": 0,
        "scoreSum": 0
    }

    for row in rows:
        daily_item = {
            "day": str(row["day"]),
            "sessionsCount": row["sessions_count"],
            "eventsCount": row["events_count"],
            "playtimeSeconds": row["playtime_seconds"],
            "wins": row["wins"],
            "losses": row["losses"],
            "scoreSum": row["score_sum"]
        }
        daily.append(daily_item)

        summary["daysActive"] += 1
        summary["eventsCount"] += row["events_count"]
        summary["playtimeSeconds"] += row["playtime_seconds"]
        summary["wins"] += row["wins"]
        summary["losses"] += row["losses"]
        summary["scoreSum"] += row["score_sum"]

    return {
        "from": date_from,
        "to": date_to,
        "daily": daily,
        "summary": summary
    }