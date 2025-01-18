# Importing necessary libraries
import pandas as pd
import numpy as np
import nltk
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Read in data
df = pd.read_csv('../youtube-comment-analyzer/Reviews.csv')  # Use your local path here
df = df.head(500)  # Limit to first 500 reviews

# Download NLTK data
nltk.download('punkt')
nltk.download('vader_lexicon')

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to classify sentiment as 'good' or 'bad'
def classify_sentiment(score):
    if score['compound'] >= 0.05:  # Positive sentiment
        return 'good'
    elif score['compound'] <= -0.05:  # Negative sentiment
        return 'bad'
    else:
        return 'neutral'  # Neutral sentiment, if you want to keep track of it

# Run sentiment analysis on the dataset
res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    text = row['Text']
    myid = row['Id']
    vader_score = sia.polarity_scores(text)
    sentiment = classify_sentiment(vader_score)
    res[myid] = {'Text': text, 'Sentiment': sentiment}

# Convert the results to DataFrame
results_df = pd.DataFrame(res).T.reset_index().rename(columns={'index': 'Id'})

# Print out the results
print(results_df[['Id', 'Text', 'Sentiment']])
