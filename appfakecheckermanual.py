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

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def app():
    st.header(f":rainbow[Manual Prediction of Fakeness by Given URL]")
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

    ##Sliders
    #bert = st.slider('Choose a weight for the Bert-Based Verification Service', min_value=0, max_value=100,step=1)
    ## st.write('Bert-Based Values:', bert/100)

    #distilbert = st.slider('Choose a weight for the DistilBert-Based Verification Service', min_value=0, max_value=100, step=1)
    ## st.write('DistilBert-Based Values:', distilbert / 100)

    #roberta = st.slider('Choose a weight for the RoBerta-Based Verification Service', min_value=0, max_value=100, step=1)
    ## st.write('RoBerta-Based Values:', roberta / 100)
    ## st.write(total_weights)
    
    #Text Inputs
    bert = st.number_input('Choose a weight for the Bert-Based Verification Service', key='text1')
    distilbert = st.number_input('Choose a weight for the DistilBert-Based Verification Service', key='text2')
    roberta = st.number_input('Choose a weight for the RoBerta-Based Verification Service', key='text3')

    total_weights = ((bert/100)+(distilbert/100)+(roberta/100))
    #if (total_weights == 1):
    #   st.success('The total sum of weights provided equals 100%')

    # Added button to proceed to misinformation analysis
    if st.button('Predict'):
        if (total_weights > 1):
            st.warning('The total sum of weights provided exceeds 100%. Please make the necessary adjustments')
        elif (total_weights < 1):
            st.warning('The total sum of weights provided is less than 100%. Please make the necessary adjustments')
        else:
            weights_real = (predict_fake(title, text)['Real'] * bert) + (predict1_fake(title, text)['Real'] * distilbert) + (
                    predict2_fake(title, text)['Real'] * roberta)
            weights_fake = (predict_fake(title, text)['Fake'] * bert) + (predict1_fake(title, text)['Fake'] * distilbert) + (
                    predict2_fake(title, text)['Fake'] * roberta)
            if (predict2_fake(title, text)['Real'] > predict2_fake(title, text)['Fake']):
                st.markdown(
                    f'According to the verification services, the URL with title: :blue[{title}] is classified as :green[Legitimate]')  # with a 100% certainty.
            else:
                st.markdown(
                    f'According to the verification services, the URL with title: :blue[{title}] is classified as :red[Fake]')  # with a 100% certainty.

            labels = 'Legitimate News', 'Fake News'
            sizes = [round(weights_real * 100, 2), round(weights_fake * 100, 2)]
            fig = px.pie(values=sizes, names=labels, hover_name=labels,
                         title='Average Weights Verification Service Result',
                         color=labels,
                         color_discrete_map={'Legitimate News': 'green', 'Fake News': 'red'})
            st.plotly_chart(fig)
