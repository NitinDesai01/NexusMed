from models.doctor import Doctor
from models.hospital import Hospital
from config.database import db
import logging

logger = logging.getLogger(__name__)

class DoctorManager:
    def __init__(self):
        pass
        
    def get_doctor_details(self, doctor_id):
        """Get detailed doctor information"""
        try:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return None
            
            doctor_dict = doctor.to_dict()
            if doctor.hospital:
                doctor_dict['hospital_name'] = doctor.hospital.name
            
            return doctor_dict
        except Exception as e:
            logger.error(f"Doctor details error: {e}")
            return None
    
    def search_doctors(self, specialization=None, hospital_id=None, rating_min=None):
        """Search for doctors"""
        try:
            query = Doctor.query
            
            if specialization:
                query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
            
            if hospital_id:
                query = query.filter_by(hospital_id=hospital_id)
            
            if rating_min:
                query = query.filter(Doctor.rating >= rating_min)
            
            doctors = query.all()
            return [d.to_dict() for d in doctors]
        except Exception as e:
            logger.error(f"Search doctors error: {e}")
            return []
    
    def get_available_doctors(self, hospital_id, time_slot):
        """Get available doctors for a time slot"""
        try:
            doctors = Doctor.query.filter_by(hospital_id=hospital_id).all()
            
            available = []
            for doctor in doctors:
                if doctor.availability:
                    # Check if doctor is available at the specified time
                    # This is simplified - would need proper time slot checking
                    available.append(doctor.to_dict())
            
            return available
        except Exception as e:
            logger.error(f"Available doctors error: {e}")
            return []
    
    def add_doctor(self, doctor_data):
        """Add a new doctor"""
        try:
            doctor = Doctor(
                name=doctor_data['name'],
                email=doctor_data['email'],
                phone=doctor_data.get('phone'),
                specialization=doctor_data.get('specialization'),
                hospital_id=doctor_data.get('hospital_id'),
                years_experience=doctor_data.get('years_experience', 0),
                consultation_fee=doctor_data.get('consultation_fee', 0),
                availability=doctor_data.get('availability'),
                rating=doctor_data.get('rating', 0)
            )
            
            db.session.add(doctor)
            db.session.commit()
            return doctor.to_dict()
        except Exception as e:
            logger.error(f"Add doctor error: {e}")
            db.session.rollback()
            return None
    
    def update_doctor_rating(self, doctor_id, new_rating):
        """Update doctor's rating"""
        try:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return False
            
            # Calculate new average rating
            current_rating = doctor.rating or 0
            # In a real app, you'd have a reviews table
            doctor.rating = new_rating
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Update rating error: {e}")
            db.session.rollback()
            return False
    
    def get_doctor_schedule(self, doctor_id):
        """Get doctor's schedule"""
        try:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return None
            
            return {
                'doctor_id': doctor.id,
                'name': doctor.name,
                'availability': doctor.availability or {},
                'appointments': []  # Would fetch from appointments table
            }
        except Exception as e:
            logger.error(f"Doctor schedule error: {e}")
            return None