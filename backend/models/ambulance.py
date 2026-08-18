from config.database import db
from datetime import datetime

class Ambulance(db.Model):
    __tablename__ = 'ambulances'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50), unique=True, nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    driver_name = db.Column(db.String(100))
    driver_phone = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String(20), default='available')  # available, busy, offline
    equipment_level = db.Column(db.String(50))  # basic, advanced, ICU
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    hospital = db.relationship('Hospital', backref='ambulances')
    
    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_number': self.vehicle_number,
            'hospital_id': self.hospital_id,
            'hospital_name': self.hospital.name if self.hospital else None,
            'driver_name': self.driver_name,
            'driver_phone': self.driver_phone,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'status': self.status,
            'equipment_level': self.equipment_level,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }