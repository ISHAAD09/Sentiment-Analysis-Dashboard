from flask import Flask, render_template, request
from textblob import TextBlob
from wordcloud import WordCloud
from nrclex import NRCLex
import nltk
import os

# Ensure required NLTK corpora
def safe_download(resource, path):
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, quiet=True)

safe_download("punkt", "tokenizers/punkt")
safe_download("wordnet", "corpora/wordnet")
safe_download("averaged_perceptron_tagger", "taggers/averaged_perceptron_tagger")

app = Flask(__name__)

STATIC_DIR = os.path.join(app.root_path, "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Store history (latest 5)
history = []

def analyze_text(text):
    # --- Sentiment Analysis ---
    try:
        blob = TextBlob(text)
        polarity = round(blob.sentiment.polarity, 3)
        subjectivity = round(blob.sentiment.subjectivity, 3)
    except Exception as e:
        print("⚠️ TextBlob error:", e)
        polarity, subjectivity = 0.0, 0.0

    if polarity > 0:
        sentiment = "Positive"
        color = "success"
    elif polarity < 0:
        sentiment = "Negative"
        color = "danger"
    else:
        sentiment = "Neutral"
        color = "secondary"

    # --- WordCloud ---
    try:
        words = text.split()
        if words:
            wordcloud = WordCloud(width=600, height=400, background_color="white").generate(" ".join(words))
            wordcloud.to_file(os.path.join(STATIC_DIR, "wordcloud.png"))
    except Exception as e:
        print("⚠️ WordCloud error:", e)

    # --- Emotion Analysis ---
    emotions = {}
    primary_emotion = None
    try:
        emotion_analyzer = NRCLex(text)
        raw_emotions = emotion_analyzer.raw_emotion_scores
        total = sum(raw_emotions.values())
        if total > 0:
            emotions = {k: round(v / total, 3) for k, v in raw_emotions.items()}
            primary_emotion = max(emotions, key=emotions.get)
    except Exception as e:
        print("⚠️ Emotion error:", e)

    return {
        "text": text,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "sentiment": sentiment,
        "color": color,
        "emotion_labels": list(emotions.keys()),
        "emotion_values": list(emotions.values()),
        "primary_emotion": primary_emotion
    }

@app.route("/", methods=["GET", "POST"])
def index():
    global history
    result = None
    if request.method == "POST":
        text = request.form.get("user_text")
        if text:
            result = analyze_text(text)
            # Save to history (keep latest 5)
            history.insert(0, result)
            history = history[:5]
    return render_template("index.html", result=result, history=history)

if __name__ == "__main__":
    app.run(debug=True)
