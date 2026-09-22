from flask import Blueprint

from .views import adapt


data_integration_bp = Blueprint(
    "data_integration",
    __name__
)


# Main adaptation endpoint
#
# This route is registered directly under
# /internal/v1 in app.py.
#
# Final endpoint:
# POST /internal/v1/adapt
data_integration_bp.route(
    "/adapt",
    methods=["POST"]
)(adapt)