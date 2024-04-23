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
import pandas as pd
import requests
from urllib.parse import urlencode

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def app():
    st.header(f":rainbow[ClickBait]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4500"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

########@@@@@@@@@@For text ONLY
    # ###Article Preprocess Area
    # # st.markdown(f"### Article URL")
    # st.markdown(f"### :gray[Text]")
    # # Text upload widget
    # text = st.text_area("Insert some text here")#, value="Add some text")
    # list_of_text = [text]
    # # st.write([text])
    #
    # if st.button('Analyze'):
    #     ### st.write(list_of_text)
    #     data = urlencode({'title': list_of_text}, True)
    #     response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/predict", data=data, headers=headers)
    #
    #     for res in response.json()['preds']:
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             # st.header("Legitimate News")
    #             st.markdown(
    #                 f":green[Title]")  # we use {}, in case we will select an integer or a float that will be stingified
    #             st.write(res['title'])
    #             # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
    #             # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")
    #
    #         with col2:
    #             st.markdown(
    #                 f":orange[Result]")  # we use {}, in case we will select an integer or a float that will be stingified
    #             st.write(res['result'])
    #         # st.write(res)

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

        # Display the data
        st.write("Uploaded Data:")
        # st.write(data_list)
        # data1 = urlencode({'title': data_list}, True)
        # st.write(data1)

    if st.button('Analyze'):
        clickbait = []
        non_clickbait = []
        for n in data_list:
            data = urlencode({'title': n}, True)
            response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/predict", data=data, headers=headers)
            if (response.json()["preds"][0]['result'] == 'True'):
                clickbait.append(response.json()["preds"][0]['result'])
            else:
                non_clickbait.append(response.json()["preds"][0]['result'])

        # st.write(f"Clickbait: {len(clickbait)}/Non-clickbait: {len(non_clickbait)}")
        # Define colors
        clickbait_color = "gray"
        non_clickbait_color = "blue"

        # Display the text with colors
        st.write(
            f"<span style='color:{clickbait_color}'>Clickbait: {len(clickbait)}</span> / <span style='color:{non_clickbait_color}'>Non-clickbait: {len(non_clickbait)}</span>",
            unsafe_allow_html=True)
        #
        labels = ['No-clickbait', 'Clickbait']
        labels1 = 'No-clickbait', 'Clickbait'
        sizes = [len(non_clickbait)/(len(non_clickbait)+len(clickbait)), len(clickbait)/(len(non_clickbait)+len(clickbait))]

        df = pd.DataFrame(
            {
                "Labels": labels,
                "(%)": sizes
            }
        )
        # st.write(df)

        fig = px.bar(df, x='Labels', y='(%)', orientation='v', hover_name=labels,
                     title='Clickbait Analysis Verification Service', color=labels1,
                     color_discrete_map={'No-clickbait': 'blue', 'Clickbait': 'gray'},
                     range_y=[0, 1])
        st.plotly_chart(fig)
################################
        # col1, col2 = st.columns(2)
        # with col1:
        #     # st.header("Legitimate News")
        #     st.markdown(
        #         f":green[Title]")  # we use {}, in case we will select an integer or a float that will be stingified
        #     for n in data_list:
        #         data = urlencode({'title': n}, True)
        #         response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/predict", data=data, headers=headers)
        #         st.write(response.json()["preds"][0]['title'])
        #
        # with col2:
        #     st.markdown(
        #         f":orange[Result]")  # we use {}, in case we will select an integer or a float that will be stingified
        #     for n in data_list:
        #         data = urlencode({'title': n}, True)
        #         response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/predict", data=data, headers=headers)
        #         st.write(response.json()["preds"][0]['result'])
        ### st.write(list_of_text)
            # st.write(response.json()["preds"][0]['title'])
            # st.write(response.json()["preds"][0]['result'])

