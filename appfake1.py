from transformers import FSMTForConditionalGeneration, FSMTTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
#from langdetect import detect
from newspaper import Article
from PIL import Image
import streamlit as st
import requests
import torch
import matplotlib.pyplot as plt
import plotly.express as px
from pysentimiento import create_analyzer
import pandas as pd
from transformers import pipeline

import os
# os.environ["TOKENIZERS_PARALLELISM"] = "false"


def app():
    st.header(f":rainbow[Prediction of NLP Tasks by Given URL]")
    # st.markdown("## Prediction of Fakeness by Given URL")
    # background = Image.open('logo.jpg')
    # st.image(background)

    ####Models Definition
    # Analyzes for the 4 Declared NLP Analysis Tasks

    irony_detection_analyzer = create_analyzer(task="irony", lang="en")
    analyzer = create_analyzer(task="sentiment", lang="en")
    emotion_analyzer = create_analyzer(task="emotion", lang="en")
    # hate_speech_analyzer = create_analyzer(task="hate_speech", lang="en")
    # Use a pipeline as a high-level helper
    hate_speech_analyzer = pipeline("text-classification", model="IMSyPP/hate_speech_en", return_all_scores=True)

    # English to Spain Translation
    # pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

    ###Article Preprocess Area
    # st.markdown(f"### Article URL")
    st.markdown(f"### :gray[Article URL]")
    url = st.text_area("Insert some url here",
                       value="https://en.globes.co.il/en/article-yandex-looks-to-expand-activities-in-israel-1001406519")
    article = Article(url)
    article.download()
    article.parse()
    title = article.title
    text = article.text
    len(text[:2000])
    len(text)

    #st.markdown(f"##### :gray[Article Title]")
    #st.markdown('"' + title + '"')
    # @st.cache_data()#allow_output_mutation=True)
    # url = 'https://edition.cnn.com/africa/live-news/morocco-earthquake-marrakech-09-11-23/index.html'
    # st.write(title)
    # st.write(predict_fake(title,text))

    # Added button to proceed to the respective analysis
    if st.button('Analyze'):
        st.markdown(f"##### :gray[Article Title]")
        st.markdown('"' + title + '"')
        ##Ironic Speech Detection
        ironic = irony_detection_analyzer.predict(text).probas['ironic']
        not_ironic = irony_detection_analyzer.predict(text).probas['not ironic']
        ironic_result = irony_detection_analyzer.predict(text).output
        ##Sentiment Analysis
        positive = analyzer.predict(text).probas['POS']
        neutral = analyzer.predict(text).probas['NEU']
        negative = analyzer.predict(text).probas['NEG']
        sentiment_result = analyzer.predict(text).output
        ##Hate Speech Analysis
        hate_result = hate_speech_analyzer(title)  # + ': ' +text[:2000])
        acceptable = hate_result[0][0]['score']
        inappropriate = hate_result[0][1]['score']
        offensive = hate_result[0][2]['score']
        violent = hate_result[0][3]['score']

        # hateful = hate_speech_analyzer.predict(text).probas['hateful']
        # targeted = hate_speech_analyzer.predict(text).probas['targeted']
        # aggressive = hate_speech_analyzer.predict(text).probas['aggressive']
        ##Emotion Analysis
        others = emotion_analyzer.predict(text).probas['others']
        sadness = emotion_analyzer.predict(text).probas['sadness']
        disgust = emotion_analyzer.predict(text).probas['disgust']
        fear = emotion_analyzer.predict(text).probas['fear']
        joy = emotion_analyzer.predict(text).probas['joy']
        anger = emotion_analyzer.predict(text).probas['anger']
        surprise = emotion_analyzer.predict(text).probas['surprise']

        ###Ironic Speech Verification Model
        st.header(f":orange[Ironic Speech Verification Service]")
        if ironic_result == 'not ironic':
            st.markdown(f"##### :green[The text below does not include any part of Ironic Speech]")
        else:
            st.markdown(f"##### :red[The text below does include any part of Ironic Speech]")

        col1, col2 = st.columns(2)
        with col1:
            # st.header("Legitimate News")
            st.markdown(
                f":green[Not Ironic Speech]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(not_ironic)
            # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

        with col2:
            st.markdown(
                f":red[Ironic Speech]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(ironic)
        # st.header("Fake News")
        # st.write(f":red[{'%.2f' % int(round(predict_fake(title, text)['Fake'] * 100, 2))}] %")

        labels = 'Not Ironic Speech', 'Ironic Speech'
        sizes = [round(not_ironic * 100, 2), round(ironic * 100, 2)]
        fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Ironic Speech Verification Service',
                     color=labels,
                     color_discrete_map={'Not Ironic Speech': 'green', 'Ironic Speech': 'red'})
        st.plotly_chart(fig)

        ###Sentiment Analysies Verification Model
        st.header(f":blue[Sentiment Analysis Verification Service]")
        col1, col2, col3 = st.columns(3)
        with col1:
            # st.header("Legitimate News")
            st.markdown(
                f":green[Positive Sentiment]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(positive)
            # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

        with col2:
            st.markdown(
                f":orange[Neutral News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(neutral)

        with col3:
            st.markdown(
                f":red[Negative News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(negative)
        # st.header("Fake News")
        # st.write(f":red[{'%.2f' % int(round(predict_fake(title, text)['Fake'] * 100, 2))}] %")

        labels = 'Positive Sentiments', 'Neutral Sentiments', 'Negative Sentiments'
        sizes = [round(positive * 100, 2), round(neutral * 100, 2), round(negative * 100, 2)]
        fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Sentiment Analysis Verification Service',
                     color=labels,
                     color_discrete_map={'Positive Sentiments': 'green', 'Neutral Sentiments': 'orange',
                                         'Negative Sentiments': 'red'})
        st.plotly_chart(fig)
        # -----
        # Hate Speech Analysis Verification Service
        st.header(f":purple[Hate Speech Analysis Verification Service]")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            # st.header("Legitimate News")
            st.markdown(
                f":green[Acceptable]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(acceptable)
            # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

        with col2:
            st.markdown(
                f":yellow[Inappropriate]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(inappropriate)

        with col3:
            st.markdown(
                f":blue[Offensive]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(offensive)

        with col4:
            st.markdown(
                f":red[Violent]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(violent)
        #
        labels = ['Acceptable', 'Inappropriate', 'Offensive', 'Violent']
        labels1 = 'Acceptable', 'Inappropriate', 'Offensive', 'Violent'
        sizes = [round(acceptable * 100, 2), round(inappropriate * 100, 2), round(offensive * 100, 2),
                 round(violent * 100, 2)]

        df = pd.DataFrame(
            {
                "Hate Speech": labels,
                "(%)": sizes
            }
        )
        # st.write(df)

        fig = px.bar(df, x='Hate Speech', y='(%)', orientation='v', hover_name=labels,
                     title='Hate Speech Analysis Verification Service', color=labels1,
                     color_discrete_map={'Acceptable': 'green', 'Inappropriate': 'yellow', 'Offensive': 'blue',
                                         'Violent': 'red'},
                     range_y=[0, 100])

        ##----Pie Chart Does NOT Make Sensein this Case-----##
        # fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Hate Speech Analysis Verification Service', color=labels,
        #              color_discrete_map={'Hateful Speech': 'red', 'Targeted Speech': 'blue', 'Aggressive Speech': 'yellow'})
        st.plotly_chart(fig)

        ###Emotion Analysis Verification Model
        st.header(f":blue[Emotion Analysis Verification Service]")
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            # st.header("Legitimate News")
            st.markdown(
                f":green[Joy]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(round(joy, 5))
            # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

        with col2:
            st.markdown(
                f":orange[Sadness]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(round(sadness, 5))

        with col3:
            st.markdown(
                f":red[Anger]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(round(anger, 5))

        with col4:
            st.markdown(
                f":red[Fear]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(round(fear, 5))

        with col5:
            st.markdown(
                f":red[Surprise]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(round(surprise, 5))

        with col6:
            st.markdown(
                f":red[Disgust]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(round(disgust, 5))

        with col7:
            st.markdown(
                f":red[Others]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(round(others, 5))

        labels = 'joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'others'
        sizes = [round(joy, 5) * 100, round(sadness, 5) * 100, round(anger, 5) * 100, round(fear, 5) * 100,
                 round(surprise, 5) * 100, round(disgust, 5) * 100, round(others, 5) * 100]

        df = pd.DataFrame(
            {
                "Emotion": labels,
                "(%)": sizes
            }
        )
        # st.write(df)

        fig = px.bar(df, x='Emotion', y='(%)', orientation='v', hover_name=labels,
                     title='Emotion Analysis Verification Service', range_y=[0, 100],
                     color=labels,
                     color_discrete_map={'joy': 'green', 'sadness': 'blue', 'anger': 'red', 'fear': 'black',
                                         'surpise': 'yellow', 'disgust': 'brown', 'others': 'gray'},
                     )

        st.plotly_chart(fig)

    # ----> PIE Chart DOES NOT Represent Properly the Results
    # fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Emotion Analysis Verification Service',
    #              color=labels,
    #              color_discrete_map={'joy': 'green', 'sadness': 'blue', 'anger': 'red', 'fear': 'gray',
    #                                  'surpise': 'yellow', 'disgust' : 'brown', 'others': 'white'})
    # st.plotly_chart(fig)

    ## ------>>>>Hate Speech Version 2: Does not provide results properly
    # -----
    # # Hate Speech Analysis Verification Service
    # st.header(f":purple[Speech Analysis Verification Service]")
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     # st.header("Legitimate News")
    #     st.markdown(
    #         f":red[Hateful]")  # we use {}, in case we will select an integer or a float that will be stingified
    #     st.write(hateful)
    #     # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
    #     # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")
    #
    # with col2:
    #     st.markdown(
    #         f":blue[Targeted]")  # we use {}, in case we will select an integer or a float that will be stingified
    #     st.write(targeted)
    #
    # with col3:
    #     st.markdown(
    #         f":grey[Aggressive]")  # we use {}, in case we will select an integer or a float that will be stingified
    #     st.write(aggressive)
    #
    # labels = ['Hateful Speech', 'Targeted Speech', 'Aggressive Speech']
    # labels1 = 'Hateful Speech', 'Targeted Speech', 'Aggressive Speech'
    # sizes = [round(hateful * 100, 2), round(targeted * 100, 2), round(aggressive * 100, 2)]
    #
    # df = pd.DataFrame(
    #     {
    #         "Hate Speech": labels,
    #         "(%)": sizes
    #     }
    # )
    # # st.write(df)
    #
    # fig = px.bar(df, x='Hate Speech', y='(%)', orientation='v', hover_name=labels,
    #              title='Hate Speech Analysis Verification Service', color=labels1,
    #              color_discrete_map={'Hateful Speech': 'red', 'Targeted Speech': 'blue', 'Aggressive Speech': 'grey'},
    #              range_y=[0, 100])
    # ##----Pie Chart Does NOT Make Sensein this Case-----##
    # # fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Hate Speech Analysis Verification Service', color=labels,
    # #              color_discrete_map={'Hateful Speech': 'red', 'Targeted Speech': 'blue', 'Aggressive Speech': 'yellow'})
    # st.plotly_chart(fig)
