from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
import json

bp = Blueprint("symptom", __name__, url_prefix="/api/symptoms")
logger = logging.getLogger(__name__)

# Expanded Disease Database with specific symptom-disease mapping
disease_db = {
    # Respiratory
    "Common Cold": ["cough", "sore throat", "runny nose", "sneezing", "congestion", "mild fever"],
    "Influenza": ["fever", "headache", "muscle pain", "fatigue", "cough", "chills", "sweating", "body ache"],
    "COVID-19": ["fever", "cough", "shortness of breath", "fatigue", "loss of taste", "loss of smell", "sore throat"],
    "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "mucus", "difficulty breathing"],
    "Bronchitis": ["cough", "mucus", "fatigue", "shortness of breath", "fever", "chest discomfort", "wheezing"],
    "Strep Throat": ["sore throat", "fever", "swollen lymph nodes", "difficulty swallowing", "red tonsils", "white patches"],
    "Tuberculosis": ["cough", "weight loss", "night sweats", "fever", "fatigue", "chest pain", "blood in cough"],
    "Asthma": ["shortness of breath", "wheezing", "cough", "chest tightness", "difficulty breathing", "allergy"],
    
    # Allergies & Sinus
    "Allergy": ["sneezing", "itchy eyes", "runny nose", "rash", "watery eyes", "hives", "itching"],
    "Sinusitis": ["headache", "facial pain", "nasal congestion", "fever", "pressure", "post nasal drip", "sinus pain"],
    "Hay Fever": ["sneezing", "runny nose", "itchy eyes", "congestion", "watery eyes", "cough"],
    
    # Neurological
    "Migraine": ["headache", "nausea", "sensitivity to light", "dizziness", "vomiting", "aura", "throbbing pain"],
    "Tension Headache": ["headache", "neck pain", "shoulder pain", "pressure", "tightness", "stress"],
    "Cluster Headache": ["severe headache", "eye pain", "redness", "tearing", "nasal congestion"],
    
    # Digestive
    "Food Poisoning": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever", "cramps", "stomach pain"],
    "Gastroenteritis": ["diarrhea", "vomiting", "abdominal pain", "fever", "nausea", "stomach cramps"],
    "Acid Reflux": ["heartburn", "chest pain", "regurgitation", "difficulty swallowing", "sour taste", "burning"],
    "Gastritis": ["abdominal pain", "nausea", "bloating", "loss of appetite", "indigestion", "burning"],
    "Ulcer": ["abdominal pain", "burning", "nausea", "bloating", "heartburn", "dark stools"],
    "IBS": ["abdominal pain", "bloating", "diarrhea", "constipation", "cramps", "gas"],
    
    # Infectious
    "Dengue": ["fever", "headache", "muscle pain", "joint pain", "rash", "eye pain", "bleeding", "low platelets", "red spots"],
    "Malaria": ["fever", "chills", "sweating", "headache", "muscle pain", "fatigue", "nausea", "vomiting"],
    "Typhoid": ["fever", "headache", "abdominal pain", "constipation", "diarrhea", "weakness", "loss of appetite"],
    "Chikungunya": ["fever", "joint pain", "muscle pain", "headache", "rash", "fatigue", "swelling"],
    "Chickenpox": ["rash", "fever", "itching", "blisters", "fatigue", "headache", "loss of appetite"],
    "Measles": ["fever", "rash", "cough", "runny nose", "red eyes", "sore throat", "white spots"],
    
    # Chronic
    "Diabetes": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow healing", "hunger", "weight loss"],
    "Hypertension": ["headache", "dizziness", "blurred vision", "chest pain", "shortness of breath", "nosebleeds"],
    "Arthritis": ["joint pain", "stiffness", "swelling", "reduced range of motion", "warmth", "morning stiffness"],
    "Osteoarthritis": ["joint pain", "stiffness", "swelling", "cracking", "bone spurs", "loss of flexibility"],
    "Rheumatoid Arthritis": ["joint pain", "swelling", "morning stiffness", "fatigue", "fever", "weight loss"],
    
    # Skin
    "Eczema": ["itchy skin", "redness", "dry skin", "rash", "cracked skin", "inflammation", "scaly patches"],
    "Hives": ["red bumps", "itching", "swelling", "rash", "burning sensation", "allergy"],
    "Psoriasis": ["red patches", "scaly skin", "itching", "dry skin", "cracked skin", "joint pain"],
    "Acne": ["pimples", "blackheads", "whiteheads", "redness", "oily skin", "scars"],
    "Ringworm": ["rash", "itching", "red ring", "scaly skin", "hair loss"],
    
    # Mental Health
    "Anxiety": ["worry", "restlessness", "fatigue", "difficulty concentrating", "irritability", "sleep problems", "racing heart"],
    "Depression": ["sadness", "loss of interest", "fatigue", "sleep changes", "appetite changes", "worthlessness", "suicidal thoughts"],
    "Panic Disorder": ["panic attacks", "racing heart", "sweating", "trembling", "shortness of breath", "fear of dying"],
    "Insomnia": ["difficulty sleeping", "waking early", "daytime fatigue", "irritability", "anxiety", "poor concentration"],
    
    # Women's Health
    "UTI": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "fever", "urgency"],
    "Pregnancy": ["missed period", "nausea", "fatigue", "breast tenderness", "frequent urination", "vomiting"],
    "PCOS": ["irregular periods", "excess hair", "acne", "weight gain", "fertility issues", "ovarian cysts"],
    "Menopause": ["hot flashes", "night sweats", "irregular periods", "mood swings", "sleep problems", "vaginal dryness"],
    
    # Emergency
    "Heart Attack": ["chest pain", "shortness of breath", "nausea", "dizziness", "sweating", "arm pain", "jaw pain"],
    "Stroke": ["facial drooping", "arm weakness", "speech difficulty", "confusion", "headache", "vision problems", "numbness"],
    "Appendicitis": ["abdominal pain", "nausea", "vomiting", "fever", "loss of appetite", "pain in lower right abdomen"],
    
    # ENT
    "Ear Infection": ["ear pain", "fever", "difficulty hearing", "fluid drainage", "irritability", "balance issues"],
    "Sinusitis": ["headache", "facial pain", "nasal congestion", "fever", "pressure", "post nasal drip", "sinus pain"],
    "Tonsillitis": ["sore throat", "difficulty swallowing", "swollen tonsils", "fever", "bad breath", "voice changes"],
    
    # Eye
    "Conjunctivitis": ["red eye", "itching", "discharge", "watery eye", "swelling", "crusting"],
    "Cataract": ["blurred vision", "cloudy vision", "difficulty seeing at night", "fading colors", "double vision"],
    "Glaucoma": ["eye pain", "headache", "blurred vision", "halos", "redness", "nausea"],
    
    # General
    "Anemia": ["fatigue", "weakness", "pale skin", "shortness of breath", "dizziness", "cold hands", "headache"],
    "Dehydration": ["thirst", "dry mouth", "dark urine", "fatigue", "dizziness", "confusion", "dry skin"],
    "Thyroid Issues": ["fatigue", "weight changes", "mood changes", "hair loss", "temperature sensitivity", "heart palpitations"],
}

