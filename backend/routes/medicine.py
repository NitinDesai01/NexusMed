from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import logging

bp = Blueprint("medicine", __name__, url_prefix="/api/medicines")
logger = logging.getLogger(__name__)

# Complete Medicine Database
medicines_db = {
    # Pain Relievers & Fever Reducers
    "Paracetamol": {
        "id": 1,
        "name": "Paracetamol",
        "generic_name": "Acetaminophen",
        "category": "Analgesic",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "description": "Used for pain relief and fever reduction.",
        "side_effects": "Nausea, rash, liver damage with overdose",
        "contraindications": "Liver disease, alcohol use",
        "interactions": "Warfarin, alcohol",
        "price": 5.00,
        "requires_prescription": False
    },
    "Ibuprofen": {
        "id": 2,
        "name": "Ibuprofen",
        "generic_name": "Ibuprofen",
        "category": "NSAID",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "400mg",
        "description": "Anti-inflammatory pain reliever.",
        "side_effects": "Stomach upset, bleeding risk",
        "contraindications": "Stomach ulcers, kidney disease",
        "interactions": "Aspirin, blood thinners",
        "price": 8.00,
        "requires_prescription": False
    },
    "Aspirin": {
        "id": 3,
        "name": "Aspirin",
        "generic_name": "Acetylsalicylic Acid",
        "category": "NSAID",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "325mg",
        "description": "Used for pain, fever, and blood thinning.",
        "side_effects": "Stomach irritation, bleeding risk",
        "contraindications": "Bleeding disorders, stomach ulcers",
        "interactions": "Blood thinners, alcohol",
        "price": 4.00,
        "requires_prescription": False
    },
    "Diclofenac": {
        "id": 4,
        "name": "Diclofenac",
        "generic_name": "Diclofenac Sodium",
        "category": "NSAID",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "50mg",
        "description": "Used for pain and inflammation.",
        "side_effects": "Stomach upset, liver damage",
        "contraindications": "Stomach ulcers, kidney disease",
        "interactions": "Blood thinners, lithium",
        "price": 6.00,
        "requires_prescription": False
    },
    "Naproxen": {
        "id": 5,
        "name": "Naproxen",
        "generic_name": "Naproxen",
        "category": "NSAID",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "250mg",
        "description": "Used for pain and inflammation.",
        "side_effects": "Stomach upset, bleeding risk",
        "contraindications": "Stomach ulcers, kidney disease",
        "interactions": "Blood thinners, lithium",
        "price": 7.00,
        "requires_prescription": False
    },
    
    # Allergy & Cold
    "Cetirizine": {
        "id": 6,
        "name": "Cetirizine",
        "generic_name": "Cetirizine HCl",
        "category": "Antihistamine",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "10mg",
        "description": "Used for allergy relief.",
        "side_effects": "Drowsiness, dry mouth",
        "contraindications": "Kidney disease",
        "interactions": "Sedatives, alcohol",
        "price": 6.00,
        "requires_prescription": False
    },
    "Loratadine": {
        "id": 7,
        "name": "Loratadine",
        "generic_name": "Loratadine",
        "category": "Antihistamine",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "10mg",
        "description": "Non-drowsy allergy relief.",
        "side_effects": "Headache, dry mouth",
        "contraindications": "Kidney disease",
        "interactions": "Sedatives, alcohol",
        "price": 7.00,
        "requires_prescription": False
    },
    
    # Antibiotics
    "Amoxicillin": {
        "id": 8,
        "name": "Amoxicillin",
        "generic_name": "Amoxicillin",
        "category": "Antibiotic",
        "manufacturer": "Various",
        "dosage_form": "Capsule",
        "strength": "500mg",
        "description": "Antibiotic for bacterial infections.",
        "side_effects": "Diarrhea, rash, yeast infection",
        "contraindications": "Penicillin allergy",
        "interactions": "Probenecid, methotrexate",
        "price": 12.00,
        "requires_prescription": True
    },
    "Azithromycin": {
        "id": 9,
        "name": "Azithromycin",
        "generic_name": "Azithromycin",
        "category": "Antibiotic",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "250mg",
        "description": "Antibiotic for respiratory infections.",
        "side_effects": "Diarrhea, nausea, abdominal pain",
        "contraindications": "Liver disease",
        "interactions": "Antacids, warfarin",
        "price": 15.00,
        "requires_prescription": True
    },
    "Ciprofloxacin": {
        "id": 10,
        "name": "Ciprofloxacin",
        "generic_name": "Ciprofloxacin",
        "category": "Antibiotic",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "description": "Antibiotic for bacterial infections.",
        "side_effects": "Nausea, diarrhea, tendon rupture",
        "contraindications": "Tendon disease, pregnancy",
        "interactions": "Antacids, warfarin",
        "price": 18.00,
        "requires_prescription": True
    },
    
    # Stomach & Digestive
    "Omeprazole": {
        "id": 11,
        "name": "Omeprazole",
        "generic_name": "Omeprazole",
        "category": "Antacid",
        "manufacturer": "Various",
        "dosage_form": "Capsule",
        "strength": "20mg",
        "description": "Reduces stomach acid production.",
        "side_effects": "Headache, diarrhea, vitamin B12 deficiency",
        "contraindications": "Liver disease",
        "interactions": "Clopidogrel, warfarin",
        "price": 10.00,
        "requires_prescription": False
    },
    "Pantoprazole": {
        "id": 12,
        "name": "Pantoprazole",
        "generic_name": "Pantoprazole",
        "category": "Antacid",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "40mg",
        "description": "Reduces stomach acid production.",
        "side_effects": "Headache, diarrhea, vitamin B12 deficiency",
        "contraindications": "Liver disease",
        "interactions": "Warfarin, methotrexate",
        "price": 12.00,
        "requires_prescription": False
    },
    
    # Diabetes
    "Metformin": {
        "id": 13,
        "name": "Metformin",
        "generic_name": "Metformin HCl",
        "category": "Antidiabetic",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "description": "Used for type 2 diabetes management.",
        "side_effects": "Diarrhea, nausea, metallic taste",
        "contraindications": "Kidney disease, liver disease",
        "interactions": "Iodinated contrast, alcohol",
        "price": 8.00,
        "requires_prescription": True
    },
    "Glimepiride": {
        "id": 14,
        "name": "Glimepiride",
        "generic_name": "Glimepiride",
        "category": "Antidiabetic",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "2mg",
        "description": "Used for type 2 diabetes management.",
        "side_effects": "Hypoglycemia, weight gain",
        "contraindications": "Kidney disease, liver disease",
        "interactions": "Insulin, alcohol",
        "price": 10.00,
        "requires_prescription": True
    },
    
    # Cholesterol
    "Atorvastatin": {
        "id": 15,
        "name": "Atorvastatin",
        "generic_name": "Atorvastatin Calcium",
        "category": "Statin",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "20mg",
        "description": "Lowers cholesterol levels.",
        "side_effects": "Muscle pain, liver enzyme elevation",
        "contraindications": "Liver disease, pregnancy",
        "interactions": "Grapefruit, cyclosporine",
        "price": 25.00,
        "requires_prescription": True
    },
    "Rosuvastatin": {
        "id": 16,
        "name": "Rosuvastatin",
        "generic_name": "Rosuvastatin",
        "category": "Statin",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "10mg",
        "description": "Lowers cholesterol levels.",
        "side_effects": "Muscle pain, liver enzyme elevation",
        "contraindications": "Liver disease, pregnancy",
        "interactions": "Grapefruit, cyclosporine",
        "price": 28.00,
        "requires_prescription": True
    },
    
    # Heart & Blood Pressure
    "Amlodipine": {
        "id": 17,
        "name": "Amlodipine",
        "generic_name": "Amlodipine Besylate",
        "category": "Calcium Channel Blocker",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "5mg",
        "description": "Used for high blood pressure and angina.",
        "side_effects": "Swelling, fatigue, dizziness",
        "contraindications": "Heart disease, liver disease",
        "interactions": "Grapefruit, cyclosporine",
        "price": 15.00,
        "requires_prescription": True
    },
    "Lisinopril": {
        "id": 18,
        "name": "Lisinopril",
        "generic_name": "Lisinopril",
        "category": "ACE Inhibitor",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "10mg",
        "description": "Used for high blood pressure and heart failure.",
        "side_effects": "Cough, dizziness, hyperkalemia",
        "contraindications": "Pregnancy, kidney disease",
        "interactions": "Potassium supplements, NSAIDs",
        "price": 15.00,
        "requires_prescription": True
    },
    "Losartan": {
        "id": 19,
        "name": "Losartan",
        "generic_name": "Losartan Potassium",
        "category": "ARB",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "50mg",
        "description": "Used for high blood pressure.",
        "side_effects": "Dizziness, cough, hyperkalemia",
        "contraindications": "Pregnancy, kidney disease",
        "interactions": "Potassium supplements, NSAIDs",
        "price": 18.00,
        "requires_prescription": True
    },
    "Metoprolol": {
        "id": 20,
        "name": "Metoprolol",
        "generic_name": "Metoprolol Tartrate",
        "category": "Beta Blocker",
        "manufacturer": "Various",
        "dosage_form": "Tablet",
        "strength": "50mg",
        "description": "Used for high blood pressure and angina.",
        "side_effects": "Fatigue, slow heart rate, dizziness",
        "contraindications": "Heart block, bradycardia",
        "interactions": "Insulin, calcium channel blockers",
        "price": 20.00,
        "requires_prescription": True
    }
}

