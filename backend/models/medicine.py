from config.database import db
from datetime import datetime

class Medicine(db.Model):
    __tablename__ = 'medicines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    generic_name = db.Column(db.String(200))
    category = db.Column(db.String(100))
    manufacturer = db.Column(db.String(200))
    dosage_form = db.Column(db.String(50))
    strength = db.Column(db.String(50))
    description = db.Column(db.Text)
    side_effects = db.Column(db.Text)
    contraindications = db.Column(db.Text)
    interactions = db.Column(db.Text)
    price = db.Column(db.Float)
    requires_prescription = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'generic_name': self.generic_name,
            'category': self.category,
            'manufacturer': self.manufacturer,
            'dosage_form': self.dosage_form,
            'strength': self.strength,
            'description': self.description,
            'side_effects': self.side_effects,
            'contraindications': self.contraindications,
            'interactions': self.interactions,
            'price': self.price,
            'requires_prescription': self.requires_prescription
        }