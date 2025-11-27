# analyser.py
"""
Analyser module for Meeting Summariser
Uses BART LLM for abstractive summary and keyword extraction + sentiment.
"""

from transformers import BartTokenizer, BartForConditionalGeneration
from rake_nltk import Rake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import re
import nltk

# Download required punkt (only first time)
nltk.download("punkt")

# Load BART (first time takes time)
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def clean_text(text: str) -> str:
    """Remove emojis and unwanted symbols before JSON save."""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # remove non-ascii
    return text.strip()

def summarise_text(text: str, max_words=120) -> str:
    """Generate abstractive LLM summary with selected word limit."""
    inputs = tokenizer.encode(
        text, return_tensors="pt", max_length=1024, truncation=True
    )
    summary_ids = model.generate(
        inputs,
        max_length=max_words,
        min_length=max_words // 2,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def extract_keywords(text: str):
    """Keyword extraction using RAKE."""
    r = Rake()
    r.extract_keywords_from_text(text)
    return r.get_ranked_phrases()[:10]

def sentiment_details(text: str) -> dict:
    """Detailed sentiment analysis with % distribution."""
    analyzer = SentimentIntensityAnalyzer()
    sentences = nltk.sent_tokenize(text)

    pos = neu = neg = 0
    for sentence in sentences:
        score = analyzer.polarity_scores(sentence)["compound"]
        if score >= 0.05:
            pos += 1
        elif score <= -0.05:
            neg += 1
        else:
            neu += 1

    total = len(sentences) if len(sentences) > 0 else 1

    return {
        "positive_percent": round((pos / total) * 100, 2),
        "neutral_percent": round((neu / total) * 100, 2),
        "negative_percent": round((neg / total) * 100, 2),
        "dominant_sentiment": (
            "Positive" if pos > max(neu, neg)
            else "Negative" if neg > max(neu, pos)
            else "Neutral"
        )
    }

def text_stats(text: str) -> dict:
    """Count words & sentences."""
    words = len(text.split())
    sentences = len(nltk.sent_tokenize(text))
    return {"word_count": words, "sentence_count": sentences}

def analyse(text: str, summary_words=120) -> dict:
    """Return proper JSON response for frontend."""
    summary = clean_text(summarise_text(text, summary_words))
    keywords = extract_keywords(text)
    sentiment = sentiment_details(text)
    stats = text_stats(text)

    return {
        "summary": summary,
        "keywords": keywords,
        "sentiment": sentiment,
        "stats": stats
    }

def save_output_to_json(text: str, filename="analysed_output.json"):
    """Write clean JSON to file."""
    data = analyse(text)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return filename


# Allow CLI run (optional)
if __name__ == "__main__":
    sample = input("Paste transcript: ")
    print(analyse(sample))
