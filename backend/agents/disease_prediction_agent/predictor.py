import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from services.dataset_loader import DatasetLoader
from agents.disease_prediction_agent.model import DiseaseModel
import logging

logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self):
        self.model = DiseaseModel()
        self.dataset = DatasetLoader()
        self.confidence_threshold = 0.4
        
    def train_from_dataset(self):
        """Train model using dataset"""
        try:
            # Load disease dataset
            diseases = self.dataset.load_diseases_dataset()
            
            if not diseases:
                logger.warning("No disease dataset found")
                return False
            
            # Prepare data
            symptoms_list = []
            disease_labels = []
            
            for disease in diseases:
                symptoms = disease.get('symptoms', '')
                disease_name = disease.get('disease', '')
                
                if symptoms and disease_name:
                    symptoms_list.append(symptoms)
                    disease_labels.append(disease_name)
            
            if not symptoms_list:
                logger.warning("No training data available")
                return False
            
            # Train model
            return self.model.train(symptoms_list, disease_labels)
            
        except Exception as e:
            logger.error(f"Training from dataset error: {e}")
            return False
    
    def predict_with_confidence(self, symptoms):
        """Make prediction with confidence assessment"""
        try:
            predictions = self.model.predict(symptoms)
            
            if not predictions:
                return {
                    'predictions': [],
                    'confidence': 'low',
                    'message': 'Unable to make prediction'
                }
            
            # Filter low confidence predictions
            filtered = [p for p in predictions if p['confidence'] >= self.confidence_threshold]
            
            if not filtered:
                return {
                    'predictions': predictions[:3],
                    'confidence': 'low',
                    'message': 'Low confidence predictions. Please consult a doctor.'
                }
            
            return {
                'predictions': filtered,
                'confidence': 'high' if filtered[0]['confidence'] > 0.7 else 'medium',
                'message': 'Prediction complete'
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {'error': str(e)}
    
    def evaluate_model(self, test_size=0.2):
        """Evaluate model performance"""
        try:
            # Load dataset
            diseases = self.dataset.load_diseases_dataset()
            
            if not diseases:
                return {'error': 'No dataset available'}
            
            # Prepare data
            symptoms_list = []
            disease_labels = []
            
            for disease in diseases:
                symptoms = disease.get('symptoms', '')
                disease_name = disease.get('disease', '')
                
                if symptoms and disease_name:
                    symptoms_list.append(symptoms)
                    disease_labels.append(disease_name)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                symptoms_list, 
                disease_labels, 
                test_size=test_size,
                random_state=42
            )
            
            # Train model
            self.model.train(X_train, y_train)
            
            # Make predictions
            predictions = []
            for symptoms in X_test:
                pred = self.model.predict(symptoms)
                if pred:
                    predictions.append(pred[0]['disease'])
                else:
                    predictions.append('Unknown')
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, predictions)
            
            return {
                'accuracy': accuracy,
                'test_size': test_size,
                'samples': len(X_test),
                'classification_report': classification_report(y_test, predictions, output_dict=True)
            }
            
        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            return {'error': str(e)}