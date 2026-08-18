from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime, timedelta
import uuid
import re

bp = Blueprint("appointment", __name__, url_prefix="/api/appointments")
logger = logging.getLogger(__name__)

# Doctor Database
doctors_db = [
    {
        "id": 1,
        "name": "Dr. Rajesh Kumar",
        "specialization": "Cardiology",
        "conditions": ["heart", "chest pain", "palpitations", "high blood pressure", "heart attack", "angina", "cardiac"],
        "hospital": "City General Hospital",
        "hospital_id": 1,
        "experience": 15,
        "consultation_fee": 1500,
        "rating": 4.8,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "available_time": "9:00 AM - 5:00 PM",
        "education": "MBBS, MD - Cardiology",
        "about": "Senior Cardiologist with 15 years of experience in treating heart conditions."
    },
    {
        "id": 2,
        "name": "Dr. Priya Sharma",
        "specialization": "Neurology",
        "conditions": ["headache", "migraine", "dizziness", "seizure", "stroke", "brain", "nerve", "tremor", "memory loss"],
        "hospital": "Memorial Medical Center",
        "hospital_id": 2,
        "experience": 12,
        "consultation_fee": 1800,
        "rating": 4.9,
        "available_days": ["Monday", "Wednesday", "Friday"],
        "available_time": "10:00 AM - 6:00 PM",
        "education": "MBBS, MD - Neurology",
        "about": "Specializes in neurological disorders and brain health."
    },
    {
        "id": 3,
        "name": "Dr. Suresh Reddy",
        "specialization": "Orthopedics",
        "conditions": ["bone", "joint pain", "back pain", "knee pain", "fracture", "arthritis", "spine", "sports injury"],
        "hospital": "St. Mary's Hospital",
        "hospital_id": 3,
        "experience": 10,
        "consultation_fee": 1200,
        "rating": 4.6,
        "available_days": ["Tuesday", "Thursday", "Saturday"],
        "available_time": "8:00 AM - 4:00 PM",
        "education": "MBBS, MS - Orthopedics",
        "about": "Expert in joint replacement and sports injuries."
    },
    {
        "id": 4,
        "name": "Dr. Ananya Patel",
        "specialization": "Pediatrics",
        "conditions": ["child", "baby", "fever", "cough", "cold", "vaccination", "growth", "development"],
        "hospital": "Children's Hospital",
        "hospital_id": 7,
        "experience": 8,
        "consultation_fee": 1000,
        "rating": 4.7,
        "available_days": ["Monday", "Tuesday", "Thursday", "Friday"],
        "available_time": "9:30 AM - 5:30 PM",
        "education": "MBBS, MD - Pediatrics",
        "about": "Dedicated to children's health and development."
    },
    {
        "id": 5,
        "name": "Dr. Vikram Singh",
        "specialization": "Gastroenterology",
        "conditions": ["stomach", "abdominal pain", "diarrhea", "constipation", "indigestion", "ulcer", "liver", "acid reflux"],
        "hospital": "Regional Medical Center",
        "hospital_id": 6,
        "experience": 14,
        "consultation_fee": 1600,
        "rating": 4.8,
        "available_days": ["Monday", "Wednesday", "Friday", "Saturday"],
        "available_time": "9:00 AM - 5:00 PM",
        "education": "MBBS, DM - Gastroenterology",
        "about": "Specializes in digestive system disorders and liver diseases."
    },
    {
        "id": 6,
        "name": "Dr. Meera Iyer",
        "specialization": "Gynecology",
        "conditions": ["pregnancy", "women", "menstrual", "ovary", "uterus", "fertility", "delivery", "pcod", "menopause"],
        "hospital": "Women's Health Center",
        "hospital_id": 8,
        "experience": 11,
        "consultation_fee": 1300,
        "rating": 4.9,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "available_time": "9:00 AM - 5:00 PM",
        "education": "MBBS, MD - Gynecology",
        "about": "Women's health specialist with expertise in pregnancy care."
    },
    {
        "id": 7,
        "name": "Dr. Arjun Nair",
        "specialization": "Dermatology",
        "conditions": ["skin", "rash", "itch", "acne", "pimple", "eczema", "hair loss", "allergy", "scaly skin"],
        "hospital": "City General Hospital",
        "hospital_id": 1,
        "experience": 9,
        "consultation_fee": 1100,
        "rating": 4.5,
        "available_days": ["Tuesday", "Thursday", "Saturday"],
        "available_time": "10:00 AM - 6:00 PM",
        "education": "MBBS, MD - Dermatology",
        "about": "Expert in skin, hair, and nail disorders."
    },
    {
        "id": 8,
        "name": "Dr. Deepak Gupta",
        "specialization": "Ophthalmology",
        "conditions": ["eye", "vision", "blurred vision", "glaucoma", "cataract", "eye pain", "redness", "vision loss"],
        "hospital": "Memorial Medical Center",
        "hospital_id": 2,
        "experience": 13,
        "consultation_fee": 1400,
        "rating": 4.7,
        "available_days": ["Monday", "Wednesday", "Friday"],
        "available_time": "9:00 AM - 5:00 PM",
        "education": "MBBS, MS - Ophthalmology",
        "about": "Specializes in eye care and vision correction."
    },
    {
        "id": 9,
        "name": "Dr. Kavya Krishnan",
        "specialization": "Psychiatry",
        "conditions": ["anxiety", "depression", "stress", "insomnia", "mental health", "panic", "mood", "behavior"],
        "hospital": "University Medical Center",
        "hospital_id": 4,
        "experience": 10,
        "consultation_fee": 1700,
        "rating": 4.6,
        "available_days": ["Monday", "Wednesday", "Thursday", "Friday"],
        "available_time": "9:30 AM - 5:30 PM",
        "education": "MBBS, MD - Psychiatry",
        "about": "Mental health specialist focusing on anxiety and depression."
    },
    {
        "id": 10,
        "name": "Dr. Ravi Desai",
        "specialization": "Cardiology",
        "conditions": ["heart", "chest pain", "palpitations", "high blood pressure", "heart attack", "angina", "cardiac"],
        "hospital": "Cardiac Care Center",
        "hospital_id": 10,
        "experience": 18,
        "consultation_fee": 2000,
        "rating": 4.9,
        "available_days": ["Monday", "Tuesday", "Thursday", "Friday"],
        "available_time": "8:00 AM - 4:00 PM",
        "education": "MBBS, DM - Cardiology",
        "about": "Senior interventional cardiologist with expertise in heart surgeries."
    },
    {
        "id": 11,
        "name": "Dr. Lakshmi Narayanan",
        "specialization": "General Medicine",
        "conditions": ["fever", "cough", "cold", "sore throat", "body pain", "infection", "general", "weakness"],
        "hospital": "Community Health Hospital",
        "hospital_id": 5,
        "experience": 20,
        "consultation_fee": 800,
        "rating": 4.4,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "available_time": "8:00 AM - 8:00 PM",
        "education": "MBBS, MD - General Medicine",
        "about": "Experienced general physician treating all common illnesses."
    },
    {
        "id": 12,
        "name": "Dr. Senthil Kumar",
        "specialization": "ENT",
        "conditions": ["ear", "nose", "throat", "sore throat", "sinus", "hearing loss", "tonsillitis", "allergy", "breathing"],
        "hospital": "St. Mary's Hospital",
        "hospital_id": 3,
        "experience": 12,
        "consultation_fee": 1200,
        "rating": 4.6,
        "available_days": ["Monday", "Wednesday", "Friday"],
        "available_time": "9:00 AM - 5:00 PM",
        "education": "MBBS, MS - ENT",
        "about": "Specialist in ear, nose, and throat disorders."
    }
]

