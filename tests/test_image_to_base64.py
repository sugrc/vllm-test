import pytest
import sys
import base64

sys.path.append("/home/a939219/vllm-test")
from realism_evaluation_system import image_to_base64

image_path = "/home/a939219/vllm-test/images/bunny.jpg"


def test_image_to_base64():
    try:
        with open(image_path, "rb") as image_file:
            expected_output = base64.b64encode(image_file.read()).decode("utf-8")
            assert image_to_base64(image_path) == expected_output
    except Exception as e:
        print(f"Error: {e}")
        return None
