import bcrypt
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.middleware.error_handler import AppError
from app.repositories.users_repo import get_user_by_email, create_user, update_last_login
from app.repositories.roles_repo import get_role_ids_by_names, assign_role_to_user, get_user_roles


def register_user_service(payload: dict) -> dict:
    email = payload["email"].strip().lower()
    password = payload["password"]
    nickname = payload["nickname"].strip()

    existing_user = get_user_by_email(db.session, email)
    if existing_user:
        raise AppError(
            code="EMAIL_ALREADY_EXISTS",
            message="User with this email already exists",
            http_status=409
        )

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        user_id = create_user(db.session, email, password_hash, nickname)

        role_rows = get_role_ids_by_names(db.session, ["player"])
        if not role_rows:
            raise AppError(
                code="ROLE_NOT_FOUND",
                message="Default role 'player' not found",
                http_status=500
            )

        for role in role_rows:
            assign_role_to_user(db.session, user_id, role["id"])

        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return {"userId": user_id}


def login_user_service(payload: dict) -> dict:
    email = payload["email"].strip().lower()
    password = payload["password"]

    user = get_user_by_email(db.session, email)
    if not user:
        raise AppError(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
            http_status=401
        )

    if user["is_banned"]:
        raise AppError(
            code="USER_BANNED",
            message="User is banned",
            http_status=403
        )

    password_hash = user["password"]
    if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
        raise AppError(
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
            http_status=401
        )

    roles = get_user_roles(db.session, user["id"])

    try:
        update_last_login(db.session, user["id"])
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    access_token = create_access_token(
        identity=str(user["id"]),
        additional_claims={"roles": roles}
    )

    return {
        "accessToken": access_token,
        "tokenType": "Bearer",
        "expiresInSeconds": 3600
    }