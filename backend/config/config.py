import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database - Use SQLite for now (no PostgreSQL needed)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///nexusmed.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # File uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    
    # LLM Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # External APIs
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    MAPS_API_KEY = os.getenv('MAPS_API_KEY', '')
    
    # Dataset paths
    DATASET_PATH = os.getenv('DATASET_PATH', 'C:/Users/nitin/OneDrive/Documents/Desktop/datasets')
    
    # Model configurations
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    
    # Redis caching (optional)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TTL = 3600
    
    # SocketIO
    SOCKETIO_CORS_ALLOWED_ORIGINS = '*'
