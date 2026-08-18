from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import logging

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
logger = logging.getLogger(__name__)

@bp.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    data = request.get_json()
    return jsonify({
        "message": "Registration successful",
        "user": {"id": 1, "name": data.get("name", "User")}
    }), 201

@bp.route("/login", methods=["POST"])
def login():
    """Login user"""
    data = request.get_json()
    access_token = create_access_token(identity=data.get("user_id", "user"))
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {"user_id": data.get("user_id", "user"), "name": "Demo User"}
    }), 200

@bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get user profile"""
    user_id = get_jwt_identity()
    return jsonify({
        "user": {
            "user_id": user_id,
            "name": "Demo User",
            "email": "demo@example.com"
        }
    }), 200

@bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update user profile"""
    data = request.get_json()
    return jsonify({
        "message": "Profile updated successfully",
        "user": data
    }), 200
