from flask import jsonify, request, g
from app.services.stats_service import get_stats_service


def stats_controller():
    user_id = g.user["userId"]
    date_from = request.args.get("from")
    date_to = request.args.get("to")

    result = get_stats_service(
        user_id=user_id,
        date_from=date_from,
        date_to=date_to
    )

    return jsonify({
        "ok": True,
        "data": result
    }), 200