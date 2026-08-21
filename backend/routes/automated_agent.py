from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime, timedelta
import uuid
import re
from data_store import add_appointment

bp = Blueprint("automated_agent", __name__, url_prefix="/api/automated")
logger = logging.getLogger(__name__)

# Disease Database for symptom analysis
disease_db = {
    "Common Cold": ["cough", "sore throat", "runny nose", "sneezing", "congestion", "mild fever"],
    "Influenza": ["fever", "headache", "muscle pain", "fatigue", "cough", "chills", "sweating"],
    "COVID-19": ["fever", "cough", "shortness of breath", "fatigue", "loss of taste", "loss of smell"],
    "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "mucus"],
    "Bronchitis": ["cough", "mucus", "fatigue", "shortness of breath", "fever"],
    "Dengue": ["fever", "headache", "muscle pain", "joint pain", "rash", "eye pain", "bleeding"],
    "Malaria": ["fever", "chills", "sweating", "headache", "muscle pain", "fatigue"],
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever"],
    "Migraine": ["headache", "nausea", "sensitivity to light", "dizziness", "vomiting"],
    "Allergy": ["sneezing", "itchy eyes", "runny nose", "rash", "watery eyes"],
    "Sinusitis": ["headache", "facial pain", "nasal congestion", "fever", "pressure"],
    "Asthma": ["shortness of breath", "wheezing", "cough", "chest tightness"],
    "Heart Attack": ["chest pain", "shortness of breath", "nausea", "dizziness", "sweating", "arm pain"],
    "Stroke": ["facial drooping", "arm weakness", "speech difficulty", "confusion", "headache"],
    "UTI": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain"],
    "Diabetes": ["increased thirst", "frequent urination", "fatigue", "blurred vision"],
    "Hypertension": ["headache", "dizziness", "blurred vision", "chest pain"],
    "Anxiety": ["worry", "restlessness", "fatigue", "difficulty concentrating", "irritability"],
    "Depression": ["sadness", "loss of interest", "fatigue", "sleep changes", "appetite changes"]
}

# Medicine Database
medicine_db = {
    "Paracetamol": {"generic": "Acetaminophen", "price": 5.00, "category": "Analgesic", "dosage": "500mg", "frequency": "Every 6 hours"},
    "Ibuprofen": {"generic": "Ibuprofen", "price": 8.00, "category": "NSAID", "dosage": "400mg", "frequency": "Every 8 hours"},
    "Cetirizine": {"generic": "Cetirizine HCl", "price": 6.00, "category": "Antihistamine", "dosage": "10mg", "frequency": "Once daily"},
    "Amoxicillin": {"generic": "Amoxicillin", "price": 12.00, "category": "Antibiotic", "dosage": "500mg", "frequency": "Every 12 hours"},
    "Omeprazole": {"generic": "Omeprazole", "price": 10.00, "category": "Antacid", "dosage": "20mg", "frequency": "Once daily"},
    "Metformin": {"generic": "Metformin HCl", "price": 8.00, "category": "Antidiabetic", "dosage": "500mg", "frequency": "Twice daily"},
    "Aspirin": {"generic": "Acetylsalicylic Acid", "price": 4.00, "category": "NSAID", "dosage": "325mg", "frequency": "Every 6 hours"},
    "Loratadine": {"generic": "Loratadine", "price": 7.00, "category": "Antihistamine", "dosage": "10mg", "frequency": "Once daily"}
}

