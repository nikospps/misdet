import json
import requests
from draw_textnetwork import draw_textnetwork, read_json_file
from draw_wordcloud import draw_wordcloud
from urllib.parse import urlencode
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import networkx as nx
from networkx.readwrite import json_graph
from networkx.algorithms import community
import matplotlib.pyplot as plt
import logging
from random import random
import tempfile

import os
import pandas as pd
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def app():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.header(f":rainbow[WordCloud]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4530"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # File upload widget for uploading xlsx files
    uploaded_file1 = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"], key='uploader1')

    if uploaded_file1 is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file1)

        # Convert the DataFrame to a list of dictionaries
        # data_list = df.to_dict(orient='records')
        # Flatten the DataFrame into a list of strings
        data_list = df.values.flatten().tolist()
        # Remove any None values and empty strings
        data_list = [str(item) for item in data_list if pd.notna(item) and str(item).strip() != ""]
        data = urlencode(
            {
                'txt': [txt for txt in data_list],
                'maxn': 20
            }, True
        )

        response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/wordcloud", data=data, headers=headers)
        # st.write(response.json())
        draw_wordcloud(response.json()["wordcloud"])
        st.pyplot()

    st.header(f":rainbow[TextNetwork]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4530"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # File upload widget for uploading xlsx files
    uploaded_file2 = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"], key='uploader2')

    if uploaded_file2 is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file2)

        # Convert the DataFrame to a list of dictionaries
        # data_list = df.to_dict(orient='records')
        # Flatten the DataFrame into a list of strings
        data_list = df.values.flatten().tolist()
        # Remove any None values and empty strings
        data_list = [str(item) for item in data_list if pd.notna(item) and str(item).strip() != ""]
        data = urlencode(
            {
                'txt': [txt for txt in data_list],
                'maxn': 20
            }, True
        )

        response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/textnetwork", data=data, headers=headers)
        draw_textnetwork(response.json()["textnetwork"])
        st.pyplot()
