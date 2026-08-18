import logging
from services.dataset_loader import DatasetLoader

logger = logging.getLogger(__name__)

class MedicineAgent:
    def __init__(self):
        self.dataset = DatasetLoader()
        
    def search_medicines(self, query):
        return {"medicines": [{"id": 1, "name": "Sample Medicine"}]}
    
    def get_medicine_details(self, medicine_id):
        return {"id": medicine_id, "name": "Sample Medicine"}
    
    def check_interactions(self, medicines):
        return {"interactions": [], "disclaimer": "Consult a healthcare professional"}
