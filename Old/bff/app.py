from flask import Flask
from flask_cors import CORS

from config import Config

from modules.process.routes import process_bp
from modules.results.routes import results_bp


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    # Enable CORS for the React frontend
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