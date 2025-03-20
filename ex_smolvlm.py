import requests
import json
import os
import base64

path = os.getcwd()

image_name = "star.jpg" #introduce name of the image

image_path = os.path.join(path, image_name)

with open(image_path, "rb") as image:
    image_bin = image.read()

image_base64 = base64.b64encode(image_bin).decode("utf-8")

ip_vllm = os.getenv('MY_URL','http://localhost:8000') #url declared as an env var, if empty, takes localhost:8000 by default

model = os.getenv('MY_MODEL','HuggingfaceTB/SmolVLM-256M-Instruct') #model declared as an env var

url= ip_vllm + '/v1/chat/completions'

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
            "image": image_base64
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
