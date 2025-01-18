# Importing necessary libraries
import pandas as pd
import numpy as np
import nltk
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify
from flask_cors import CORS

# Download NLTK data
nltk.download('punkt')
nltk.download('vader_lexicon')

# Initialize the Flask app and CORS
app = Flask(__name__)
CORS(app)

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to classify sentiment as 'good' or 'bad'
def classify_sentiment(score):
    if score['compound'] >= 0.05:  # Positive sentiment
        return 'good'
    elif score['compound'] <= -0.05:  # Negative sentiment
        return 'bad'
    else:
        return 'neutral'  # Neutral sentiment

# API endpoint for sentiment analysis
@app.route('/analyze', methods=['POST'])
def analyze_comments():
    data = request.json
    comments = data.get('comments', [])
    
    res = {}
    for i, text in enumerate(comments):
        vader_score = sia.polarity_scores(text)
        sentiment = classify_sentiment(vader_score)
        res[i] = {'Text': text, 'Sentiment': sentiment}
    
    # Convert the results to DataFrame
    results_df = pd.DataFrame(res).T.reset_index().rename(columns={'index': 'Id'})
    
    return jsonify(results_df.to_dict(orient='records'))

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
