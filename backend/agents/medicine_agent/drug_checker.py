import re
from services.openfda_service import OpenFDAService
import logging

logger = logging.getLogger(__name__)

class DrugChecker:
    def __init__(self):
        self.openfda = OpenFDAService()
        self.drug_interactions = self._load_interactions()
        
    def _load_interactions(self):
        """Load known drug interactions"""
        return {
            ('warfarin', 'aspirin'): {
                'severity': 'high',
                'description': 'Increased risk of bleeding when combining warfarin and aspirin'
            },
            ('digoxin', 'quinidine'): {
                'severity': 'high',
                'description': 'Increased digoxin levels leading to toxicity'
            },
            ('theophylline', 'ciprofloxacin'): {
                'severity': 'moderate',
                'description': 'Decreased theophylline clearance'
            },
            ('lisinopril', 'potassium'): {
                'severity': 'moderate',
                'description': 'Increased risk of hyperkalemia'
            },
            ('metformin', 'iodinated_contrast'): {
                'severity': 'high',
                'description': 'Risk of lactic acidosis'
            }
        }
    
    def check_interaction(self, drug1, drug2):
        """Check interaction between two drugs"""
        try:
            # Normalize drug names
            d1 = self._normalize_drug_name(drug1)
            d2 = self._normalize_drug_name(drug2)
            
            # Check known interactions
            interaction_key = tuple(sorted([d1, d2]))
            if interaction_key in self.drug_interactions:
                return self.drug_interactions[interaction_key]
            
            # Check OpenFDA
            fda_interaction = self.openfda.get_drug_interactions([drug1, drug2])
            if fda_interaction:
                return fda_interaction
            
            return {
                'severity': 'unknown',
                'description': 'No known interaction found. Consult a healthcare professional.'
            }
            
        except Exception as e:
            logger.error(f"Interaction check error: {e}")
            return {
                'severity': 'unknown',
                'description': 'Interaction check failed. Consult a healthcare professional.'
            }
    
    def check_all_interactions(self, drugs):
        """Check interactions among multiple drugs"""
        interactions = []
        
        for i in range(len(drugs)):
            for j in range(i + 1, len(drugs)):
                interaction = self.check_interaction(drugs[i], drugs[j])
                interactions.append({
                    'drug1': drugs[i],
                    'drug2': drugs[j],
                    'interaction': interaction
                })
        
        return interactions
    
    def _normalize_drug_name(self, name):
        """Normalize drug name for matching"""
        # Remove brand names and keep generic
        name = re.sub(r'\(.*?\)', '', name)
        name = name.strip().lower()
        return name
    
    def get_alternative(self, drug, condition):
        """Get alternative drug based on condition"""
        alternatives = {
            'warfarin': ['apixaban', 'rivaroxaban', 'dabigatran'],
            'aspirin': ['clopidogrel', 'ticagrelor'],
            'digoxin': ['metoprolol', 'carvedilol'],
            'lisinopril': ['losartan', 'valsartan', 'amlodipine'],
            'metformin': ['sitagliptin', 'liraglutide', 'empagliflozin']
        }
        
        drug_norm = self._normalize_drug_name(drug)
        return alternatives.get(drug_norm, [])