from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import logging

bp = Blueprint("symptom", __name__, url_prefix="/api/symptoms")
logger = logging.getLogger(__name__)

# Expanded Disease Database
disease_db = {
    # Respiratory
    "Common Cold": ["cough", "sore throat", "runny nose", "fever", "sneezing", "congestion"],
    "Influenza": ["fever", "headache", "muscle pain", "fatigue", "cough", "chills", "sweating"],
    "COVID-19": ["fever", "cough", "shortness of breath", "fatigue", "loss of taste", "loss of smell", "sore throat"],
    "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "mucus"],
    "Bronchitis": ["cough", "mucus", "fatigue", "shortness of breath", "fever", "chest discomfort"],
    "Strep Throat": ["sore throat", "fever", "swollen lymph nodes", "difficulty swallowing", "red tonsils"],
    
    # Allergies & Sinus
    "Allergy": ["sneezing", "itchy eyes", "runny nose", "rash", "watery eyes", "hives"],
    "Sinusitis": ["headache", "facial pain", "nasal congestion", "fever", "pressure", "post nasal drip"],
    
    # Neurological
    "Migraine": ["headache", "nausea", "sensitivity to light", "dizziness", "vomiting", "aura"],
    "Tension Headache": ["headache", "neck pain", "shoulder pain", "pressure", "tightness"],
    
    # Digestive
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever", "cramps"],
    "Gastroenteritis": ["diarrhea", "vomiting", "abdominal pain", "fever", "nausea"],
    "Acid Reflux": ["heartburn", "chest pain", "regurgitation", "difficulty swallowing", "sour taste"],
    "Gastritis": ["abdominal pain", "nausea", "bloating", "loss of appetite", "indigestion"],
    
    # Infectious
    "Dengue": ["fever", "headache", "muscle pain", "joint pain", "rash", "eye pain", "bleeding", "low platelets"],
    "Malaria": ["fever", "chills", "sweating", "headache", "muscle pain", "fatigue", "nausea"],
    "Typhoid": ["fever", "headache", "abdominal pain", "constipation", "diarrhea", "weakness"],
    "Chikungunya": ["fever", "joint pain", "muscle pain", "headache", "rash", "fatigue"],
    "Tuberculosis": ["cough", "weight loss", "night sweats", "fever", "fatigue", "chest pain"],
    
    # Chronic
    "Diabetes": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow healing", "hunger"],
    "Hypertension": ["headache", "dizziness", "blurred vision", "chest pain", "shortness of breath"],
    "Arthritis": ["joint pain", "stiffness", "swelling", "reduced range of motion", "warmth"],
    "Asthma": ["shortness of breath", "wheezing", "cough", "chest tightness", "difficulty breathing"],
    
    # Skin
    "Eczema": ["itchy skin", "redness", "dry skin", "rash", "cracked skin", "inflammation"],
    "Hives": ["red bumps", "itching", "swelling", "rash", "burning sensation"],
    
    # Mental Health
    "Anxiety": ["worry", "restlessness", "fatigue", "difficulty concentrating", "irritability", "sleep problems"],
    "Depression": ["sadness", "loss of interest", "fatigue", "sleep changes", "appetite changes", "worthlessness"],
    
    # Women's Health
    "UTI": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "fever"],
    "Pregnancy": ["missed period", "nausea", "fatigue", "breast tenderness", "frequent urination"],
    
    # Emergency
    "Heart Attack": ["chest pain", "shortness of breath", "nausea", "dizziness", "sweating", "arm pain"],
    "Stroke": ["facial drooping", "arm weakness", "speech difficulty", "confusion", "headache", "vision problems"]
}

