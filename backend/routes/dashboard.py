from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime, timedelta
import uuid
from data_store import appointments_db, get_user_appointments

bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")
logger = logging.getLogger(__name__)

# Health tips
health_tips = [
    {"id": 1, "title": "Stay Hydrated", "description": "Drink at least 8 glasses of water daily", "icon": "💧"},
    {"id": 2, "title": "Regular Exercise", "description": "30 minutes of exercise 5 times a week", "icon": "🏃"},
    {"id": 3, "title": "Balanced Diet", "description": "Eat fruits, vegetables, and whole grains", "icon": "🥗"},
    {"id": 4, "title": "Adequate Sleep", "description": "Get 7-8 hours of quality sleep", "icon": "😴"},
    {"id": 5, "title": "Stress Management", "description": "Practice meditation or deep breathing", "icon": "🧘"},
    {"id": 6, "title": "Regular Checkups", "description": "Visit your doctor annually", "icon": "🩺"},
    {"id": 7, "title": "Vaccination", "description": "Stay up to date with vaccinations", "icon": "💉"},
    {"id": 8, "title": "Mental Health", "description": "Take care of your mental wellbeing", "icon": "🧠"},
]

@bp.route("/stats", methods=["GET"])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics with AI recommendations"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's appointments from shared storage
        user_appointments = get_user_appointments(user_id)
        total_appointments = len(user_appointments)
        upcoming_appointments = [a for a in user_appointments if a["status"] == "confirmed" and a["date"] >= datetime.now().strftime("%Y-%m-%d")]
        
        # Calculate stats
        stats = {
            "total_appointments": total_appointments,
            "upcoming_appointments": len(upcoming_appointments),
            "completed_appointments": len([a for a in user_appointments if a["status"] == "completed"]),
            "cancelled_appointments": len([a for a in user_appointments if a["status"] == "cancelled"]),
            "next_appointment": upcoming_appointments[0] if upcoming_appointments else None,
            "health_score": calculate_health_score(user_appointments)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations():
    """Get AI-powered health recommendations"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's appointments from shared storage
        user_appointments = get_user_appointments(user_id)
        
        # AI-based recommendations
        recommendations = []
        
        # If no appointments, suggest booking
        if len(user_appointments) == 0:
            recommendations.append({
                "id": "rec1",
                "title": "Book Your First Appointment",
                "description": "Regular health checkups are important. Book your first appointment today.",
                "type": "action",
                "priority": "high",
                "icon": "📅",
                "action": "Go to Appointment Booking"
            })
        
        # Check for upcoming appointments
        upcoming = [a for a in user_appointments if a["status"] == "confirmed" and a["date"] >= datetime.now().strftime("%Y-%m-%d")]
        if len(upcoming) == 0 and len(user_appointments) > 0:
            recommendations.append({
                "id": "rec2",
                "title": "Schedule a Follow-up",
                "description": "You don't have any upcoming appointments. Consider scheduling a follow-up.",
                "type": "reminder",
                "priority": "medium",
                "icon": "🔔",
                "action": "Book Appointment"
            })
        
        # Health tips based on previous appointments
        if len(user_appointments) > 0:
            latest = user_appointments[-1]
            if latest.get("specialization") == "Cardiology":
                recommendations.append({
                    "id": "rec3",
                    "title": "Heart Health Tips",
                    "description": "Maintain a heart-healthy diet, exercise regularly, and monitor blood pressure.",
                    "type": "tip",
                    "priority": "medium",
                    "icon": "❤️"
                })
            elif latest.get("specialization") == "Neurology":
                recommendations.append({
                    "id": "rec4",
                    "title": "Brain Health Tips",
                    "description": "Keep your brain active with puzzles, reading, and social connections.",
                    "type": "tip",
                    "priority": "medium",
                    "icon": "🧠"
                })
            elif latest.get("specialization") == "Orthopedics":
                recommendations.append({
                    "id": "rec5",
                    "title": "Bone Health Tips",
                    "description": "Maintain strong bones with calcium-rich foods and weight-bearing exercises.",
                    "type": "tip",
                    "priority": "medium",
                    "icon": "🦴"
                })
            elif latest.get("specialization") == "Dermatology":
                recommendations.append({
                    "id": "rec6",
                    "title": "Skin Care Tips",
                    "description": "Protect your skin with sunscreen, moisturize daily, and stay hydrated.",
                    "type": "tip",
                    "priority": "medium",
                    "icon": "🧴"
                })
        
        # Add general health tips
        recommendations.extend([
            {
                "id": "rec7",
                "title": "Stay Hydrated",
                "description": "Drink at least 8 glasses of water daily for optimal health.",
                "type": "tip",
                "priority": "low",
                "icon": "💧"
            },
            {
                "id": "rec8",
                "title": "Regular Exercise",
                "description": "30 minutes of moderate exercise 5 days a week.",
                "type": "tip",
                "priority": "low",
                "icon": "🏃"
            },
            {
                "id": "rec9",
                "title": "Stress Management",
                "description": "Practice meditation or deep breathing for 10 minutes daily.",
                "type": "tip",
                "priority": "low",
                "icon": "🧘"
            }
        ])
        
        return jsonify({"recommendations": recommendations}), 200
        
    except Exception as e:
        logger.error(f"Recommendations error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/health-tips", methods=["GET"])
@jwt_required()
def get_health_tips():
    """Get daily health tips"""
    try:
        # Rotate tips based on day
        day = datetime.now().day
        tip_index = day % len(health_tips)
        return jsonify({
            "tip": health_tips[tip_index],
            "tips": health_tips
        }), 200
        
    except Exception as e:
        logger.error(f"Health tips error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def calculate_health_score(appointments):
    """Calculate health score based on appointment history"""
    if not appointments:
        return 70  # Default score
    
    total = len(appointments)
    completed = len([a for a in appointments if a["status"] == "completed"])
    
    if total == 0:
        return 70
    
    # Base score
    score = 60
    
    # Add points for completed appointments
    if total > 0:
        score += (completed / total) * 20
    
    # Add points for regular checkups
    if total >= 3:
        score += 10
    
    # Add points for recent appointments
    recent = [a for a in appointments if a.get("booked_at") and datetime.fromisoformat(a["booked_at"]) > datetime.now() - timedelta(days=180)]
    if len(recent) > 0:
        score += 10
    
    return min(round(score), 100)

# Add some sample appointments for testing
@bp.route("/add-sample", methods=["POST"])
@jwt_required()
def add_sample_appointment():
    try:
        user_id = get_jwt_identity()
        doctors = [
            {"id": 1, "name": "Dr. Rajesh Kumar", "specialization": "Cardiology", "hospital": "City General Hospital"},
            {"id": 2, "name": "Dr. Priya Sharma", "specialization": "Neurology", "hospital": "Memorial Medical Center"},
            {"id": 3, "name": "Dr. Suresh Reddy", "specialization": "Orthopedics", "hospital": "St. Mary's Hospital"},
        ]
        
        for doctor in doctors:
            booking_id = str(uuid.uuid4())[:8]
            date = (datetime.now() + timedelta(days=7 + len(appointments_db))).strftime("%Y-%m-%d")
            appointment = {
                "booking_id": booking_id,
                "user_id": user_id,
                "doctor_id": doctor["id"],
                "doctor_name": doctor["name"],
                "specialization": doctor["specialization"],
                "hospital": doctor["hospital"],
                "date": date,
                "time": f"{9 + (len(appointments_db) % 8)}:30",
                "patient_name": "Demo Patient",
                "patient_phone": "9876543210",
                "patient_email": "demo@nexusmed.com",
                "symptoms": "Routine checkup",
                "status": "confirmed" if len(appointments_db) < 2 else "completed",
                "consultation_fee": 1500,
                "booked_at": datetime.now().isoformat()
            }
            appointments_db.append(appointment)
        
        return jsonify({"message": "Sample appointments added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500