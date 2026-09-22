from flask import Blueprint

from views import process_request, health_check


bff_routes = Blueprint(
    "bff_routes",
    __name__
)


@bff_routes.route("/process", methods=["POST"])
def process_route():
    return process_request()


@bff_routes.route("/health", methods=["GET"])
def health_route():
    return health_check()