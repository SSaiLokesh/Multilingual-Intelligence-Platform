from flask import Flask

from config import Config

from modules.process.routes import process_bp
from modules.preprocessing.routes import preprocessing_bp
from modules.language_detection.routes import language_detection_bp
from modules.aspect_extraction.routes import aspect_extraction_bp
from modules.aspect_categorization.routes import aspect_categorization_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Main pipeline
    app.register_blueprint(
        process_bp,
        url_prefix=f"{Config.API_PREFIX}/process"
    )

    # Individual modules
    app.register_blueprint(
        preprocessing_bp,
        url_prefix=f"{Config.API_PREFIX}/preprocessing"
    )

    app.register_blueprint(
        language_detection_bp,
        url_prefix=f"{Config.API_PREFIX}/language"
    )

    app.register_blueprint(
        aspect_extraction_bp,
        url_prefix=f"{Config.API_PREFIX}/aspect"
    )

    app.register_blueprint(
        aspect_categorization_bp,
        url_prefix=f"{Config.API_PREFIX}/aspect"
    )

    @app.get("/")
    def home():
        return {
            "service": Config.SERVICE_NAME,
            "version": Config.SERVICE_VERSION,
            "status": "running"
        }

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