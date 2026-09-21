from flask import Flask
from flask_cors import CORS

from config import Config

from modules.process.routes import process_bp
from modules.sentiment.routes import sentiment_bp
from modules.stance.routes import stance_bp


def create_app():
    """
    Create and configure the Flask application.
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
    # Main processing endpoint
    # -----------------------------------------

    app.register_blueprint(
        process_bp,
        url_prefix=f"{Config.API_PREFIX}/analyze"
    )

    # -----------------------------------------
    # Individual sentiment endpoint
    # -----------------------------------------

    app.register_blueprint(
        sentiment_bp,
        url_prefix=f"{Config.API_PREFIX}/sentiment"
    )

    # -----------------------------------------
    # Individual stance endpoint
    # -----------------------------------------

    app.register_blueprint(
        stance_bp,
        url_prefix=f"{Config.API_PREFIX}/stance"
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