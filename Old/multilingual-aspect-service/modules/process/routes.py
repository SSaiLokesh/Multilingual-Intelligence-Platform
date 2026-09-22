from flask import Blueprint

from .views import process


process_bp = Blueprint(
    "process",
    __name__
)


process_bp.route(
    "",
    methods=["POST"]
)(process)