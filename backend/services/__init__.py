# Services package
try:
    from dataset_loader import DatasetLoader, get_dataset_loader
except ImportError:
    pass

try:
    from llm_service import LLMService
except ImportError:
    class LLMService:
        def __init__(self):
            pass
        def generate_response(self, *args, **kwargs):
            return "LLM service not configured"

try:
    from weather_service import WeatherService
except ImportError:
    class WeatherService:
        def __init__(self):
            pass

try:
    from maps_service import MapsService
except ImportError:
    class MapsService:
        def __init__(self):
            pass

try:
    from openfda_service import OpenFDAService
except ImportError:
    class OpenFDAService:
        def __init__(self):
            pass

try:
    from notification_service import NotificationService
except ImportError:
    class NotificationService:
        def __init__(self):
            pass

__all__ = [
    "DatasetLoader",
    "get_dataset_loader",
    "LLMService",
    "WeatherService",
    "MapsService",
    "OpenFDAService",
    "NotificationService"
]
