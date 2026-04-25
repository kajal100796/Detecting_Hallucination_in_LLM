
def build_prompt(question, context):
    """
    Constructs a structured prompt for RAG to minimize hallucinations.
    """
    
    # Clean whitespace to ensure the prompt structure remains crisp
    context = context.strip()
    question = question.strip()

    return f"""
### SYSTEM INSTRUCTIONS ###
You are a precise Information Extraction Assistant. Your sole purpose is to answer questions based strictly on the provided Context.

### STRICT RULES ###
1. Use ONLY the information provided in the "CONTEXT" section below.
2. If the answer is not explicitly stated in the Context, you must respond with: "Not available in context."
3. Do NOT use any outside knowledge, personal opinions, or pre-trained facts.
4. Do NOT attempt to be "helpful" by making up details that aren't there.

### CONTEXT ###
{context}

### USER QUESTION ###
{question}

### FINAL ANSWER ###
"""