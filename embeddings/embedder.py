from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        
    def embed_chunks(self, chunks):
        """
        Takes a list of text chunks and returns their vector embeddings.
        """
        if not chunks:
            return []
        print(f"Generating embeddings for {len(chunks)} chunks...")
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        return embeddings

    def embed_query(self, query):
        """
        Takes a single query string and returns its vector embedding.
        """
        return self.model.encode([query])[0]
