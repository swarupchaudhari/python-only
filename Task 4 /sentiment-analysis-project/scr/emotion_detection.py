"""
emotion_detection.py

Detects specific emotions in text using the NRC Word-Emotion Association
Lexicon (via the `nrclex` package): joy, anger, fear, sadness, trust,
surprise, disgust, anticipation (plus positive/negative affect).
"""

from nrclex import NRCLex

EMOTIONS = [
    "joy", "anger", "fear", "sadness",
    "trust", "surprise", "disgust", "anticipation",
]


def detect_emotions(text: str) -> dict:
    """Return normalized emotion frequency scores for a single text."""
    if not isinstance(text, str) or not text.strip():
        return {e: 0.0 for e in EMOTIONS}

    doc = NRCLex(text)
    freqs = doc.affect_frequencies
    return {e: round(freqs.get(e, 0.0), 4) for e in EMOTIONS}


def top_emotion(text: str) -> str:
    """Return the single dominant emotion for a piece of text (or 'none')."""
    scores = detect_emotions(text)
    if not scores or max(scores.values()) == 0:
        return "none"
    return max(scores, key=scores.get)


def detect_batch(texts) -> list:
    return [detect_emotions(t) for t in texts]


if __name__ == "__main__":
    samples = [
        "I'm so excited and grateful for this amazing surprise!",
        "I'm furious, this is disgusting and completely unacceptable.",
        "I'm terrified about what might happen next.",
    ]
    for s in samples:
        print(s, "->", detect_emotions(s), "| top:", top_emotion(s))