# Symptom recommendations
symptom_advice = {
    "fever": "Rest, stay hydrated, use fever reducers like paracetamol if needed. Monitor temperature.",
    "cough": "Use honey or lozenges for relief. Stay hydrated. Avoid irritants.",
    "headache": "Rest in a quiet dark room. Apply cold compress. Stay hydrated.",
    "sore throat": "Gargle with warm salt water. Use throat lozenges. Drink warm fluids.",
    "fatigue": "Get plenty of rest. Stay hydrated. Eat nutritious food.",
    "nausea": "Eat small bland meals. Stay hydrated. Avoid strong odors.",
    "vomiting": "Stay hydrated with small sips of water. Rest. Eat bland foods when ready.",
    "diarrhea": "Stay hydrated. Eat bland foods like bananas and rice. Avoid dairy.",
    "muscle pain": "Rest the affected area. Apply heat or cold therapy. Gentle stretching.",
    "joint pain": "Rest. Apply ice or heat. Consider anti-inflammatory medication.",
    "shortness of breath": "Sit upright. Seek immediate medical attention if severe.",
    "chest pain": "Seek immediate emergency medical attention. Call emergency services.",
    "dizziness": "Sit or lie down. Drink water. Avoid sudden movements.",
    "rash": "Avoid scratching. Use anti-itch cream. See doctor if severe.",
    "skin rash": "Avoid scratching. Use anti-itch cream. Keep skin moisturized.",
    "itching": "Apply cold compress. Use anti-itch cream. Avoid scratching.",
    "acne": "Wash face gently. Use non-comedogenic products. Avoid picking.",
    "anxiety": "Practice deep breathing. Talk to someone. Seek professional help if needed.",
    "depression": "Talk to someone. Seek professional help. Practice self-care.",
    "insomnia": "Maintain sleep schedule. Avoid screens before bed. Create relaxing routine.",
    "stomach pain": "Rest. Eat bland foods. Stay hydrated. Avoid spicy foods.",
    "back pain": "Rest. Apply heat or ice. Gentle stretching. Proper posture.",
    "knee pain": "Rest. Apply ice. Elevate. Avoid weight-bearing activities.",
    "joint swelling": "Rest. Apply ice. Elevate. See doctor if persistent.",
    "runny nose": "Stay hydrated. Use saline spray. Rest.",
    "sneezing": "Avoid allergens. Use antihistamines. Stay indoors.",
    "cold": "Rest. Stay hydrated. Use over-the-counter cold medicine.",
    "flu": "Rest. Stay hydrated. Use fever reducers. See doctor if severe.",
    "body pain": "Rest. Apply heat or cold. Gentle stretching. Stay hydrated.",
}

