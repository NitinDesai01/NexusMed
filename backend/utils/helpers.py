import re
import uuid
from datetime import datetime, timedelta
import hashlib
import json

def generate_id(prefix=''):
    """Generate a unique ID"""
    uid = str(uuid.uuid4())[:8]
    return f"{prefix}_{uid}" if prefix else uid

def format_datetime(dt):
    """Format datetime to ISO string"""
    if isinstance(dt, str):
        return dt
    return dt.isoformat() if dt else None

def parse_datetime(dt_str):
    """Parse ISO datetime string"""
    try:
        return datetime.fromisoformat(dt_str)
    except:
        return None

def hash_string(text):
    """Hash a string using SHA-256"""
    return hashlib.sha256(text.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[0-9]{10,15}$'
    return re.match(pattern, phone) is not None

def calculate_age(birth_date):
    """Calculate age from birth date"""
    if not birth_date:
        return None
    
    if isinstance(birth_date, str):
        birth_date = datetime.fromisoformat(birth_date)
    
    today = datetime.now()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

def is_valid_date(date_str):
    """Check if a string is a valid date"""
    try:
        datetime.fromisoformat(date_str)
        return True
    except:
        return False

def safe_json_loads(json_str, default=None):
    """Safely parse JSON string"""
    try:
        return json.loads(json_str)
    except:
        return default

def safe_json_dumps(obj, default=None):
    """Safely convert to JSON string"""
    try:
        return json.dumps(obj)
    except:
        return default

def get_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates in km"""
    from math import radians, sin, cos, sqrt, asin
    
    R = 6371  # Earth's radius in km
    
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def truncate_string(text, max_length=100, suffix='...'):
    """Truncate a string to max length"""
    if not text:
        return text
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def extract_keywords(text, max_keywords=10):
    """Extract keywords from text"""
    # Remove common words
    stopwords = {'the', 'a', 'an', 'of', 'for', 'on', 'at', 'to', 'in', 'is', 'it', 'and', 'or', 'but'}
    
    # Split and clean
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    # Count frequencies
    freq = {}
    for word in words:
        if word not in stopwords and len(word) > 2:
            freq[word] = freq.get(word, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    return [word for word, _ in sorted_words[:max_keywords]]