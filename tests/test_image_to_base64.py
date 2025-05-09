import pytest
import sys
import base64
import requests

sys.path.append("/home/a939219/vllm-test")
from realism_evaluation_system import image_to_base64

image_url = "https://picsum.photos/200/300"


def test_image_to_base64():
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        expected_output = base64.b64encode(response.content).decode("utf-8")
        assert image_to_base64(image_url) == expected_output
    except Exception as e:
        print(f"Error: {e}")
        return None
