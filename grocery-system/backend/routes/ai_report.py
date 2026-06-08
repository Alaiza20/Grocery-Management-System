# Blueprint for AI-related endpoints
# This keeps future AI features separate from core business logic
from flask import Blueprint, jsonify


# Create AI blueprint
ai_bp = Blueprint("ai", __name__)


# Temporary endpoint for AI reporting feature
# Currently returns placeholder response (feature not implemented yet)
@ai_bp.route("/report", methods=["GET"])
def report():

    # Return simple JSON message indicating future AI feature
    return jsonify({
        "message": "AI report coming in final days"
    })