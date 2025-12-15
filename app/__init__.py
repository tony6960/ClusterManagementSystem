from flask import Flask

from app.management.routes import management_bp
from app.agent.routes import agent_bp


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="cluster-management-secret",
    )

    app.register_blueprint(management_bp, url_prefix="/management")
    app.register_blueprint(agent_bp, url_prefix="/agent")

    @app.route("/")
    def index():
        return "Welcome to the Cluster Management System. Visit /management or /agent."

    return app
