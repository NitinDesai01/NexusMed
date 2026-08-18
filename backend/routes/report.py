from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint("report", __name__, url_prefix="/api/reports")

@bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_report():
    return jsonify({
        "message": "Report uploaded successfully",
        "report_id": 1,
        "summary": "Report processed"
    }), 201

@bp.route("/history", methods=["GET"])
@jwt_required()
def get_report_history():
    return jsonify({
        "reports": [
            {"id": 1, "type": "Blood Test", "date": "2024-01-15", "status": "processed"},
            {"id": 2, "type": "X-Ray", "date": "2024-01-10", "status": "processed"}
        ]
    }), 200

@bp.route("/<int:report_id>", methods=["GET"])
@jwt_required()
def get_report(report_id):
    return jsonify({
        "report": {
            "id": report_id,
            "type": "Lab Report",
            "findings": "Normal",
            "recommendations": "Follow up in 6 months"
        }
    }), 200
