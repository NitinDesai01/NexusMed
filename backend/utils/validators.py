import re
from datetime import datetime

def validate_required(value, field_name):
    """Validate that a required field is not empty"""
    if not value or str(value).strip() == '':
        return False, f"{field_name} is required"
    return True, None

def validate_email(email):
    """Validate email format"""
    if not email:
        return True, None  # Optional field
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None

def validate_phone(phone):
    """Validate phone number"""
    if not phone:
        return True, None  # Optional field
    
    pattern = r'^[0-9]{10,15}$'
    if not re.match(pattern, phone.replace('+', '').replace('-', '').replace(' ', '')):
        return False, "Invalid phone number format"
    return True, None

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)"""
    if not date_str:
        return True, None  # Optional field
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, None
    except:
        return False, "Invalid date format. Use YYYY-MM-DD"

def validate_blood_group(blood_group):
    """Validate blood group"""
    if not blood_group:
        return True, None  # Optional field
    
    valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if blood_group not in valid_groups:
        return False, f"Invalid blood group. Must be one of: {', '.join(valid_groups)}"
    return True, None

def validate_gender(gender):
    """Validate gender"""
    if not gender:
        return True, None  # Optional field
    
    valid_genders = ['male', 'female', 'non-binary', 'prefer-not-to-say']
    if gender.lower() not in valid_genders:
        return False, f"Invalid gender. Must be one of: {', '.join(valid_genders)}"
    return True, None

def validate_age(dob):
    """Validate age (must be between 0 and 120)"""
    if not dob:
        return True, None  # Optional field
    
    try:
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year
        
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        if age < 0 or age > 120:
            return False, "Age must be between 0 and 120"
        
        return True, None
    except:
        return False, "Invalid date of birth"

def validate_password(password):
    """Validate password strength"""
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None

def validate_medicine_dosage(dosage):
    """Validate medicine dosage format"""
    if not dosage:
        return False, "Dosage is required"
    
    pattern = r'^[\d.]+(mg|g|mcg|ml|l|IU|units?)$'
    if not re.match(pattern, dosage.lower()):
        return False, "Invalid dosage format. Example: 500mg, 1g, 5ml"
    
    return True, None

def validate_text_length(text, min_len=0, max_len=1000):
    """Validate text length"""
    if not text:
        return True, None  # Optional field
    
    if len(text) < min_len:
        return False, f"Text must be at least {min_len} characters"
    
    if len(text) > max_len:
        return False, f"Text must be at most {max_len} characters"
    
    return True, None

def validate_boolean(value):
    """Validate boolean value"""
    if value is None:
        return True, None
    
    if isinstance(value, bool):
        return True, None
    
    if isinstance(value, str):
        if value.lower() in ['true', 'false', '1', '0']:
            return True, None
    
    return False, "Value must be a boolean"

def validate_json_schema(data, schema):
    """Validate data against a JSON schema"""
    for key, rules in schema.items():
        if key not in data:
            if rules.get('required', False):
                return False, f"'{key}' is required"
            continue
        
        value = data[key]
        
        # Check type
        expected_type = rules.get('type')
        if expected_type:
            if expected_type == 'string' and not isinstance(value, str):
                return False, f"'{key}' must be a string"
            elif expected_type == 'number' and not isinstance(value, (int, float)):
                return False, f"'{key}' must be a number"
            elif expected_type == 'boolean' and not isinstance(value, bool):
                return False, f"'{key}' must be a boolean"
            elif expected_type == 'array' and not isinstance(value, list):
                return False, f"'{key}' must be an array"
            elif expected_type == 'object' and not isinstance(value, dict):
                return False, f"'{key}' must be an object"
        
        # Check min value
        min_val = rules.get('min')
        if min_val is not None:
            if expected_type == 'number' and value < min_val:
                return False, f"'{key}' must be at least {min_val}"
            elif expected_type == 'string' and len(value) < min_val:
                return False, f"'{key}' must be at least {min_val} characters"
        
        # Check max value
        max_val = rules.get('max')
        if max_val is not None:
            if expected_type == 'number' and value > max_val:
                return False, f"'{key}' must be at most {max_val}"
            elif expected_type == 'string' and len(value) > max_val:
                return False, f"'{key}' must be at most {max_val} characters"
    
    return True, None