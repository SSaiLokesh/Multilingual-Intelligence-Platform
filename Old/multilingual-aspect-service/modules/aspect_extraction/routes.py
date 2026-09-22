from flask import Blueprint

from .views import extract_aspects


aspect_extraction_bp = Blueprint(
    "aspect_extraction",
    __name__
)


aspect_extraction_bp.route(
    "/extract",
    methods=["POST"]
)(extract_aspects)