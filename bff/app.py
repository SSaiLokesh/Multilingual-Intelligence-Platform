from flask import Flask

from config import Config
from routes import bff_routes


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    app.register_blueprint(bff_routes)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=Config.BFF_HOST,
        port=Config.BFF_PORT,
        debug=True
    )