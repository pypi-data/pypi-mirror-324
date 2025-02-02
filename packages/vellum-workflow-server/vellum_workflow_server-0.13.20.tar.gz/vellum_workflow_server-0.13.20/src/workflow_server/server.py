import logging
import os

from flask import Flask

from workflow_server.api.auth_middleware import AuthMiddleware
from workflow_server.api.healthz_view import bp as healthz_bp
from workflow_server.api.workflow_view import bp as workflow_bp
from workflow_server.utils.log_proxy import enable_log_proxy

enable_log_proxy()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def create_app() -> Flask:
    FLASK_ENV = os.getenv("FLASK_ENV", "local")

    logger.info(f"Creating App using config: config.{FLASK_ENV}")
    app = Flask(__name__)
    app.wsgi_app = AuthMiddleware(app.wsgi_app)

    # Register blueprints
    app.register_blueprint(healthz_bp, url_prefix="/healthz")
    app.register_blueprint(workflow_bp, url_prefix="/workflow")

    return app


app = create_app()
