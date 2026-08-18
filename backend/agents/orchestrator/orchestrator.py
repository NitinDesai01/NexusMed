from agents.symptom_agent.symptom_agent import SymptomAgent
from agents.disease_prediction_agent.disease_agent import DiseasePredictionAgent
from agents.medicine_agent.medicine_agent import MedicineAgent
from agents.ambulance_agent.ambulance_agent import AmbulanceAgent
from agents.hospital_agent.hospital_agent import HospitalAgent
from agents.community_agent.community_agent import CommunityAgent
from agents.report_agent.report_agent import ReportAgent
from agents.knowledge_agent.knowledge_agent import KnowledgeAgent
from agents.orchestrator.workflow import Workflow
import logging

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.symptom_agent = SymptomAgent()
        self.disease_agent = DiseasePredictionAgent()
        self.medicine_agent = MedicineAgent()
        self.ambulance_agent = AmbulanceAgent()
        self.hospital_agent = HospitalAgent()
        self.community_agent = CommunityAgent()
        self.report_agent = ReportAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.workflow = Workflow()
        
    def process_health_query(self, query_type, data):
        """Process health queries using appropriate agents"""
        try:
            if query_type == 'symptom_analysis':
                return self._handle_symptom_analysis(data)
            elif query_type == 'emergency':
                return self._handle_emergency(data)
            elif query_type == 'medicine':
                return self._handle_medicine_query(data)
            elif query_type == 'hospital':
                return self._handle_hospital_query(data)
            elif query_type == 'report':
                return self._handle_report_query(data)
            elif query_type == 'knowledge':
                return self._handle_knowledge_query(data)
            else:
                return {'error': 'Unknown query type'}
        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            return {'error': str(e)}
    
    def _handle_symptom_analysis(self, data):
        """Handle symptom analysis workflow"""
        symptoms = data.get('symptoms', '')
        analysis = self.symptom_agent.analyze_symptoms(symptoms)
        predictions = self.disease_agent.predict(symptoms)
        emergency = self.symptom_agent.check_emergency(symptoms)
        
        return {
            'analysis': analysis,
            'predictions': predictions,
            'emergency_check': emergency
        }
    
    def _handle_emergency(self, data):
        """Handle emergency workflow"""
        lat = data.get('lat')
        lng = data.get('lng')
        
        if not lat or not lng:
            return {'error': 'Location required'}
        
        ambulances = self.ambulance_agent.find_nearby_ambulances(lat, lng)
        hospitals = self.hospital_agent.get_nearest_emergency_hospitals(lat, lng)
        beds = self.hospital_agent.get_available_beds(lat, lng)
        
        return {
            'ambulances': ambulances,
            'hospitals': hospitals,
            'available_beds': beds
        }
    
    def _handle_medicine_query(self, data):
        """Handle medicine query workflow"""
        query = data.get('query', '')
        return self.medicine_agent.search_medicines(query)
    
    def _handle_hospital_query(self, data):
        """Handle hospital query workflow"""
        lat = data.get('lat')
        lng = data.get('lng')
        specialty = data.get('specialty', '')
        
        return self.hospital_agent.search_hospitals(lat, lng, specialty=specialty)
    
    def _handle_report_query(self, data):
        """Handle report query workflow"""
        file = data.get('file')
        user_id = data.get('user_id')
        
        if not file:
            return {'error': 'No file provided'}
        
        return self.report_agent.process_report(file, user_id)
    
    def _handle_knowledge_query(self, data):
        """Handle knowledge query workflow"""
        question = data.get('question', '')
        return self.knowledge_agent.query(question)