import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"  # Make sure this matches your installed model

def ask_llm(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        print("Ollama response:", data)  # For debugging
        return data.get("response", "").strip()
    except Exception as e:
        print("Error calling Ollama:", e)
        return f"Error: {e}"