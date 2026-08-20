from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import Config
from config.database import init_db
from routes import auth, symptom, medicine, report, hospital, ambulance, community, appointment, dashboard
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins="*")
jwt = JWTManager(app)

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(symptom.bp, url_prefix='/api/symptoms')
app.register_blueprint(medicine.bp, url_prefix='/api/medicines')
app.register_blueprint(report.bp, url_prefix='/api/reports')
app.register_blueprint(hospital.bp, url_prefix='/api/hospitals')
app.register_blueprint(ambulance.bp, url_prefix='/api/ambulances')
app.register_blueprint(community.bp, url_prefix='/api/community')
app.register_blueprint(appointment.bp, url_prefix='/api/appointments')
app.register_blueprint(dashboard.bp, url_prefix='/api/dashboard')  # Add this

@app.route('/')
def index():
    return jsonify({
        "status": "NexusMed API Running",
        "version": "1.0.0",
        "endpoints": [
            "/api/auth",
            "/api/symptoms",
            "/api/medicines",
            "/api/reports",
            "/api/hospitals",
            "/api/ambulances",
            "/api/community",
            "/api/appointments",
            "/api/dashboard"
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "message": "NexusMed API is running"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)