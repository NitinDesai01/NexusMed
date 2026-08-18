from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint("ambulance", __name__, url_prefix="/api/ambulances")

@bp.route("/track", methods=["GET"])
@jwt_required()
def track_ambulances():
    return jsonify({
        "ambulances": [
            {"id": 1, "vehicle": "AMB-001", "status": "available", "distance": 2.5},
            {"id": 2, "vehicle": "AMB-002", "status": "busy", "distance": 5.0}
        ]
    }), 200

@bp.route("/request", methods=["POST"])
@jwt_required()
def request_ambulance():
    data = request.get_json()
    return jsonify({
        "request_id": "REQ-12345",
        "status": "assigned",
        "estimated_arrival": "5 minutes"
    }), 200
