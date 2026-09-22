from flask import Blueprint

from .views import (
    add_to_memory,
    get_memory,
    clear_memory
)


memory_bp = Blueprint(
    "memory",
    __name__
)


# Add a record to replay memory
memory_bp.route(
    "/add",
    methods=["POST"]
)(add_to_memory)


# Get current memory
memory_bp.route(
    "",
    methods=["GET"]
)(get_memory)


# Clear memory
memory_bp.route(
    "/clear",
    methods=["DELETE"]
)(clear_memory)