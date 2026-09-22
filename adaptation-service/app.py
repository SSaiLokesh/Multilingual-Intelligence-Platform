from flask import Flask

from config import (
    SERVICE_NAME,
    SERVICE_VERSION
)

from routes import register_routes


def create_app():

    app = Flask(__name__)

    app.config["SERVICE_NAME"] = SERVICE_NAME
    app.config["SERVICE_VERSION"] = SERVICE_VERSION

    register_routes(app)

    return app


app = create_app()


if __name__ == "__main__":

    from config import HOST, PORT, DEBUG

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )