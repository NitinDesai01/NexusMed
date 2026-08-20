from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime
import uuid

bp = Blueprint("appointment", __name__, url_prefix="/api/appointments")
logger = logging.getLogger(__name__)

# Doctor Database with better condition matching
doctors_db = [
    {
        "id": 1,
        "name": "Dr. Rajesh Kumar",
        "specialization": "Cardiology",
        "keywords": ["heart", "chest", "palpitations", "blood pressure", "cardiac", "angina", "heart attack", "breath", "shortness"],
        "hospital": "City General Hospital",
        "experience": 15,
        "consultation_fee": 1500,
        "rating": 4.8,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    },
    {
        "id": 2,
        "name": "Dr. Priya Sharma",
        "specialization": "Neurology",
        "keywords": ["headache", "migraine", "dizziness", "seizure", "stroke", "brain", "nerve", "tremor", "memory", "confusion", "faint"],
        "hospital": "Memorial Medical Center",
        "experience": 12,
        "consultation_fee": 1800,
        "rating": 4.9,
        "available_days": ["Monday", "Wednesday", "Friday"]
    },
    {
        "id": 3,
        "name": "Dr. Suresh Reddy",
        "specialization": "Orthopedics",
        "keywords": ["bone", "joint", "knee", "fracture", "arthritis", "spine", "sports", "back", "hip", "shoulder", "ligament", "cartilage"],
        "hospital": "St. Mary's Hospital",
        "experience": 10,
        "consultation_fee": 1200,
        "rating": 4.6,
        "available_days": ["Tuesday", "Thursday", "Saturday"]
    },
    {
        "id": 4,
        "name": "Dr. Ananya Patel",
        "specialization": "Pediatrics",
        "keywords": ["child", "baby", "fever", "cough", "cold", "vaccination", "growth", "development", "infant", "toddler", "teen"],
        "hospital": "Children's Hospital",
        "experience": 8,
        "consultation_fee": 1000,
        "rating": 4.7,
        "available_days": ["Monday", "Tuesday", "Thursday", "Friday"]
    },
    {
        "id": 5,
        "name": "Dr. Vikram Singh",
        "specialization": "Gastroenterology",
        "keywords": ["stomach", "abdominal", "diarrhea", "constipation", "indigestion", "ulcer", "liver", "acid", "reflux", "gas", "bloating"],
        "hospital": "Regional Medical Center",
        "experience": 14,
        "consultation_fee": 1600,
        "rating": 4.8,
        "available_days": ["Monday", "Wednesday", "Friday", "Saturday"]
    },
    {
        "id": 6,
        "name": "Dr. Meera Iyer",
        "specialization": "Gynecology",
        "keywords": ["pregnancy", "women", "menstrual", "ovary", "uterus", "fertility", "delivery", "pcod", "menopause", "period", "cramps"],
        "hospital": "Women's Health Center",
        "experience": 11,
        "consultation_fee": 1300,
        "rating": 4.9,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    },
    {
        "id": 7,
        "name": "Dr. Arjun Nair",
        "specialization": "Dermatology",
        "keywords": ["skin", "rash", "itch", "acne", "pimple", "eczema", "hair", "allergy", "scaly", "dry", "redness", "bumps"],
        "hospital": "City General Hospital",
        "experience": 9,
        "consultation_fee": 1100,
        "rating": 4.5,
        "available_days": ["Tuesday", "Thursday", "Saturday"]
    },
    {
        "id": 8,
        "name": "Dr. Deepak Gupta",
        "specialization": "Ophthalmology",
        "keywords": ["eye", "vision", "blurred", "glaucoma", "cataract", "redness", "sight", "blind", "double vision", "eye pain"],
        "hospital": "Memorial Medical Center",
        "experience": 13,
        "consultation_fee": 1400,
        "rating": 4.7,
        "available_days": ["Monday", "Wednesday", "Friday"]
    },
    {
        "id": 9,
        "name": "Dr. Kavya Krishnan",
        "specialization": "Psychiatry",
        "keywords": ["anxiety", "depression", "stress", "insomnia", "mental", "panic", "mood", "behavior", "sleep", "worry", "sad"],
        "hospital": "University Medical Center",
        "experience": 10,
        "consultation_fee": 1700,
        "rating": 4.6,
        "available_days": ["Monday", "Wednesday", "Thursday", "Friday"]
    },
    {
        "id": 10,
        "name": "Dr. Ravi Desai",
        "specialization": "Cardiology",
        "keywords": ["heart", "chest", "palpitations", "blood pressure", "cardiac", "angina", "heart attack", "breath", "shortness"],
        "hospital": "Cardiac Care Center",
        "experience": 18,
        "consultation_fee": 2000,
        "rating": 4.9,
        "available_days": ["Monday", "Tuesday", "Thursday", "Friday"]
    },
    {
        "id": 11,
        "name": "Dr. Lakshmi Narayanan",
        "specialization": "General Medicine",
        "keywords": ["fever", "cough", "cold", "sore", "throat", "body", "pain", "infection", "weakness", "flu", "viral"],
        "hospital": "Community Health Hospital",
        "experience": 20,
        "consultation_fee": 800,
        "rating": 4.4,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    },
    {
        "id": 12,
        "name": "Dr. Senthil Kumar",
        "specialization": "ENT",
        "keywords": ["ear", "nose", "throat", "sinus", "hearing", "tonsillitis", "breathing", "snoring", "voice", "hoarseness"],
        "hospital": "St. Mary's Hospital",
        "experience": 12,
        "consultation_fee": 1200,
        "rating": 4.6,
        "available_days": ["Monday", "Wednesday", "Friday"]
    }
]

