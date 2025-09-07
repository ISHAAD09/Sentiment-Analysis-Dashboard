# Sentiment Analysis Dashboard

A Flask-based web application to analyze text sentiment and emotions, visualize results, and generate word clouds.

## Features

- **Polarity & Subjectivity Analysis** using TextBlob
- **Emotion Detection** using NRCLex
- **Word Cloud Generation**
- **History** of last 5 analyses
- **Interactive Charts** using Chart.js
- **Upload .txt files** or input text directly

## Requirements

- Python 3.10+
- Flask
- TextBlob
- nltk
- NRCLex
- WordCloud

## Setup Instructions

1. **Clone the repository**

```bash
https://github.com/ISHAAD09/Sentiment-Analysis-Dashboard.git
cd <Sentiment-Analysis-Dashboard >

##Install dependencies

pip install -r requirements.txt

##Download NLTK corpora

python -m textblob.download_corpora

##Run the app

python app.py

##Open in browser

Visit: http://127.0.0.1:5000

##Folder Structure

sentiment_app/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── (wordcloud.png generated at runtime)
├── requirements.txt
└── README.md

##Usage
1.Enter text or upload a .txt file.
2.Click Analyze.
3.View:
*Polarity & Subjectivity charts
*Emotion bar chart
*Word Cloud
*History of last 5 analyses


