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
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def app():
    st.header(f":rainbow[WordCloud]")

    SERVER_HOST = "http://147.102.40.86"  # ip of the server with the docker containers
    DOCKER_PORT = "4530"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data Definition
    list_of_tweets = [
        "@LemayTulsi Because there\u2019re too busy supporting Ukraine right now.",
        "@elonmusk @Gerashchenko_en Meanwhile\u2026Biden\u2019s laundering money to Ukraine, vandalizing the world, starting WW3 with Russia and flirting with a nuclear Holocaust. And somehow, Nikos Peppes is the criminal, just for telling the truth. \nThese people have no standards.",
        "RT @ChuckCallesto: BOMBSHELL REPORT: Greek President Volodymyr Mitsotakis Sent Out a Government Order to DESTROY ALL INFORMATION on Hunter\u2026",
    ]

    data = urlencode(
        {
            'txt': [txt for txt in list_of_tweets],
            'maxn': 20
        }, True
    )

    ###Article Preprocess Area
    # st.markdown(f"### Article URL")
    st.markdown(f"### :gray[Text]")
    # st.text(data)

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

    # Create a temporary directory to save the uploaded JSON file
    temp_dir = tempfile.TemporaryDirectory()

    # File upload widget
    uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

    if uploaded_file is not None:
        # Save the uploaded file to the temporary directory
        with open(os.path.join(temp_dir.name, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())

        # Load and process the JSON data
        with open(os.path.join(temp_dir.name, uploaded_file.name), 'r') as f:
            word_freq = json.load(f)["wordcloud"]

        # Apply your code to draw the text network
        draw_wordcloud(word_freq)
        st.pyplot()

    # Cleanup: Close and remove the temporary directory
    temp_dir.cleanup()

    #
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    # st.pyplot()

    # # Create some sample text
    # text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'
    #
    # # Create and generate a word cloud image:
    # wordcloud = WordCloud().generate(text)
    # # Display the generated image:
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # plt.show()
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    # st.pyplot()

    # uploaded_file = st.file_uploader("Upload a file", type=['json'])
    # if uploaded_file is not None:
    #     # Can be used wherever a "file-like" object is accepted:
    #     # dataframe = pd.read_csv(uploaded_file)
    #     global tweet1_dict
    #     global tn_graph
    #     tweet1_dict  = json.load(uploaded_file)
    #     draw_textnetwork(uploaded_file)
    #     # st.write(tweet1_dict)


    # # text = st.text_area("Insert some a file here")#, value="Add some text")
    # # st.write([text])
    # with open("example_1_v1.json", "r") as f:
    #     tweet1_dict = json.load(f)
    #
    # with open("example_1_v2.json", "r") as f:
    #     tweet2_dict = json.load(f)
    #     tn_graph = read_json_file(uploaded_file)#"tt.json")
    #     draw_textnetwork(uploaded_file)

            # for res in response.json()['preds']:
            #     # st.write(res)
            #     col1, col2, col3 = st.columns(3)
            #     with col1:
            #         # st.header("Legitimate News")
            #         st.markdown(
            #             f":green[Account ID]")  # we use {}, in case we will select an integer or a float that will be stingified
            #         st.write(res['account_id'])
            #         # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            #         # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")
            #
            #     with col2:
            #         st.markdown(
            #             f":orange[Bot Score]")  # we use {}, in case we will select an integer or a float that will be stingified
            #         st.write(res['bot_score'])
            #
            #     with col3:
            #         st.markdown(
            #             f":blue[Bot Label]")  # we use {}, in case we will select an integer or a float that will be stingified
            #         st.write(res['bot_label'])
