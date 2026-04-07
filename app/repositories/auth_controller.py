from flask import jsonify, request
from app.services.auth_service import register_user_service, login_user_service


def register_controller():
    payload = request.get_json()
    result = register_user_service(payload)
    return jsonify({
        "ok": True,
        "data": result
    }), 201


def login_controller():
    payload = request.get_json()
    result = login_user_service(payload)
    return jsonify({
        "ok": True,
        "data": result
    }), 200