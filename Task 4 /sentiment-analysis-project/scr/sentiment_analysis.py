"""
sentiment_analysis.py

Lexicon-based sentiment classification using VADER (primary) with a
TextBlob polarity score included for comparison/cross-validation.

Classifies text as: positive, negative, or neutral.
"""

import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

_vader = None


def _get_vader():
    """Lazily initialize the VADER analyzer, downloading its lexicon if needed."""
    global _vader
    if _vader is None:
        try:
            _vader = SentimentIntensityAnalyzer()
        except LookupError:
            import nltk
            nltk.download("vader_lexicon")
            _vader = SentimentIntensityAnalyzer()
    return _vader


def clean_text(text: str) -> str:
    """Light cleaning: strip URLs/mentions/extra whitespace, keep emphasis
    (caps, punctuation) intact since VADER uses those signals."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def classify_compound(compound: float) -> str:
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    return "neutral"


def analyze_sentiment(text: str) -> dict:
    """Return sentiment label + scores for a single piece of text."""
    cleaned = clean_text(text)
    vader = _get_vader()
    scores = vader.polarity_scores(cleaned)
    label = classify_compound(scores["compound"])

    blob_polarity = TextBlob(cleaned).sentiment.polarity

    return {
        "label": label,
        "compound": scores["compound"],
        "pos": scores["pos"],
        "neu": scores["neu"],
        "neg": scores["neg"],
        "textblob_polarity": round(blob_polarity, 4),
    }


def analyze_batch(texts) -> list:
    """Analyze a list/Series of texts, returning a list of result dicts."""
    return [analyze_sentiment(t) for t in texts]


if __name__ == "__main__":
    samples = [
        "I absolutely love this product, it exceeded my expectations!",
        "This is the worst experience I've had with a brand, never again.",
        "It's an average day, nothing special.",
    ]
    for s in samples:
        print(s, "->", analyze_sentiment(s))
