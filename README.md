🧠 RAG Hallucination Detection
📌 Overview

This project detects whether an LLM-generated answer is grounded in context or a hallucination.

It uses LLM in two roles:

Generator → generates answer
Evaluator (LLM-as-a-Judge) → verifies answer

⚙️ Workflow
Input → Question
Retrieve → Context
Generate → Answer (LLM)
Evaluate → Check answer vs context
Output → Label + Confidence
🏷️ Output Labels
✅ Grounded
⚠️ Partially Grounded
❌ Hallucinated
