from transformers import FSMTForConditionalGeneration, FSMTTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from langdetect import detect
from newspaper import Article
from PIL import Image
import streamlit as st
import requests
import torch
import matplotlib.pyplot as plt
import plotly.express as px
import json
import requests
from urllib.parse import urlencode

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def app():
    st.header(f":rainbow[Bot Detector]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4510"
    headers = {
        "Content-Type": "application/json"
    }

    ###Article Preprocess Area
    # st.markdown(f"### Article URL")
    #st.markdown(f"### :gray[Text]")

    uploaded_file = st.file_uploader("Upload a file", type=['json'])
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        # dataframe = pd.read_csv(uploaded_file)
        global tweet1_dict
        tweet1_dict  = json.load(uploaded_file)
        # st.write(tweet1_dict)


    # # text = st.text_area("Insert some a file here")#, value="Add some text")
    # # st.write([text])
    # with open("example_1_v1.json", "r") as f:
    #     tweet1_dict = json.load(f)
    #
    # with open("example_1_v2.json", "r") as f:
    #     tweet2_dict = json.load(f)
    if st.button('Analyze'):
        if tweet1_dict:
            # , tweet2_dict
            response = requests.post(
                f"{SERVER_HOST}:{DOCKER_PORT}/predict",
                data=json.dumps([tweet1_dict]),
                params={"thr": 0.7},
                headers=headers
            )

            for res in response.json()['preds']:
                # st.write(res)
                col1, col2, col3 = st.columns(3)
                with col1:
                    # st.header("Legitimate News")
                    st.markdown(
                        f":green[Account ID]")  # we use {}, in case we will select an integer or a float that will be stingified
                    st.write(res['account_id'])
                    # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
                    # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

                with col2:
                    st.markdown(
                        f":orange[Bot Score]")  # we use {}, in case we will select an integer or a float that will be stingified
                    st.write(res['bot_score'])

                with col3:
                    st.markdown(
                        f":blue[Bot Label]")  # we use {}, in case we will select an integer or a float that will be stingified
                    st.write(res['bot_label'])


