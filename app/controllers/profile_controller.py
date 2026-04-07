from flask import jsonify, g
from app.services.profile_service import get_profile_service


def profile_controller():
    user_id = g.user["userId"]
    result = get_profile_service(user_id)

    return jsonify({
        "ok": True,
        "data": result
    }), 200