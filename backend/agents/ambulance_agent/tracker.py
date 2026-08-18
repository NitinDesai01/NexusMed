from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

class AmbulanceTracker:
    def __init__(self):
        self.active_ambulances = {}
        self.history = {}
        
    def update_location(self, ambulance_id, lat, lng, status='en_route'):
        """Update ambulance location"""
        try:
            if ambulance_id not in self.active_ambulances:
                self.active_ambulances[ambulance_id] = {
                    'id': ambulance_id,
                    'locations': [],
                    'current_status': status,
                    'last_update': datetime.utcnow().isoformat()
                }
            
            location_data = {
                'lat': lat,
                'lng': lng,
                'timestamp': datetime.utcnow().isoformat(),
                'status': status            }
            
            self.active_ambulances[ambulance_id]['locations'].append(location_data)
            self.active_ambulances[ambulance_id]['current_status'] = status
            self.active_ambulances[ambulance_id]['last_update'] = location_data['timestamp']
            
            # Keep only last 100 locations
            if len(self.active_ambulances[ambulance_id]['locations']) > 100:
                self.active_ambulances[ambulance_id]['locations'] = \
                    self.active_ambulances[ambulance_id]['locations'][-100:]
            
            return True
            
        except Exception as e:
            logger.error(f"Location update error: {e}")
            return False
    
    def get_ambulance_location(self, ambulance_id):
        """Get current ambulance location"""
        ambulance = self.active_ambulances.get(ambulance_id)
        if ambulance:
            locations = ambulance['locations']
            if locations:
                return {
                    'ambulance_id': ambulance_id,
                    'current_location': locations[-1],
                    'status': ambulance['current_status'],
                    'last_update': ambulance['last_update']
                }
        return None
    
    def get_ambulance_trail(self, ambulance_id, minutes=30):
        """Get ambulance trail for last N minutes"""
        ambulance = self.active_ambulances.get(ambulance_id)
        if not ambulance:
            return None
        
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        cutoff = cutoff_time.isoformat()
        
        trail = [
            loc for loc in ambulance['locations']
            if loc['timestamp'] >= cutoff
        ]
        
        return {
            'ambulance_id': ambulance_id,
            'trail': trail,
            'trail_duration_minutes': minutes
        }
    
    def get_all_active_ambulances(self):
        """Get all active ambulances"""
        active = []
        for ambulance_id, data in self.active_ambulances.items():
            if data['current_status'] in ['en_route', 'available']:
                active.append({
                    'id': ambulance_id,
                    'status': data['current_status'],
                    'last_update': data['last_update']
                })
        return active
    
    def calculate_eta(self, ambulance_id, destination_lat, destination_lng):
        """Calculate ETA for ambulance to destination"""
        ambulance = self.active_ambulances.get(ambulance_id)
        if not ambulance:
            return None
        
        current_location = ambulance['locations'][-1] if ambulance['locations'] else None
        if not current_location:
            return None
        
        from services.maps_service import MapsService
        maps = MapsService()
        
        distance = maps.get_distance(
            current_location['lat'],
            current_location['lng'],
            destination_lat,
            destination_lng
        )
        
        # Assume average speed of 40 km/h
        eta_minutes = (distance / 40) * 60
        
        return {
            'ambulance_id': ambulance_id,
            'distance_km': round(distance, 2),
            'eta_minutes': round(eta_minutes, 2),
            'estimated_arrival': (datetime.utcnow() + timedelta(minutes=eta_minutes)).isoformat()
        }