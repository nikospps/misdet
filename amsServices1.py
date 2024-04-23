import streamlit as st
import plotly.express as px
import requests
from urllib.parse import urlencode
import json

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

    # Xlsx File uploader
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
        data = urlencode({'txt': [txt for txt in data_list]}, True)

    if st.button('Analyze', key='but1'):
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

    st.header(f":rainbow[ClickBait]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4500"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # File upload widget for uploading xlsx files
    uploaded_file2 = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"], key='uploader2')

    if uploaded_file2 is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file2)

        data_list = df.values.flatten().tolist()
        # Remove any None values and empty strings
        data_list = [str(item) for item in data_list if pd.notna(item) and str(item).strip() != ""]

    if st.button('Analyze', key='but2'):
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

        labels = ['No-clickbait', 'Clickbait']
        labels1 = 'No-clickbait', 'Clickbait'
        sizes = [len(non_clickbait) / (len(non_clickbait) + len(clickbait)),
                 len(clickbait) / (len(non_clickbait) + len(clickbait))]

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

        st.write(f"<span style='color:{clickbait_color}'>Clickbait: {len(clickbait)}</span> / <span style='color:{non_clickbait_color}'>Non-clickbait: {len(non_clickbait)}</span>",
            unsafe_allow_html=True)
##
    st.header(f":rainbow[Bot Detector]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4510"
    headers = {
        "Content-Type": "application/json"
    }

    ###Article Preprocess Area
    # st.markdown(f"### Article URL")

    uploaded_file3 = st.file_uploader("Upload a file", type=['json'], key='uploader3')
    if uploaded_file3 is not None:
        # Can be used wherever a "file-like" object is accepted:
        global tweet1_dict
        tweet1_dict = json.load(uploaded_file3)

    if st.button('Analyze', key='but3'):
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
##
    st.header(f":rainbow[Spam-SMS Detection]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4540"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }


    # File upload widget for uploading xlsx files
    uploaded_file4 = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"], key='uploader4')

    if uploaded_file4 is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file4)

        # Convert the DataFrame to a list of dictionaries
        # data_list = df.to_dict(orient='records')
        # Flatten the DataFrame into a list of strings
        data_list = df.values.flatten().tolist()
        # Remove any None values and empty strings
        data_list = [str(item) for item in data_list if pd.notna(item) and str(item).strip() != ""]


    if st.button('Analyze', key='but4'):
        spam = []
        ham = []

        data = urlencode({'txt': [txt for txt in data_list]}, True)
        response = requests.post(f"{SERVER_HOST}:{DOCKER_PORT}/predict", data=data, headers=headers)

        for prediction in response.json()["preds"]:
            if (prediction['label'] == 'spam'):
                spam.append(prediction)
            else:
                ham.append(prediction)

        spam_color = "gray"
        ham_color = "blue"

        labels = ['Ham', 'Spam']
        labels1 = 'Ham', 'Spam'
        sizes = [len(ham) / (len(ham) + len(spam)), len(spam) / (len(ham) + len(spam))]

        df = pd.DataFrame(
            {
                "Labels": labels,
                "(%)": sizes
            }
        )
        fig = px.bar(df, x='Labels', y='(%)', orientation='v', hover_name=labels,
                     title='Spam SMS Detection Verification Service', color=labels1,
                     color_discrete_map={'Ham': 'blue', 'Spam': 'gray'},
                     range_y=[0, 1])
        st.plotly_chart(fig)

        st.write(
            f"<span style='color:{spam_color}'>Spam: {len(spam)}</span> / <span style='color:{ham_color}'>Ham: {len(ham)}</span>",
            unsafe_allow_html=True)
