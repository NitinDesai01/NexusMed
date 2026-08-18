from datetime import datetime
import json
import uuid
import logging

logger = logging.getLogger(__name__)

class AlertManager:
    def __init__(self):
        self.alerts = []
        self.subscribers = {}
        
    def create_alert(self, title, message, lat, lng, radius=10, alert_type='general', priority='medium'):
        """Create a community alert"""
        try:
            alert = {
                'id': str(uuid.uuid4())[:8],
                'title': title,
                'message': message,
                'lat': lat,
                'lng': lng,
                'radius': radius,
                'type': alert_type,
                'priority': priority,
                'status': 'active',
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'views': 0,
                'acknowledgements': []
            }
            
            self.alerts.append(alert)
            
            # Notify subscribers in the area
            self._notify_subscribers(alert)
            
            return alert
        except Exception as e:
            logger.error(f"Create alert error: {e}")
            return None
    
    def get_alerts(self, lat=None, lng=None, radius=None, limit=20):
        """Get alerts, optionally filtered by location"""
        try:
            filtered = self.alerts.copy()
            
            if lat and lng and radius:
                filtered = [
                    a for a in filtered
                    if self._is_within_radius(lat, lng, a['lat'], a['lng'], radius)
                ]
            
            # Sort by created_at descending
            filtered.sort(key=lambda x: x['created_at'], reverse=True)
            
            return filtered[:limit]
        except Exception as e:
            logger.error(f"Get alerts error: {e}")
            return []
    
    def get_alert_by_id(self, alert_id):
        """Get alert by ID"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                return alert
        return None
    
    def acknowledge_alert(self, alert_id, user_id):
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledgements'].append({
                    'user_id': user_id,
                    'timestamp': datetime.utcnow().isoformat()
                })
                return True
        return False
    
    def resolve_alert(self, alert_id):
        """Resolve/mark alert as complete"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['status'] = 'resolved'
                alert['updated_at'] = datetime.utcnow().isoformat()
                return True
        return False
    
    def subscribe(self, user_id, lat, lng, radius=10):
        """Subscribe a user to alerts in an area"""
        self.subscribers[user_id] = {
            'lat': lat,
            'lng': lng,
            'radius': radius,
            'subscribed_at': datetime.utcnow().isoformat()
        }
        return True
    
    def unsubscribe(self, user_id):
        """Unsubscribe a user"""
        if user_id in self.subscribers:
            del self.subscribers[user_id]
            return True
        return False
    
    def _notify_subscribers(self, alert):
        """Notify subscribers about a new alert"""
        for user_id, subscriber in self.subscribers.items():
            if self._is_within_radius(
                alert['lat'],
                alert['lng'],
                subscriber['lat'],
                subscriber['lng'],
                min(alert['radius'], subscriber['radius'])
            ):
                # In production, would send real notifications
                logger.info(f"Notifying user {user_id} about alert {alert['id']}")
    
    def _is_within_radius(self, lat1, lng1, lat2, lng2, radius_km):
        """Check if two points are within a radius"""
        from math import radians, sin, cos, sqrt, asin
        
        R = 6371  # Earth's radius in km
        
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * asin(sqrt(a))
        distance = R * c
        
        return distance <= radius_km