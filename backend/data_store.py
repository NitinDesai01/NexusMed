# Shared data storage for appointments
# This file is imported by both appointment and dashboard routes

appointments_db = []

def get_appointments():
    """Get all appointments"""
    return appointments_db

def add_appointment(appointment):
    """Add a new appointment"""
    appointments_db.append(appointment)
    return appointment

def get_user_appointments(user_id):
    """Get appointments for a specific user"""
    return [a for a in appointments_db if a["user_id"] == user_id]

def clear_appointments():
    """Clear all appointments (for testing)"""
    appointments_db.clear()
