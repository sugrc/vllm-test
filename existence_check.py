import requests
import os
import base64
import logging
import argparse

logging.basicConfig(level=logging.INFO)




ip_vllm = os.getenv('IP','http://vllm:8000') 

model = os.getenv('MODEL','HuggingfaceTB/SmolVLM-256M-Instruct')

url= ip_vllm + '/v1/chat/completions'

headers = {
    "Content-Type": "application/json"
}


# --- FUNCTIONS ---

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


def query_vlm(image, prompt):
    """
    Given an image, makes a payload in json format
    Params:
        image: name of the image
        prompt: what to analize in the image
    Returns: 
        payload in json format
    """
    image_base64 = image_to_base64(image)
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
                "content": prompt,
                "image": image_json
            }
        ],
        "max_tokens": 50
    }
    return payload


def existence_check(object, image):
    """
    Checks the existence of a given object in a given image.
    Params:
        object: object to be checked
        image: image to be analized
    Returns:
        True if the object is in the image, False if not.
    """
    prompt = "Is there " + str(object) + " in the image?"
    payload = query_vlm(image, prompt)
    response = requests.post(url, json=payload, headers=headers)
    logging.info("Request sent for: %s", image)
    logging.info("Payload sent: %s", payload)
    logging.info("URL: %s", url)
    if response.status_code == 200:
        logging.info("Answer: %s", response.json())
        content = response.json()
        answer = content['choices'][0]['message']['content']
        logging.info("Content: %s", str(content))
        if ("yes" or "Yes") in answer:
            return True
        else: 
            return False
    else:
        logging.error("Error: %s, %s", response.status_code, response.text)


def main():
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

    for image in list_images:
        existence_check(object, image)
        logging.info("Bool for %s: %s ", image, existence_check(object,image))


if __name__ == "__main__":
    main()