@bp.route("/search", methods=["GET"])
@jwt_required()
def search_medicines():
    try:
        query = request.args.get("q", "").strip()
        logger.info(f"Searching for medicines with query: {query}")
        
        if not query:
            # Return all medicines if no query
            results = list(medicines_db.values())
            return jsonify({"medicines": results, "count": len(results)}), 200
        
        # Search in medicine names and generic names
        results = []
        query_lower = query.lower()
        
        for key, medicine in medicines_db.items():
            # Exact match or partial match
            if (query_lower in key.lower() or 
                query_lower in medicine.get("generic_name", "").lower() or
                query_lower in medicine.get("category", "").lower() or
                key.lower().startswith(query_lower) or
                medicine.get("generic_name", "").lower().startswith(query_lower)):
                results.append(medicine)
        
        # Sort results by relevance (exact matches first)
        results.sort(key=lambda x: (
            0 if x["name"].lower() == query_lower else 
            1 if x["name"].lower().startswith(query_lower) else 
            2 if query_lower in x["name"].lower() else 3
        ))
        
        logger.info(f"Found {len(results)} medicines matching query: {query}")
        return jsonify({"medicines": results, "count": len(results)}), 200
        
    except Exception as e:
        logger.error(f"Medicine search error: {str(e)}")
        return jsonify({"error": str(e), "medicines": []}), 500

