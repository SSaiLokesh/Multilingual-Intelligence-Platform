from flask import Blueprint

from .views import predict_sentiment_view


sentiment_bp = Blueprint(
    "sentiment",
    __name__
)


sentiment_bp.route(
    "/predict",
    methods=["POST"]
)(predict_sentiment_view)
