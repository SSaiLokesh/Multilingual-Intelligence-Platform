from flask import Flask

from flask_cors import CORS

from config import Config
from routes import bff_routes


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    # Enable CORS for the frontend
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173"
                ]
            }
        },
        methods=[
            "GET",
            "POST",
            "OPTIONS"
        ],
        allow_headers=[
            "Content-Type",
            "Authorization"
        ]
    )

    app.register_blueprint(bff_routes)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=Config.BFF_HOST,
        port=Config.BFF_PORT,
        debug=True
    )