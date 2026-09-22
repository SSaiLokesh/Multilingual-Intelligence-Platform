from views import adapt_view, health_view


def register_routes(app):

    app.add_url_rule(
        "/adapt",
        view_func=adapt_view,
        methods=["POST"]
    )

    app.add_url_rule(
        "/health",
        view_func=health_view,
        methods=["GET"]
    )