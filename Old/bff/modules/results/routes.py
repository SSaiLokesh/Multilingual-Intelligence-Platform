from flask import Blueprint

from .views import get_result
from .views import get_results


results_bp = Blueprint(
    "results",
    __name__
)


results_bp.route(
    "/<result_id>",
    methods=["GET"]
)(get_result)


results_bp.route(
    "",
    methods=["GET"]
)(get_results)