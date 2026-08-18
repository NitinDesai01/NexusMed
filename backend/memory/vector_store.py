import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config.config import Config
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = None
        self.documents = []
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self._initialize_index()
        
    def _initialize_index(self):
        """Initialize FAISS index"""
        try:
            self.index = faiss.IndexFlatL2(self.dimension)
            logger.info("Vector store initialized")
        except Exception as e:
            logger.error(f"Vector store initialization error: {e}")
            self.index = None
    
    def add_documents(self, documents):
        """Add documents to vector store"""
        try:
            if not self.index:
                self._initialize_index()
            
            if not documents:
                return False
            
            # Generate embeddings
            embeddings = self.model.encode(documents)
            
            # Add to index
            self.index.add(np.array(embeddings).astype('float32'))
            self.documents.extend(documents)
            
            logger.info(f"Added {len(documents)} documents to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Add documents error: {e}")
            return False
    
    def search(self, query, top_k=5):
        """Search for similar documents"""
        try:
            if not self.index or not self.documents:
                return []
            
            # Generate query embedding
            query_embedding = self.model.encode([query])
            
            # Search
            distances, indices = self.index.search(
                np.array(query_embedding).astype('float32'),
                min(top_k, len(self.documents))
            )
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'document': self.documents[idx],
                        'distance': float(distances[0][i])
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Vector search error: {e}")
            return []
    
    def save(self, path):
        """Save vector store to disk"""
        try:
            if not self.index:
                return False
            
            # Save FAISS index
            faiss.write_index(self.index, f"{path}.faiss")
            
            # Save documents
            with open(f"{path}_docs.pkl", 'wb') as f:
                pickle.dump(self.documents, f)
            
            logger.info(f"Vector store saved to {path}")
            return True
            
        except Exception as e:
            logger.error(f"Save vector store error: {e}")
            return False
    
    def load(self, path):
        """Load vector store from disk"""
        try:
            # Load FAISS index
            if os.path.exists(f"{path}.faiss"):
                self.index = faiss.read_index(f"{path}.faiss")
                
                # Load documents
                with open(f"{path}_docs.pkl", 'rb') as f:
                    self.documents = pickle.load(f)
                
                logger.info(f"Vector store loaded from {path}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Load vector store error: {e}")
            return False
    
    def clear(self):
        """Clear vector store"""
        self.index = None
        self.documents = []
        self._initialize_index()
        return True
    
    def get_stats(self):
        """Get vector store statistics"""
        return {
            'document_count': len(self.documents),
            'dimension': self.dimension,
            'index_type': type(self.index).__name__ if self.index else None
        }