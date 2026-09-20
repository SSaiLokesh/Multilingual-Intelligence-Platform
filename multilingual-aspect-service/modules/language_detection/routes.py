from flask import Blueprint

from .views import detect_language


language_detection_bp = Blueprint(
    "language_detection",
    __name__
)


language_detection_bp.route(
    "/detect",
    methods=["POST"]
)(detect_language)