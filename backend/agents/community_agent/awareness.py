from services.llm_service import LLMService
from services.dataset_loader import DatasetLoader
import logging

logger = logging.getLogger(__name__)

class HealthAwareness:
    def __init__(self):
        self.llm = LLMService()
        self.dataset = DatasetLoader()
        self.topics = [
            'Common cold prevention',
            'Heart health',
            'Diabetes management',
            'Mental health awareness',
            'Nutrition and diet',
            'Exercise and fitness',
            'Vaccination importance',
            'Cancer screening',
            'Asthma care',
            'Allergy management',
            'Stress management',
            'Sleep hygiene',
            'First aid',
            'Pregnancy care',
            'Senior health'
        ]
        
    def get_content(self, topic):
        """Get health awareness content for a topic"""
        try:
            # Check dataset first
            awareness_data = self.dataset.load_health_awareness_dataset()
            
            if awareness_data:
                for item in awareness_data:
                    if topic.lower() in item.get('topic', '').lower():
                        return item
            
            # Generate using LLM if not in dataset
            content = self.llm.health_awareness(topic)
            
            return {
                'topic': topic,
                'content': content,
                'source': 'ai-generated',
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Awareness content error: {e}")
            return {
                'topic': topic,
                'content': 'Content not available at the moment.',
                'source': 'error'
            }
    
    def get_recommended_topics(self, user_profile):
        """Get recommended awareness topics based on user profile"""
        recommendations = []
        
        if user_profile:
            # Age-based recommendations
            if user_profile.get('age', 0) > 50:
                recommendations.extend(['Heart health', 'Cancer screening', 'Senior health'])
            
            if user_profile.get('blood_group') in ['A+', 'B+']:
                recommendations.append('Nutrition and diet')
            
            if user_profile.get('allergies'):
                recommendations.append('Allergy management')
            
            if user_profile.get('chronic_conditions'):
                if 'diabetes' in user_profile.get('chronic_conditions', '').lower():
                    recommendations.append('Diabetes management')
                if 'asthma' in user_profile.get('chronic_conditions', '').lower():
                    recommendations.append('Asthma care')
        
        # Add general topics if no specific recommendations
        if not recommendations:
            recommendations = ['Common cold prevention', 'Mental health awareness', 'Nutrition and diet']
        
        return recommendations[:5]
    
    def create_summary(self, topic, content):
        """Create a summary of awareness content"""
        try:
            summary_prompt = f"""
            Create a concise summary of the following health awareness content:
            
            Topic: {topic}
            Content: {content}
            
            Summary should be easy to read and understand.
            """
            
            summary = self.llm.generate_response(summary_prompt)
            return summary
        except Exception as e:
            logger.error(f"Summary creation error: {e}")
            return content[:500] + '...' if len(content) > 500 else content