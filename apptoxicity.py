import streamlit as st
import requests
import json
import torch
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def app():
    st.header(f":rainbow[Prediction of Toxicity by Given Text]")
    headers = {'accept': 'application/json',}

    ###Article Preprocess Area
    # st.markdown(f"### Article URL")
    text = st.text_area("Insert some text title context here", value="This is a text context")

    json_data = {'input_text': text }

    response = requests.post('http://81.189.135.251:8080/toxicity', headers=headers, json=json_data)
    response_dict = json.loads(response.text)

    # Added button to proceed to misinformation analysis
    if st.button('Predict'):
        if(response_dict['toxic']>response_dict['not_toxic']):
            st.markdown(f'According to the verification services, the text is classified as :red[Toxic]')  # with a 100% certainty.
        else:
            st.markdown(f'According to the verification services, the text is classified as :red[not Toxic]')  # with a 100% certainty.
    st.header(f":rainbow[Estimation of Geolocation by Given Image]")
    # Include PIL, load_image before main()

    # Function to load an image
    def load_image(image_file):
        img = Image.open(image_file)
        return img

    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])

    if image_file is not None:
        try:
            st.image(load_image(image_file), width=250)
            # Get the name of the uploaded image
            image_name = image_file.name
            st.write(f"Uploaded Image Name: {image_name}")

            # Convert the image to bytes
            img_bytes = image_file.read()

            headers = {
                'accept': 'application/json',
            }

            files = {'file': img_bytes}

            response = requests.post('http://81.189.135.251:8080/geolocestim', headers=headers, files=files)
            # st.write(response.text)
            response_dict = json.loads(response.text)
            st.write('Coarse:')
            st.write(response_dict['coarse'])
            st.write('Middle:')
            st.write(response_dict['middle'])
            st.write('Fine:')
            st.write(response_dict['fine'])
            st.write('Hierarchy:')
            st.write(response_dict['hierarchy'])
            # st.write(response_dict)
        except Exception as e:
            st.write(f"An error occurred: {e}")

        # labels = 'Legitimate News', 'Fake News'
        # sizes = [round(weights_real* 100, 2), round(weights_fake * 100, 2)]
        # fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Average Weights Verification Service Result', color=labels,
        #              color_discrete_map={'Legitimate News': 'green', 'Fake News': 'red'})
        # st.plotly_chart(fig)
