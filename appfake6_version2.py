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
    st.header(f":rainbow[TextNetwork]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4530"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data Definition
    # list_of_tweets = [
    #     "@LemayTulsi Because there\u2019re too busy supporting Ukraine right now.",
    #     "@elonmusk @Gerashchenko_en Meanwhile\u2026Biden\u2019s laundering money to Ukraine, vandalizing the world, starting WW3 with Russia and flirting with a nuclear Holocaust. And somehow, Nikos Peppes is the criminal, just for telling the truth. \nThese people have no standards.",
    #     "RT @ChuckCallesto: BOMBSHELL REPORT: Greek President Volodymyr Mitsotakis Sent Out a Government Order to DESTROY ALL INFORMATION on Hunter\u2026",
    # ]

    # File upload widget for uploading xlsx files
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)

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

        # st.write(data_list)
        # st.write(data)

        ###Article Preprocess Area
        # st.markdown(f"### Article URL")
        # st.markdown(f"### :gray[Text]")
        # st.text(data)
        response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/textnetwork", data=data, headers=headers)
        # st.write(response.json())
        draw_textnetwork(response.json()["textnetwork"])
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
        # if response.status_code == 200:
        #     st.write(response.json()["wordcloud"])
        #     draw_wordcloud(response.json()["wordcloud"])
        #     st.pyplot()
    # response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/wordcloud", data=data, headers=headers)
    # if response.status_code == 200:
    #     # st.text(response.json()["wordcloud"])
    #     # draw_wordcloud(response.json()["wordcloud"])
    #     word_freq = {item["text"]: item["weight"] for item in response.json()["wordcloud"]}  # Refactor format
    #
    #     # Generate the word cloud
    #     wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    #
    #     # Display the word cloud using Matplotlib
    #     plt.figure(figsize=(10, 5))
    #     plt.imshow(wordcloud, interpolation='bilinear')
    #     plt.axis("off")
    #     plt.show()
    #     st.set_option('deprecation.showPyplotGlobalUse', False)
    #     st.pyplot()

    # # Create a temporary directory to save the uploaded JSON file
    # temp_dir = tempfile.TemporaryDirectory()
    #
    # # File upload widget
    # uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])
    #
    # if uploaded_file is not None:
    #     # Save the uploaded file to the temporary directory
    #     with open(os.path.join(temp_dir.name, uploaded_file.name), "wb") as f:
    #         f.write(uploaded_file.read())
    #
    #     # Load and process the JSON data
    #     with open(os.path.join(temp_dir.name, uploaded_file.name), 'r') as f:
    #         word_freq = json.load(f)["wordcloud"]
    #
    #     # Apply your code to draw the text network
    #     draw_wordcloud(word_freq)
    #     st.pyplot()
    #
    # # Cleanup: Close and remove the temporary directory
    # temp_dir.cleanup()

    #