# Symptom to specialization mapping
symptom_to_specialization = {
    # Cardiology
    "chest": "Cardiology",
    "heart": "Cardiology",
    "palpitations": "Cardiology",
    "blood pressure": "Cardiology",
    "angina": "Cardiology",
    "shortness of breath": "Cardiology",
    "breath": "Cardiology",
    
    # Neurology
    "headache": "Neurology",
    "migraine": "Neurology",
    "dizziness": "Neurology",
    "seizure": "Neurology",
    "stroke": "Neurology",
    "brain": "Neurology",
    "nerve": "Neurology",
    "memory": "Neurology",
    "confusion": "Neurology",
    
    # Orthopedics
    "knee": "Orthopedics",
    "joint": "Orthopedics",
    "bone": "Orthopedics",
    "fracture": "Orthopedics",
    "arthritis": "Orthopedics",
    "back": "Orthopedics",
    "spine": "Orthopedics",
    "hip": "Orthopedics",
    "shoulder": "Orthopedics",
    
    # Dermatology
    "skin": "Dermatology",
    "rash": "Dermatology",
    "itch": "Dermatology",
    "acne": "Dermatology",
    "eczema": "Dermatology",
    "hair": "Dermatology",
    "dry skin": "Dermatology",
    
    # Psychiatry
    "anxiety": "Psychiatry",
    "depression": "Psychiatry",
    "stress": "Psychiatry",
    "insomnia": "Psychiatry",
    "panic": "Psychiatry",
    "mood": "Psychiatry",
    "sleep": "Psychiatry",
    
    # Gastroenterology
    "stomach": "Gastroenterology",
    "abdominal": "Gastroenterology",
    "diarrhea": "Gastroenterology",
    "constipation": "Gastroenterology",
    "ulcer": "Gastroenterology",
    "liver": "Gastroenterology",
    "acid": "Gastroenterology",
    "gas": "Gastroenterology",
    "bloating": "Gastroenterology",
    
    # Gynecology
    "pregnancy": "Gynecology",
    "menstrual": "Gynecology",
    "period": "Gynecology",
    "ovary": "Gynecology",
    "pcod": "Gynecology",
    "menopause": "Gynecology",
    "cramps": "Gynecology",
    
    # ENT
    "ear": "ENT",
    "nose": "ENT",
    "throat": "ENT",
    "sinus": "ENT",
    "hearing": "ENT",
    "snoring": "ENT",
    "voice": "ENT",
    
    # Pediatrics
    "child": "Pediatrics",
    "baby": "Pediatrics",
    "infant": "Pediatrics",
    "toddler": "Pediatrics",
    "vaccination": "Pediatrics",
    "growth": "Pediatrics",
    "development": "Pediatrics",
    
    # General Medicine
    "fever": "General Medicine",
    "cough": "General Medicine",
    "cold": "General Medicine",
    "sore throat": "General Medicine",
    "body pain": "General Medicine",
    "infection": "General Medicine",
    "weakness": "General Medicine",
    "flu": "General Medicine",
    "viral": "General Medicine"
}

appointments_db = []

