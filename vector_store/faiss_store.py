import faiss
import numpy as np

class FAISSStore:
    def __init__(self, embedding_dim):
        self.embedding_dim = embedding_dim
        # Using IndexFlatL2 for exact search (L2 distance)
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.chunks = []
        
    def add_embeddings(self, embeddings, chunks):
        """
        Adds vector embeddings and their corresponding text chunks to the store.
        """
        if len(embeddings) == 0:
            return
            
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        self.chunks.extend(chunks)
        print(f"Added {len(chunks)} chunks to FAISS index. Total: {self.index.ntotal}")
        
    def search(self, query_embedding, k=3):
        """
        Searches the FAISS index for the top k most similar chunks to the query embedding.
        Returns a list of matching chunks.
        """
        if self.index.ntotal == 0:
            print("Warning: FAISS index is empty.")
            return []
            
        query_vector = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1 and idx < len(self.chunks):
                results.append(self.chunks[idx])
                
        return results
