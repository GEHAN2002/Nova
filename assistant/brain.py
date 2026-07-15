import ollama

MODEL = "llama3.2:3b"

def ask_nova(prompt):
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Nova, a helpful AI assistant. "
                        "Be concise, friendly, and helpful."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]
    except Exception as error:
        print(f"Local AI unavailable: {error}")
        return "My local AI is not running. Start Ollama and install llama3.2:3b, or use a built-in command."
