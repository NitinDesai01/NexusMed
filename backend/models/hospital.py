from config.database import db
from datetime import datetime

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    total_beds = db.Column(db.Integer)
    available_beds = db.Column(db.Integer)
    emergency_services = db.Column(db.Boolean, default=False)
    ambulance_available = db.Column(db.Boolean, default=False)
    specialties = db.Column(db.Text)
    rating = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'total_beds': self.total_beds,
            'available_beds': self.available_beds,
            'emergency_services': self.emergency_services,
            'ambulance_available': self.ambulance_available,
            'specialties': self.specialties,
            'rating': self.rating
        }