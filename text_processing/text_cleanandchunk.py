"""
Module: Text Extractor
Purpose: Extract text from PDF files
"""
import re

def chunk_text(text, max_chars=1000, overlap=200):
    # Basic Cleaning
    text = re.sub(r'\s+', ' ', text).strip()
    
    if not text:
        return []

    if overlap >= max_chars:
        overlap = max_chars // 2 

    chunks = []
    start = 0
    
    # Step 2: The "Moving Window" Loop
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk)
        
     
        step = max_chars - overlap
        start += max(step, 1) 
        
    return chunks