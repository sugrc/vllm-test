import requests
import os
import base64
import logging
import argparse

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument(
    '--path',
    type=str,
    required=True
)

args = parser.parse_args()

path = args.path
logging.info("Path: %s", path)

#path = '/app/images'
#logging.info("Path: %s", path)

list_images = [file for file in os.listdir(path) if file.endswith((".jpg"))]
logging.info("List of images: %s", list_images)


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
logging.info("List of encoded images: %s",list_images_base64)



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


image_counter=0 #counter to show which image

for payload in list_payload:
    response = requests.post(url, json=payload, headers=headers)
    logging.info("Request sent for file: %s",list_images[image_counter])
    logging.info("Payload sent: %s", payload)
    logging.info("URL: %s", url)
    image_counter +=1
    if response.status_code == 200:
        logging.info("Answer: %s", response.json())
    else:
        logging.error("Error: %s, %s", response.status_code, response.text)
