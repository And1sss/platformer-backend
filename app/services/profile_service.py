from app.extensions import db
from app.repositories.users_repo import get_user_by_id
from app.repositories.roles_repo import get_user_roles
from app.repositories.progress_repo import get_progress_by_user_id, ensure_progress_row
from app.middleware.error_handler import AppError


def get_profile_service(user_id: int) -> dict:
    user_id = int(user_id)

    user = get_user_by_id(db.session, user_id)
    if not user:
        raise AppError(
            code="NOT_FOUND",
            message="User not found",
            http_status=404
        )

    ensure_progress_row(db.session, user_id)
    db.session.commit()

    progress = get_progress_by_user_id(db.session, user_id)
    roles = get_user_roles(db.session, user_id)

    return {
        "user": {
            "id": user["id"],
            "email": user["email"],
            "nickname": user["nickname"],
            "createdAt": str(user["created_at"]) if user["created_at"] else None,
            "lastLoginAt": str(user["last_login_at"]) if user["last_login_at"] else None,
            "isBanned": bool(user["is_banned"]),
            "roles": roles
        },
        "progress": {
            "level": progress["level"],
            "xp": progress["xp"],
            "softCurrency": progress["soft_currency"],
            "hardCurrency": progress["hard_currency"],
            "updatedAt": str(progress["updated_at"]) if progress["updated_at"] else None
        }
    }