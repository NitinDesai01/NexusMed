from config.database import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'))
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, confirmed, completed, cancelled
    symptoms = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')
    hospital = db.relationship('Hospital', backref='appointments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'hospital_id': self.hospital_id,
            'hospital_name': self.hospital.name if self.hospital else None,
            'appointment_date': self.appointment_date.isoformat(),
            'status': self.status,
            'symptoms': self.symptoms,
            'notes': self.notes
        }