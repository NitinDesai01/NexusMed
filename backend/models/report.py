from config.database import db
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    report_type = db.Column(db.String(50))  # blood_test, mri, xray, etc.
    file_path = db.Column(db.String(500))
    extracted_text = db.Column(db.Text)
    summary = db.Column(db.Text)
    findings = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    report_date = db.Column(db.Date)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    
    patient = db.relationship('Patient', backref='reports')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'report_type': self.report_type,
            'file_path': self.file_path,
            'extracted_text': self.extracted_text,
            'summary': self.summary,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'report_date': self.report_date.isoformat() if self.report_date else None,
            'uploaded_at': self.uploaded_at.isoformat(),
            'processed': self.processed
        }