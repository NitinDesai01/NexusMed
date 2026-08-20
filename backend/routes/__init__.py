from routes.auth import bp as auth_bp
from routes.symptom import bp as symptom_bp
from routes.medicine import bp as medicine_bp
from routes.report import bp as report_bp
from routes.hospital import bp as hospital_bp
from routes.ambulance import bp as ambulance_bp
from routes.community import bp as community_bp
from routes.appointment import bp as appointment_bp
from routes.dashboard import bp as dashboard_bp

__all__ = [
    "auth_bp",
    "symptom_bp",
    "medicine_bp",
    "report_bp",
    "hospital_bp",
    "ambulance_bp",
    "community_bp",
    "appointment_bp",
    "dashboard_bp"
]