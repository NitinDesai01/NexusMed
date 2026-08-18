import logging
from services.dataset_loader import DatasetLoader

logger = logging.getLogger(__name__)

class DiseasePredictionAgent:
    def __init__(self):
        self.dataset = DatasetLoader()
        
    def predict(self, symptoms):
        """Predict diseases based on symptoms"""
        try:
            # Simple rule-based prediction
            predictions = []
            symptoms_lower = symptoms.lower()
            
            # Common disease patterns
            disease_patterns = {
                "Common Cold": ["cough", "sore throat", "runny nose", "fever"],
                "Influenza": ["fever", "headache", "muscle pain", "fatigue", "cough"],
                "COVID-19": ["fever", "cough", "shortness of breath", "fatigue", "loss of taste"],
                "Allergy": ["sneezing", "itchy eyes", "runny nose", "rash"],
                "Sinusitis": ["headache", "facial pain", "nasal congestion", "fever"],
                "Migraine": ["headache", "nausea", "sensitivity to light", "dizziness"],
                "Food Poisoning": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever"],
                "Gastroenteritis": ["diarrhea", "vomiting", "abdominal pain", "fever"],
                "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain", "fatigue"],
                "Bronchitis": ["cough", "mucus", "fatigue", "shortness of breath", "fever"]
            }
            
            for disease, required_symptoms in disease_patterns.items():
                match_count = sum(1 for s in required_symptoms if s in symptoms_lower)
                confidence = match_count / len(required_symptoms) if required_symptoms else 0
                
                if confidence > 0.3:
                    predictions.append({
                        "disease": disease,
                        "confidence": round(confidence, 2)
                    })
            
            # Sort by confidence
            predictions.sort(key=lambda x: x["confidence"], reverse=True)
            
            return {
                "predictions": predictions[:5],
                "model_used": "rule-based"
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {
                "predictions": [],
                "model_used": "rule-based",
                "error": str(e)
            }
