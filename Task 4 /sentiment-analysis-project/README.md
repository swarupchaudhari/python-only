# Sentiment Analysis Project

Analyze text data from sources like Amazon reviews, social media, and news
sites to classify sentiment (positive / negative / neutral), detect specific
emotions, surface trends in public opinion, and turn the results into
insights for marketing, product development, and social research.

## Features

1. **Sentiment Classification** — Classify any piece of text as
   `positive`, `negative`, or `neutral` using the VADER lexicon (tuned for
   short, informal text like reviews and social posts) with a TextBlob
   fallback/comparison score.
2. **Emotion Detection** — Detect specific emotions (joy, anger, fear,
   sadness, trust, surprise, disgust, anticipation) using the NRC Emotion
   Lexicon via `NRCLex`.
3. **Multi-Source Input** — Works on any CSV of text (Amazon reviews,
   tweets/social posts, news headlines/articles) — just point it at a file
   with a text column.
4. **Trend & Pattern Analysis** — Aggregates sentiment/emotion over time
   (if a date column is present) or by category, and generates charts
   (sentiment distribution, emotion breakdown, trend line).
5. **Actionable Output** — Produces a scored CSV report plus summary
   statistics that can feed into marketing, product, or social-insight
   decisions.

## Project Structure

```
sentiment-analysis-project/
├── README.md
├── requirements.txt
├── data/
│   └── sample_reviews.csv        # example input data
├── src/
│   ├── sentiment_analysis.py     # sentiment classification (VADER + TextBlob)
│   ├── emotion_detection.py      # emotion detection (NRCLex)
│   └── analyze.py                # end-to-end pipeline: load -> analyze -> report -> charts
└── outputs/                      # generated reports & charts land here
```

## Installation

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

## Usage

Run the full pipeline on the sample data:

```bash
python src/analyze.py --input data/sample_reviews.csv --text-col text --date-col date
```

Run on your own data (only `--text-col` is required; `--date-col` is optional):

```bash
python src/analyze.py --input path/to/your_data.csv --text-col review_text
```

This will produce, inside `outputs/`:
- `scored_results.csv` — every row with sentiment label, sentiment score,
  compound VADER score, and top emotion(s)
- `sentiment_distribution.png` — bar chart of positive/negative/neutral counts
- `emotion_breakdown.png` — bar chart of overall emotion frequencies
- `sentiment_trend.png` — line chart of sentiment over time (only if a
  date column is provided)
- `summary.txt` — plain-text summary of key findings

You can also use the modules directly in Python:

```python
from src.sentiment_analysis import analyze_sentiment
from src.emotion_detection import detect_emotions

text = "I absolutely love this product, it exceeded my expectations!"
print(analyze_sentiment(text))   # {'label': 'positive', 'compound': 0.86, ...}
print(detect_emotions(text))     # {'joy': 0.5, 'trust': 0.5, ...}
```

## How It Works

- **Sentiment**: VADER (Valence Aware Dictionary and sEntiment Reasoner)
  scores text using a lexicon plus rules for intensifiers, negation, and
  punctuation/capitalization emphasis — well suited to reviews, tweets, and
  informal writing. The compound score is thresholded (`>= 0.05` positive,
  `<= -0.05` negative, else neutral).
- **Emotion detection**: NRCLex maps words in the text to the NRC Word-Emotion
  Association Lexicon, returning a distribution across 8 core emotions plus
  positive/negative affect.
- **Trends**: When a date column is supplied, daily/weekly average sentiment
  is plotted to reveal shifts in public opinion over time (e.g., around a
  product launch or news event).

## Data Sources

The pipeline is source-agnostic — feed it CSV exports from:
- Amazon / e-commerce review exports
- Twitter/X, Reddit, or other social media exports
- News article headlines or body text

Any CSV with a text column (and optionally a date column) will work.

## Applying the Results

- **Marketing**: identify which messaging or campaigns drive positive
  sentiment and which trigger negative reactions.
- **Product development**: surface recurring complaints (negative +
  "anger"/"disgust" emotion) to prioritize fixes.
- **Social insight**: track how public opinion shifts over time in response
  to events, launches, or news coverage.

## Requirements

See `requirements.txt`. Core libraries: `pandas`, `nltk` (VADER),
`textblob`, `nrclex`, `matplotlib`.

## License

MIT — free to use and adapt.
