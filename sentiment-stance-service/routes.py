from views import analyze_view, health_view


def register_routes(app):

    app.add_url_rule(
        "/analyze",
        view_func=analyze_view,
        methods=["POST"]
    )

    app.add_url_rule(
        "/health",
        view_func=health_view,
        methods=["GET"]
    )