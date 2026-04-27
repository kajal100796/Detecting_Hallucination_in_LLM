from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_chunks(self, chunks):
        """Generate embeddings for document chunks."""
        if not chunks:
            return np.array([])

        print(f"Generating embeddings for {len(chunks)} chunks...")
        embeddings = self.model.encode(chunks)

        return np.array(embeddings, dtype='float32')

    def embed_query(self, query):
        """Generate embedding for query."""
        embedding = self.model.encode([query])[0]
        return np.array(embedding, dtype='float32')