@bp.route("/<int:medicine_id>", methods=["GET"])
@jwt_required()
def get_medicine_details(medicine_id):
    try:
        for key, medicine in medicines_db.items():
            if medicine.get("id") == medicine_id:
                return jsonify({"medicine": medicine}), 200
        return jsonify({"error": "Medicine not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/interactions", methods=["POST"])
@jwt_required()
def check_interactions():
    try:
        data = request.get_json()
        medicine_ids = data.get("medicines", [])
        
        if not medicine_ids or len(medicine_ids) < 2:
            return jsonify({
                "interactions": [],
                "message": "Select at least 2 medicines to check interactions",
                "disclaimer": "Consult a healthcare professional for complete interaction information."
            }), 200
        
        # Get medicine names from IDs
        medicine_names = []
        for med_id in medicine_ids:
            for key, med in medicines_db.items():
                if med.get("id") == med_id:
                    medicine_names.append(med["name"])
                    break
        
        # Real drug interactions
        interaction_db = {
            ("Aspirin", "Ibuprofen"): {"severity": "high", "description": "Increased risk of gastrointestinal bleeding"},
            ("Aspirin", "Naproxen"): {"severity": "high", "description": "Increased risk of gastrointestinal bleeding"},
            ("Aspirin", "Diclofenac"): {"severity": "high", "description": "Increased risk of gastrointestinal bleeding"},
            ("Aspirin", "Warfarin"): {"severity": "high", "description": "Increased risk of bleeding"},
            ("Amoxicillin", "Metformin"): {"severity": "moderate", "description": "May affect blood sugar levels"},
            ("Amoxicillin", "Ciprofloxacin"): {"severity": "moderate", "description": "Decreased antibiotic effectiveness"},
            ("Lisinopril", "Metformin"): {"severity": "moderate", "description": "May affect kidney function"},
            ("Lisinopril", "Losartan"): {"severity": "moderate", "description": "Increased risk of kidney problems"},
            ("Atorvastatin", "Amlodipine"): {"severity": "moderate", "description": "May increase side effects"},
            ("Atorvastatin", "Rosuvastatin"): {"severity": "moderate", "description": "Increased risk of muscle damage"},
            ("Metoprolol", "Amlodipine"): {"severity": "moderate", "description": "May cause excessive heart rate slowing"},
            ("Metformin", "Glimepiride"): {"severity": "moderate", "description": "Increased risk of hypoglycemia"},
            ("Paracetamol", "Ibuprofen"): {"severity": "low", "description": "Generally safe to use together"},
            ("Paracetamol", "Aspirin"): {"severity": "low", "description": "Generally safe to use together"},
            ("Paracetamol", "Diclofenac"): {"severity": "low", "description": "Generally safe to use together"},
            ("Cetirizine", "Loratadine"): {"severity": "low", "description": "No significant interaction"},
            ("Omeprazole", "Pantoprazole"): {"severity": "low", "description": "No significant interaction"}
        }
        
        interactions = []
        for i, med1 in enumerate(medicine_names):
            for j, med2 in enumerate(medicine_names):
                if i < j:
                    # Check both orders
                    for (key1, key2), interaction in interaction_db.items():
                        if (med1 == key1 and med2 == key2) or (med1 == key2 and med2 == key1):
                            interactions.append({
                                "medicine1": med1,
                                "medicine2": med2,
                                "severity": interaction["severity"],
                                "description": interaction["description"]
                            })
                            break
        
        return jsonify({
            "interactions": interactions,
            "message": f"Found {len(interactions)} interactions",
            "disclaimer": "This is a preliminary check. Always consult a healthcare professional."
        }), 200
        
    except Exception as e:
        logger.error(f"Interaction check error: {str(e)}")
        return jsonify({"error": str(e)}), 500
