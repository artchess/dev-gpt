import json
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64

def func(input_json_dict_string: str) -> str:
    # Parse the input JSON string
    input_data = json.loads(input_json_dict_string)

    # Retrieve the image from the provided URL
    image_url = input_data['image_url']
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Overlay the top and bottom caption texts on the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=30)
    top_caption = input_data['top_caption']
    bottom_caption = input_data['bottom_caption']
    top_text_size = draw.textsize(top_caption, font)
    bottom_text_size = draw.textsize(bottom_caption, font)

    # Calculate the position of the top and bottom caption texts
    top_position = ((image.width - top_text_size[0]) // 2, 10)
    bottom_position = ((image.width - bottom_text_size[0]) // 2, image.height - bottom_text_size[1] - 10)

    # Draw the caption texts on the image
    draw.text(top_position, top_caption, font=font, fill="white")
    draw.text(bottom_position, bottom_caption, font=font, fill="white")

    # Convert the image to a base64 encoded string
    output_buffer = BytesIO()
    image.save(output_buffer, format="PNG")
    base64_image = base64.b64encode(output_buffer.getvalue()).decode("utf-8")

    # Return the generated meme as a JSON string
    output_data = {"meme": base64_image}
    return json.dumps(output_data)