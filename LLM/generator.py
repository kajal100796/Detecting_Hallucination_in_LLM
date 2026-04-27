from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, context):
    """
    Returns ONLY a direct, concise answer
    """

    prompt = f"""
You are an AI assistant in a RAG system.

Answer the question using the given context.

Rules:
- Give ONLY the direct answer
- Be concise and precise (2–4 lines max)
- Do NOT explain unless necessary
- Do NOT add headings or bullet points
- Do NOT say "based on context"
- Do NOT hallucinate

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You give short, precise answers."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,   # lower = more direct
            max_tokens=150
        )

        answer = response.choices[0].message.content.strip()

        # Clean formatting
        answer = answer.replace("Answer:", "").strip()

        # Fallback
        if not answer or len(answer) < 5:
            return "Insufficient context for grounding"

        return answer

    except Exception as e:
        return f"Error during generation: {str(e)}"
