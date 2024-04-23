import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the JSON data

def draw_wordcloud(word_freq):
    """ Wordcloud dict from the api_data module
    """
    word_freq = {item["text"]: item["weight"] for item in word_freq} # Refactor format

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    # Display the word cloud using Matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


#with open("ww.json", "r") as file:
#    word_freq = json.load(file)["wordcloud"]
#    draw_wordcloud(word_freq)