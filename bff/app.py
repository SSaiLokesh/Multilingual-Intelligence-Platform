from flask import Flask

from config import Config

from modules.process.routes import process_bp
from modules.results.routes import results_bp


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(
        process_bp,
        url_prefix=f"{Config.API_PREFIX}/process"
    )

    app.register_blueprint(
        results_bp,
        url_prefix=f"{Config.API_PREFIX}/results"
    )

    @app.get("/")
    def home():
        return {
            "service": "bff",
            "status": "running"
        }

    @app.get("/health")
    def health():
        return {
            "service": "bff",
            "status": "healthy"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=Config.DEBUG
    )