@bp.route("/find-doctor", methods=["POST"])
@jwt_required()
def find_doctor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        symptoms = data.get("symptoms", "").strip()
        if not symptoms:
            return jsonify({"error": "Symptoms are required"}), 400
        
        logger.info(f"Finding doctor for symptoms: {symptoms}")
        symptoms_lower = symptoms.lower()
        
        # Step 1: Find matching specialization
        matched_specializations = {}
        for keyword, specialization in symptom_to_specialization.items():
            if keyword in symptoms_lower:
                matched_specializations[specialization] = matched_specializations.get(specialization, 0) + 1
        
        # Step 2: Find doctors for the best matching specialization
        if matched_specializations:
            best_specialization = max(matched_specializations, key=matched_specializations.get)
        else:
            best_specialization = "General Medicine"
        
        logger.info(f"Best matching specialization: {best_specialization}")
        
        # Step 3: Find doctors with that specialization
        matched_doctors = []
        for doctor in doctors_db:
            if doctor["specialization"] == best_specialization:
                # Calculate match score based on keywords
                score = 0
                for keyword in doctor.get("keywords", []):
                    if keyword in symptoms_lower:
                        score += 2
                matched_doctors.append({
                    "id": doctor["id"],
                    "name": doctor["name"],
                    "specialization": doctor["specialization"],
                    "hospital": doctor["hospital"],
                    "experience": doctor["experience"],
                    "consultation_fee": doctor["consultation_fee"],
                    "rating": doctor["rating"],
                    "match_score": score
                })
        
        # Sort by match score and rating
        matched_doctors.sort(key=lambda x: (x.get("match_score", 0), x["rating"]), reverse=True)
        
        return jsonify({
            "analysis": {
                "symptoms": symptoms,
                "identified_specialization": best_specialization,
                "confidence": len(matched_doctors) > 0,
                "matched_keywords": list(matched_specializations.keys())
            },
            "recommended_doctors": matched_doctors[:3],
            "message": f"We found {len(matched_doctors)} doctors for your condition"
        }), 200
        
    except Exception as e:
        logger.error(f"Find doctor error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/book", methods=["POST"])
@jwt_required()
def book_appointment():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user_id = get_jwt_identity()
        
        patient_name = data.get("patient_name", "")
        patient_phone = data.get("patient_phone", "")
        patient_email = data.get("patient_email", "")
        doctor_id = data.get("doctor_id")
        date = data.get("date")
        time = data.get("time")
        symptoms = data.get("symptoms", "")
        
        if not patient_name or not patient_phone:
            return jsonify({"error": "Patient name and phone are required"}), 400
        
        if not doctor_id or not date or not time:
            return jsonify({"error": "Doctor, date and time are required"}), 400
        
        doctor = None
        for d in doctors_db:
            if d["id"] == doctor_id:
                doctor = d
                break
        
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404
        
        for appointment in appointments_db:
            if (appointment["doctor_id"] == doctor_id and 
                appointment["date"] == date and 
                appointment["time"] == time and
                appointment["status"] != "cancelled"):
                return jsonify({"error": "Slot not available"}), 400
        
        booking_id = str(uuid.uuid4())[:8]
        booking = {
            "booking_id": booking_id,
            "user_id": user_id,
            "doctor_id": doctor_id,
            "doctor_name": doctor["name"],
            "specialization": doctor["specialization"],
            "hospital": doctor["hospital"],
            "date": date,
            "time": time,
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "patient_email": patient_email,
            "symptoms": symptoms,
            "status": "confirmed",
            "consultation_fee": doctor["consultation_fee"],
            "booked_at": datetime.now().isoformat()
        }
        
        appointments_db.append(booking)
        
        return jsonify({
            "message": "✅ Appointment booked successfully!",
            "booking": booking
        }), 201
        
    except Exception as e:
        logger.error(f"Book appointment error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/my-appointments", methods=["GET"])
@jwt_required()
def get_my_appointments():
    user_id = get_jwt_identity()
    user_appointments = [a for a in appointments_db if a["user_id"] == user_id]
    user_appointments.sort(key=lambda x: x["date"])
    return jsonify({"appointments": user_appointments}), 200

@bp.route("/cancel/<booking_id>", methods=["POST"])
@jwt_required()
def cancel_appointment(booking_id):
    user_id = get_jwt_identity()
    for appointment in appointments_db:
        if appointment["booking_id"] == booking_id:
            if appointment["user_id"] != user_id:
                return jsonify({"error": "Unauthorized"}), 403
            appointment["status"] = "cancelled"
            return jsonify({"message": "Appointment cancelled successfully"}), 200
    return jsonify({"error": "Appointment not found"}), 404

@bp.route("/available-slots/<int:doctor_id>", methods=["GET"])
@jwt_required()
def get_available_slots(doctor_id):
    date = request.args.get("date", "")
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    slots = []
    for hour in range(9, 17):
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            booked = False
            for app in appointments_db:
                if (app["doctor_id"] == doctor_id and 
                    app["date"] == date and
                    app["time"] == time_str and
                    app["status"] != "cancelled"):
                    booked = True
                    break
            if not booked:
                slots.append(time_str)
    
    return jsonify({
        "doctor_id": doctor_id,
        "date": date,
        "available_slots": slots[:10]
    }), 200

@bp.route("/doctors", methods=["GET"])
@jwt_required()
def get_doctors():
    return jsonify({"doctors": doctors_db}), 200