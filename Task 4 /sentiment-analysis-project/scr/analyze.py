"""
analyze.py

End-to-end pipeline:
  1. Load a CSV of text data (Amazon reviews, social posts, news, etc.)
  2. Run sentiment classification (VADER + TextBlob)
  3. Run emotion detection (NRCLex)
  4. Aggregate results into a summary and charts
  5. Save everything to outputs/

Usage:
    python src/analyze.py --input data/sample_reviews.csv --text-col text --date-col date
"""

import argparse
import os
import sys

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__file__))
from sentiment_analysis import analyze_sentiment
from emotion_detection import detect_emotions, top_emotion


def run_pipeline(input_path: str, text_col: str, date_col: str | None, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_path)
    if text_col not in df.columns:
        raise ValueError(f"Column '{text_col}' not found. Available columns: {list(df.columns)}")

    print(f"Loaded {len(df)} rows from {input_path}")

    # --- Sentiment ---
    sentiment_results = df[text_col].apply(analyze_sentiment)
    df["sentiment_label"] = sentiment_results.apply(lambda r: r["label"])
    df["sentiment_compound"] = sentiment_results.apply(lambda r: r["compound"])
    df["textblob_polarity"] = sentiment_results.apply(lambda r: r["textblob_polarity"])

    # --- Emotions ---
    df["top_emotion"] = df[text_col].apply(top_emotion)
    emotion_dicts = df[text_col].apply(detect_emotions)
    emotion_df = pd.DataFrame(list(emotion_dicts))
    df = pd.concat([df, emotion_df.add_prefix("emotion_")], axis=1)

    # --- Save scored results ---
    scored_path = os.path.join(output_dir, "scored_results.csv")
    df.to_csv(scored_path, index=False)
    print(f"Saved scored results -> {scored_path}")

    # --- Sentiment distribution chart ---
    counts = df["sentiment_label"].value_counts().reindex(
        ["positive", "neutral", "negative"], fill_value=0
    )
    plt.figure(figsize=(6, 4))
    colors = ["#4CAF50", "#9E9E9E", "#F44336"]
    plt.bar(counts.index, counts.values, color=colors)
    plt.title("Sentiment Distribution")
    plt.ylabel("Count")
    plt.tight_layout()
    dist_path = os.path.join(output_dir, "sentiment_distribution.png")
    plt.savefig(dist_path)
    plt.close()
    print(f"Saved chart -> {dist_path}")

    # --- Emotion breakdown chart ---
    emotion_means = emotion_df.mean().sort_values(ascending=False)
    plt.figure(figsize=(7, 4))
    plt.bar(emotion_means.index, emotion_means.values, color="#3F51B5")
    plt.title("Average Emotion Breakdown")
    plt.ylabel("Average Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    emo_path = os.path.join(output_dir, "emotion_breakdown.png")
    plt.savefig(emo_path)
    plt.close()
    print(f"Saved chart -> {emo_path}")

    # --- Trend chart (if date column provided) ---
    trend_path = None
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        trend = df.dropna(subset=[date_col]).groupby(date_col)["sentiment_compound"].mean()
        if len(trend) > 1:
            plt.figure(figsize=(8, 4))
            plt.plot(trend.index, trend.values, marker="o", color="#009688")
            plt.axhline(0, color="gray", linestyle="--", linewidth=1)
            plt.title("Sentiment Trend Over Time")
            plt.ylabel("Avg. Compound Sentiment")
            plt.xticks(rotation=45)
            plt.tight_layout()
            trend_path = os.path.join(output_dir, "sentiment_trend.png")
            plt.savefig(trend_path)
            plt.close()
            print(f"Saved chart -> {trend_path}")

    # --- Summary ---
    summary_lines = [
        "SENTIMENT ANALYSIS SUMMARY",
        "=" * 30,
        f"Total records analyzed: {len(df)}",
        "",
        "Sentiment distribution:",
    ]
    for label, count in counts.items():
        pct = 100 * count / len(df) if len(df) else 0
        summary_lines.append(f"  {label:>8}: {count} ({pct:.1f}%)")

    summary_lines.append("")
    summary_lines.append("Top emotions (by average score):")
    for emo, val in emotion_means.items():
        summary_lines.append(f"  {emo:>13}: {val:.3f}")

    if "source" in df.columns:
        summary_lines.append("")
        summary_lines.append("Sentiment by source:")
        by_source = df.groupby("source")["sentiment_label"].value_counts().unstack(fill_value=0)
        summary_lines.append(by_source.to_string())

    summary_text = "\n".join(summary_lines)
    summary_path = os.path.join(output_dir, "summary.txt")
    with open(summary_path, "w") as f:
        f.write(summary_text)
    print(f"Saved summary -> {summary_path}")
    print("\n" + summary_text)

    return df


def main():
    parser = argparse.ArgumentParser(description="Run sentiment + emotion analysis pipeline.")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--text-col", default="text", help="Name of the text column")
    parser.add_argument("--date-col", default=None, help="Optional name of a date column for trend analysis")
    parser.add_argument("--output-dir", default=os.path.join(os.path.dirname(__file__), "..", "outputs"),
                         help="Directory to write outputs to")
    args = parser.parse_args()

    run_pipeline(args.input, args.text_col, args.date_col, args.output_dir)


if __name__ == "__main__":
    main()
