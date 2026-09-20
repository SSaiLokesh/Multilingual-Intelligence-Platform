from flask import Blueprint

from .views import categorize_aspects


aspect_categorization_bp = Blueprint(
    "aspect_categorization",
    __name__
)


aspect_categorization_bp.route(
    "/categorize",
    methods=["POST"]
)(categorize_aspects)