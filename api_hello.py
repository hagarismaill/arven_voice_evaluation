import requests

r = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={
        "model": "llama3.1:8b",
        "prompt": "Say hello in one sentence.",
        "stream": False,
    },
    timeout=3600,
)
r.raise_for_status()
print(r.json()["response"])