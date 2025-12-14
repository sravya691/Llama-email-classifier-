import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def classify_email(prompt: str, model: str, temperature: float) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "options": {
            "temperature": temperature
        },
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"]