# Doctors Database
doctors_db = [
    {"id": 1, "name": "Dr. Rajesh Kumar", "specialization": "Cardiology", "hospital": "City General Hospital", "experience": 15, "consultation_fee": 1500, "rating": 4.8},
    {"id": 2, "name": "Dr. Priya Sharma", "specialization": "Neurology", "hospital": "Memorial Medical Center", "experience": 12, "consultation_fee": 1800, "rating": 4.9},
    {"id": 3, "name": "Dr. Suresh Reddy", "specialization": "Orthopedics", "hospital": "St. Mary's Hospital", "experience": 10, "consultation_fee": 1200, "rating": 4.6},
    {"id": 4, "name": "Dr. Ananya Patel", "specialization": "Pediatrics", "hospital": "Children's Hospital", "experience": 8, "consultation_fee": 1000, "rating": 4.7},
    {"id": 5, "name": "Dr. Vikram Singh", "specialization": "Gastroenterology", "hospital": "Regional Medical Center", "experience": 14, "consultation_fee": 1600, "rating": 4.8},
    {"id": 6, "name": "Dr. Meera Iyer", "specialization": "Gynecology", "hospital": "Women's Health Center", "experience": 11, "consultation_fee": 1300, "rating": 4.9},
    {"id": 7, "name": "Dr. Arjun Nair", "specialization": "Dermatology", "hospital": "City General Hospital", "experience": 9, "consultation_fee": 1100, "rating": 4.5},
    {"id": 8, "name": "Dr. Deepak Gupta", "specialization": "Ophthalmology", "hospital": "Memorial Medical Center", "experience": 13, "consultation_fee": 1400, "rating": 4.7},
    {"id": 9, "name": "Dr. Kavya Krishnan", "specialization": "Psychiatry", "hospital": "University Medical Center", "experience": 10, "consultation_fee": 1700, "rating": 4.6},
    {"id": 10, "name": "Dr. Ravi Desai", "specialization": "Cardiology", "hospital": "Cardiac Care Center", "experience": 18, "consultation_fee": 2000, "rating": 4.9}
]

# Symptom to specialization mapping
symptom_to_specialization = {
    "chest": "Cardiology",
    "heart": "Cardiology",
    "palpitations": "Cardiology",
    "headache": "Neurology",
    "migraine": "Neurology",
    "dizziness": "Neurology",
    "knee": "Orthopedics",
    "joint": "Orthopedics",
    "bone": "Orthopedics",
    "child": "Pediatrics",
    "baby": "Pediatrics",
    "stomach": "Gastroenterology",
    "abdominal": "Gastroenterology",
    "pregnancy": "Gynecology",
    "women": "Gynecology",
    "skin": "Dermatology",
    "rash": "Dermatology",
    "eye": "Ophthalmology",
    "vision": "Ophthalmology",
    "anxiety": "Psychiatry",
    "depression": "Psychiatry",
    "stress": "Psychiatry",
    "fever": "General Medicine",
    "cough": "General Medicine",
    "cold": "General Medicine"
}

# Emergency keywords
emergency_keywords = [
    "chest pain", "difficulty breathing", "shortness of breath", 
    "severe bleeding", "loss of consciousness", "stroke", 
    "severe allergy", "head injury", "heart attack", 
    "severe pain", "unconscious", "bleeding"
]

# Store automated sessions
automated_sessions = []

