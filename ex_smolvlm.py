import requests
import json
import os
import base64
import time


path = os.getcwd() #introduce the path of the directory

l_images = [file for file in os.listdir(path) if file.endswith((".png",".jpg"))]


def image_to_base64(im):
    """
    Encodes an image to base64.
    Params:
        im: name of the image
    Returns:
        str of the image encoded in base64
    """
    with open(im, "rb") as image:
        image_bin = image.read()
    image_base64 = base64.b64encode(image_bin).decode("utf-8")
    return image_base64


l_images_base64 = list(map(image_to_base64,l_images))



ip_vllm = os.getenv('MY_URL','http://localhost:8000') #url declared as an env var, if empty, takes localhost:8000 by default

model = os.getenv('MY_MODEL','HuggingfaceTB/SmolVLM-256M-Instruct') #model declared as an env var

url= ip_vllm + '/v1/chat/completions'



def make_a_payload(image_base64):
    """
    Given an encoded image, makes a payload in json format
    """
    image_json = "data:image/jpg;base64," + image_base64
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
                "image": image_json
            }
        ],
        "max_tokens": 50
    }

    return payload


l_payload = list(map(make_a_payload,l_images_base64))



#Then we make the requests

headers = {
    "Content-Type": "application/json"
}

for payload in l_payload:
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Answer:", response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")

    time.sleep(60)

