from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime
import uuid

bp = Blueprint("emergency", __name__, url_prefix="/api/emergency")
logger = logging.getLogger(__name__)

# Sample ambulance data
ambulances_db = [
    {
        "id": 1,
        "vehicle_number": "AMB-001",
        "driver_name": "Rajesh Kumar",
        "driver_phone": "+91-9876543210",
        "status": "available",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "equipment_level": "Advanced",
        "hospital": "City General Hospital"
    },
    {
        "id": 2,
        "vehicle_number": "AMB-002",
        "driver_name": "Milkha Singh",
        "driver_phone": "+91-9876543211",
        "status": "available",
        "latitude": 12.9816,
        "longitude": 77.6046,
        "equipment_level": "Basic",
        "hospital": "Memorial Medical Center"
    },
    {
        "id": 3,
        "vehicle_number": "AMB-003",
        "driver_name": "Suresh Reddy",
        "driver_phone": "+91-9876543212",
        "status": "busy",
        "latitude": 12.9616,
        "longitude": 77.5846,
        "equipment_level": "Advanced",
        "hospital": "St. Mary's Hospital"
    }
]

# Emergency request storage
emergency_requests = []

@bp.route("/request", methods=["POST"])
@jwt_required()
def request_emergency():
    """Request emergency help"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        lat = data.get("lat")
        lng = data.get("lng")
        
        if not lat or not lng:
            return jsonify({"error": "Location coordinates required"}), 400
        
        # Generate request ID
        request_id = "EMG-" + str(uuid.uuid4())[:8].upper()
        
        # Find nearest available ambulance
        nearest_ambulance = None
        nearest_distance = float('inf')
        
        for ambulance in ambulances_db:
            if ambulance["status"] == "available":
                # Calculate distance (simplified)
                distance = ((ambulance["latitude"] - lat) ** 2 + (ambulance["longitude"] - lng) ** 2) ** 0.5 * 111
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_ambulance = ambulance
        
        # If no ambulance available, use a default one
        if not nearest_ambulance:
            nearest_ambulance = {
                "id": 1,
                "vehicle_number": "AMB-001",
                "driver_name": "Rajesh Kumar",
                "driver_phone": "+91-9876543210",
                "status": "en_route",
                "equipment_level": "Advanced",
                "hospital": "City General Hospital"
            }
            estimated_arrival = "8-12 minutes"
        else:
            # Mark ambulance as busy
            for amb in ambulances_db:
                if amb["id"] == nearest_ambulance["id"]:
                    amb["status"] = "en_route"
                    break
            # Calculate estimated arrival time
            estimated_time = max(5, int(nearest_distance * 1.5))
            estimated_arrival = f"{estimated_time}-{estimated_time + 5} minutes"
        
        # Create emergency request
        emergency_request = {
            "request_id": request_id,
            "user_id": user_id,
            "latitude": lat,
            "longitude": lng,
            "ambulance_id": nearest_ambulance["id"],
            "ambulance_vehicle": nearest_ambulance["vehicle_number"],
            "driver_name": nearest_ambulance["driver_name"],
            "driver_phone": nearest_ambulance["driver_phone"],
            "status": "dispatched",
            "estimated_arrival": estimated_arrival,
            "requested_at": datetime.now().isoformat()
        }
        
        emergency_requests.append(emergency_request)
        
        return jsonify({
            "status": "success",
            "message": "Emergency help dispatched",
            "request_id": request_id,
            "ambulance": {
                "vehicle_number": nearest_ambulance["vehicle_number"],
                "driver_name": nearest_ambulance["driver_name"],
                "driver_phone": nearest_ambulance["driver_phone"],
                "estimated_arrival": estimated_arrival,
                "equipment_level": nearest_ambulance.get("equipment_level", "Basic")
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Emergency request error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/status/<request_id>", methods=["GET"])
@jwt_required()
def get_emergency_status(request_id):
    """Get emergency request status"""
    try:
        for request in emergency_requests:
            if request["request_id"] == request_id:
                return jsonify({
                    "status": request["status"],
                    "estimated_arrival": request.get("estimated_arrival", "10 minutes"),
                    "ambulance_vehicle": request.get("ambulance_vehicle", "AMB-001"),
                    "driver_name": request.get("driver_name", "Rajesh Kumar"),
                    "driver_phone": request.get("driver_phone", "+91-9876543210")
                }), 200
        
        return jsonify({"error": "Request not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/ambulances", methods=["GET"])
@jwt_required()
def get_ambulances():
    """Get all ambulances"""
    try:
        return jsonify({"ambulances": ambulances_db}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500