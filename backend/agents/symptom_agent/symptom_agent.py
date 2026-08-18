from services.llm_service import LLMService
from services.dataset_loader import DatasetLoader
import logging
import json

logger = logging.getLogger(__name__)

class SymptomAgent:
    def __init__(self):
        self.llm = LLMService()
        self.dataset = DatasetLoader()
        
    def analyze_symptoms(self, symptoms):
        """Analyze symptoms and provide insights"""
        try:
            # Get disease mapping for context
            disease_mapping = self.dataset.get_symptom_disease_mapping()
            
            # Simple analysis based on symptoms
            symptoms_lower = symptoms.lower()
            
            # Check for common conditions
            conditions = []
            if "fever" in symptoms_lower or "temperature" in symptoms_lower:
                conditions.append("Possible infection or inflammation")
            if "cough" in symptoms_lower:
                conditions.append("Possible respiratory infection")
            if "headache" in symptoms_lower:
                conditions.append("Possible tension headache or migraine")
            if "pain" in symptoms_lower:
                conditions.append("Possible inflammation or injury")
            if "nausea" in symptoms_lower or "vomiting" in symptoms_lower:
                conditions.append("Possible gastrointestinal issue")
            if "fatigue" in symptoms_lower:
                conditions.append("Possible viral infection or stress")
            
            # Determine severity
            severity = "low"
            emergency_signs = ["chest pain", "difficulty breathing", "severe bleeding", 
                              "loss of consciousness", "stroke", "severe allergy"]
            for sign in emergency_signs:
                if sign in symptoms_lower:
                    severity = "high"
                    break
            if "fever" in symptoms_lower and "cough" in symptoms_lower:
                severity = "medium"
            
            # Generate recommendations
            recommendations = []
            if severity == "high":
                recommendations.append("Seek immediate emergency medical attention")
                recommendations.append("Call emergency services (112)")
            elif severity == "medium":
                recommendations.append("Consult a healthcare professional within 24 hours")
                recommendations.append("Rest and monitor symptoms")
            else:
                recommendations.append("Rest and stay hydrated")
                recommendations.append("Monitor symptoms for any changes")
                recommendations.append("Consult a doctor if symptoms persist")
            
            # Build response
            analysis = {
                "symptoms_analyzed": symptoms,
                "possible_conditions": conditions if conditions else ["No specific conditions identified"],
                "severity": severity,
                "recommendations": recommendations,
                "emergency_signs": severity == "high",
                "disclaimer": "This is an AI-based analysis. Always consult a healthcare professional."
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Symptom analysis error: {e}")
            return {
                "error": str(e),
                "symptoms_analyzed": symptoms,
                "possible_conditions": ["Unable to analyze symptoms"],
                "severity": "unknown",
                "recommendations": ["Please consult a healthcare professional"],
                "emergency_signs": False,
                "disclaimer": "This is an AI-based analysis. Always consult a healthcare professional."
            }
    
    def get_common_symptoms(self):
        """Get list of common symptoms"""
        return [
            "Fever", "Headache", "Cough", "Sore throat", "Fatigue",
            "Nausea", "Vomiting", "Diarrhea", "Muscle pain", "Joint pain",
            "Shortness of breath", "Chest pain", "Dizziness", "Rash",
            "Abdominal pain", "Back pain", "Neck pain", "Sweating",
            "Chills", "Loss of appetite", "Weight loss", "Insomnia"
        ]
    
    def check_emergency(self, symptoms):
        """Check if symptoms indicate an emergency"""
        emergency_symptoms = [
            "chest pain", "difficulty breathing", "severe bleeding",
            "loss of consciousness", "stroke symptoms", "severe allergy",
            "severe head injury", "suicidal thoughts", "severe pain"
        ]
        
        is_emergency = False
        severity = "low"
        recommendation = "Monitor symptoms and consult a doctor if they persist"
        emergency_services = []
        
        symptoms_lower = symptoms.lower()
        for symptom in emergency_symptoms:
            if symptom in symptoms_lower:
                is_emergency = True
                severity = "high"
                recommendation = "Seek immediate emergency medical attention"
                emergency_services = ["call_ambulance", "go_to_emergency"]
                break
        
        return {
            "is_emergency": is_emergency,
            "severity": severity,
            "recommendation": recommendation,
            "emergency_services": emergency_services
        }
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()