# Appointment bookings storage
appointments_db = []

# Condition to specialization mapping
condition_to_specialization = {
    "heart": "Cardiology", "chest pain": "Cardiology", "palpitations": "Cardiology",
    "high blood pressure": "Cardiology", "heart attack": "Cardiology", "angina": "Cardiology",
    "headache": "Neurology", "migraine": "Neurology", "dizziness": "Neurology",
    "seizure": "Neurology", "stroke": "Neurology", "brain": "Neurology",
    "nerve": "Neurology", "tremor": "Neurology", "memory loss": "Neurology",
    "bone": "Orthopedics", "joint pain": "Orthopedics", "back pain": "Orthopedics",
    "knee pain": "Orthopedics", "fracture": "Orthopedics", "arthritis": "Orthopedics",
    "spine": "Orthopedics", "sports injury": "Orthopedics",
    "child": "Pediatrics", "baby": "Pediatrics", "vaccination": "Pediatrics",
    "growth": "Pediatrics", "development": "Pediatrics",
    "stomach": "Gastroenterology", "abdominal pain": "Gastroenterology", "diarrhea": "Gastroenterology",
    "constipation": "Gastroenterology", "indigestion": "Gastroenterology", "ulcer": "Gastroenterology",
    "liver": "Gastroenterology", "acid reflux": "Gastroenterology",
    "pregnancy": "Gynecology", "women": "Gynecology", "menstrual": "Gynecology",
    "ovary": "Gynecology", "uterus": "Gynecology", "fertility": "Gynecology",
    "delivery": "Gynecology", "pcod": "Gynecology", "menopause": "Gynecology",
    "skin": "Dermatology", "rash": "Dermatology", "itch": "Dermatology",
    "acne": "Dermatology", "pimple": "Dermatology", "eczema": "Dermatology",
    "hair loss": "Dermatology", "eye": "Ophthalmology", "vision": "Ophthalmology",
    "blurred vision": "Ophthalmology", "glaucoma": "Ophthalmology", "cataract": "Ophthalmology",
    "eye pain": "Ophthalmology", "anxiety": "Psychiatry", "depression": "Psychiatry",
    "stress": "Psychiatry", "insomnia": "Psychiatry", "mental health": "Psychiatry",
    "panic": "Psychiatry", "mood": "Psychiatry", "ear": "ENT", "nose": "ENT",
    "throat": "ENT", "sinus": "ENT", "hearing loss": "ENT", "tonsillitis": "ENT",
    "breathing": "ENT", "fever": "General Medicine", "cough": "General Medicine",
    "cold": "General Medicine", "sore throat": "General Medicine", "body pain": "General Medicine",
    "infection": "General Medicine", "weakness": "General Medicine",
}

