import numpy as np
from sentence_transformers import SentenceTransformer
from config.config import Config
import logging
import os

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.documents = []
        self.embeddings = []
        self._load_documents()
        
    def _load_documents(self):
        """Load medical documents for RAG"""
        try:
            # Load from dataset
            doc_path = os.path.join(Config.DATASET_PATH, 'medical_knowledge.txt')
            if os.path.exists(doc_path):
                with open(doc_path, 'r', encoding='utf-8') as f:
                    self.documents = f.read().split('\n\n')
            else:
                # Use default medical knowledge
                self.documents = [
                    "Common cold is a viral infection of the upper respiratory tract.",
                    "Hypertension is high blood pressure that can lead to heart disease.",
                    "Diabetes is a condition where blood sugar levels are too high.",
                    "Asthma is a chronic lung condition that causes breathing difficulties.",
                    "Allergies are immune system reactions to harmless substances."
                ]
            
            # Generate embeddings
            self.embeddings = self.model.encode(self.documents)
            logger.info(f"Loaded {len(self.documents)} documents for RAG")
        except Exception as e:
            logger.error(f"RAG document loading error: {e}")
    
    def retrieve(self, query, top_k=5):
        """Retrieve relevant documents for a query"""
        try:
            query_embedding = self.model.encode([query])[0]
            
            # Calculate similarities
            similarities = np.dot(self.embeddings, query_embedding) / (
                np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Get top k
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = [self.documents[i] for i in top_indices]
            return results
        except Exception as e:
            logger.error(f"RAG retrieval error: {e}")
            return []