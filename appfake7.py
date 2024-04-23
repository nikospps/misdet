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
    st.header(f":rainbow[Spam-SMS Detection]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4540"
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
        # st.write("Uploaded Data:")
        # st.write(data_list)
        # data1 = urlencode({'title': data_list}, True)
        # st.write(data1)

    if st.button('Analyze'):
        spam = []
        ham = []

        data = urlencode({'txt': [txt for txt in data_list]}, True)
        response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/predict", data=data, headers=headers)

        for prediction in response.json()["preds"]:
            if(prediction['label']=='spam'):
                spam.append(prediction)
            else:
                ham.append(prediction)

        # st.write(len(spam)+len(ham))
        # st.write(len(spam))
        # st.write(len(ham))
        #
        # st.write(f"Spam: {len(spam)}/Ham: {len(ham)}")
        # Define colors
        spam_color = "gray"
        ham_color = "blue"

        # Display the text with colors
        # st.write(
        #     f"<span style='color:{spam_color}'>Spam: {len(spam)}</span> / <span style='color:{ham_color}'>Ham: {len(ham)}</span>",
        #     unsafe_allow_html=True)
        #
        labels = ['Ham', 'Spam']
        labels1 = 'Ham', 'Spam'
        sizes = [len(ham)/(len(ham)+len(spam)), len(spam)/(len(ham)+len(spam))]

        df = pd.DataFrame(
            {
                "Labels": labels,
                "(%)": sizes
            }
        )
        # st.write(df)

        fig = px.bar(df, x='Labels', y='(%)', orientation='v', hover_name=labels,
                     title='Spam SMS Detection Verification Service', color=labels1,
                     color_discrete_map={'Ham': 'blue', 'Spam': 'gray'},
                     range_y=[0, 1])
        st.plotly_chart(fig)

        st.write(
            f"<span style='color:{spam_color}'>Spam: {len(spam)}</span> / <span style='color:{ham_color}'>Ham: {len(ham)}</span>",
            unsafe_allow_html=True)
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

