from models.hospital import Hospital
from config.database import db
import logging

logger = logging.getLogger(__name__)

class BedManager:
    def __init__(self):
        pass
        
    def get_bed_availability(self, hospital_id):
        """Get bed availability for a hospital"""
        try:
            hospital = Hospital.query.get(hospital_id)
            if not hospital:
                return None
            
            return {
                'hospital_name': hospital.name,
                'total_beds': hospital.total_beds,
                'available_beds': hospital.available_beds,
                'occupancy_rate': self._calculate_occupancy_rate(
                    hospital.total_beds,
                    hospital.available_beds
                )
            }
        except Exception as e:
            logger.error(f"Bed availability error: {e}")
            return None
    
    def _calculate_occupancy_rate(self, total, available):
        """Calculate occupancy rate"""
        if total <= 0:
            return 0
        return round(((total - available) / total) * 100, 2)
    
    def update_beds(self, hospital_id, available_beds):
        """Update available beds count"""
        try:
            hospital = Hospital.query.get(hospital_id)
            if not hospital:
                return False
            
            hospital.available_beds = available_beds
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Update beds error: {e}")
            db.session.rollback()
            return False
    
    def reserve_bed(self, hospital_id, count=1):
        """Reserve beds"""
        try:
            hospital = Hospital.query.get(hospital_id)
            if not hospital or hospital.available_beds < count:
                return False
            
            hospital.available_beds -= count
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Reserve bed error: {e}")
            db.session.rollback()
            return False
    
    def release_bed(self, hospital_id, count=1):
        """Release reserved beds"""
        try:
            hospital = Hospital.query.get(hospital_id)
            if not hospital:
                return False
            
            hospital.available_beds += count
            if hospital.available_beds > hospital.total_beds:
                hospital.available_beds = hospital.total_beds
            
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Release bed error: {e}")
            db.session.rollback()
            return False
    
    def get_bed_statistics(self, city=None):
        """Get bed statistics for a city"""
        try:
            query = Hospital.query
            if city:
                query = query.filter_by(city=city)
            
            hospitals = query.all()
            
            total_beds = sum(h.total_beds for h in hospitals)
            available_beds = sum(h.available_beds for h in hospitals)
            
            return {
                'city': city or 'all',
                'total_hospitals': len(hospitals),
                'total_beds': total_beds,
                'available_beds': available_beds,
                'occupancy_rate': self._calculate_occupancy_rate(total_beds, available_beds)
            }
        except Exception as e:
            logger.error(f"Bed statistics error: {e}")
            return None