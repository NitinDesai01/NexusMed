from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import logging

bp = Blueprint("community", __name__, url_prefix="/api/community")
logger = logging.getLogger(__name__)

# Health awareness content database
health_content = {
    "Heart Health": {
        "title": "Heart Health",
        "icon": "❤️",
        "content": "Heart disease is the leading cause of death worldwide. Taking care of your heart is essential for a long and healthy life.",
        "symptoms": "Chest pain, shortness of breath, palpitations, fatigue, swelling in legs",
        "prevention": "Regular exercise, healthy diet, avoid smoking, control blood pressure and cholesterol",
        "tips": [
            "Exercise for at least 30 minutes daily",
            "Eat a heart-healthy diet rich in fruits and vegetables",
            "Avoid processed foods and excess salt",
            "Monitor your blood pressure regularly",
            "Quit smoking and limit alcohol consumption",
            "Get regular health checkups"
        ],
        "risk_factors": "High blood pressure, high cholesterol, smoking, obesity, diabetes, family history"
    },
    "Diabetes Prevention": {
        "title": "Diabetes Prevention",
        "icon": "💉",
        "content": "Type 2 diabetes is largely preventable through lifestyle changes. Early intervention can significantly reduce your risk.",
        "symptoms": "Increased thirst, frequent urination, fatigue, blurred vision, slow healing wounds",
        "prevention": "Maintain healthy weight, regular exercise, balanced diet, regular blood sugar monitoring",
        "tips": [
            "Maintain a healthy weight",
            "Exercise regularly (at least 30 minutes daily)",
            "Eat a balanced diet with limited sugar and refined carbs",
            "Monitor your blood sugar levels",
            "Stay hydrated with water instead of sugary drinks",
            "Get regular health screenings"
        ],
        "risk_factors": "Family history, overweight, physical inactivity, high blood pressure, age over 45"
    },
    "Mental Health": {
        "title": "Mental Health Awareness",
        "icon": "🧠",
        "content": "Mental health is just as important as physical health. Taking care of your mental wellbeing is essential for overall health.",
        "symptoms": "Persistent sadness, anxiety, mood swings, social withdrawal, changes in sleep or appetite",
        "prevention": "Regular exercise, adequate sleep, social connections, stress management techniques",
        "tips": [
            "Practice mindfulness and meditation daily",
            "Stay connected with friends and family",
            "Get adequate sleep (7-8 hours)",
            "Exercise regularly to boost mood",
            "Seek professional help when needed",
            "Limit social media and screen time"
        ],
        "risk_factors": "Stress, trauma, family history, substance abuse, social isolation"
    },
    "Nutrition": {
        "title": "Nutrition and Diet",
        "icon": "🥗",
        "content": "Proper nutrition is essential for optimal health. A balanced diet provides the nutrients your body needs to function properly.",
        "symptoms": "Fatigue, weakness, poor concentration, frequent illness",
        "prevention": "Eat a variety of fruits and vegetables, whole grains, lean proteins, healthy fats",
        "tips": [
            "Eat at least 5 servings of fruits and vegetables daily",
            "Choose whole grains over refined grains",
            "Include lean proteins in your meals",
            "Stay hydrated with water",
            "Limit processed foods and added sugars",
            "Practice mindful eating"
        ],
        "risk_factors": "Poor diet, processed food consumption, lack of fruits and vegetables"
    },
    "Exercise": {
        "title": "Exercise and Fitness",
        "icon": "🏃",
        "content": "Regular physical activity is crucial for maintaining good health and preventing chronic diseases.",
        "symptoms": "Fatigue, weight gain, muscle weakness, joint stiffness",
        "prevention": "Regular exercise, proper form, gradual progression, variety in workouts",
        "tips": [
            "Get at least 150 minutes of moderate exercise weekly",
            "Include both cardio and strength training",
            "Start slowly and gradually increase intensity",
            "Find activities you enjoy",
            "Stay consistent with your routine",
            "Include stretching and flexibility exercises"
        ],
        "risk_factors": "Sedentary lifestyle, lack of time, no proper guidance"
    },
    "Stress Management": {
        "title": "Stress Management",
        "icon": "🧘",
        "content": "Chronic stress can have serious effects on both mental and physical health. Learning to manage stress is essential.",
        "symptoms": "Anxiety, irritability, sleep problems, headaches, fatigue, muscle tension",
        "prevention": "Regular relaxation, time management, healthy boundaries, self-care practices",
        "tips": [
            "Practice deep breathing exercises daily",
            "Try meditation or yoga",
            "Set realistic goals and priorities",
            "Take regular breaks during work",
            "Maintain a healthy work-life balance",
            "Talk to someone about your feelings"
        ],
        "risk_factors": "High workload, lack of support, financial stress, relationship issues"
    },
    "Vaccination": {
        "title": "Vaccination Awareness",
        "icon": "💉",
        "content": "Vaccines are one of the most effective ways to prevent infectious diseases and protect public health.",
        "symptoms": "No symptoms (preventive measure)",
        "prevention": "Stay up to date with recommended vaccines for your age group",
        "tips": [
            "Follow the recommended vaccination schedule",
            "Get annual flu shots",
            "Stay updated with COVID-19 vaccines",
            "Consult your doctor about vaccines for travel",
            "Keep vaccination records",
            "Encourage family members to get vaccinated"
        ],
        "risk_factors": "Age, underlying health conditions, travel, exposure to high-risk environments"
    },
    "Cancer Screening": {
        "title": "Cancer Screening",
        "icon": "🔬",
        "content": "Regular cancer screenings can detect cancer early when it is most treatable.",
        "symptoms": "Varies by cancer type",
        "prevention": "Regular screenings, healthy lifestyle, avoiding risk factors",
        "tips": [
            "Follow recommended screening guidelines for your age group",
            "Get regular mammograms for breast cancer",
            "Schedule colonoscopies for colorectal cancer",
            "Get regular Pap tests for cervical cancer",
            "Screen for prostate cancer as recommended",
            "Know your family history"
        ],
        "risk_factors": "Age, family history, genetic mutations, lifestyle factors"
    },
    "Asthma": {
        "title": "Asthma Management",
        "icon": "🫁",
        "content": "Asthma is a chronic lung condition that can be managed with proper treatment and lifestyle modifications.",
        "symptoms": "Wheezing, shortness of breath, chest tightness, coughing",
        "prevention": "Avoid triggers, take prescribed medications, monitor symptoms regularly",
        "tips": [
            "Use your inhaler as prescribed",
            "Identify and avoid asthma triggers",
            "Monitor your symptoms daily",
            "Keep your home dust-free",
            "Exercise with caution",
            "Have an asthma action plan"
        ],
        "risk_factors": "Family history, allergies, respiratory infections, environmental factors"
    },
    "Allergies": {
        "title": "Allergy Prevention",
        "icon": "🤧",
        "content": "Allergies are immune system reactions to normally harmless substances. Proper management can reduce symptoms significantly.",
        "symptoms": "Sneezing, runny nose, itchy eyes, rash, hives, breathing difficulties",
        "prevention": "Avoid allergens, use antihistamines, keep environment clean",
        "tips": [
            "Keep windows closed during high pollen seasons",
            "Use HEPA filters in your home",
            "Take antihistamines as needed",
            "Avoid known allergens",
            "Carry an epinephrine auto-injector if prescribed",
            "Identify food allergies and avoid triggers"
        ],
        "risk_factors": "Family history, environmental exposure, immune system sensitivity"
    },
    "Sleep Hygiene": {
        "title": "Sleep Hygiene",
        "icon": "😴",
        "content": "Good sleep is essential for physical and mental health. Poor sleep can affect your health in many ways.",
        "symptoms": "Daytime fatigue, irritability, difficulty concentrating, mood changes",
        "prevention": "Consistent sleep schedule, relaxing bedtime routine, comfortable environment",
        "tips": [
            "Maintain a consistent sleep schedule",
            "Create a relaxing bedtime routine",
            "Keep your bedroom cool and dark",
            "Avoid screens before bedtime",
            "Limit caffeine and alcohol consumption",
            "Exercise during the day"
        ],
        "risk_factors": "Irregular schedule, stress, caffeine, alcohol, poor sleep environment"
    },
    "First Aid": {
        "title": "First Aid Basics",
        "icon": "🩹",
        "content": "Knowing basic first aid can save lives. Everyone should learn essential first aid skills.",
        "symptoms": "Bleeding, burns, fractures, choking, unconsciousness",
        "prevention": "Learn CPR, keep first aid kit handy, take first aid training",
        "tips": [
            "Learn CPR and first aid techniques",
            "Keep a well-stocked first aid kit",
            "Know emergency contact numbers",
            "Stay calm in emergencies",
            "Treat wounds properly to prevent infection",
            "Take a certified first aid course"
        ],
        "risk_factors": "Accidents, injuries, medical emergencies"
    }
}

