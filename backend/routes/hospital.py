from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import logging

bp = Blueprint("hospital", __name__, url_prefix="/api/hospitals")
logger = logging.getLogger(__name__)

# Hospital Database
hospitals_db = [
    {
        "id": 1,
        "name": "City General Hospital",
        "address": "123 Main Street",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560001",
        "phone": "080-555-0100",
        "email": "info@citygeneral.com",
        "website": "www.citygeneral.com",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "total_beds": 500,
        "available_beds": 50,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "General Medicine, Surgery, Pediatrics, Cardiology",
        "rating": 4.5
    },
    {
        "id": 2,
        "name": "Memorial Medical Center",
        "address": "456 Oak Avenue",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560002",
        "phone": "080-555-0101",
        "email": "info@memorialmedical.com",
        "website": "www.memorialmedical.com",
        "latitude": 12.9816,
        "longitude": 77.6046,
        "total_beds": 400,
        "available_beds": 30,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "Cardiology, Neurology, Oncology, Orthopedics",
        "rating": 4.7
    },
    {
        "id": 3,
        "name": "St. Mary's Hospital",
        "address": "789 Pine Road",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560003",
        "phone": "080-555-0102",
        "email": "info@stmarys.com",
        "website": "www.stmarys.com",
        "latitude": 12.9616,
        "longitude": 77.5846,
        "total_beds": 350,
        "available_beds": 20,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "Pediatrics, OB/GYN, General Surgery, ENT",
        "rating": 4.3
    },
    {
        "id": 4,
        "name": "University Medical Center",
        "address": "100 University Drive",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560004",
        "phone": "080-555-0103",
        "email": "info@universitymedical.com",
        "website": "www.universitymedical.com",
        "latitude": 12.9916,
        "longitude": 77.6146,
        "total_beds": 600,
        "available_beds": 60,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "All Specialties, Research, Oncology, Neurology",
        "rating": 4.8
    },
    {
        "id": 5,
        "name": "Community Health Hospital",
        "address": "200 Community Lane",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560005",
        "phone": "080-555-0104",
        "email": "info@communityhealth.com",
        "website": "www.communityhealth.com",
        "latitude": 12.9516,
        "longitude": 77.5746,
        "total_beds": 250,
        "available_beds": 40,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "Family Medicine, Internal Medicine, Pediatrics",
        "rating": 4.0
    },
    {
        "id": 6,
        "name": "Regional Medical Center",
        "address": "300 Regional Boulevard",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560006",
        "phone": "080-555-0105",
        "email": "info@regionalmedical.com",
        "website": "www.regionalmedical.com",
        "latitude": 12.9416,
        "longitude": 77.5646,
        "total_beds": 450,
        "available_beds": 35,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "Cardiology, Orthopedics, Neurology, Gastroenterology",
        "rating": 4.6
    },
    {
        "id": 7,
        "name": "Children's Hospital",
        "address": "400 Child Street",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560007",
        "phone": "080-555-0106",
        "email": "info@childrenshospital.com",
        "website": "www.childrenshospital.com",
        "latitude": 12.9316,
        "longitude": 77.5546,
        "total_beds": 300,
        "available_beds": 25,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "Pediatrics, Pediatric Surgery, Neonatology",
        "rating": 4.4
    },
    {
        "id": 8,
        "name": "Women's Health Center",
        "address": "500 Women's Way",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560008",
        "phone": "080-555-0107",
        "email": "info@womenshealth.com",
        "website": "www.womenshealth.com",
        "latitude": 12.9216,
        "longitude": 77.5446,
        "total_beds": 200,
        "available_beds": 15,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "OB/GYN, Neonatology, Breast Health",
        "rating": 4.2
    },
    {
        "id": 9,
        "name": "Orthopedic Specialty Hospital",
        "address": "600 Orthopedic Drive",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560009",
        "phone": "080-555-0108",
        "email": "info@orthopedicspecialty.com",
        "website": "www.orthopedicspecialty.com",
        "latitude": 12.9116,
        "longitude": 77.5346,
        "total_beds": 250,
        "available_beds": 30,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "Orthopedics, Sports Medicine, Joint Replacement",
        "rating": 4.5
    },
    {
        "id": 10,
        "name": "Cardiac Care Center",
        "address": "700 Heart Lane",
        "city": "Bangalore",
        "state": "Karnataka",
        "zip_code": "560010",
        "phone": "080-555-0109",
        "email": "info@cardiaccare.com",
        "website": "www.cardiaccare.com",
        "latitude": 12.9016,
        "longitude": 77.5246,
        "total_beds": 300,
        "available_beds": 20,
        "emergency_services": True,
        "ambulance_available": True,
        "specialties": "Cardiology, Cardiac Surgery, Interventional Cardiology",
        "rating": 4.7
    }
]

@bp.route("/search", methods=["GET"])
@jwt_required()
def search_hospitals():
    try:
        specialty = request.args.get("specialty", "").strip().lower()
        lat = request.args.get("lat", type=float)
        lng = request.args.get("lng", type=float)
        radius = request.args.get("radius", 50, type=float)
        
        results = hospitals_db.copy()
        
        # Filter by specialty
        if specialty:
            results = [h for h in results if specialty in h["specialties"].lower()]
        
        # Calculate distance if coordinates provided
        if lat and lng:
            for h in results:
                if h["latitude"] and h["longitude"]:
                    distance = calculate_distance(lat, lng, h["latitude"], h["longitude"])
                    h["distance_km"] = round(distance, 2)
                else:
                    h["distance_km"] = None
            
            # Filter by radius
            results = [h for h in results if h.get("distance_km", 0) <= radius]
            
            # Sort by distance
            results.sort(key=lambda x: x.get("distance_km", float("inf")))
        
        return jsonify({"hospitals": results}), 200
        
    except Exception as e:
        logger.error(f"Hospital search error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/<int:hospital_id>", methods=["GET"])
@jwt_required()
def get_hospital_details(hospital_id):
    try:
        for hospital in hospitals_db:
            if hospital["id"] == hospital_id:
                return jsonify({"hospital": hospital}), 200
        return jsonify({"error": "Hospital not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/beds", methods=["GET"])
@jwt_required()
def get_available_beds():
    try:
        beds = [{
            "hospital_name": h["name"],
            "available_beds": h["available_beds"],
            "total_beds": h["total_beds"],
            "emergency": h["emergency_services"]
        } for h in hospitals_db if h["available_beds"] > 0]
        
        beds.sort(key=lambda x: x["available_beds"], reverse=True)
        return jsonify({"available_beds": beds}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def calculate_distance(lat1, lng1, lat2, lng2):
    from math import radians, sin, cos, sqrt, asin
    R = 6371
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    return R * c
