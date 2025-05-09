import pytest
import sys
import os
import base64
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from realism_evaluation_system import image_to_base64

image_path = "./tests/images_test/image1.jpg"

def test_image_to_base64():
    try:
        with open(image_path, "rb") as image_file:
            expected_output = base64.b64encode(image_file.read()).decode("utf-8")
            assert image_to_base64(image_path) == expected_output
    except Exception as e:
        print(f"Error: {e}")
        return None