@bp.route("/analyze-and-act", methods=["POST"])
@jwt_required()
def analyze_and_act():
    """Fully automated AI agent - analyze symptoms and take action"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        symptoms = data.get("symptoms", "").strip()
        patient_name = data.get("patient_name", "Patient")
        patient_phone = data.get("patient_phone", "")
        patient_email = data.get("patient_email", "")
        
        if not symptoms:
            return jsonify({"error": "Please describe your symptoms"}), 400
        
        logger.info(f"🤖 Automated Agent processing: {symptoms}")
        
        # Step 1: Analyze symptoms
        analysis = analyze_symptoms(symptoms)
        
        # Step 2: Check for emergency
        emergency_check = check_emergency(symptoms)
        
        # Step 3: Predict diseases
        predictions = predict_diseases(symptoms)
        
        # Step 4: Find specialization
        specialization = find_specialization(symptoms)
        
        # Step 5: Find doctors (with fallback)
        doctors = find_doctors(specialization)
        if not doctors:
            # Fallback: Get all doctors or General Medicine doctors
            doctors = [d for d in doctors_db if d["specialization"] == "General Medicine"]
        
        # Step 6: Recommend medicines
        medicines = recommend_medicines(symptoms, analysis)
        
        # Step 7: Generate session ID
        session_id = "AUTO-" + str(uuid.uuid4())[:8].upper()
        
        # Step 8: Create automated response with permission requests
        response = {
            "session_id": session_id,
            "analysis": analysis,
            "emergency_check": emergency_check,
            "predictions": predictions[:5] if predictions else [],
            "specialization": specialization,
            "recommended_doctors": doctors[:3] if doctors else [],
            "recommended_medicines": medicines[:3] if medicines else [],
            "actions": {
                "emergency_required": emergency_check["is_emergency"],
                "appointment_suggested": len(doctors) > 0 and not emergency_check["is_emergency"],
                "medicine_suggested": len(medicines) > 0
            },
            "permission_requests": {
                "appointment": {
                    "required": len(doctors) > 0 and not emergency_check["is_emergency"],
                    "message": f"Would you like to book an appointment with {doctors[0]['name'] if doctors else 'a General Physician'} ({doctors[0]['specialization'] if doctors else 'General Medicine'})?",
                    "doctor": doctors[0] if doctors else None,
                    "status": "pending"
                },
                "ambulance": {
                    "required": emergency_check["is_emergency"],
                    "message": "🚨 Emergency detected! Would you like to request an ambulance?",
                    "status": "pending"
                }
            },
            "summary": generate_summary(symptoms, analysis, predictions, doctors, medicines, emergency_check),
            "next_steps": generate_next_steps(emergency_check, doctors, medicines)
        }
        
        # Store session
        automated_sessions.append({
            "session_id": session_id,
            "user_id": user_id,
            "symptoms": symptoms,
            "patient_name": patient_name,
            "patient_phone": patient_phone,
            "patient_email": patient_email,
            "response": response,
            "appointment_booked": False,
            "ambulance_requested": False,
            "created_at": datetime.now().isoformat()
        })
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Automated agent error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/confirm-appointment", methods=["POST"])
@jwt_required()
def confirm_appointment():
    """Confirm appointment booking after user permission"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        session_id = data.get("session_id")
        confirm = data.get("confirm", False)
        
        if not session_id:
            return jsonify({"error": "Session ID required"}), 400
        
        # Find session
        session = None
        for s in automated_sessions:
            if s["session_id"] == session_id:
                session = s
                break
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        if not confirm:
            return jsonify({
                "message": "Appointment booking cancelled",
                "status": "cancelled"
            }), 200
        
        # Get doctor from session
        recommended_doctors = session["response"].get("recommended_doctors", [])
        if not recommended_doctors:
            return jsonify({"error": "No doctor available"}), 404
        
        doctor = recommended_doctors[0]
        
        # Generate appointment date
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        time = "10:00"
        
        # Create booking
        booking_id = str(uuid.uuid4())[:8]
        booking = {
            "booking_id": booking_id,
            "user_id": user_id,
            "doctor_id": doctor["id"],
            "doctor_name": doctor["name"],
            "specialization": doctor["specialization"],
            "hospital": doctor["hospital"],
            "date": date,
            "time": time,
            "patient_name": session["patient_name"],
            "patient_phone": session["patient_phone"],
            "patient_email": session["patient_email"],
            "symptoms": session["symptoms"],
            "status": "confirmed",
            "consultation_fee": doctor["consultation_fee"],
            "booked_at": datetime.now().isoformat()
        }
        
        # Add to shared appointments database
        add_appointment(booking)
        
        # Update session
        session["appointment_booked"] = True
        session["booking_id"] = booking_id
        
        return jsonify({
            "message": "✅ Appointment booked successfully!",
            "booking": booking,
            "doctor": doctor,
            "status": "confirmed"
        }), 201
        
    except Exception as e:
        logger.error(f"Confirm appointment error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/confirm-ambulance", methods=["POST"])
