from flask import Blueprint

from .views import preprocess_text


preprocessing_bp = Blueprint(
    "preprocessing",
    __name__
)


preprocessing_bp.route(
    "/process",
    methods=["POST"]
)(preprocess_text)