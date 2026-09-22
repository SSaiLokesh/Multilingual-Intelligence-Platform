from flask import Flask
from flask_cors import CORS

from config import Config

from modules.data_integration.routes import data_integration_bp
from modules.memory.routes import memory_bp
from modules.versioning.routes import versioning_bp


def create_app():
    """
    Create and configure the Adaptation Service Flask application.
    """

    app = Flask(__name__)

    # -----------------------------------------
    # Enable CORS for React Frontend
    # -----------------------------------------

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173"
                ]
            }
        },
        methods=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS"
        ],
        allow_headers=[
            "Content-Type",
            "Authorization"
        ],
        supports_credentials=True
    )

    # -----------------------------------------
    # Load configuration
    # -----------------------------------------

    app.config.from_object(Config)

    # -----------------------------------------
    # Data Integration
    # -----------------------------------------

    app.register_blueprint(
        data_integration_bp,
        url_prefix=f"{Config.API_PREFIX}/data"
    )

    # -----------------------------------------
    # Memory
    # -----------------------------------------

    app.register_blueprint(
        memory_bp,
        url_prefix=f"{Config.API_PREFIX}/memory"
    )

    # -----------------------------------------
    # Versioning
    # -----------------------------------------

    app.register_blueprint(
        versioning_bp,
        url_prefix=f"{Config.API_PREFIX}/version"
    )

    # -----------------------------------------
    # Service information
    # -----------------------------------------

    @app.get("/")
    def home():
        return {
            "service": Config.SERVICE_NAME,
            "version": Config.SERVICE_VERSION,
            "status": "running"
        }

    # -----------------------------------------
    # Health check
    # -----------------------------------------

    @app.get("/health")
    def health():
        return {
            "service": Config.SERVICE_NAME,
            "status": "healthy"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=Config.DEBUG
    )