# Symptom recommendations
symptom_advice = {
    "fever": "Rest, stay hydrated, use fever reducers like paracetamol if needed.",
    "cough": "Use honey or lozenges for relief. Stay hydrated.",
    "headache": "Rest in a quiet dark room. Apply cold compress.",
    "sore throat": "Gargle with warm salt water. Use throat lozenges.",
    "fatigue": "Get plenty of rest. Stay hydrated.",
    "nausea": "Eat small bland meals. Stay hydrated.",
    "vomiting": "Stay hydrated with small sips of water. Rest.",
    "diarrhea": "Stay hydrated. Eat bland foods like bananas and rice.",
    "muscle pain": "Rest the affected area. Apply heat or cold therapy.",
    "joint pain": "Rest. Apply ice or heat. Consider anti-inflammatory medication.",
    "shortness of breath": "Sit upright. Seek immediate medical attention if severe.",
    "chest pain": "Seek immediate emergency medical attention.",
    "dizziness": "Sit or lie down. Drink water. Avoid sudden movements.",
    "rash": "Avoid scratching. Use anti-itch cream. See doctor if severe.",
    "chills": "Keep warm. Rest. Monitor temperature.",
    "sweating": "Stay hydrated. Rest in a cool environment.",
    "weight loss": "Consult a doctor. Monitor diet.",
    "loss of appetite": "Eat small frequent meals. Stay hydrated.",
    "bleeding": "Apply pressure. Seek immediate medical attention.",
    "eye pain": "Rest eyes. Avoid bright light. Consult doctor."
}

@bp.route("/analyze", methods=["POST"])
@jwt_required()
def analyze_symptoms():
    try:
        data = request.get_json()
        symptoms_text = data.get("symptoms", "").strip()
        
        if not symptoms_text:
            return jsonify({"error": "Symptoms are required"}), 400
        
        symptoms_lower = symptoms_text.lower()
        logger.info(f"Analyzing symptoms: {symptoms_text}")
        
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
        top_predictions = matched_diseases[:5]
        
        # Determine severity
        severity = "low"
        emergency_keywords = ["chest pain", "difficulty breathing", "shortness of breath", "severe", "unconscious", "bleeding"]
        for keyword in emergency_keywords:
            if keyword in symptoms_lower:
                severity = "high"
                break
        
        if "fever" in symptoms_lower and "cough" in symptoms_lower:
            if severity == "low":
                severity = "medium"
        if "dengue" in symptoms_lower:
            severity = "high"
        
        # Get recommendations
        recommendations = []
        for symptom in symptoms_lower.split(","):
            symptom = symptom.strip()
            if symptom in symptom_advice:
                recommendations.append(symptom_advice[symptom])
        
        if not recommendations:
            recommendations = [
                "Rest and stay hydrated",
                "Monitor your symptoms",
                "Consult a healthcare professional if symptoms persist"
            ]
        
        response = {
            "analysis": {
                "symptoms_analyzed": symptoms_text,
                "possible_conditions": [d["disease"] for d in top_predictions] if top_predictions else ["No specific conditions identified"],
                "severity": severity,
                "recommendations": recommendations[:5],
                "emergency_signs": severity == "high",
                "disclaimer": "This is an AI-based analysis. Always consult a healthcare professional."
            },
            "predictions": {
                "predictions": top_predictions,
                "model_used": "rule-based"
            },
            "disclaimer": "This is an AI-based analysis. Always consult a healthcare professional."
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Symptom analysis error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/common", methods=["GET"])
@jwt_required()
def get_common_symptoms():
    symptoms = list(symptom_advice.keys())
    return jsonify({"symptoms": symptoms}), 200

@bp.route("/emergency", methods=["POST"])
@jwt_required()
def check_emergency():
    try:
        data = request.get_json()
        symptoms = data.get("symptoms", "").lower()
        
        emergency_keywords = ["chest pain", "difficulty breathing", "shortness of breath", 
                             "severe bleeding", "loss of consciousness", "stroke", 
                             "severe allergy", "head injury", "suicidal"]
        
        is_emergency = False
        matched_emergency = []
        for keyword in emergency_keywords:
            if keyword in symptoms:
                is_emergency = True
                matched_emergency.append(keyword)
        
        return jsonify({
            "is_emergency": is_emergency,
            "severity": "high" if is_emergency else "low",
            "recommendation": "Seek immediate emergency medical attention" if is_emergency else "Monitor symptoms",
            "emergency_services": ["call_ambulance", "go_to_emergency"] if is_emergency else [],
            "matched_emergency_signs": matched_emergency
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
