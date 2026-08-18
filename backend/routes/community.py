from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint("community", __name__, url_prefix="/api/community")

@bp.route("/awareness", methods=["GET"])
@jwt_required()
def get_awareness_content():
    topic = request.args.get("topic", "general")
    return jsonify({
        "content": {
            "topic": topic,
            "title": f"Health Awareness: {topic}",
            "content": f"Information about {topic}. Stay healthy!",
            "tips": ["Tip 1", "Tip 2", "Tip 3"]
        }
    }), 200

@bp.route("/alerts", methods=["GET"])
@jwt_required()
def get_alerts():
    return jsonify({
        "alerts": [
            {"id": 1, "title": "Health Alert", "message": "Stay safe", "status": "active"}
        ]
    }), 200

@bp.route("/alerts", methods=["POST"])
@jwt_required()
def create_alert():
    data = request.get_json()
    return jsonify({
        "id": 1,
        "title": data.get("title", "Alert"),
        "message": data.get("message", ""),
        "status": "active"
    }), 201
