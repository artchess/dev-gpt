import json
import os

import streamlit as st
from jina import Client, Document, DocumentArray
import io

st.set_page_config(
    page_title="Meme Generator",
    page_icon=":smiley:",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title(":smiley: Meme Generator")
st.markdown(
    "Generate memes with custom captions."
    "To generate and deploy your own microservice, click [here](https://github.com/jina-ai/dev-gpt)."
)
st.subheader(":speech_balloon: Enter your captions")
with st.form(key="input_form"):
    image_url = st.text_input("Image URL")
    top_caption = st.text_input("Top Caption")
    bottom_caption = st.text_input("Bottom Caption")
    input_json_dict = {
        "image_url": image_url,
        "top_caption": top_caption,
        "bottom_caption": bottom_caption
    }

    input_json_dict_string = json.dumps(input_json_dict)
    submitted = st.form_submit_button("Generate Meme")

# Process input and call microservice
if submitted:
    if not image_url or not top_caption or not bottom_caption:
        st.error("Please provide a valid image URL and captions.")
    else:
        with st.spinner("Generating your meme..."):
            client = Client(host="http://localhost:8080")
            d = Document(text=input_json_dict_string)
            response = client.post("/", inputs=DocumentArray([d]))

            output_data = json.loads(response[0].text)
            if "error" in output_data:
                st.error(output_data["error"])
            else:
                st.image(output_data["meme"], caption="Your Meme", use_column_width=True)

# Display curl command
deployment_id = os.environ.get("K8S_NAMESPACE_NAME", "")
api_endpoint = (
    f"https://dev-gpt-{deployment_id.split('-')[1]}.wolf.jina.ai/post"
    if deployment_id
    else "http://localhost:8080/post"
)

with st.expander("See curl command"):
    st.markdown("You can use the following curl command to send a request to the microservice from the command line:")
    escaped_input_json_dict_string = input_json_dict_string.replace('"', '\\"')

    st.code(
        f'curl -X "POST" "{api_endpoint}" -H "accept: application/json" -H "Content-Type: application/json" -d \'{{"data": [{{"text": "{escaped_input_json_dict_string}"}}]}}\'',
        language="bash",
    )