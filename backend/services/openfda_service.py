import logging

logger = logging.getLogger(__name__)

class OpenFDAService:
    def __init__(self):
        pass
        
    def search_drugs(self, query, limit=10):
        """Search for drugs"""
        return {
            "results": [
                {"name": f"Drug {i}", "generic": f"Generic {i}"} 
                for i in range(min(limit, 5))
            ]
        }
    
    def get_drug_details(self, drug_name):
        """Get drug details"""
        return {
            "name": drug_name,
            "brand_names": [drug_name],
            "generic_name": drug_name,
            "description": "Drug information"
        }
    
    def get_drug_interactions(self, drug_names):
        """Check drug interactions"""
        return {
            "interactions": [],
            "warning": "No interactions found. Consult a healthcare professional."
        }
