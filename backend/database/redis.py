import redis
from config.config import Config
import json
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        self.client = None
        self._initialize()
        
    def _initialize(self):
        """Initialize Redis connection"""
        try:
            self.client = redis.Redis.from_url(
                Config.REDIS_URL,
                decode_responses=True,
                socket_keepalive=True
            )
            self.client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Redis initialization error: {e}")
            self.client = None
    
    def get(self, key):
        """Get value from cache"""
        if not self.client:
            return None
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(self, key, value, ttl=None):
        """Set value in cache with optional TTL"""
        if not self.client:
            return False
        try:
            value_str = json.dumps(value)
            if ttl:
                self.client.setex(key, ttl, value_str)
            else:
                self.client.set(key, value_str)
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def delete(self, key):
        """Delete from cache"""
        if not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    def exists(self, key):
        """Check if key exists in cache"""
        if not self.client:
            return False
        try:
            return self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    def set_session(self, session_id, data, ttl=3600):
        """Store session data"""
        return self.set(f"session:{session_id}", data, ttl)
    
    def get_session(self, session_id):
        """Get session data"""
        return self.get(f"session:{session_id}")
    
    def delete_session(self, session_id):
        """Delete session"""
        return self.delete(f"session:{session_id}")
    
    def set_realtime_data(self, key, data, ttl=300):
        """Store real-time data (e.g., ambulance location)"""
        return self.set(f"realtime:{key}", data, ttl)
    
    def get_realtime_data(self, key):
        """Get real-time data"""
        return self.get(f"realtime:{key}")
    
    def health_check(self):
        """Check Redis health"""
        try:
            if not self.client:
                return {'status': 'unhealthy', 'message': 'No Redis connection'}
            self.client.ping()
            return {'status': 'healthy', 'message': 'Redis connection successful'}
        except Exception as e:
            return {'status': 'unhealthy', 'message': str(e)}