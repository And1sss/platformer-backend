from flask import Blueprint
from app.controllers.level_controller import level_start_controller, level_finish_controller
from app.middleware.auth_jwt import auth_required
from app.middleware.validate_api import validate_level_start, validate_level_finish

level_bp = Blueprint("level", __name__, url_prefix="/api/v1/level")


@level_bp.post("/start")
@auth_required(roles=["player"])
@validate_level_start
def level_start():
    return level_start_controller()


@level_bp.post("/finish")
@auth_required(roles=["player"])
@validate_level_finish
def level_finish():
    return level_finish_controller()