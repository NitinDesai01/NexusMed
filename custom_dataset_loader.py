"""
Custom Dataset Loader for NexusMed - Maps your Kaggle datasets to the required format
"""
import pandas as pd
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomDatasetLoader:
    def __init__(self, dataset_path='C:/Users/nitin/OneDrive/Documents/Desktop/datasets'):
        self.dataset_path = dataset_path
        self.data = {}
        self.load_all_datasets()
    
    def load_all_datasets(self):
        """Load and map all your Kaggle datasets"""
        try:
            # Load your actual files
            self._load_patients()
            self._load_doctors()
            self._load_hospitals()
            self._load_medical_qa()
            self._load_healthcare_rag()
            self._load_staff()
            self._load_services()
            
            # Create required datasets from your data
            self._create_symptoms_from_qa()
            self._create_diseases_from_qa()
            self._create_medicines_from_qa()
            
            logger.info("All datasets loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
    
    def _load_patients(self):
        """Load patients dataset"""
        filepath = os.path.join(self.dataset_path, 'patients.csv')
        if os.path.exists(filepath):
            self.data['patients'] = pd.read_csv(filepath)
            logger.info(f"Loaded patients: {len(self.data['patients'])} records")
        else:
            self.data['patients'] = pd.DataFrame()
    
    def _load_doctors(self):
        """Load doctors dataset"""
        filepath = os.path.join(self.dataset_path, 'bangalore_doctors_final.csv')
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Map columns to what NexusMed expects
            df = df.rename(columns={
                'name': 'doctor_name',
                'specialty': 'specialization',
                'degree': 'qualification',
                'experience_years': 'years_experience',
                'consultation_fee': 'consultation_fee',
                'rating': 'rating',
                'bangalore_location': 'location',
                'latitude': 'latitude',
                'longitude': 'longitude'
            })
            self.data['doctors'] = df
            logger.info(f"Loaded doctors: {len(self.data['doctors'])} records")
        else:
            self.data['doctors'] = pd.DataFrame()
    
    def _load_hospitals(self):
        """Load hospitals from services data"""
        filepath = os.path.join(self.dataset_path, 'services_weekly.csv')
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            # Create hospital-like data from services
            hospitals = []
            services = df['service'].unique()
            for idx, service in enumerate(services):
                service_data = df[df['service'] == service]
                hospitals.append({
                    'id': idx + 1,
                    'name': f"{service.title()} Hospital",
                    'service_type': service,
                    'available_beds': service_data['available_beds'].mean() if 'available_beds' in service_data.columns else 0,
                    'patients_admitted': service_data['patients_admitted'].sum() if 'patients_admitted' in service_data.columns else 0,
                    'avg_satisfaction': service_data['patient_satisfaction'].mean() if 'patient_satisfaction' in service_data.columns else 0,
                    'city': 'Bangalore',
                    'state': 'Karnataka'
                })
            self.data['hospitals'] = pd.DataFrame(hospitals)
            logger.info(f"Created hospitals from services: {len(self.data['hospitals'])} records")
        else:
            self.data['hospitals'] = pd.DataFrame()
    
    def _load_medical_qa(self):
        """Load medical Q&A dataset"""
        filepath = os.path.join(self.dataset_path, 'medical_question_answer_dataset_50000.csv')
        if os.path.exists(filepath):
            self.data['medical_qa'] = pd.read_csv(filepath)
            logger.info(f"Loaded medical QA: {len(self.data['medical_qa'])} records")
        else:
            self.data['medical_qa'] = pd.DataFrame()
    
    def _load_healthcare_rag(self):
        """Load healthcare RAG dataset"""
        filepath = os.path.join(self.dataset_path, 'healthcare_rag_dataset.csv')
        if os.path.exists(filepath):
            self.data['healthcare_rag'] = pd.read_csv(filepath)
            logger.info(f"Loaded healthcare RAG: {len(self.data['healthcare_rag'])} records")
        else:
            self.data['healthcare_rag'] = pd.DataFrame()
    
    def _load_staff(self):
        """Load staff dataset"""
        filepath = os.path.join(self.dataset_path, 'staff.csv')
        if os.path.exists(filepath):
            self.data['staff'] = pd.read_csv(filepath)
            logger.info(f"Loaded staff: {len(self.data['staff'])} records")
        else:
            self.data['staff'] = pd.DataFrame()
    
    def _load_services(self):
        """Load services dataset"""
        filepath = os.path.join(self.dataset_path, 'services_weekly.csv')
        if os.path.exists(filepath):
            self.data['services'] = pd.read_csv(filepath)
            logger.info(f"Loaded services: {len(self.data['services'])} records")
        else:
            self.data['services'] = pd.DataFrame()
    
    def _create_symptoms_from_qa(self):
        """Extract symptoms from medical QA dataset"""
        if 'medical_qa' in self.data and not self.data['medical_qa'].empty:
            qa_df = self.data['medical_qa']
            
            # Common symptom keywords to extract
            symptom_keywords = [
                'fever', 'cough', 'headache', 'pain', 'nausea', 'vomiting',
                'diarrhea', 'fatigue', 'dizziness', 'rash', 'sweating', 'chills',
                'shortness of breath', 'chest pain', 'abdominal pain', 'back pain',
                'joint pain', 'muscle pain', 'sore throat', 'runny nose',
                'loss of appetite', 'weight loss', 'insomnia', 'anxiety',
                'depression', 'stress', 'allergy', 'itching', 'swelling'
            ]
            
            symptoms_set = set()
            for _, row in qa_df.head(1000).iterrows():
                question = str(row.get('Symptoms/Question', '')).lower()
                for symptom in symptom_keywords:
                    if symptom in question:
                        symptoms_set.add(symptom)
            
            # Create symptoms dataframe
            symptoms_list = []
            for symptom in symptoms_set:
                # Determine category
                category = 'General'
                if symptom in ['fever', 'sweating', 'chills']:
                    category = 'General'
                elif symptom in ['cough', 'shortness of breath', 'sore throat', 'runny nose']:
                    category = 'Respiratory'
                elif symptom in ['headache', 'dizziness', 'insomnia', 'anxiety', 'depression']:
                    category = 'Neurological'
                elif symptom in ['nausea', 'vomiting', 'diarrhea', 'abdominal pain']:
                    category = 'Digestive'
                elif symptom in ['joint pain', 'muscle pain', 'back pain']:
                    category = 'Musculoskeletal'
                elif symptom in ['rash', 'itching', 'swelling']:
                    category = 'Dermatological'
                
                symptoms_list.append({
                    'symptom_name': symptom.title(),
                    'category': category,
                    'severity': 'medium'
                })
            
            self.data['symptoms'] = pd.DataFrame(symptoms_list)
            logger.info(f"Created symptoms: {len(self.data['symptoms'])} records")
        else:
            self.data['symptoms'] = pd.DataFrame()
    
    def _create_diseases_from_qa(self):
        """Extract diseases from medical QA dataset"""
        if 'medical_qa' in self.data and not self.data['medical_qa'].empty:
            qa_df = self.data['medical_qa']
            
            # Get unique diseases from the dataset
            diseases_dict = {}
            for _, row in qa_df.head(1000).iterrows():
                disease = str(row.get('Disease Prediction', '')).strip()
                symptoms = str(row.get('Symptoms/Question', '')).strip()
                medicines = str(row.get('Recommended Medicines', '')).strip()
                advice = str(row.get('Advice', '')).strip()
                
                if disease and disease not in diseases_dict:
                    diseases_dict[disease] = {
                        'disease': disease,
                        'symptoms': symptoms,
                        'treatments': medicines,
                        'advice': advice,
                        'severity': 'medium'
                    }
            
            self.data['diseases'] = pd.DataFrame(list(diseases_dict.values()))
            logger.info(f"Created diseases: {len(self.data['diseases'])} records")
        else:
            self.data['diseases'] = pd.DataFrame()
    
    def _create_medicines_from_qa(self):
        """Extract medicines from medical QA dataset"""
        if 'medical_qa' in self.data and not self.data['medical_qa'].empty:
            qa_df = self.data['medical_qa']
            
            medicines_set = set()
            for _, row in qa_df.head(1000).iterrows():
                medicines = str(row.get('Recommended Medicines', '')).strip()
                if medicines:
                    # Split by comma and clean
                    for med in medicines.split(','):
                        med_clean = med.strip()
                        if med_clean and len(med_clean) > 2:
                            medicines_set.add(med_clean)
            
            medicines_list = []
            for med in medicines_set:
                medicines_list.append({
                    'name': med,
                    'generic_name': med,
                    'category': 'General',
                    'manufacturer': 'Various',
                    'dosage_form': 'Tablet',
                    'strength': 'Standard',
                    'price': 0,
                    'requires_prescription': False
                })
            
            self.data['medicines'] = pd.DataFrame(medicines_list)
            logger.info(f"Created medicines: {len(self.data['medicines'])} records")
        else:
            self.data['medicines'] = pd.DataFrame()
    
    # Public getter methods
    def get_symptoms(self):
        return self.data.get('symptoms', pd.DataFrame())
    
    def get_diseases(self):
        return self.data.get('diseases', pd.DataFrame())
    
    def get_medicines(self):
        return self.data.get('medicines', pd.DataFrame())
    
    def get_hospitals(self):
        return self.data.get('hospitals', pd.DataFrame())
    
    def get_doctors(self):
        return self.data.get('doctors', pd.DataFrame())
    
    def get_patients(self):
        return self.data.get('patients', pd.DataFrame())
    
    def get_medical_qa(self):
        return self.data.get('medical_qa', pd.DataFrame())
    
    def get_healthcare_rag(self):
        return self.data.get('healthcare_rag', pd.DataFrame())
    
    def get_staff(self):
        return self.data.get('staff', pd.DataFrame())
    
    def get_services(self):
        return self.data.get('services', pd.DataFrame())
    
    def get_stats(self):
        """Get statistics about all loaded datasets"""
        stats = {}
        for key, df in self.data.items():
            stats[key] = {
                'records': len(df),
                'columns': list(df.columns) if not df.empty else []
            }
        return stats
    
    def get_symptom_disease_mapping(self):
        """Create symptom to disease mapping"""
        mapping = {}
        diseases_df = self.get_diseases()
        if not diseases_df.empty:
            for _, row in diseases_df.iterrows():
                disease = row.get('disease', '')
                symptoms = row.get('symptoms', '')
                if disease and symptoms:
                    for symptom in symptoms.split(','):
                        symptom = symptom.strip().lower()
                        if symptom:
                            if symptom not in mapping:
                                mapping[symptom] = []
                            mapping[symptom].append(disease)
        return mapping

# Test the loader
if __name__ == "__main__":
    print("=" * 50)
    print("Testing Custom Dataset Loader")
    print("=" * 50)
    
    loader = CustomDatasetLoader()
    
    print("\nDataset Statistics:")
    for name, stats in loader.get_stats().items():
        print(f"  {name}: {stats['records']} records")
    
    print("\nSample Data:")
    print("\nDoctors (first 2):")
    if not loader.get_doctors().empty:
        print(loader.get_doctors()[['doctor_name', 'specialization', 'rating']].head(2))
    
    print("\nPatients (first 2):")
    if not loader.get_patients().empty:
        print(loader.get_patients()[['patient_id', 'name', 'age']].head(2))
    
    print("\nSymptoms (first 5):")
    if not loader.get_symptoms().empty:
        print(loader.get_symptoms().head(5))
    
    print("\nDiseases (first 3):")
    if not loader.get_diseases().empty:
        print(loader.get_diseases().head(3))
    
    print("\n Custom dataset loader ready!")