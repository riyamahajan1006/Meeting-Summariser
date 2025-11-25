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

# Load BART (first time takes time)
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def clean_text(text: str) -> str:
    """Remove emojis and unwanted symbols before JSON save."""
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # remove non-ascii
    return text.strip()

def summarise_text(text: str) -> str:
    """Generate abstractive LLM summary."""
    inputs = tokenizer.encode(
        text, return_tensors="pt", max_length=1024, truncation=True
    )
    summary_ids = model.generate(
        inputs,
        max_length=160,
        min_length=60,
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

def analyse_sentiment(text: str) -> str:
    """Sentiment using VADER (Positive / Neutral / Negative)."""
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def analyse(text: str) -> dict:
    """Return proper JSON response for frontend."""
    summary = clean_text(summarise_text(text))
    keywords = extract_keywords(text)
    sentiment = analyse_sentiment(text)

    return {
        "summary": summary,
        "keywords": keywords,
        "sentiment": sentiment
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
