from flask import Blueprint

from .views import analyze


process_bp = Blueprint(
    "process",
    __name__
)


process_bp.route(
    "",
    methods=["POST"]
)(analyze)
