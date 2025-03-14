import requests
import json
import os

url = os.getenv('MY_URL','http://localhost:8000/v1/chat/completions') #url declared as an env var, if empty, takes that url by default

model = os.getenv('MY_MODEL','HuggingfaceTB/SmolVLM-256M-Instruct') #model declared as an env var

payload = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": "You are a vision-language model."
        },
        {
            "role": "user",
            "content": "Describe this image.",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/wcAAwAB/edwMjcAAAAASUVORK5CYII="
        }
    ],
    "max_tokens": 50
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    print("Answer:", response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
