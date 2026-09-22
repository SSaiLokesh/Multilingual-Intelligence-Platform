from views import process_request


def register_routes(app):

    @app.route("/process", methods=["POST"])
    def process():
        return process_request()