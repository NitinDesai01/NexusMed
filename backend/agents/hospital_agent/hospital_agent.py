import logging

logger = logging.getLogger(__name__)

class HospitalAgent:
    def __init__(self):
        pass
        
    def search_hospitals(self, lat, lng, radius=10, specialty=""):
        return [{"id": 1, "name": "City Hospital", "available_beds": 50}]
    
    def get_hospital_details(self, hospital_id):
        return {"id": hospital_id, "name": "City Hospital", "available_beds": 50}
    
    def get_available_beds(self, lat, lng, radius=10):
        return [{"hospital_name": "City Hospital", "available_beds": 50}]