@bp.route("/find-doctor", methods=["POST"])
@jwt_required()
def find_doctor():
    try:
        data = request.get_json()
        symptoms = data.get("symptoms", "").strip()
        
        if not symptoms:
            return jsonify({"error": "Please describe your symptoms"}), 400
        
        symptoms_lower = symptoms.lower()
        matched_specializations = {}
        
        for condition, specialization in condition_to_specialization.items():
            if condition in symptoms_lower:
                matched_specializations[specialization] = matched_specializations.get(specialization, 0) + 1
        
        if not matched_specializations:
            matched_specializations = {"General Medicine": 1}
        
        best_specialization = max(matched_specializations, key=matched_specializations.get)
        
        matched_doctors = []
        for doctor in doctors_db:
            if doctor["specialization"] == best_specialization:
                score = 0
                for condition in doctor.get("conditions", []):
                    if condition in symptoms_lower:
                        score += 1
                matched_doctors.append({**doctor, "match_score": score})
        
        matched_doctors.sort(key=lambda x: (x.get("match_score", 0), x["rating"]), reverse=True)
        
        return jsonify({
            "analysis": {
                "symptoms": symptoms,
                "identified_specialization": best_specialization,
                "matched_conditions": list(matched_specializations.keys())
            },
            "recommended_doctors": matched_doctors[:5],
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
        
        # Check slot availability
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
    for i, appointment in enumerate(appointments_db):
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
