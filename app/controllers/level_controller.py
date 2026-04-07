from flask import jsonify, request, g
from app.services.level_service import level_start_service, level_finish_service


def level_start_controller():
    user_id = g.user["userId"]
    payload = request.get_json()
    result = level_start_service(user_id, payload)

    return jsonify({
        "ok": True,
        "data": result
    }), 200


def level_finish_controller():
    user_id = g.user["userId"]
    payload = request.get_json()
    result = level_finish_service(user_id, payload)

    return jsonify({
        "ok": True,
        "data": result
    }), 200