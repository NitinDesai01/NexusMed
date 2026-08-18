"""
Dataset Loader for NexusMed
This module handles loading and processing of all dataset files from the specified path.
Expected dataset files:
- symptoms.csv: List of symptoms
- diseases.csv: Disease-symptom mapping
- medicines.csv: Medicine information
- hospitals.csv: Hospital details
- ambulances.csv: Ambulance details
- doctors.csv: Doctor information
- appointments.csv: Appointment records
- health_awareness.csv: Health awareness content
"""

import pandas as pd
import os
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetLoader:
    """
    Main dataset loader class for NexusMed.
    Loads all required datasets from the specified directory.
    """
    
    def __init__(self, dataset_path=None):
        """
        Initialize the dataset loader.
        
        Args:
            dataset_path: Path to the datasets folder. If None, uses default path.
        """
        if dataset_path is None:
            # Default path - can be overridden by environment variable or parameter
            self.dataset_path = os.environ.get('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets')
        else:
            self.dataset_path = dataset_path
        
        self._ensure_dataset_path()
        self.datasets = {}
        self._load_all_datasets()
    
    def _ensure_dataset_path(self):
        """Ensure the dataset path exists."""
        if not os.path.exists(self.dataset_path):
            logger.warning(f"Dataset path {self.dataset_path} does not exist. Creating directory...")
            os.makedirs(self.dataset_path, exist_ok=True)
            self._create_sample_datasets()
    
    def _create_sample_datasets(self):
        """Create sample dataset files if they don't exist."""
        logger.info("Creating sample dataset files...")
        
        # Sample symptoms data
        symptoms_df = pd.DataFrame({
            'symptom_id': range(1, 23),
            'symptom_name': [
                'Fever', 'Headache', 'Cough', 'Sore throat', 'Fatigue',
                'Nausea', 'Vomiting', 'Diarrhea', 'Muscle pain', 'Joint pain',
                'Shortness of breath', 'Chest pain', 'Dizziness', 'Rash',
                'Abdominal pain', 'Back pain', 'Neck pain', 'Sweating',
                'Chills', 'Loss of appetite', 'Weight loss', 'Insomnia'
            ],
            'category': [
                'General', 'Neurological', 'Respiratory', 'Respiratory', 'General',
                'Digestive', 'Digestive', 'Digestive', 'Musculoskeletal', 'Musculoskeletal',
                'Respiratory', 'Cardiovascular', 'Neurological', 'Dermatological',
                'Digestive', 'Musculoskeletal', 'Musculoskeletal', 'General',
                'General', 'General', 'General', 'Neurological'
            ],
            'severity': [
                'medium', 'low', 'low', 'low', 'medium',
                'medium', 'medium', 'medium', 'low', 'low',
                'high', 'high', 'medium', 'low',
                'high', 'low', 'low', 'low',
                'low', 'low', 'medium', 'medium'
            ]
        })
        symptoms_df.to_csv(os.path.join(self.dataset_path, 'symptoms.csv'), index=False)
        
        # Sample diseases data
        diseases_df = pd.DataFrame({
            'disease_id': range(1, 11),
            'disease': [
                'Common Cold', 'Influenza', 'COVID-19', 'Allergy', 'Sinusitis',
                'Migraine', 'Food Poisoning', 'Gastroenteritis', 'Pneumonia', 'Bronchitis'
            ],
            'symptoms': [
                'cough, sore throat, runny nose, fever',
                'fever, headache, muscle pain, fatigue, cough',
                'fever, cough, shortness of breath, fatigue, loss of taste',
                'sneezing, itchy eyes, runny nose, rash',
                'headache, facial pain, nasal congestion, fever',
                'headache, nausea, sensitivity to light, dizziness',
                'nausea, vomiting, diarrhea, abdominal pain, fever',
                'diarrhea, vomiting, abdominal pain, fever',
                'fever, cough, shortness of breath, chest pain, fatigue',
                'cough, mucus, fatigue, shortness of breath, fever'
            ],
            'severity': [
                'low', 'medium', 'high', 'low', 'medium',
                'medium', 'medium', 'medium', 'high', 'medium'
            ],
            'common_treatments': [
                'Rest, fluids, over-the-counter cold medicine',
                'Rest, fluids, antiviral medication if early',
                'Rest, isolation, supportive care, vaccination',
                'Antihistamines, avoid allergens, nasal sprays',
                'Decongestants, nasal irrigation, pain relievers',
                'Pain relievers, rest, dark room, hydration',
                'Hydration, rest, electrolyte replacement',
                'Hydration, rest, BRAT diet',
                'Antibiotics, rest, fluids, hospitalization if severe',
                'Rest, fluids, cough medicine, inhalers if needed'
            ]
        })
        diseases_df.to_csv(os.path.join(self.dataset_path, 'diseases.csv'), index=False)
        
        # Sample medicines data
        medicines_df = pd.DataFrame({
            'medicine_id': range(1, 16),
            'name': [
                'Paracetamol', 'Ibuprofen', 'Aspirin', 'Cetirizine', 'Loratadine',
                'Amoxicillin', 'Azithromycin', 'Omeprazole', 'Lansoprazole', 'Metformin',
                'Atorvastatin', 'Amlodipine', 'Metoprolol', 'Losartan', 'Lisinopril'
            ],
            'generic_name': [
                'Acetaminophen', 'Ibuprofen', 'Acetylsalicylic Acid', 'Cetirizine HCl', 'Loratadine',
                'Amoxicillin', 'Azithromycin', 'Omeprazole', 'Lansoprazole', 'Metformin HCl',
                'Atorvastatin Calcium', 'Amlodipine Besylate', 'Metoprolol Tartrate', 'Losartan Potassium', 'Lisinopril'
            ],
            'category': [
                'Analgesic', 'NSAID', 'NSAID', 'Antihistamine', 'Antihistamine',
                'Antibiotic', 'Antibiotic', 'Antacid', 'Antacid', 'Antidiabetic',
                'Statin', 'Calcium Channel Blocker', 'Beta Blocker', 'ARB', 'ACE Inhibitor'
            ],
            'manufacturer': [
                'Various', 'Various', 'Various', 'Various', 'Various',
                'Various', 'Various', 'Various', 'Various', 'Various',
                'Various', 'Various', 'Various', 'Various', 'Various'
            ],
            'dosage_form': [
                'Tablet', 'Tablet', 'Tablet', 'Tablet', 'Tablet',
                'Capsule', 'Tablet', 'Capsule', 'Tablet', 'Tablet',
                'Tablet', 'Tablet', 'Tablet', 'Tablet', 'Tablet'
            ],
            'strength': [
                '500mg', '400mg', '325mg', '10mg', '10mg',
                '500mg', '250mg', '20mg', '30mg', '500mg',
                '20mg', '5mg', '50mg', '50mg', '10mg'
            ],
            'price': [
                5.00, 8.00, 4.00, 6.00, 7.00,
                12.00, 15.00, 10.00, 12.00, 8.00,
                25.00, 15.00, 18.00, 20.00, 15.00
            ],
            'requires_prescription': [
                False, False, False, False, False,
                True, True, False, False, True,
                True, True, True, True, True
            ],
            'side_effects': [
                'Nausea, rash, liver damage with overdose',
                'Stomach upset, bleeding risk',
                'Stomach irritation, bleeding risk',
                'Drowsiness, dry mouth',
                'Headache, dry mouth',
                'Diarrhea, rash, yeast infection',
                'Diarrhea, nausea, abdominal pain',
                'Headache, diarrhea, vitamin B12 deficiency',
                'Diarrhea, headache, nausea',
                'Diarrhea, nausea, metallic taste',
                'Muscle pain, liver enzyme elevation',
                'Swelling, fatigue, dizziness',
                'Dizziness, fatigue, slow heart rate',
                'Dizziness, cough, hyperkalemia',
                'Cough, dizziness, hyperkalemia'
            ]
        })
        medicines_df.to_csv(os.path.join(self.dataset_path, 'medicines.csv'), index=False)
        
        # Sample hospitals data
        hospitals_df = pd.DataFrame({
            'hospital_id': range(1, 11),
            'name': [
                'City General Hospital', 'Memorial Medical Center', 'St. Mary\'s Hospital',
                'University Medical Center', 'Community Health Hospital', 'Regional Medical Center',
                'Children\'s Hospital', 'Women\'s Health Center', 'Orthopedic Specialty Hospital',
                'Cardiac Care Center'
            ],
            'address': [
                '123 Main Street', '456 Oak Avenue', '789 Pine Road',
                '100 University Drive', '200 Community Lane', '300 Regional Boulevard',
                '400 Child Street', '500 Women\'s Way', '600 Orthopedic Drive',
                '700 Heart Lane'
            ],
            'city': [
                'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin'
            ],
            'state': [
                'NY', 'CA', 'IL', 'TX', 'AZ',
                'PA', 'TX', 'CA', 'TX', 'TX'
            ],
            'zip_code': [
                '10001', '90001', '60601', '77001', '85001',
                '19101', '78201', '92101', '75201', '78701'
            ],
            'phone': [
                '212-555-0100', '213-555-0100', '312-555-0100', '713-555-0100',
                '602-555-0100', '215-555-0100', '210-555-0100', '619-555-0100',
                '214-555-0100', '512-555-0100'
            ],
            'email': [
                'info@citygeneral.com', 'info@memorialmedical.com', 'info@stmarys.com',
                'info@universitymedical.com', 'info@communityhealth.com', 'info@regionalmedical.com',
                'info@childrenshospital.com', 'info@womenshealth.com', 'info@orthopedicspecialty.com',
                'info@cardiaccare.com'
            ],
            'website': [
                'www.citygeneral.com', 'www.memorialmedical.com', 'www.stmarys.com',
                'www.universitymedical.com', 'www.communityhealth.com', 'www.regionalmedical.com',
                'www.childrenshospital.com', 'www.womenshealth.com', 'www.orthopedicspecialty.com',
                'www.cardiaccare.com'
            ],
            'latitude': [
                40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
                39.9526, 29.4241, 32.7157, 32.7767, 30.2672
            ],
            'longitude': [
                -74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
                -75.1652, -98.4936, -117.1611, -96.7970, -97.7431
            ],
            'total_beds': [
                500, 400, 350, 600, 250, 450, 300, 200, 250, 300
            ],
            'available_beds': [
                50, 30, 20, 60, 40, 35, 25, 15, 30, 20
            ],
            'emergency_services': [
                True, True, True, True, True,
                True, True, True, True, True
            ],
            'ambulance_available': [
                True, True, True, True, True,
                True, True, True, True, True
            ],
            'specialties': [
                'General Medicine, Surgery, Pediatrics',
                'Cardiology, Neurology, Oncology',
                'Pediatrics, OB/GYN, General Surgery',
                'All Specialties, Research',
                'Family Medicine, Internal Medicine',
                'Cardiology, Orthopedics, Neurology',
                'Pediatrics, Pediatric Surgery',
                'OB/GYN, Neonatology',
                'Orthopedics, Sports Medicine',
                'Cardiology, Cardiac Surgery'
            ],
            'rating': [
                4.5, 4.7, 4.3, 4.8, 4.0,
                4.6, 4.4, 4.2, 4.5, 4.7
            ]
        })
        hospitals_df.to_csv(os.path.join(self.dataset_path, 'hospitals.csv'), index=False)
        
        # Sample ambulances data
        ambulances_df = pd.DataFrame({
            'ambulance_id': range(1, 11),
            'vehicle_number': [
                'AMB-001', 'AMB-002', 'AMB-003', 'AMB-004', 'AMB-005',
                'AMB-006', 'AMB-007', 'AMB-008', 'AMB-009', 'AMB-010'
            ],
            'hospital_id': [
                1, 1, 2, 2, 3, 3, 4, 4, 5, 5
            ],
            'driver_name': [
                'John Smith', 'Mary Johnson', 'Robert Williams', 'Patricia Brown',
                'Michael Jones', 'Jennifer Garcia', 'William Miller', 'Linda Davis',
                'David Martinez', 'Elizabeth Wilson'
            ],
            'driver_phone': [
                '212-555-1000', '212-555-1001', '213-555-1000', '213-555-1001',
                '312-555-1000', '312-555-1001', '713-555-1000', '713-555-1001',
                '602-555-1000', '602-555-1001'
            ],
            'latitude': [
                40.7130, 40.7120, 34.0520, 34.0530, 41.8780,
                41.8790, 29.7600, 29.7610, 33.4480, 33.4490
            ],
            'longitude': [
                -74.0060, -74.0050, -118.2430, -118.2440, -87.6290,
                -87.6280, -95.3690, -95.3680, -112.0740, -112.0730
            ],
            'status': [
                'available', 'available', 'available', 'busy', 'available',
                'available', 'available', 'busy', 'available', 'available'
            ],
            'equipment_level': [
                'advanced', 'basic', 'advanced', 'advanced', 'basic',
                'advanced', 'basic', 'advanced', 'basic', 'advanced'
            ]
        })
        ambulances_df.to_csv(os.path.join(self.dataset_path, 'ambulances.csv'), index=False)
        
        # Sample doctors data
        doctors_df = pd.DataFrame({
            'doctor_id': range(1, 16),
            'name': [
                'Dr. James Wilson', 'Dr. Sarah Johnson', 'Dr. Michael Chen',
                'Dr. Emily Brown', 'Dr. Robert Taylor', 'Dr. Lisa Martinez',
                'Dr. David Kim', 'Dr. Jennifer Lee', 'Dr. William Park',
                'Dr. Maria Garcia', 'Dr. Thomas Wright', 'Dr. Patricia Anderson',
                'Dr. Joseph Thompson', 'Dr. Elizabeth White', 'Dr. Charles Davis'
            ],
            'email': [
                'jwilson@hospital.com', 'sjohnson@hospital.com', 'mchen@hospital.com',
                'ebrown@hospital.com', 'rtaylor@hospital.com', 'lmartinez@hospital.com',
                'dkim@hospital.com', 'jlee@hospital.com', 'wpark@hospital.com',
                'mgarcia@hospital.com', 'twright@hospital.com', 'panderson@hospital.com',
                'jthompson@hospital.com', 'ewhite@hospital.com', 'cdavis@hospital.com'
            ],
            'phone': [
                '212-555-2000', '212-555-2001', '213-555-2000', '213-555-2001',
                '312-555-2000', '312-555-2001', '713-555-2000', '713-555-2001',
                '602-555-2000', '602-555-2001', '215-555-2000', '215-555-2001',
                '210-555-2000', '210-555-2001', '619-555-2000'
            ],
            'specialization': [
                'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
                'Internal Medicine', 'Family Medicine', 'Oncology', 'OB/GYN',
                'Dermatology', 'Psychiatry', 'Ophthalmology', 'ENT',
                'Urology', 'Nephrology', 'Gastroenterology'
            ],
            'hospital_id': [
                1, 1, 2, 3, 4, 5, 1, 3, 2, 4, 5, 1, 3, 2, 4
            ],
            'years_experience': [
                15, 12, 10, 8, 20, 7, 14, 11, 9, 13, 16, 10, 12, 8, 15
            ],
            'consultation_fee': [
                150, 175, 120, 100, 200, 90, 180, 130, 110, 160, 140, 120, 170, 145, 155
            ],
            'rating': [
                4.8, 4.7, 4.6, 4.5, 4.9, 4.4, 4.7, 4.6, 4.5, 4.8, 4.6, 4.7, 4.5, 4.6, 4.8
            ]
        })
        doctors_df.to_csv(os.path.join(self.dataset_path, 'doctors.csv'), index=False)
        
        # Sample appointments data
        appointments_df = pd.DataFrame({
            'appointment_id': range(1, 11),
            'patient_id': [
                'P001', 'P002', 'P003', 'P004', 'P005',
                'P001', 'P003', 'P002', 'P004', 'P005'
            ],
            'doctor_id': [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10
            ],
            'hospital_id': [
                1, 1, 2, 3, 4, 5, 1, 3, 2, 4
            ],
            'appointment_date': [
                '2024-01-15 10:00:00', '2024-01-15 11:30:00', '2024-01-16 09:00:00',
                '2024-01-16 14:00:00', '2024-01-17 10:30:00', '2024-01-18 11:00:00',
                '2024-01-18 15:00:00', '2024-01-19 09:30:00', '2024-01-19 13:00:00',
                '2024-01-20 10:00:00'
            ],
            'status': [
                'scheduled', 'confirmed', 'scheduled', 'completed', 'scheduled',
                'confirmed', 'scheduled', 'completed', 'scheduled', 'confirmed'
            ],
            'symptoms': [
                'Chest pain, shortness of breath', 'Headache, dizziness',
                'Joint pain, swelling', 'Fever, cough', 'Abdominal pain, nausea',
                'Rash, itching', 'Fatigue, weight loss', 'Back pain',
                'Anxiety, insomnia', 'Vision problems'
            ],
            'notes': [
                'Patient reports chest discomfort', 'Migraine history',
                'Knee pain for 3 months', 'Child with persistent cough',
                'Food poisoning suspected', 'Allergic reaction',
                'Unexplained weight loss', 'Chronic back pain',
                'Stress-related symptoms', 'Blurry vision'
            ]
        })
        appointments_df.to_csv(os.path.join(self.dataset_path, 'appointments.csv'), index=False)
        
        # Sample health awareness data
        awareness_df = pd.DataFrame({
            'topic_id': range(1, 11),
            'topic': [
                'Heart Health', 'Diabetes Prevention', 'Mental Health Awareness',
                'Nutrition and Diet', 'Exercise Benefits', 'Stress Management',
                'Vaccination Importance', 'Cancer Screening', 'Asthma Management',
                'Allergy Prevention'
            ],
            'content': [
                'Heart disease is the leading cause of death worldwide. Regular exercise, healthy diet, and avoiding smoking can significantly reduce risk.',
                'Type 2 diabetes can be prevented through healthy eating, regular exercise, and maintaining a healthy weight. Regular screening is important.',
                'Mental health is just as important as physical health. Practice self-care, seek help when needed, and maintain social connections.',
                'A balanced diet rich in fruits, vegetables, whole grains, and lean proteins is essential for overall health. Limit processed foods and sugar.',
                'Regular physical activity (150 minutes per week) can prevent chronic diseases, improve mood, and increase life expectancy.',
                'Chronic stress can affect both mental and physical health. Practice mindfulness, deep breathing, and take regular breaks.',
                'Vaccines prevent serious diseases and save millions of lives each year. Stay up to date with recommended immunizations.',
                'Regular cancer screenings can detect cancer early when it is most treatable. Follow recommended screening guidelines.',
                'Asthma is a chronic lung condition that can be managed with proper medication, avoiding triggers, and regular monitoring.',
                'Common allergies can be managed with avoidance strategies, medication, and immunotherapy. Identify and avoid triggers.'
            ],
            'tips': [
                'Exercise 30 mins daily, eat heart-healthy foods, avoid smoking.',
                'Regular blood sugar checks, healthy diet, regular exercise.',
                'Talk to someone, practice mindfulness, seek professional help.',
                'Eat 5 servings of fruits/vegetables, stay hydrated.',
                'Start with 10-minute walks, gradually increase intensity.',
                'Deep breathing exercises, take breaks, maintain work-life balance.',
                'Follow CDC vaccine schedule, discuss with your doctor.',
                'Regular mammograms, colonoscopies, and other screenings.',
                'Use inhaler as prescribed, avoid triggers, monitor symptoms.',
                'Keep windows closed, use HEPA filters, take antihistamines.'
            ],
            'severity': [
                'high', 'high', 'medium', 'medium', 'low',
                'medium', 'high', 'high', 'medium', 'low'
            ],
            'target_audience': [
                'all', 'high-risk', 'all', 'all', 'all',
                'all', 'all', 'adults', 'asthmatics', 'allergy-prone'
            ]
        })
        awareness_df.to_csv(os.path.join(self.dataset_path, 'health_awareness.csv'), index=False)
        
        # Save a README for the datasets
        readme_content = """
        # NexusMed Datasets

        This folder contains all dataset files used by NexusMed.

        ## Files

        1. **symptoms.csv** - List of common symptoms with categories and severity
        2. **diseases.csv** - Disease-symptom mapping with treatments
        3. **medicines.csv** - Medicine information including pricing and side effects
        4. **hospitals.csv** - Hospital details with locations and bed availability
        5. **ambulances.csv** - Ambulance details with locations and status
        6. **doctors.csv** - Doctor information with specializations and ratings
        7. **appointments.csv** - Sample appointment records
        8. **health_awareness.csv** - Health awareness content for community education

        ## Usage

        These datasets are automatically loaded by the DatasetLoader class.
        You can replace these with your own data maintaining the same structure.

        ## Customization

        To use your own data, ensure your CSV files have the same column names and formats.
        """
        
        with open(os.path.join(self.dataset_path, 'README.md'), 'w') as f:
            f.write(readme_content)
        
        logger.info("Sample datasets created successfully in " + self.dataset_path)
    
    def _load_all_datasets(self):
        """Load all datasets into memory."""
        try:
            dataset_files = {
                'symptoms': 'symptoms.csv',
                'diseases': 'diseases.csv',
                'medicines': 'medicines.csv',
                'hospitals': 'hospitals.csv',
                'ambulances': 'ambulances.csv',
                'doctors': 'doctors.csv',
                'appointments': 'appointments.csv',
                'health_awareness': 'health_awareness.csv'
            }
            
            for name, filename in dataset_files.items():
                filepath = os.path.join(self.dataset_path, filename)
                if os.path.exists(filepath):
                    self.datasets[name] = pd.read_csv(filepath)
                    logger.info(f"Loaded {name} dataset with {len(self.datasets[name])} records")
                else:
                    logger.warning(f"Dataset file not found: {filepath}")
                    self.datasets[name] = pd.DataFrame()
            
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
            raise
    
    def get_symptoms(self):
        """Get symptoms dataset."""
        return self.datasets.get('symptoms', pd.DataFrame())
    
    def get_diseases(self):
        """Get diseases dataset."""
        return self.datasets.get('diseases', pd.DataFrame())
    
    def get_medicines(self):
        """Get medicines dataset."""
        return self.datasets.get('medicines', pd.DataFrame())
    
    def get_hospitals(self):
        """Get hospitals dataset."""
        return self.datasets.get('hospitals', pd.DataFrame())
    
    def get_ambulances(self):
        """Get ambulances dataset."""
        return self.datasets.get('ambulances', pd.DataFrame())
    
    def get_doctors(self):
        """Get doctors dataset."""
        return self.datasets.get('doctors', pd.DataFrame())
    
    def get_appointments(self):
        """Get appointments dataset."""
        return self.datasets.get('appointments', pd.DataFrame())
    
    def get_health_awareness(self):
        """Get health awareness dataset."""
        return self.datasets.get('health_awareness', pd.DataFrame())
    
    def get_symptom_disease_mapping(self):
        """
        Get a mapping of symptoms to diseases.
        
        Returns:
            dict: Dictionary with symptoms as keys and list of diseases as values
        """
        diseases_df = self.get_diseases()
        if diseases_df.empty:
            return {}
        
        mapping = {}
        for _, row in diseases_df.iterrows():
            disease = row.get('disease', '')
            symptoms_str = row.get('symptoms', '')
            if disease and symptoms_str:
                symptoms = [s.strip().lower() for s in symptoms_str.split(',')]
                for symptom in symptoms:
                    if symptom:
                        if symptom not in mapping:
                            mapping[symptom] = []
                        mapping[symptom].append(disease)
        
        return mapping
    
    def get_disease_symptoms(self):
        """
        Get a mapping of diseases to symptoms.
        
        Returns:
            dict: Dictionary with diseases as keys and list of symptoms as values
        """
        diseases_df = self.get_diseases()
        if diseases_df.empty:
            return {}
        
        mapping = {}
        for _, row in diseases_df.iterrows():
            disease = row.get('disease', '')
            symptoms_str = row.get('symptoms', '')
            if disease and symptoms_str:
                symptoms = [s.strip() for s in symptoms_str.split(',')]
                mapping[disease] = symptoms
        
        return mapping
    
    def get_medicine_by_category(self, category):
        """
        Get medicines by category.
        
        Args:
            category: Medicine category to filter by
        
        Returns:
            DataFrame: Filtered medicines
        """
        medicines_df = self.get_medicines()
        if medicines_df.empty:
            return pd.DataFrame()
        
        return medicines_df[medicines_df['category'].str.contains(category, case=False, na=False)]
    
    def get_hospitals_near_location(self, lat, lng, radius_km=10):
        """
        Get hospitals near a location.
        
        Args:
            lat: Latitude of the location
            lng: Longitude of the location
            radius_km: Search radius in kilometers
        
        Returns:
            DataFrame: Filtered hospitals
        """
        from math import radians, sin, cos, sqrt, asin
        
        hospitals_df = self.get_hospitals()
        if hospitals_df.empty:
            return pd.DataFrame()
        
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth's radius in kilometers
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            return R * c
        
        hospitals_df['distance_km'] = hospitals_df.apply(
            lambda row: haversine(lat, lng, row['latitude'], row['longitude']),
            axis=1
        )
        
        return hospitals_df[hospitals_df['distance_km'] <= radius_km].sort_values('distance_km')
    
    def get_available_ambulances(self):
        """
        Get available ambulances.
        
        Returns:
            DataFrame: Available ambulances
        """
        ambulances_df = self.get_ambulances()
        if ambulances_df.empty:
            return pd.DataFrame()
        
        return ambulances_df[ambulances_df['status'] == 'available']
    
    def get_doctors_by_specialization(self, specialization):
        """
        Get doctors by specialization.
        
        Args:
            specialization: Doctor specialization to filter by
        
        Returns:
            DataFrame: Filtered doctors
        """
        doctors_df = self.get_doctors()
        if doctors_df.empty:
            return pd.DataFrame()
        
        return doctors_df[doctors_df['specialization'].str.contains(specialization, case=False, na=False)]
    
    def get_health_tips(self, topic=None):
        """
        Get health tips.
        
        Args:
            topic: Specific topic to filter by
        
        Returns:
            DataFrame: Health tips
        """
        awareness_df = self.get_health_awareness()
        if awareness_df.empty:
            return pd.DataFrame()
        
        if topic:
            return awareness_df[awareness_df['topic'].str.contains(topic, case=False, na=False)]
        
        return awareness_df
    
    def reload_datasets(self):
        """Reload all datasets from files."""
        self.datasets = {}
        self._load_all_datasets()
        return True
    
    def get_stats(self):
        """
        Get statistics about loaded datasets.
        
        Returns:
            dict: Dataset statistics
        """
        stats = {}
        for name, df in self.datasets.items():
            stats[name] = {
                'records': len(df),
                'columns': list(df.columns) if not df.empty else []
            }
        return stats

# Singleton instance for global use
_dataset_loader = None

def get_dataset_loader(dataset_path=None):
    """
    Get the global dataset loader instance.
    
    Args:
        dataset_path: Path to datasets folder (only used on first call)
    
    Returns:
        DatasetLoader: The global dataset loader instance
    """
    global _dataset_loader
    if _dataset_loader is None:
        _dataset_loader = DatasetLoader(dataset_path)
    return _dataset_loader

# Example usage
if __name__ == "__main__":
    # Test the dataset loader
    loader = get_dataset_loader()
    
    print("Dataset Statistics:")
    for name, stats in loader.get_stats().items():
        print(f"  {name}: {stats['records']} records")
    
    # Test symptom-disease mapping
    mapping = loader.get_symptom_disease_mapping()
    print(f"\nSymptom-Disease Mapping: {len(mapping)} symptoms found")
    
    # Test nearby hospitals
    hospitals = loader.get_hospitals_near_location(40.7128, -74.0060, 100)
    print(f"\nNearby hospitals: {len(hospitals)} found")
    
    print("\nDataset loader test completed successfully!")