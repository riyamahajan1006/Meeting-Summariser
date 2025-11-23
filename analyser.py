# analyser.py
from rake_nltk import Rake
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from summa.summarizer import summarize
import re

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def summarise_text(text: str, ratio: float = 0.25) -> str:
    """
    Abstractive/extractive if summa available - uses TextRank (summa).
    If text is short, returns original.
    """
    text = clean_text(text)
    if not text:
        return ""
    if len(text.split()) < 30:
        return text
    try:
        s = summarize(text, ratio=ratio)
        return s if s else text
    except Exception:
        return " ".join(text.split()[:60]) + "..."

def extract_keywords(text: str, top_n: int = 8):
    text = clean_text(text)
    if not text:
        return []
    r = Rake()
    r.extract_keywords_from_text(text)
    phrases = r.get_ranked_phrases()[:top_n]
    return phrases

def sentiment_analysis(text: str):
    text = clean_text(text)
    if not text:
        return {"neg": 0.0, "neu": 0.0, "pos": 0.0, "compound": 0.0}
    analyser = SentimentIntensityAnalyzer()
    return analyser.polarity_scores(text)

def analyse_meeting(text: str):
    text = clean_text(text)
    return {
        "summary": summarise_text(text),
        "keywords": extract_keywords(text),
        "sentiment": sentiment_analysis(text),
        "word_count": len(text.split())
    }
