import math
from services.maps_service import MapsService
import logging

logger = logging.getLogger(__name__)

class AmbulanceRouting:
    def __init__(self):
        self.maps = MapsService()
        self.traffic_factors = {
            'low': 1.0,
            'medium': 1.3,
            'high': 1.8,
            'very_high': 2.5
        }
        
    def calculate_route(self, origin_lat, origin_lng, dest_lat, dest_lng, traffic='medium'):
        """Calculate optimal route for ambulance"""
        try:
            # Calculate direct distance
            distance = self.maps.get_distance(origin_lat, origin_lng, dest_lat, dest_lng)
            
            # Apply traffic factor
            traffic_factor = self.traffic_factors.get(traffic, 1.3)
            
            # Calculate estimated time (assuming average speed 40 km/h with traffic)
            avg_speed = 40 / traffic_factor  # km/h
            estimated_time = (distance / avg_speed) * 60  # minutes
            
            # Determine if route needs rerouting
            reroute_needed = distance > 10  # If distance > 10km, consider rerouting
            
            return {
                'distance_km': round(distance, 2),
                'estimated_time_minutes': round(estimated_time, 2),
                'traffic_level': traffic,
                'reroute_needed': reroute_needed,
                'route_points': self._generate_route_points(origin_lat, origin_lng, dest_lat, dest_lng)
            }
            
        except Exception as e:
            logger.error(f"Route calculation error: {e}")
            return None
    
    def _generate_route_points(self, origin_lat, origin_lng, dest_lat, dest_lng, num_points=10):
        """Generate intermediate points along the route"""
        points = []
        
        for i in range(num_points + 1):
            t = i / num_points
            lat = origin_lat + (dest_lat - origin_lat) * t
            lng = origin_lng + (dest_lng - origin_lng) * t
            points.append({'lat': lat, 'lng': lng})
            
        return points
    
    def get_nearest_hospital_route(self, ambulance_lat, ambulance_lng, hospitals):
        """Get route to nearest hospital with available beds"""
        try:
            nearest = None
            shortest_distance = float('inf')
            
            for hospital in hospitals:
                if hospital.get('available_beds', 0) > 0:
                    distance = self.maps.get_distance(
                        ambulance_lat,
                        ambulance_lng,
                        hospital.get('latitude', 0),
                        hospital.get('longitude', 0)
                    )
                    
                    if distance < shortest_distance:
                        shortest_distance = distance
                        nearest = hospital
            
            if nearest:
                route = self.calculate_route(
                    ambulance_lat,
                    ambulance_lng,
                    nearest.get('latitude'),
                    nearest.get('longitude')
                )
                
                return {
                    'hospital': nearest,
                    'route': route
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Nearest hospital route error: {e}")
            return None
    
    def optimize_ambulance_routing(self, ambulance_lat, ambulance_lng, destinations):
        """Optimize route for multiple destinations"""
        try:
            routes = []
            current_lat = ambulance_lat
            current_lng = ambulance_lng
            
            for dest in destinations:
                route = self.calculate_route(
                    current_lat,
                    current_lng,
                    dest['lat'],
                    dest['lng']
                )
                
                if route:
                    routes.append({
                        'destination': dest['name'],
                        'route': route
                    })
                    
                    current_lat = dest['lat']
                    current_lng = dest['lng']
            
            return {
                'total_distance': sum(r['route']['distance_km'] for r in routes),
                'total_time': sum(r['route']['estimated_time_minutes'] for r in routes),
                'routes': routes
            }
            
        except Exception as e:
            logger.error(f"Route optimization error: {e}")
            return None