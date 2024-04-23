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
    st.header(f":rainbow[Prediction of Fakeness by Given Text]")
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
    st.markdown(f"### :gray[Article Title]")
    title = st.text_area("Insert some text title here", value="This is a text tile")
    text = st.text_area("Insert some text title context here", value="This is a text context")
    # File upload widget for uploading xlsx files
    uploaded_file = st.file_uploader("Upload a file here", type=["xlsx", "xls", "pdf","docx"])

    len(text[:2000])
    len(text)

    # Added button to proceed to misinformation analysis
    if st.button('Predict'):
        weights_real=(predict_fake(title, text)['Real']*0.1)+(predict1_fake(title, text)['Real']*0.1)+(predict2_fake(title, text)['Real']*0.8)
        weights_fake=(predict_fake(title, text)['Fake'] * 0.1) + (predict1_fake(title, text)['Fake'] * 0.1) + (predict2_fake(title, text)['Fake'] * 0.8)
        if(predict2_fake(title, text)['Real']>predict2_fake(title, text)['Fake']):
            st.markdown(f'According to the verification services, the URL with title: :blue[{title}] is classified as :green[Legitimate]')  # with a 100% certainty.
        else:
            st.markdown(f'According to the verification services, the URL with title: :blue[{title}] is classified as :red[Fake]')  # with a 100% certainty.

        labels = 'Legitimate News', 'Fake News'
        sizes = [round(weights_real* 100, 2), round(weights_fake * 100, 2)]
        fig = px.pie(values=sizes, names=labels, hover_name=labels, title='Average Weights Verification Service Result', color=labels,
                     color_discrete_map={'Legitimate News': 'green', 'Fake News': 'red'})
        st.plotly_chart(fig)
