import logging

logger = logging.getLogger(__name__)

class CommunityAgent:
    def __init__(self):
        pass
        
    def get_awareness_content(self, topic):
        return {"topic": topic, "content": f"Health awareness about {topic}"}
    
    def get_alerts(self, lat=None, lng=None):
        return [{"id": 1, "title": "Health Alert", "status": "active"}]
    
    def create_alert(self, title, message, lat, lng, radius=10, alert_type="general"):
        return {"id": 1, "title": title, "message": message, "status": "active"}
