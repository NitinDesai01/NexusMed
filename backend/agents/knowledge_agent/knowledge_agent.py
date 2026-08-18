import logging

logger = logging.getLogger(__name__)

class KnowledgeAgent:
    def __init__(self):
        pass
        
    def query(self, question):
        return {"answer": f"Answer to: {question}", "sources": [], "confidence": "high"}
