import requests
import json

def generate_answer(question, context):
    """
    Sends a request to the local Ollama server to generate a grounded answer.
    If the context is missing information, it returns a technical refusal.
    """
    url = "http://localhost:11434/api/generate"
    
    # We define a strict prompt to ensure the model doesn't over-explain
    prompt = (
        f"Context: {context}\n\n"
        f"Task: Using the provided context, answer the question accurately. "
        f"Be concise. If the specific information is not present in the context, "
        f"reply with exactly: 'Insufficient context for grounding'.\n\n"
        f"Question: {question}\n"
        f"Answer:"
    )

    data = {
        "model": "llama3", 
        "prompt": prompt,
        "stream": False     # Set to False to get the full response at once
    }

    try:
        # Send request to Ollama local server
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Extract response text
        answer = result.get("response", "").strip()

        # Artifact Cleaning (Removing structural noise)
        answer = answer.replace("Answer:", "").replace("Question:", "").strip()

        # --- TECHNICAL GROUNDING CHECK ---
        # If the model gives an empty string or a generic refusal, use your technical term
        refusal_triggers = ["i do not know", "not mentioned", "not found", "i'm sorry"]
        
        if not answer or any(trigger in answer.lower() for trigger in refusal_triggers):
            return "Insufficient context for grounding"
            
        return answer

    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Please start Ollama and run 'ollama run llama3'."
    except Exception as e:
        return f"Error during generation: {e}"