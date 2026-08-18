import re
from services.dataset_loader import DatasetLoader
import logging

logger = logging.getLogger(__name__)

class SymptomTools:
    def __init__(self):
        self.dataset = DatasetLoader()
        self.symptom_patterns = self._load_symptom_patterns()
        
    def _load_symptom_patterns(self):
        """Load common symptom patterns for matching"""
        return {
            'fever': ['fever', 'high temperature', 'pyrexia', 'febrile'],
            'headache': ['headache', 'cephalalgia', 'head pain', 'migraine'],
            'cough': ['cough', 'coughing', 'tussis', 'hacking cough'],
            'fatigue': ['fatigue', 'tiredness', 'exhaustion', 'lethargy', 'weakness'],
            'nausea': ['nausea', 'queasy', 'sick stomach', 'upset stomach'],
            'pain': ['pain', 'ache', 'discomfort', 'soreness', 'tenderness'],
            'shortness_of_breath': ['shortness of breath', 'difficulty breathing', 'dyspnea', 'wheezing'],
            'chest_pain': ['chest pain', 'chest tightness', 'angina'],
            'dizziness': ['dizziness', 'vertigo', 'lightheaded', 'unsteady'],
            'rash': ['rash', 'skin rash', 'hives', 'eczema', 'dermatitis']
        }
        
    def extract_symptoms(self, text):
        """Extract symptoms from text"""
        text = text.lower()
        found_symptoms = []
        
        for symptom, patterns in self.symptom_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    found_symptoms.append(symptom)
                    break
                    
        return list(set(found_symptoms))
    
    def severity_score(self, symptoms):
        """Calculate severity score based on symptoms"""
        severe_symptoms = ['chest_pain', 'shortness_of_breath', 'severe_bleeding', 
                          'loss_of_consciousness', 'stroke_symptoms']
        
        score = 0
        for symptom in symptoms:
            if symptom in severe_symptoms:
                score += 3
            elif symptom in ['fever', 'headache', 'dizziness']:
                score += 2
            else:
                score += 1
                
        return min(score, 10)  # Cap at 10
    
    def categorize_symptoms(self, symptoms):
        """Categorize symptoms by body system"""
        categories = {
            'respiratory': ['cough', 'shortness_of_breath', 'wheezing', 'sore throat'],
            'cardiovascular': ['chest_pain', 'palpitations', 'high blood pressure'],
            'neurological': ['headache', 'dizziness', 'confusion', 'seizures'],
            'digestive': ['nausea', 'vomiting', 'diarrhea', 'abdominal pain'],
            'musculoskeletal': ['muscle pain', 'joint pain', 'back pain'],
            'dermatological': ['rash', 'itching', 'skin lesions'],
            'general': ['fever', 'fatigue', 'weight loss', 'sweating']
        }
        
        categorized = {}
        for category, symptoms_list in categories.items():
            matched = [s for s in symptoms if s in symptoms_list]
            if matched:
                categorized[category] = matched
                
        return categorized
    
    def get_recommendations(self, symptoms, severity):
        """Get recommendations based on symptoms and severity"""
        recommendations = []
        emergency_warnings = []
        
        if severity >= 7:
            emergency_warnings.append("Seek immediate emergency medical attention")
            recommendations.append("Call emergency services immediately")
        elif severity >= 4:
            recommendations.append("Consult a healthcare professional within 24 hours")
            recommendations.append("Monitor symptoms closely")
        else:
            recommendations.append("Rest and monitor symptoms")
            recommendations.append("Consider home remedies for symptom relief")
            
        # Specific recommendations
        if 'fever' in symptoms:
            recommendations.append("Stay hydrated and rest")
            if severity > 5:
                recommendations.append("Consider over-the-counter fever reducers")
                
        if 'cough' in symptoms:
            recommendations.append("Use honey or lozenges for cough relief")
            
        if 'headache' in symptoms:
            recommendations.append("Rest in a quiet, dark room")
            recommendations.append("Apply cold compress")
            
        return {
            'recommendations': recommendations,
            'emergency_warnings': emergency_warnings
        }