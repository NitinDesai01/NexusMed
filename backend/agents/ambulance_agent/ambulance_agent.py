import logging

logger = logging.getLogger(__name__)

class AmbulanceAgent:
    def __init__(self):
        pass
        
    def find_nearby_ambulances(self, lat, lng, radius=10):
        return [{"id": 1, "status": "available", "distance": 2.5}]
    
    def track_ambulances(self, lat, lng, radius=10):
        return [{"id": 1, "status": "available", "distance": 2.5}]
    
    def request_ambulance(self, lat, lng, patient_name, patient_phone, description=""):
        return {"request_id": "REQ-123", "status": "assigned"}
