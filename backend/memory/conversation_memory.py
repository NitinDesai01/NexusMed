from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class ConversationMemory:
    def __init__(self, max_messages=50):
        self.conversations = {}
        self.max_messages = max_messages
        
    def add_message(self, session_id, role, content):
        """Add a message to conversation history"""
        try:
            if session_id not in self.conversations:
                self.conversations[session_id] = []
            
            message = {
                'role': role,
                'content': content,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.conversations[session_id].append(message)
            
            # Keep only last N messages
            if len(self.conversations[session_id]) > self.max_messages:
                self.conversations[session_id] = \
                    self.conversations[session_id][-self.max_messages:]
            
            return True
            
        except Exception as e:
            logger.error(f"Add message error: {e}")
            return False
    
    def get_conversation(self, session_id, limit=None):
        """Get conversation history"""
        if session_id not in self.conversations:
            return []
        
        messages = self.conversations[session_id]
        
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def get_context(self, session_id, max_messages=10):
        """Get conversation context for LLM"""
        messages = self.get_conversation(session_id, max_messages)
        
        if not messages:
            return ""
        
        context = ""
        for msg in messages:
            context += f"{msg['role']}: {msg['content']}\n"
        
        return context
    
    def clear_conversation(self, session_id):
        """Clear conversation history"""
        if session_id in self.conversations:
            self.conversations[session_id] = []
            return True
        return False
    
    def summarize_conversation(self, session_id):
        """Summarize conversation"""
        messages = self.get_conversation(session_id)
        
        if not messages:
            return "No conversation history"
        
        # Extract key points
        user_messages = [msg for msg in messages if msg['role'] == 'user']
        bot_messages = [msg for msg in messages if msg['role'] == 'assistant']
        
        summary = {
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'bot_messages': len(bot_messages),
            'time_range': {
                'start': messages[0]['timestamp'] if messages else None,
                'end': messages[-1]['timestamp'] if messages else None
            },
            'key_topics': self._extract_topics(messages)
        }
        
        return summary
    
    def _extract_topics(self, messages):
        """Extract key topics from conversation"""
        topics = []
        keywords = ['symptom', 'medicine', 'doctor', 'hospital', 'pain', 
                   'condition', 'treatment', 'emergency', 'health']
        
        for msg in messages:
            content = msg['content'].lower()
            for keyword in keywords:
                if keyword in content and keyword not in topics:
                    topics.append(keyword)
        
        return topics[:5]  # Return top 5 topics
    
    def get_conversation_stats(self):
        """Get conversation statistics"""
        stats = {
            'total_conversations': len(self.conversations),
            'total_messages': sum(len(messages) for messages in self.conversations.values()),
            'sessions': []
        }
        
        for session_id, messages in self.conversations.items():
            stats['sessions'].append({
                'session_id': session_id,
                'message_count': len(messages),
                'last_message': messages[-1]['timestamp'] if messages else None
            })
        
        return stats