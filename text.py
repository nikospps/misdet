# from transformers import FSMTForConditionalGeneration, FSMTTokenizer
# from transformers import AutoModelForSequenceClassification
# from transformers import AutoTokenizer
# from langdetect import detect
from newspaper import Article
from PIL import Image
import streamlit as st
# import requests
# import torch
# import matplotlib.pyplot as plt
# import plotly.express as px
# from pysentimiento import create_analyzer
# import pandas as pd
# from transformers import pipeline
# Load model directly
# from transformers import AutoTokenizer, AutoModelForSequenceClassification, DistilBertForSequenceClassification
# from transformers import TFAutoModelForSequenceClassification,TFDistilBertForSequenceClassification, TFBertForSequenceClassification
# import tensorflow as tf
import os
# from transformers import pipeline

# os.environ["TOKENIZERS_PARALLELISM"] = "false"
#

# text_classifier = TextClassificationPipeline(model, tokenizer)

def app():
    st.header(f":rainbow[URL Content Insights]")
    # st.markdown("## Prediction of Fakeness by Given URL")
    # background = Image.open('logo.jpg')
    # st.image(background)

    # English to Spain Translation
    # pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")

    # # torch.cuda.empty_cache()
    # model_name = "darkdwine/news_classification_model"
    # model_name = 'Yueh-Huan/news-category-classification-distilbert'# Replace with the model name or path you want to load.
    # # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
    ###Article Preprocess Area
    # st.markdown(f"### Article URL")
    st.markdown(f"### :gray[Article URL]")
    url = st.text_area("Insert some url here",
                       value="https://en.globes.co.il/en/article-yandex-looks-to-expand-activities-in-israel-1001406519")

    # @st.cache_data()#allow_output_mutation=True)
    # url = 'https://edition.cnn.com/africa/live-news/morocco-earthquake-marrakech-09-11-23/index.html'
    # st.write(title)
    # st.write(predict_fake(title,text))

    # Added button to proceed to the respective analysis
    if st.button('Analyze'):
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        text = article.text
        len(text[:2000])
        len(text)

        st.markdown(f"##### :gray[Article Title]")
        st.markdown('"' + title + '"')

        st.markdown(f"##### :blue[Article Text]")
        st.markdown('"' + text + '"')

        # title_news_analyzer = pipeline("text-classification", model="Yueh-Huan/news-category-classification-distilbert")#, from_pt=True)#, return_all_scores=True)
        #
        # prediction = title_news_analyzer.predict(text)
        #
        # typess = prediction[0]['label']
        #
        # st.write(typess)

        # # # Tokenize the text and convert it into the expected format
        # inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        # #
        # # # Pass the inputs to the model for classification
        # outputs = model(inputs)

        # # Access the classification scores
        # logits = outputs.logits
        #
        # # Get the predicted class label
        # predicted_class = logits.argmax().item()
        #
        # # You can also get the class names from the model configuration if available
        # class_names = model.config.id2label
        # predicted_class_name = class_names[h['label']]
        #
        # # Print the results
        # # print("Predicted Class:", predicted_class_name)
        # # print("Predicted Class Score:", logits[0][predicted_class].item())
        # st.write(predicted_class_name)
        # st.write(logits[0][predicted_class].item())



# Load the pre-trained model and tokenizer

# tokenizer = AutoTokenizer.from_pretrained("darkdwine/news_classification_model")
# model = AutoModelForSequenceClassification.from_pretrained("darkdwine/news_classification_model")



# tokenizer = AutoTokenizer.from_pretrained("kartashoffv/news_topic_classification")
# model = AutoModelForSequenceClassification.from_pretrained("kartashoffv/news_topic_classification")

# Define the text you want to classify
# text = "Barcelona Football Club"

# # Tokenize the text and convert it into the expected format
# inputs = tokenizer(text, return_tensors="pt")
#
# # Pass the inputs to the model for classification
# outputs = model(**inputs)
#
# # Access the classification scores
# logits = outputs.logits
#
# # Get the predicted class label
# predicted_class = logits.argmax().item()
#
# # You can also get the class names from the model configuration if available
# class_names = model.config.id2label
# predicted_class_name = class_names[predicted_class]
#
# # Print the results
# print("Predicted Class:", predicted_class_name)
# print("Predicted Class Score:", logits[0][predicted_class].item())
