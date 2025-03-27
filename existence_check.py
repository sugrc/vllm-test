import requests
import os
import base64
import logging

logging.basicConfig(level=logging.INFO)


def existence_check(object: str, image_file: str):
    """
    Checks the existence of the given object in the image
    """
    try:
        with open(image_file, "rb") as image:
            image_bin = image.read()
        image_base64 = base64.b64encode(image_bin).decode("utf-8")
        
        ip_vllm = os.getenv('IP','http://vllm:8000') 
        model = os.getenv('MODEL','HuggingfaceTB/SmolVLM-256M-Instruct')
        url= ip_vllm + '/v1/chat/completions'

        question = "Is " + object + " in the image?"

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
                    "content": "Describe this image",
                    "image": image_json
                }
            ],
            "max_tokens": 1
        }

        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        logging.info("Request sent")

        if response.status_code == 200:
            print("Answer:", response.json())
            # return checks if the response is either 'yes' or 'no'
        else:
            print(f"Error: {response.status_code}, {response.text}")


    except Exception as e:
        print(e)


path = os.getcwd()
logging.info("Path: %s", path)

image_path = path + '/images/star.jpg'
logging.info("Image path: %s", image_path)

existence_check("star", image_path)


"""
The response has this format:
Answer: {'id': 'chatcmpl-91684fc3ece941fe8a9fd3d50be34ad0',
 'object': 'chat.completion', 
 'created': 1742912756, 
 'model': 'HuggingfaceTB/SmolVLM-256M-Instruct', 
 'choices': [{'index': 0, 
    'message': {'role': 'assistant', 
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

"""