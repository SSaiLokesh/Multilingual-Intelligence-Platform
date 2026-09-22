from flask import Blueprint

from .views import predict_stance_view


stance_bp = Blueprint(
    "stance",
    __name__
)


stance_bp.route(
    "/predict",
    methods=["POST"]
)(predict_stance_view)
