import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

class DiseaseModel:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
    def train(self, X, y):
        """Train the disease prediction model"""
        try:
            # Vectorize symptoms
            self.vectorizer = TfidfVectorizer(max_features=1000)
            X_vectorized = self.vectorizer.fit_transform(X)
            
            # Encode labels
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_vectorized, y_encoded)
            
            self.is_trained = True
            logger.info("Disease model trained successfully")
            return True
            
        except Exception as e:
            logger.error(f"Model training error: {e}")
            return False
    
    def predict(self, symptoms_text):
        """Predict disease from symptoms"""
        if not self.is_trained or not self.model:
            return None
            
        try:
            # Vectorize input
            X_vectorized = self.vectorizer.transform([symptoms_text])
            
            # Predict probabilities
            probabilities = self.model.predict_proba(X_vectorized)[0]
            predicted_class = self.model.predict(X_vectorized)[0]
            
            # Get class labels
            classes = self.label_encoder.classes_
            
            # Get top predictions
            top_indices = np.argsort(probabilities)[::-1][:5]
            predictions = []
            
            for idx in top_indices:
                predictions.append({
                    'disease': classes[idx],
                    'confidence': float(probabilities[idx])
                })
            
            return predictions
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return None
    
    def save_model(self, path):
        """Save model to disk"""
        try:
            with open(path, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'vectorizer': self.vectorizer,
                    'label_encoder': self.label_encoder
                }, f)
            logger.info(f"Model saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Save model error: {e}")
            return False
    
    def load_model(self, path):
        """Load model from disk"""
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.vectorizer = data['vectorizer']
                self.label_encoder = data['label_encoder']
                self.is_trained = True
            logger.info(f"Model loaded from {path}")
            return True
        except Exception as e:
            logger.error(f"Load model error: {e}")
            return False