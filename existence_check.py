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
parser.add_argument(
    '--object',
    type=str,
    required=True
)
args = parser.parse_args()


path = args.path
logging.info("Path: %s", path)

object = args.object
logging.info("Object: %s", object)


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
    question = "Is there " + str(object) + " in the image?"
    logging.info("Question: %s", question)
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
                "content": str(question),
                "image": image_json
            }
        ],
        "max_tokens": 50
    }

    return payload


list_payload = list(map(make_a_payload,list_images_base64))
logging.info("List of payload")


headers = {
    "Content-Type": "application/json"
}


def existence_check(answer):
    if ("yes" or "Yes") in answer:
        return True
    else: 
        return False

image_counter=0 #counter to show which image

for payload in list_payload:
    response = requests.post(url, json=payload, headers=headers)
    logging.info("Request sent for file: %s",list_images[image_counter])
    logging.info("Payload sent: %s", payload)
    logging.info("URL: %s", url)
    image_counter +=1
    if response.status_code == 200:
        logging.info("Answer: %s", response.json())
        content = response.json()
        logging.info(type(content))
        answer = content['choices'][0]['message']['content']
        bool_answer = existence_check(answer)
        logging.info(bool_answer)
        logging.info("Content: %s", str(content))
    else:
        logging.error("Error: %s, %s", response.status_code, response.text)



"""
The response has this format:
Answer: {'id': 'chatcmpl-91684fc3ece941fe8a9fd3d50be34ad0',
 'object': 'chat.completion', 
 'created': 1742912756, 
 'model': 'HuggingfaceTB/SmolVLM-256M-Instruct', 
 'choices': [{'index': 0, 
    'message': 
        {'role': 'assistant', 
        'reasoning_content': None, 
        'content': '<RESPONSE>', 
        'tool_calls': []}, 
    'logprobs': None, 
    'finish_reason': 'length', 
    'stop_reason': None}], 
'usage': {'prompt_tokens': 24, 
'total_tokens': 74, 
'completion_tokens': 50, 
'prompt_tokens_details': None}, 
'prompt_logprobs': None}

So, it is a dictionary. To access to the message we c

"""