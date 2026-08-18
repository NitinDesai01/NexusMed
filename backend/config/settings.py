import os

class Settings:
    # Agent configurations
    AGENT_CONFIGS = {
        'symptom_agent': {
            'enabled': True,
            'confidence_threshold': 0.7
        },
        'disease_prediction_agent': {
            'enabled': True,
            'model_path': 'models/disease_predictor.pkl'
        },
        'medicine_agent': {
            'enabled': True,
            'drug_interaction_check': True
        },
        'ambulance_agent': {
            'enabled': True,
            'response_time': 300  # 5 minutes
        },
        'hospital_agent': {
            'enabled': True,
            'max_bed_search_radius': 50  # km
        },
        'community_agent': {
            'enabled': True,
            'alert_radius': 10  # km
        },
        'report_agent': {
            'enabled': True,
            'ocr_confidence': 0.8
        },
        'knowledge_agent': {
            'enabled': True,
            'top_k_results': 5
        }
    }
    
    # Dataset paths (from your specified location)
    DATASET_PATHS = {
        'symptoms': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'symptoms.csv'),
        'diseases': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'diseases.csv'),
        'medicines': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'medicines.csv'),
        'hospitals': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'hospitals.csv'),
        'ambulances': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'ambulances.csv'),
        'doctors': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'doctors.csv'),
        'appointments': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'appointments.csv'),
        'health_awareness': os.path.join(os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets'), 'health_awareness.csv')
    }