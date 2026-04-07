from functools import wraps
from flask import request
from .error_handler import AppError


def _bad_body(details):
    raise AppError(
        code="VALIDATION_ERROR",
        message="Invalid request body",
        http_status=400,
        details=details
    )


def validate_register(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            _bad_body({"body": "JSON object expected"})

        email = data.get("email")
        password = data.get("password")
        nickname = data.get("nickname")

        if not isinstance(email, str) or "@" not in email or len(email) > 255:
            _bad_body({"email": "valid email string required"})

        if not isinstance(password, str) or len(password) < 6:
            _bad_body({"password": "string with min length 6 required"})

        if not isinstance(nickname, str) or not nickname.strip() or len(nickname) > 64:
            _bad_body({"nickname": "non-empty string with max length 64 required"})

        return fn(*args, **kwargs)

    return wrapper


def validate_login(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            _bad_body({"body": "JSON object expected"})

        email = data.get("email")
        password = data.get("password")

        if not isinstance(email, str) or "@" not in email:
            _bad_body({"email": "valid email string required"})

        if not isinstance(password, str) or len(password) < 1:
            _bad_body({"password": "password string required"})

        return fn(*args, **kwargs)

    return wrapper


def validate_event(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            _bad_body({"body": "JSON object expected"})

        event_type = data.get("eventType")
        payload = data.get("payload")

        if not isinstance(event_type, str) or not event_type.strip():
            _bad_body({"eventType": "non-empty string required"})

        if payload is None or not isinstance(payload, dict):
            _bad_body({"payload": "object required"})

        return fn(*args, **kwargs)

    return wrapper


def validate_level_start(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            _bad_body({"body": "JSON object expected"})

        level_code = data.get("levelCode")

        if not isinstance(level_code, str) or not level_code.strip():
            _bad_body({"levelCode": "non-empty string required"})

        return fn(*args, **kwargs)

    return wrapper


def validate_level_finish(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            _bad_body({"body": "JSON object expected"})

        attempt_id = data.get("attemptId")
        result = data.get("result")

        if not isinstance(attempt_id, int):
            _bad_body({"attemptId": "int required"})

        if not isinstance(result, dict):
            _bad_body({"result": "object required"})

        is_completed = result.get("isCompleted")
        score = result.get("score")
        duration = result.get("durationSeconds")
        coins_collected = result.get("coinsCollected")
        enemies_defeated = result.get("enemiesDefeated")

        if not isinstance(is_completed, bool):
            _bad_body({"result.isCompleted": "bool required"})

        if not isinstance(score, int) or score < 0:
            _bad_body({"result.score": "int >= 0 required"})

        if not isinstance(duration, int) or duration < 0:
            _bad_body({"result.durationSeconds": "int >= 0 required"})

        if not isinstance(coins_collected, int) or coins_collected < 0:
            _bad_body({"result.coinsCollected": "int >= 0 required"})

        if not isinstance(enemies_defeated, int) or enemies_defeated < 0:
            _bad_body({"result.enemiesDefeated": "int >= 0 required"})

        return fn(*args, **kwargs)

    return wrapper