from flask import jsonify, request
from app.services.leaderboard_service import get_leaderboard_service


def leaderboard_controller():
    board_code = request.args.get("boardCode", "platformer_score")
    season = int(request.args.get("season", 1))
    limit = int(request.args.get("limit", 10))

    result = get_leaderboard_service(
        board_code=board_code,
        season=season,
        limit=limit
    )

    return jsonify({
        "ok": True,
        "data": result
    }), 200