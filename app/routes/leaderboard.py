from flask import Blueprint
from app.controllers.leaderboard_controller import leaderboard_controller

leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/api/v1")


@leaderboard_bp.get("/leaderboard")
def leaderboard():
    return leaderboard_controller()