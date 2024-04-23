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
import pandas as pd
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def app():
    st.header(f":rainbow[Sentiment Analysis]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4520"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # ###Article Preprocess Area
    # # st.markdown(f"### Article URL")
    # st.markdown(f"### :gray[Text]")
    # text = st.text_area("Insert some text here")#, value="Add some text")
    # list_of_text = [text]
    # # st.write([text])

    # Xlsx File uploader
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
        data = urlencode({'txt': [txt for txt in data_list]}, True)

    if st.button('Analyze'):
        positive = []
        neutral = []
        negative = []

        response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/predict", data=data, headers=headers)

        for prediction in response.json()["preds"]:
            if(prediction['label']=='positive'):
                positive.append(prediction)
            elif(prediction['label']=='negative'):
                negative.append(prediction)
            else:
                neutral.append(prediction)

        # st.write(len(positive))
        # st.write(len(negative))
        # st.write(len(neutral))
        # st.write(len(positive)+len(negative)+len(neutral))

        #Bar Charts
        positive_color = "green"
        negative_color = "red"
        neutral_color = "yellow"

        # Display the text with colors
        # st.write(
        #     f"<span style='color:{spam_color}'>Spam: {len(spam)}</span> / <span style='color:{ham_color}'>Ham: {len(ham)}</span>",
        #     unsafe_allow_html=True)
        #
        labels = ['Positive', 'Neutral', 'Negative']
        labels1 = 'Positive', 'Neutral', 'Negative'
        sizes = [(len(positive) / (len(positive) + len(negative) + len(neutral))), (len(neutral) / (len(positive) + len(negative) + len(neutral))),
                 (len(negative) / (len(positive) + len(negative) + len(neutral)))]

        df = pd.DataFrame(
            {
                "Labels": labels,
                "(%)": sizes
            }
        )
        # st.write(df)

        fig = px.bar(df, x='Labels', y='(%)', orientation='v', hover_name=labels,
                     title='Spam SMS Detection Verification Service', color=labels1,
                     color_discrete_map={'Positive': 'green', 'Neutral': 'yellow', 'Negative': 'red'},
                     range_y=[0, 1])
        st.plotly_chart(fig)

        st.write(
            f"<span style='color:{positive_color}'>Positive: {len(positive)}</span> / <span style='color:{neutral_color}'>Neutral: {len(neutral)}</span> / "
            f"<span style='color:{negative_color}'>Negative: {len(negative)}</span>",
            unsafe_allow_html=True)

        ###@@@In case we need to visualize the results into columns including score and labels
        # col1, col2 = st.columns(2)
        # with col1:
        #     # st.header("Legitimate News")
        #     st.markdown(
        #         f":green[Score]")  # we use {}, in case we will select an integer or a float that will be stingified
        #     for prediction in response.json()["preds"]:
        #         st.write(prediction['score'])
        #
        # with col2:
        #     st.markdown(
        #         f":orange[Label]")  # we use {}, in case we will select an integer or a float that will be stingified
        #     for prediction in response.json()["preds"]:
        #         st.write(prediction['label'])
