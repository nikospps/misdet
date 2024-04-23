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
import pandas as pd

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def app():
    st.header(f":rainbow[Prediction of Fakeness by Given URL]")
    # st.markdown("## Prediction of Fakeness by Given URL")
    # background = Image.open('logo.jpg')
    # st.image(background)

    ####Models Definition
    # Bert
    model_name = "./Bert2_FN_Classification/"  # Path to the local clone repository
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def predict_fake(title, text):
        input_str = "<title>" + title + "<content>" + text + "<end>"
        input_ids = tokenizer.encode_plus(input_str, max_length=512, padding="max_length", truncation=True,
                                          return_tensors="pt")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model.to(device)
        with torch.no_grad():
            output = model(input_ids["input_ids"].to(device), attention_mask=input_ids["attention_mask"].to(device))
        return dict(zip(["Fake", "Real"], [x.item() for x in list(torch.nn.Softmax()(output.logits)[0])]))

    # DistilBert
    model_name1 = "./Distilbert_FN_classification/"  # Path to the local clone repository
    model1 = AutoModelForSequenceClassification.from_pretrained(model_name1)
    tokenizer1 = AutoTokenizer.from_pretrained(model_name1)

    def predict1_fake(title, text):
        input_str = "<title>" + title + "<content>" + text + "<end>"
        input_ids = tokenizer1.encode_plus(input_str, max_length=512, padding="max_length", truncation=True,
                                           return_tensors="pt")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model1.to(device)
        with torch.no_grad():
            output = model1(input_ids["input_ids"].to(device), attention_mask=input_ids["attention_mask"].to(device))
        return dict(zip(["Fake", "Real"], [x.item() for x in list(torch.nn.Softmax()(output.logits)[0])]))

    # RoBERTa
    model_name2 = "./roberta_FN_classification"  # Path to the local clone repository
    model2 = AutoModelForSequenceClassification.from_pretrained(model_name2)
    tokenizer2 = AutoTokenizer.from_pretrained(model_name2)

    def predict2_fake(title, text):
        input_str = "<title>" + title + "<content>" + text + "<end>"
        input_ids = tokenizer2.encode_plus(input_str, max_length=512, padding="max_length", truncation=True,
                                           return_tensors="pt")
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model2.to(device)
        with torch.no_grad():
            output = model2(input_ids["input_ids"].to(device), attention_mask=input_ids["attention_mask"].to(device))
        return dict(zip(["Fake", "Real"], [x.item() for x in list(torch.nn.Softmax()(output.logits)[0])]))

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

    # st.markdown(f"##### :gray[Article Title]")
    # st.markdown('"' + title + '"')

    # @st.cache_data()#allow_output_mutation=True)
    # url = 'https://edition.cnn.com/africa/live-news/morocco-earthquake-marrakech-09-11-23/index.html'
    # st.write(title)
    # st.write(predict_fake(title,text))

    # Added button to proceed to misinformation analysis
    if st.button('Predict'):
        ###Bert-Based Verification Model
        st.header(f":orange[Bert-Based Verification Service]")
        col1, col2 = st.columns(2)
        with col1:
            # st.header("Legitimate News")
            st.markdown(
                f":green[Legitimate News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(predict_fake(title, text)['Real'])
            # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

        with col2:
            st.markdown(
                f":red[Fake News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(predict_fake(title, text)['Fake'])
        # st.header("Fake News")
        # st.write(f":red[{'%.2f' % int(round(predict_fake(title, text)['Fake'] * 100, 2))}] %")

        labels = 'Legitimate News', 'Fake News'
        sizes = [round(predict_fake(title, text)['Real'] * 100, 2), round(predict_fake(title, text)['Fake'] * 100, 2)]
        fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Bert Verification Service', color=labels,
                     color_discrete_map={'Legitimate News': 'green', 'Fake News': 'red'})
        st.plotly_chart(fig)

        ###Bert-Based Verification Model
        st.header(f":blue[DistilBert-Based Verification Service]")
        col1, col2 = st.columns(2)
        with col1:
            # st.header("Legitimate News")
            st.markdown(
                f":green[Legitimate News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(predict1_fake(title, text)['Real'])
            # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

        with col2:
            st.markdown(
                f":red[Fake News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(predict1_fake(title, text)['Fake'])
        # st.header("Fake News")
        # st.write(f":red[{'%.2f' % int(round(predict_fake(title, text)['Fake'] * 100, 2))}] %")

        labels = 'Legitimate News', 'Fake News'
        sizes = [round(predict1_fake(title, text)['Real'] * 100, 2), round(predict1_fake(title, text)['Fake'] * 100, 2)]
        fig = px.pie(values=sizes, names=labels, hover_name=labels, title='DistilBert Verification Service',
                     color=labels,
                     color_discrete_map={'Legitimate News': 'green', 'Fake News': 'red'})
        st.plotly_chart(fig)

        ###RoBerta-Based Verification Model
        st.header(f":violet[RoBerta-Based Verification Service]")
        col1, col2 = st.columns(2)
        with col1:
            # st.header("Legitimate News")
            st.markdown(
                f":green[Legitimate News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(predict2_fake(title, text)['Real'])
            # st.write(round(predict_fake(title, text)['Real'] * 100, 2))
            # st.write(f":green[{'%.2f' % int(round(predict_fake(title, text)['Real'] * 100, 2))}] %")

        with col2:
            st.markdown(
                f":red[Fake News]")  # we use {}, in case we will select an integer or a float that will be stingified
            st.write(predict2_fake(title, text)['Fake'])
        # st.header("Fake News")
        # st.write(f":red[{'%.2f' % int(round(predict_fake(title, text)['Fake'] * 100, 2))}] %")

        labels = 'Legitimate News', 'Fake News'
        sizes = [round(predict2_fake(title, text)['Real'] * 100, 2), round(predict2_fake(title, text)['Fake'] * 100, 2)]
        fig = px.pie(values=sizes, names=labels, hover_name=labels, title='RoBerta Verification Service', color=labels,
                     color_discrete_map={'Legitimate News': 'green', 'Fake News': 'red'})
        st.plotly_chart(fig)
        st.header(f":rainbow[Historical Analysis by Given URLs]")
        df = pd.read_csv(r'misdet_results.csv',delimiter=',')
        st.dataframe(df)
