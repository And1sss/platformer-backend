from flask import Flask
from .extensions import db, jwt, cors
from .middleware.request_id import register_request_id
from .middleware.error_handler import register_error_handlers

from .routes.health import health_bp
from .routes.auth import auth_bp
from .routes.profile import profile_bp
from .routes.events import events_bp
from .routes.leaderboard import leaderboard_bp
from .routes.level import level_bp
from .routes.stats import stats_bp



def create_app(config_object="app.config.Config") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    register_request_id(app)
    register_error_handlers(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(level_bp)
    app.register_blueprint(stats_bp)

    return app