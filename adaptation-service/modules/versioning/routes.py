from flask import Blueprint

from .views import (
    get_current_version,
    get_versions
)


versioning_bp = Blueprint(
    "versioning",
    __name__
)


# Current version
versioning_bp.route(
    "",
    methods=["GET"]
)(get_current_version)


# All versions
versioning_bp.route(
    "/history",
    methods=["GET"]
)(get_versions)