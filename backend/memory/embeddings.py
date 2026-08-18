import numpy as np
from sentence_transformers import SentenceTransformer
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.model_name = Config.EMBEDDING_MODEL
        
    def encode(self, texts, batch_size=32):
        """Generate embeddings for texts"""
        try:
            if isinstance(texts, str):
                texts = [texts]
            
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=False
            )
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            return None
    
    def encode_query(self, query):
        """Encode a query string"""
        return self.encode(query)[0]
    
    def similarity(self, embedding1, embedding2):
        """Calculate cosine similarity between two embeddings"""
        try:
            # Normalize embeddings
            norm1 = embedding1 / np.linalg.norm(embedding1)
            norm2 = embedding2 / np.linalg.norm(embedding2)
            
            # Calculate cosine similarity
            similarity = np.dot(norm1, norm2)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Similarity calculation error: {e}")
            return 0.0
    
    def find_most_similar(self, query_embedding, embeddings, top_k=5):
        """Find most similar embeddings"""
        try:
            # Normalize query
            query_norm = query_embedding / np.linalg.norm(query_embedding)
            
            # Normalize all embeddings
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            normalized = embeddings / norms
            
            # Calculate similarities
            similarities = np.dot(normalized, query_norm)
            
            # Get top k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = [
                {
                    'index': idx,
                    'similarity': float(similarities[idx])
                }
                for idx in top_indices
            ]
            
            return results
            
        except Exception as e:
            logger.error(f"Find similar error: {e}")
            return []
    
    def get_model_info(self):
        """Get embedding model information"""
        return {
            'model_name': self.model_name,
            'max_sequence_length': self.model.max_seq_length,
            'embedding_dimension': self.model.get_sentence_embedding_dimension()
        }