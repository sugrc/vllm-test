import requests
import os
import base64
import logging
import argparse
import ast

logging.basicConfig(level=logging.INFO)


ip_vllm = os.getenv("IP", "http://vllm:8000")

model = os.getenv("MODEL", "HuggingfaceTB/SmolVLM-256M-Instruct")

url = ip_vllm + "/v1/chat/completions"

headers = {"Content-Type": "application/json"}


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
                {"role": "system",
                 "content": "You are a vision-language model."},
                {"role": "user", "content": prompt, "image": image_json},
            ],
            "max_tokens": 50,
        }
        response = requests.post(url, json=payload, headers=headers)
        logging.info("Request sent for: %s", image)
        if response.status_code == 200:
            content = response.json()
            answer = content["choices"][0]["message"]["content"]
            logging.info("Answer: %s", answer)
            return answer
        else:
            logging.error("Error: %s, %s", response.status_code, response.text)
    except Exception as e:
        logging.error(e)
        raise e


def is_object_present_in_image(object, image):
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
    if "yes" in answer.lower():
        return True
    else:
        return False


def is_attribute_visible_in_image(attribute, image):
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
    if "yes" in answer.lower():
        return True
    else:
        return False


def does_attribute_match_description(attribute, description, image):
    """
    Checks if the given attribute matches the given description in the image
    Params:
        attribute: attribute to be checked
        description: description of the attribute
        image: image to be analized
    Returns:
        True if the object is in the image, False if not.
    """
    if is_attribute_visible_in_image(attribute, image):
        prompt = "Is the " + str(attribute) + str(description) + " ?"
        answer = query_vlm(image, prompt)
        if "yes" in answer.lower():
            return True
        else:
            return False
    return False


def is_entity_realistic_in_image(entity, image):
    """
    Checks the realism of a given entity in a given image.
    Params:
        entity: entity to be checked
        image: image to be analized
    Returns:
        True if the entity is realistic and natural, False if not.
    """
    prompt = "Is " + str(entity) + " realistic and natural in this image?"
    answer = query_vlm(image, prompt)
    if "yes" in answer.lower():
        return True
    else:
        return False


def relationship_check(entity_1, entity_2, relation, image):
    """
    ...
    Params:
        entity_1: entity to be checked
        entity_2:
        relation:
        image: image to be analized
    Returns:
        True if ..., False if not.
    """
    prompt = (
        "Is "
        + str(entity_1)
        + " "
        + str(relation)
        + " "
        + str(entity_2)
        + " in this image?"
    )
    answer = query_vlm(image, prompt)
    if "yes" in answer.lower():
        return True
    else:
        return False


def normalized_attribute_score_function(image, object, attributes):
    """
    Scores the given image
    Params:
        image: image
        object: object to be checked about
        attributes: list of lists with two elements ['attribute','description']
    Returns:
        Integer wich scores the image
    """
    confidence_score = 0
    realism_score = 0
    normalized_attribute_score = 0
    existence_check = is_object_present_in_image(object, image)
    if existence_check:
        logging.info(
            "Existence check for %s: %s ", image, existence_check)
        for attribute_pair in attributes:
            attribute = attribute_pair[0]
            logging.info("Attribute: %s", attribute)
            description = attribute_pair[1]
            logging.info("Description: %s", description)
            bool_visibility = is_attribute_visible_in_image(attribute, image)
            bool_description = does_attribute_match_description(attribute, description,
                                                       image)
            logging.info(
                "Description match check for %s with attribute %s "
                "and description %s: %s ",
                image,
                attribute,
                description,
                bool_description,
            )
            confidence_score += bool_visibility * 1
            realism_score += (bool_visibility * 1) * (bool_description * 1)
        logging.info("Confidence score is: %s", confidence_score)
        logging.info("Realism score is: %s", realism_score)
        if confidence_score > 0:
            normalized_attribute_score = realism_score / confidence_score
    return normalized_attribute_score


def relationship_score_function(image, relationships):
    """
    Scores the given image
    Params:
        image: image
        object: object to be checked about
        attributes: list of lists with two elements ['attribute','description']
    Returns:
        Integer wich scores the image
    """
    entities_vector = relationships[0]
    logging.info("Entities vector: %s", entities_vector)
    relationships_matrix = relationships[1]
    logging.info("Relationship matrix: %s", relationships_matrix)
    visibility_check_vector = list(
        map(lambda x: is_attribute_visible_in_image(x, image), entities_vector)
    )
    logging.info("Visibility check vector: %s", visibility_check_vector)
    realism_check_vector = list(map(lambda x: is_entity_realistic_in_image(x, image),
                                    entities_vector))
    logging.info("Realism check vector: %s", realism_check_vector)
    if (False in visibility_check_vector) or (False in realism_check_vector):
        relationship_score = 0
    else:
        counter_i = 0
        N = len(entities_vector)
        while counter_i < N:
            counter_j = 0
            entity_i = entities_vector[counter_i]
            while counter_j < N:
                if counter_i != counter_j:
                    entity_j = entities_vector[counter_j]
                    relation = relationships_matrix[counter_i][counter_j]
                    if relation != " ":
                        bool_relation = relationship_check(entity_i, entity_j,
                                                           relation)
                        relationship_score += bool_relation * 1
                counter_j += 1
            relationship_score += (
                visibility_check_vector[counter_i] * 1
                + realism_check_vector[counter_i] * 1
            )
            counter_i += 1
    return relationship_score


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--path", type=str, required=True)
    parser.add_argument("--object", type=str, required=True)
    parser.add_argument("--attributes", type=str, required=True)
    parser.add_argument("--relationships", type=str, required=True)
    args = parser.parse_args()

    path = args.path
    logging.info("Path: %s", path)

    object = args.object
    logging.info("Object: %s", object)

    attributes = ast.literal_eval(args.attributes)
    logging.info("Attributes: %s", attributes)

    relationships = ast.literal_eval(args.relationships)
    logging.info("Relationships: %s", relationships)

    list_images = [file for file in os.listdir(path)
                   if file.endswith((".jpg"))]
    logging.info("List of images: %s", list_images)

    list_images_path = []
    for each in list_images:
        image_path = path + "/" + each
        list_images_path.append(image_path)
    logging.info("List of images: %s", list_images_path)

    for image in list_images_path:

        # First dimension: Evaluation of visual attributes

        logging.info("Evaluation of visual attributes")
        normalized_attribute_score = normalized_attribute_score_function(
            image, object, attributes
        )
        logging.info(
            "Normalized attribute score for %s is : %s",
            image,
            normalized_attribute_score,
        )

        # Second dimension: Evaluation of visual relations

        logging.info("Evaluation of visual relations")
        relationship_score = relationship_score_function(image, relationships)
        logging.info("Relationship score for %s is: %s", image,
                     relationship_score)


if __name__ == "__main__":
    main()
