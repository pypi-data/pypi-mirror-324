import requests
import json

def get_local_models():
    models = []
    response = requests.get("http://localhost:11434/api/tags")
    response.raise_for_status()
    for model in response.json()["models"]:
        models.append(model["name"])
    return models

def call_llm_chat_local(model: str, temperature: float, user_prompt: str, system_prompt: str = "", stream: bool = False):
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}],
        "stream": stream,
        "options": {
            "temperature": temperature,
        }
    }
    
    if stream:
        response = requests.post("http://localhost:11434/api/chat", json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if chunk["done"]:
                    break
                yield chunk["message"]["content"]
    else:
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        return response.json()["message"]["content"]