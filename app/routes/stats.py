from flask import Blueprint
from app.controllers.stats_controller import stats_controller
from app.middleware.auth_jwt import auth_required

stats_bp = Blueprint("stats", __name__, url_prefix="/api/v1")


@stats_bp.get("/stats")
@auth_required(roles=["player", "admin", "moderator"])
def stats():
    return stats_controller()