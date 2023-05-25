from .microservice import func
import json
import requests
import base64
from PIL import Image
from io import BytesIO

def test_microservice_output_base64_encoded_string():
    """
    This test case asserts that the output of the microservice is a base64 encoded string (type 'str').
    The test provides a sample image URL, top caption text, and bottom caption text as input to the microservice.
    It then checks if the output is a valid base64 encoded string and if it is of type 'str'.
    """
    # Sample input data
    input_data = {
        "image_url": "https://via.placeholder.com/300x200.png",
        "top_caption": "Top Caption",
        "bottom_caption": "Bottom Caption"
    }

    # Call the microservice function with the input data
    input_json_dict_string = json.dumps(input_data)
    output_json_string = func(input_json_dict_string)

    # Parse the output JSON string
    output_data = json.loads(output_json_string)

    # Check if the output is a valid base64 encoded string and if it is of type 'str'
    try:
        base64_image = output_data["meme"]
        assert isinstance(base64_image, str)
        decoded_image = base64.b64decode(base64_image)
        image = Image.open(BytesIO(decoded_image))
    except (KeyError, ValueError, OSError):
        assert False, "The output is not a valid base64 encoded string"