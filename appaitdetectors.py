import numpy as np
import streamlit as st
import requests
import json
from PIL import Image
import torch
import matplotlib.pyplot as plt
import plotly.express as px

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def app():
    st.header(f":rainbow[Symbol Detection by Given Image]")
    # Include PIL, load_image before main()

    # Function to load an image
    def load_image(image_file):
        img = Image.open(image_file)
        return img

    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], key='1')

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

            response = requests.post('http://81.189.135.251:8080/symboldetect', headers=headers, files=files)            # st.write(response.text)
            response_dict = json.loads(response.text)
            st.write('Keltenkreuz:')
            st.write(response_dict['Keltenkreuz'])
            st.write('Hakenkreuz:')
            st.write(response_dict['Hakenkreuz'])
            st.write('DoppelSigrune:')
            st.write(response_dict['DoppelSigrune'])
            # st.write(response_dict)
        except Exception as e:
            st.write(f"An error occurred: {e}")

    st.header(f":rainbow[Manipulation Detection by Given Image]")

    # Include PIL, load_image before main()

    # Function to load an image
    def load_image(image_file):
        img = Image.open(image_file)
        return img

    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"],key='2')

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

            response = requests.post('http://81.189.135.251:8080/manipulationdetect', headers=headers, files=files)
            response_dict = json.loads(response.text)
            st.write('Rv1:')
            st.write(response_dict['rv1'])
            st.write('Rv2:')
            st.write(response_dict['rv2'])
            st.write('Result:')
            st.write(response_dict['result'])
            st.write('Short Result:')
            st.write(response_dict['short_result'])
            # st.write(response_dict)
        except Exception as e:
            st.write(f"An error occurred: {e}")
