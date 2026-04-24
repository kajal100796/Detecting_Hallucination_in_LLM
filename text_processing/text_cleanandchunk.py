"""
Module: Text Extractor
Purpose: Extract text from PDF files
"""

import re

def clean_text(text):
    """Removing messy whitespaces."""
    text = re.sub(r'\s+', ' ', text) # Merge multiple spaces/newlines
    return text.strip()

def chunk_text(text, max_chars=1000, overlap=200):
    """Slicing text into large 1000-char blocks with overlap."""
    cleaned = clean_text(text)
    chunks = []
    current_pos = 0
    
    while current_pos < len(cleaned):
        end_pos = min(current_pos + max_chars, len(cleaned))
        
        # Grab the chunk
        chunk = cleaned[current_pos:end_pos]
        
        # finding a logical break
        if end_pos < len(cleaned):
            last_space = chunk.rfind(" ")
            if last_space != -1:
                end_pos = current_pos + last_space
                chunk = cleaned[current_pos:end_pos]

        chunks.append(chunk.strip())
        current_pos += (len(chunk) - overlap)
        
    return chunks