@jwt_required()
def confirm_ambulance():
    """Confirm ambulance request after user permission"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        session_id = data.get("session_id")
        confirm = data.get("confirm", False)
        
        if not session_id:
            return jsonify({"error": "Session ID required"}), 400
        
        # Find session
        session = None
        for s in automated_sessions:
            if s["session_id"] == session_id:
                session = s
                break
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        if not confirm:
            return jsonify({
                "message": "Ambulance request cancelled",
                "status": "cancelled"
            }), 200
        
        # Generate ambulance request
        request_id = "EMG-" + str(uuid.uuid4())[:8].upper()
        
        ambulance_response = {
            "request_id": request_id,
            "status": "dispatched",
            "ambulance": {
                "vehicle_number": "AMB-001",
                "driver_name": "Rajesh Kumar",
                "driver_phone": "+91-9876543210",
                "estimated_arrival": "5-10 minutes",
                "equipment_level": "Advanced"
            },
            "message": "🚨 Ambulance dispatched to your location!"
        }
        
        # Update session
        session["ambulance_requested"] = True
        session["ambulance_request_id"] = request_id
        
        return jsonify(ambulance_response), 201
        
    except Exception as e:
        logger.error(f"Confirm ambulance error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def analyze_symptoms(symptoms):
    """Analyze symptoms and return analysis"""
    symptoms_lower = symptoms.lower()
    
    # Find matching diseases
    matched_diseases = []
    for disease, disease_symptoms in disease_db.items():
        match_count = sum(1 for s in disease_symptoms if s in symptoms_lower)
        if match_count > 0:
            confidence = (match_count / len(disease_symptoms)) * 100
            matched_diseases.append({
                "disease": disease,
                "confidence": round(confidence, 0),
                "matching_symptoms": [s for s in disease_symptoms if s in symptoms_lower]
            })
    
    matched_diseases.sort(key=lambda x: x["confidence"], reverse=True)
    
    # Determine severity
    severity = "low"
    if "chest pain" in symptoms_lower or "difficulty breathing" in symptoms_lower:
        severity = "high"
    elif "fever" in symptoms_lower and "cough" in symptoms_lower:
        severity = "medium"
    
    return {
        "symptoms_analyzed": symptoms,
        "possible_conditions": [d["disease"] for d in matched_diseases[:3]] if matched_diseases else ["No specific conditions identified"],
        "top_predictions": matched_diseases[:3] if matched_diseases else [],
        "severity": severity,
        "severity_level": severity.upper()
    }

def check_emergency(symptoms):
    """Check if symptoms indicate emergency"""
    symptoms_lower = symptoms.lower()
    matched_emergency = []
    
    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            matched_emergency.append(keyword)
    
    is_emergency = len(matched_emergency) > 0
    
    return {
        "is_emergency": is_emergency,
        "matched_signs": matched_emergency,
        "severity": "high" if is_emergency else "low",
        "message": "🚨 Emergency signs detected! Immediate action required." if is_emergency else "No emergency signs detected."
    }

def predict_diseases(symptoms):
    """Predict diseases with confidence"""
    symptoms_lower = symptoms.lower()
    predictions = []
    
    for disease, disease_symptoms in disease_db.items():
        match_count = sum(1 for s in disease_symptoms if s in symptoms_lower)
        if match_count > 0:
            confidence = (match_count / len(disease_symptoms)) * 100
            predictions.append({
                "disease": disease,
                "confidence": round(confidence, 0),
                "matching_symptoms": [s for s in disease_symptoms if s in symptoms_lower]
            })
    
    predictions.sort(key=lambda x: x["confidence"], reverse=True)
    return predictions[:5]

def find_specialization(symptoms):
    """Find specialization based on symptoms"""
    symptoms_lower = symptoms.lower()
    matched_specializations = {}
    
    for keyword, specialization in symptom_to_specialization.items():
        if keyword in symptoms_lower:
            matched_specializations[specialization] = matched_specializations.get(specialization, 0) + 1
    
    if matched_specializations:
        return max(matched_specializations, key=matched_specializations.get)
    return "General Medicine"

def find_doctors(specialization):
    """Find doctors by specialization"""
    matched_doctors = []
    for doctor in doctors_db:
        if doctor["specialization"] == specialization:
            matched_doctors.append(doctor)
    return matched_doctors

def recommend_medicines(symptoms, analysis):
    """Recommend medicines based on symptoms"""
    symptoms_lower = symptoms.lower()
    recommended = []
    
    # Check for specific conditions
    if "fever" in symptoms_lower and "cough" in symptoms_lower:
        recommended.append({
            "name": "Paracetamol",
            "dosage": "500mg",
            "frequency": "Every 6 hours",
            "purpose": "Fever and pain relief"
        })
        recommended.append({
            "name": "Cetirizine",
            "dosage": "10mg",
            "frequency": "Once daily",
            "purpose": "Cold and allergy relief"
        })
    
    if "headache" in symptoms_lower:
        recommended.append({
            "name": "Paracetamol",
            "dosage": "500mg",
            "frequency": "Every 6 hours",
            "purpose": "Headache relief"
        })
    
    if "pain" in symptoms_lower and "joint" in symptoms_lower:
        recommended.append({
            "name": "Ibuprofen",
            "dosage": "400mg",
            "frequency": "Every 8 hours",
            "purpose": "Pain and inflammation relief"
        })
    
    if "allergy" in symptoms_lower or "rash" in symptoms_lower:
        recommended.append({
            "name": "Cetirizine",
            "dosage": "10mg",
            "frequency": "Once daily",
            "purpose": "Allergy relief"
        })
    
    # Add general recommendation if none found
    if not recommended:
        recommended.append({
            "name": "Paracetamol",
            "dosage": "500mg",
            "frequency": "Every 6 hours",
            "purpose": "General pain and fever relief"
        })
    
    return recommended[:3]

def generate_summary(symptoms, analysis, predictions, doctors, medicines, emergency_check):
    """Generate user-friendly summary"""
    summary_parts = []
    
    summary_parts.append(f"📋 Symptoms: {symptoms}")
    summary_parts.append(f"⚕️ Severity: {analysis['severity'].upper()}")
    
    if emergency_check["is_emergency"]:
        summary_parts.append("🚨 EMERGENCY: Immediate medical attention required!")
    
    if predictions:
        top_disease = predictions[0]["disease"] if predictions else "Unknown"
        summary_parts.append(f"🔍 Likely Condition: {top_disease}")
    
    if doctors:
        summary_parts.append(f"👨‍⚕️ Recommended Specialist: {doctors[0]['specialization'] if doctors else 'General Medicine'}")
    
    if medicines:
        summary_parts.append(f"💊 Recommended Medicine: {medicines[0]['name'] if medicines else 'None'}")
    
    return " | ".join(summary_parts)

def generate_next_steps(emergency_check, doctors, medicines):
    """Generate next steps for user"""
    next_steps = []
    
    if emergency_check["is_emergency"]:
        next_steps.append({
            "action": "ambulance",
            "message": "🚑 Emergency ambulance dispatched",
            "priority": "high"
        })
    
    if doctors and not emergency_check["is_emergency"]:
        next_steps.append({
            "action": "appointment",
            "message": f"📅 Book appointment with {doctors[0]['name'] if doctors else 'a General Physician'} ({doctors[0]['specialization'] if doctors else 'General Medicine'})",
            "priority": "medium"
        })
    
    if medicines:
        next_steps.append({
            "action": "medicine",
            "message": f"💊 Take {medicines[0]['name'] if medicines else 'Paracetamol'} ({medicines[0]['dosage'] if medicines else '500mg'}) - {medicines[0]['frequency'] if medicines else 'Every 6 hours'}",
            "priority": "medium"
        })
    
    if not emergency_check["is_emergency"]:
        next_steps.append({
            "action": "rest",
            "message": "🛌 Rest and stay hydrated",
            "priority": "low"
        })
    
    return next_steps