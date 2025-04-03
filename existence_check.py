import requests
import os
import base64
import logging
import argparse
import ast

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
        logging.error(e)
        raise e


def query_vlm(image, prompt):
    """
    Given an image, makes a payload in json format
    Params:
        image: name of the image
        prompt: what to analize in the image
    Returns: 
        payload in json format
    """
    try:
        image_base64 = image_to_base64(image)
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
        response = requests.post(url, json=payload, headers=headers)
        logging.info("Request sent for: %s", image)
        if response.status_code == 200:
            logging.info("Answer: %s", response.json())
            content = response.json()
            answer = content['choices'][0]['message']['content']
            return answer
        else:
            logging.error("Error: %s, %s", response.status_code, response.text)
    except Exception as e:
        logging.error(e)
        raise e


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
    answer = query_vlm(image, prompt)
    if ("yes" or "Yes") in answer:
        return True
    else: 
        return False
    
    
def visibility_check(attribute, image):
    """
    Checks the visibility of a given attribute in a given image.
    Params:
        attribute: attribute to be checked
        image: image to be analized
    Returns:
        True if the attribute is visible in the image, False if not.
    """
    prompt = "Can you see " + str(attribute) + " in the image?"
    answer = query_vlm(image, prompt)
    if ("yes" or "Yes") in answer:
        return True
    else: 
        return False
    
    
def description_match_check(attribute, description, image):
    """
    Checks if the given attribute matches the given description in the image
    Params:
        attribute: attribute to be checked
        description: description of the attribute
        image: image to be analized
    Returns:
        True if the object is in the image, False if not.
    """
    if visibility_check(attribute, image):
        prompt = "Is the " + str(attribute) + str(description) + " ?"
        answer = query_vlm(image, prompt)
        if ("yes" or "Yes") in answer:
            return True
        else: 
            return False
    return False


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
    parser.add_argument(
        '--attributes',
        type=str,
        required=True
    )
    args = parser.parse_args()

    path = args.path
    logging.info("Path: %s", path)

    object = args.object
    logging.info("Object: %s", object)

    attributes = ast.literal_eval(args.attributes)
    logging.info("Attributes: %s", attributes)
    logging.info("type of atributes: %s", type(attributes))

    list_images = [file for file in os.listdir(path) if file.endswith((".jpg"))]
    logging.info("List of images: %s", list_images)

    list_images_path =[]
    for each in list_images:
        image_path = path + "/" + each
        list_images_path.append(image_path)
    logging.info("List of images: %s", list_images_path)
    
    for image in list_images_path:
        if existence_check(object, image):
            logging.info("Existence check for %s: %s ", image, existence_check(object,image))     
            for attribute_pair in attributes:
                attribute = attribute_pair[0]
                logging.info('Attribute: %s', attribute)
                description = attribute_pair[1]
                logging.info('Description: %s', description)
                description_match_check(attribute, description, image)
                logging.info("Description match check for %s with attribute %s and description %s: %s ", 
                             image, 
                             attribute, 
                             description, 
                             description_match_check(attribute, description, image))


if __name__ == "__main__":
    main()