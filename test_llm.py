from LLM.generator import generate_answer

question = "What is AI?"
context = "Artificial Intelligence is the simulation of human intelligence in machines."

result = generate_answer(question, context)

print("Generated Answer:\n")
print(result)