@bp.route("/awareness", methods=["GET"])
@jwt_required()
def get_awareness_content():
    """Get health awareness content for a specific topic"""
    try:
        topic = request.args.get("topic", "general")
        logger.info(f"Fetching awareness content for: {topic}")
        
        # Find matching content
        matched_content = None
        matched_key = None
        
        for key, content in health_content.items():
            if topic.lower() in key.lower() or key.lower() in topic.lower():
                matched_content = content
                matched_key = key
                break
        
        # If no exact match, try partial match
        if not matched_content:
            for key, content in health_content.items():
                if any(word in key.lower() for word in topic.lower().split()):
                    matched_content = content
                    matched_key = key
                    break
        
        # If still no match, return general health info
        if not matched_content:
            matched_content = {
                "title": "Health Awareness",
                "icon": "📚",
                "content": "Health is a state of complete physical, mental and social well-being.",
                "tips": [
                    "Stay active and exercise regularly",
                    "Eat a balanced and nutritious diet",
                    "Get enough sleep and rest",
                    "Stay hydrated",
                    "Manage stress effectively",
                    "Visit your doctor regularly"
                ],
                "prevention": "Adopt a healthy lifestyle",
                "risk_factors": "Various factors depending on specific health topics"
            }
            matched_key = "Health Awareness"
        
        return jsonify({
            "content": {
                "topic": matched_key,
                "title": matched_content.get("title", matched_key),
                "icon": matched_content.get("icon", "📚"),
                "content": matched_content.get("content", "Information about " + matched_key),
                "symptoms": matched_content.get("symptoms", "No specific symptoms listed"),
                "prevention": matched_content.get("prevention", "Maintain a healthy lifestyle"),
                "tips": matched_content.get("tips", ["Maintain a healthy lifestyle", "Consult your doctor for personalized advice"]),
                "risk_factors": matched_content.get("risk_factors", "Consult your doctor for personalized advice")
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Awareness content error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/alerts", methods=["GET"])
@jwt_required()
def get_alerts():
    """Get community health alerts"""
    try:
        # Return sample alerts
        alerts = [
            {"id": 1, "title": "Flu Season", "message": "Get your flu shot today!", "status": "active", "type": "warning"},
            {"id": 2, "title": "Health Camp", "message": "Free health checkup this weekend", "status": "active", "type": "info"},
            {"id": 3, "title": "COVID-19 Booster", "message": "Booster shots available now", "status": "active", "type": "info"}
        ]
        return jsonify({"alerts": alerts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/alerts", methods=["POST"])
@jwt_required()
def create_alert():
    """Create a community alert"""
    try:
        data = request.get_json()
        alert = {
            "id": 4,
            "title": data.get("title", "Health Alert"),
            "message": data.get("message", ""),
            "status": "active",
            "type": data.get("type", "info")
        }
        return jsonify(alert), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500