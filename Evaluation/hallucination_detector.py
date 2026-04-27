from groq import Groq
from dotenv import load_dotenv
import os
import re

# Load API key
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def detect_hallucination(question, context, answer):
    """
    Detects whether the answer is grounded in context.

    Returns:
    - confidence_score (0 to 1)
    - label (Grounded / Partially Grounded / Hallucinated)
    """

    prompt = f"""
You are a strict evaluator in a Retrieval-Augmented Generation (RAG) system.

Your task is to verify whether the answer is supported by the context.

Rules:
- YES → Fully supported by context
- PARTIAL → Some parts supported
- NO → Not supported (hallucination)

Do NOT assume missing information.

Context:
{context}

Question:
{question}

Answer:
{answer}

Output STRICTLY:
Label: YES / PARTIAL / NO
Confidence: <number between 0 and 1>
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a strict factual evaluator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=100
        )

        output = response.choices[0].message.content.strip()

        # --- PARSE OUTPUT ---
        label_match = re.search(r"(YES|PARTIAL|NO)", output, re.IGNORECASE)
        conf_match = re.search(r"(0(\.\d+)?|1(\.0+)?)", output)

        label = label_match.group(1).upper() if label_match else "NO"
        confidence = float(conf_match.group(1)) if conf_match else 0.0

        # --- MAP LABEL ---
        if label == "YES":
            final_label = "Grounded"
            confidence = max(confidence, 0.8)
        elif label == "PARTIAL":
            final_label = "Partially Grounded"
            confidence = min(max(confidence, 0.4), 0.79)
        else:
            final_label = "Hallucinated"
            confidence = min(confidence, 0.39)

        return {
            "confidence_score": round(confidence, 2),
            "label": final_label,
            "raw_output": output
        }

    except Exception as e:
        return {
            "confidence_score": 0.0,
            "label": "Error",
            "raw_output": str(e)
        }
