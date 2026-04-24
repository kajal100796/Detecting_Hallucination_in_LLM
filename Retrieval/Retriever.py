from sentence_transformers import SentenceTransformer

# Load same model used in embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query, index, chunks, top_k=3):
    """
    Retrieve top_k most relevant chunks for a query
    """
    
    # Step 1: Convert query → embedding
    query_vector = model.encode([query])
    
    # Step 2: Search in FAISS index
    distances, indices = index.search(query_vector, top_k)
    
    # Step 3: Get actual chunks
    results = []
    for i in indices[0]:
        results.append(chunks[i])
    
    return results