@bp.route("/analyze", methods=["POST"])
@jwt_required()
def analyze_symptoms():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        symptoms_text = data.get("symptoms", "").strip()
        if not symptoms_text:
            return jsonify({"error": "Symptoms are required"}), 400
        
        logger.info(f"Analyzing symptoms: {symptoms_text}")
        symptoms_lower = symptoms_text.lower()
        
        # Find matching diseases
        matched_diseases = []
        for disease, disease_symptoms in disease_db.items():
            match_count = 0
            matched_symptoms = []
            for symptom in disease_symptoms:
                if symptom in symptoms_lower:
                    match_count += 1
                    matched_symptoms.append(symptom)
            
            if match_count > 0:
                confidence = (match_count / len(disease_symptoms)) * 100
                matched_diseases.append({
                    "disease": disease,
                    "confidence": round(confidence, 0),
                    "matching_symptoms": matched_symptoms,
                    "match_count": match_count,
                    "total_symptoms": len(disease_symptoms)
                })
        
        # Sort by confidence
        matched_diseases.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Get top 5 predictions
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
        
        # Get recommendations
        recommendations = []
        for symptom in symptoms_lower.split():
            if symptom in symptom_advice:
                recommendations.append(symptom_advice[symptom])
            # Also check for multi-word symptoms
            for advice_symptom, advice in symptom_advice.items():
                if advice_symptom in symptoms_lower and advice not in recommendations:
                    recommendations.append(advice)
        
        if not recommendations:
            recommendations = [
                "Rest and stay hydrated",
                "Monitor your symptoms",
                "Consult a healthcare professional if symptoms persist"
            ]
        
        # Remove duplicates
        recommendations = list(dict.fromkeys(recommendations))[:5]
        
        response = {
            "analysis": {
                "symptoms_analyzed": symptoms_text,
                "possible_conditions": [d["disease"] for d in top_predictions] if top_predictions else ["No specific conditions identified"],
                "severity": severity,
                "recommendations": recommendations,
                "emergency_signs": severity == "high",
                "disclaimer": "This is an AI-based analysis. Always consult a healthcare professional."
            },
            "predictions": {
                "predictions": top_predictions,
                "model_used": "rule-based"
            },
            "disclaimer": "This is an AI-based analysis. Always consult a healthcare professional."
        }
        
        logger.info(f"Analysis complete: Found {len(top_predictions)} possible conditions")
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
                             "severe allergy", "head injury", "suicidal", "heart attack"]
        
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
        logger.error(f"Emergency check error: {str(e)}")
        return jsonify({"error": str(e)}), 500