from flask import Blueprint

from .views import process_text
from .views import process_dataset


process_bp = Blueprint(
    "process",
    __name__
)


process_bp.route(
    "/text",
    methods=["POST"]
)(process_text)


process_bp.route(
    "/dataset",
    methods=["POST"]
)(process_dataset)