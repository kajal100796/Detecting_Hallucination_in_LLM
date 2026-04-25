import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the model and tokenizer
model_id = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

def generate_answer(question, context):
    """
    Generates an answer with strict extraction instructions to 
    prevent the model from missing data at the bottom of the context.
    """
    # IMPROVED PROMPT: Using 'Background:' and 'Question:' helps T5 focus.
    # We explicitly tell it to look at the WHOLE text.
    prompt = (
    f"Background: {context}\n\n"
    f"Task: Using ONLY the labels provided in the Background, answer the question. "
    f"Do not use outside knowledge. If the answer is not a direct word-for-word match, say 'I do not know'.\n\n"
    f"Question: {question}\n"
    f"Answer:"
)
    
    try:
        # Tokenize the input
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

        with torch.no_grad():
            output_tokens = model.generate(
                **inputs, 
                max_new_tokens=30,     # Slightly increased to allow for full phrase extraction
                do_sample=False,        # Stay deterministic
                num_beams=4,            # Increased beams to help find the best path in long context
                no_repeat_ngram_size=2
            )

        # Decode the answer
        answer = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
        
        # --- ARTIFACT CLEANING ---
        # Removes common Flan-T5 glitches like (i), (ii), or repeating the question
        junk_list = ["(ii)", "(i)", "(iii)", "Answer:", "Question:", "Background:"]
        for junk in junk_list:
            answer = answer.replace(junk, "")
        
        answer = answer.strip()

        # --- DATA EXTRACTION LOGIC ---
        # If the model gives a list, we take the first few relevant parts.
        if "," in answer:
            parts = answer.split(',')
            if len(parts) >= 2:
                # Joining only the first two items keeps the UI clean for Ayushi
                answer = f"{parts[0].strip()}, {parts[1].strip()}"
        
        # FINAL GUARDRAIL:
        # If the model gives a 1-2 word answer that is just punctuation, or is empty
        if len(answer) < 2 or answer.lower() in ["none", "n/a"]:
            return "I do not know"
        
        return answer

    except Exception as e:
        return f"Error during generation: {e}"