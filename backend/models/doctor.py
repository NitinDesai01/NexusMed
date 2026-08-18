from config.database import db
from datetime import datetime

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    specialization = db.Column(db.String(100))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    years_experience = db.Column(db.Integer)
    consultation_fee = db.Column(db.Float)
    availability = db.Column(db.JSON)
    rating = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    hospital = db.relationship('Hospital', backref='doctors')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'specialization': self.specialization,
            'hospital_id': self.hospital_id,
            'years_experience': self.years_experience,
            'consultation_fee': self.consultation_fee,
            'availability': self.availability,
            'rating': self.rating
        }