import requests
from config.config import Config
import logging
import json

logger = logging.getLogger(__name__)

class MedicalSearch:
    def __init__(self):
        self.api_key = Config.GOOGLE_API_KEY if hasattr(Config, 'GOOGLE_API_KEY') else None
        self.search_engine_id = Config.SEARCH_ENGINE_ID if hasattr(Config, 'SEARCH_ENGINE_ID') else None
        
    def search_medical_terms(self, query, num_results=5):
        """Search for medical terms using Google Custom Search"""
        try:
            if not self.api_key or not self.search_engine_id:
                return self._search_fallback(query)
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': f"medical {query}",
                'num': num_results
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_search_results(data)
            else:
                return self._search_fallback(query)
                
        except Exception as e:
            logger.error(f"Search error: {e}")
            return self._search_fallback(query)
    
    def _search_fallback(self, query):
        """Fallback search when API is not available"""
        # Return canned results based on query
        fallback_results = {
            'diabetes': {
                'results': [
                    {'title': 'Diabetes Overview', 'snippet': 'Diabetes is a chronic condition affecting blood sugar...'},
                    {'title': 'Diabetes Treatment', 'snippet': 'Treatment includes medication, diet, and exercise...'}
                ]
            },
            'hypertension': {
                'results': [
                    {'title': 'High Blood Pressure', 'snippet': 'Hypertension is a common condition...'},
                    {'title': 'Managing Hypertension', 'snippet': 'Lifestyle changes and medication...'}
                ]
            }
        }
        
        query_lower = query.lower()
        for key, value in fallback_results.items():
            if key in query_lower:
                return value
        
        return {
            'results': [
                {'title': f'Information about {query}', 'snippet': f'Medical information about {query}...'}
            ]
        }
    
    def _format_search_results(self, data):
        """Format Google search results"""
        results = []
        
        if 'items' in data:
            for item in data['items'][:5]:
                results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', '')
                })
        
        return {'results': results}
    
    def search_pubmed(self, query, max_results=10):
        """Search PubMed for medical literature"""
        # In production, use PubMed API
        # For now, return empty results with a note
        return {
            'results': [],
            'message': 'PubMed search not configured. Please set up PubMed API access.'
        }
    
    def search_wikipedia(self, query):
        """Search Wikipedia for medical articles"""
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': f'medical {query}',
                'format': 'json',
                'srlimit': 3
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'query' in data and 'search' in data['query']:
                    return {
                        'results': [
                            {
                                'title': item['title'],
                                'snippet': item['snippet'],
                                'pageid': item['pageid']
                            }
                            for item in data['query']['search']
                        ]
                    }
            
            return {'results': []}
            
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            return {'results': []}