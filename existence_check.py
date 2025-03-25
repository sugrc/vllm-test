import requests
import os
import base64
import logging

def existence_check(object: str, image_file: str) -> bool:
    """
    Checks the existence of the given object in the image
    """
    try:
        with open(image, "rb") as image:
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
                    "content": question,
                    "image": image_json
                }
            ],
            "max_tokens": 1
        }

        headers = {
            "Content-Type": "application/json"
        
}       response = requests.post(url, json=payload, headers=headers)
        logging.info("Request sent")

        if response.status_code == 200:
            print("Answer:", response.json())
            # return checks if the response is either 'yes' or 'no'
        else:
            print(f"Error: {response.status_code}, {response.text}")


    except Exception as e:
        print(e)

