import requests
import os
import base64
import logging
import argparse

logging.basicConfig(level=logging.INFO)


path = '/app/images'
logging.info("Path")

list_images = [file for file in os.listdir(path) if file.endswith((".jpg"))]
logging.info("List of images")


def image_to_base64(image):
    """
    Encodes an image to base64.
    Params:
        image: name of the image
    Returns:
        string of the image encoded in base64
    """
    try:
        with open(image, "rb") as image:
            image_bin = image.read()
        image_base64 = base64.b64encode(image_bin).decode("utf-8")
        return image_base64
    except Exception as e:
        print(e)

list_images_base64 = list(map(image_to_base64,list_images))
logging.info("List of encoded images")



ip_vllm = os.getenv('IP','http://vllm:8000') 

model = os.getenv('MODEL','HuggingfaceTB/SmolVLM-256M-Instruct')

url= ip_vllm + '/v1/chat/completions'



def make_a_payload(image_base64):
    """
    Given an encoded image, makes a payload in json format
    """
    image_json = "data:image/jpg;base64," + str(image_base64)
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


list_payload = list(map(make_a_payload,list_images_base64))
logging.info("List of payload")



#Then we make the requests

headers = {
    "Content-Type": "application/json"
}

for payload in list_payload:
    response = requests.post(url, json=payload, headers=headers)
    logging.info("Request sent")

    if response.status_code == 200:
        print("Answer:", response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")

