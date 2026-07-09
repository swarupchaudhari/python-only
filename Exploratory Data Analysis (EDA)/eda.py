"""
eda.py

General-purpose Exploratory Data Analysis pipeline, structured around five
stages:

  1. Ask meaningful questions about the dataset before analysis.
  2. Explore the data structure (variables, data types).
  3. Identify trends, patterns, and anomalies.
  4. Test hypotheses and validate assumptions using statistics + visuals.
  5. Detect potential data issues to flag for further cleaning.

Runs on data/customer_transactions.csv by default but works on any CSV with
minor column-name adjustments.

Usage:
    python src/eda.py --input data/customer_transactions.csv --output-dir outputs
"""

import argparse
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

RESEARCH_QUESTIONS = [
    "Which product categories generate the most revenue and the most orders?",
    "Do returning customers spend more per transaction than new customers?",
    "Does customer age relate to spending amount or product category choice?",
    "Are there seasonal/monthly trends in purchase volume or revenue?",
    "Which regions and payment methods are most common, and does that vary by category?",
    "Are there outlier transactions (unusually large/negative amounts) that need investigation?",
    "Is there a relationship between rating and repeat-purchase behavior?",
]


# --------------------------------------------------------------------------
# 1. Meaningful questions
# --------------------------------------------------------------------------
def print_research_questions():
    print("=" * 70)
    print("STEP 1: MEANINGFUL QUESTIONS TO GUIDE THE ANALYSIS")
    print("=" * 70)
    for i, q in enumerate(RESEARCH_QUESTIONS, 1):
        print(f"  Q{i}. {q}")
    print()


# --------------------------------------------------------------------------
# 2. Explore data structure
# --------------------------------------------------------------------------
def explore_structure(df: pd.DataFrame):
    print("=" * 70)
    print("STEP 2: DATA STRUCTURE")
    print("=" * 70)
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
    print("Columns and dtypes:")
    print(df.dtypes, "\n")
    print("First 5 rows:")
    print(df.head(), "\n")
    print("Summary statistics (numeric columns):")
    print(df.describe(), "\n")
    print("Summary statistics (categorical columns):")
    print(df.describe(include=["object", "str"]), "\n")


# --------------------------------------------------------------------------
# 5. Detect data issues (done early, before trend/hypothesis work, since
#    those steps need clean-ish data to be trustworthy)
# --------------------------------------------------------------------------
def detect_data_issues(df: pd.DataFrame) -> pd.DataFrame:
    print("=" * 70)
    print("STEP 5 (performed early): DATA ISSUE DETECTION")
    print("=" * 70)

    print("Missing values per column:")
    missing = df.isnull().sum()
    print(missing[missing > 0], "\n")

    dupes = df.duplicated().sum()
    print(f"Exact duplicate rows: {dupes}")

    # Inconsistent categorical text (casing/whitespace)
    for col in ["Region", "ProductCategory"]:
        raw_uniques = df[col].dropna().unique()
        normalized = pd.Series(raw_uniques).str.strip().str.title().unique()
        if len(raw_uniques) != len(normalized):
            print(f"Inconsistent text formatting detected in '{col}': "
                  f"{len(raw_uniques)} raw variants -> {len(normalized)} after normalizing "
                  f"(e.g. mixed casing / stray whitespace).")

    # Impossible values
    if "Age" in df.columns:
        bad_age = df[(df["Age"] < 0) | (df["Age"] > 100)]
        print(f"Implausible Age values (<0 or >100): {len(bad_age)}")
    if "Amount" in df.columns:
        negative_amount = df[df["Amount"] < 0]
        print(f"Negative Amount values (invalid for a purchase): {len(negative_amount)}")

    print()
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply fixes for the issues identified above."""
    df = df.copy()

    # Normalize inconsistent text
    for col in ["Region", "ProductCategory", "Gender", "PaymentMethod"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            df.loc[df[col].isin(["Nan", "None"]), col] = np.nan

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"Dropped {before - len(df)} exact duplicate rows.")

    # Fix impossible values by treating them as missing (safer than silently
    # clipping — an implausible Age of 130 or a negative Amount is a data
    # error, not a real extreme value)
    if "Age" in df.columns:
        df.loc[(df["Age"] < 0) | (df["Age"] > 100), "Age"] = np.nan
    if "Amount" in df.columns:
        df.loc[df["Amount"] < 0, "Amount"] = np.nan

    # Drop rows missing critical fields for this analysis
    before = len(df)
    df = df.dropna(subset=["Amount", "Age", "Region"])
    print(f"Dropped {before - len(df)} rows missing critical fields (Amount/Age/Region).")

    df["PurchaseDate"] = pd.to_datetime(df["PurchaseDate"], errors="coerce")
    print(f"Final cleaned shape: {df.shape}\n")
    return df


# --------------------------------------------------------------------------
# 3. Trends, patterns, anomalies
# --------------------------------------------------------------------------
def trends_and_patterns(df: pd.DataFrame, output_dir: str):
    print("=" * 70)
    print("STEP 3: TRENDS, PATTERNS & ANOMALIES")
    print("=" * 70)

    revenue_by_cat = df.groupby("ProductCategory")["Amount"].sum().sort_values(ascending=False)
    orders_by_cat = df["ProductCategory"].value_counts()
    print("Revenue by category:\n", revenue_by_cat.round(2), "\n")
    print("Orders by category:\n", orders_by_cat, "\n")

    monthly = df.set_index("PurchaseDate").resample("ME")["Amount"].sum()
    print("Monthly revenue trend:\n", monthly.round(2), "\n")

    region_payment = pd.crosstab(df["Region"], df["PaymentMethod"])
    print("Region vs payment method counts:\n", region_payment, "\n")

    # Anomaly detection via IQR on Amount
    Q1, Q3 = df["Amount"].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    anomalies = df[(df["Amount"] < lower) | (df["Amount"] > upper)]
    print(f"Amount anomalies (IQR method, bounds [{lower:.2f}, {upper:.2f}]): {len(anomalies)} rows")
    if len(anomalies):
        print(anomalies[["CustomerID", "ProductCategory", "Amount"]].sort_values("Amount", ascending=False).head(10))
    print()

    # --- Charts ---
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(8, 4))
    revenue_by_cat.plot(kind="bar", color="#3F51B5")
    plt.title("Revenue by Product Category")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "revenue_by_category.png"))
    plt.close()

    plt.figure(figsize=(8, 4))
    monthly.plot(kind="line", marker="o", color="#009688")
    plt.title("Monthly Revenue Trend")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "monthly_revenue_trend.png"))
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.boxplot(df["Amount"], vert=True)
    plt.title("Transaction Amount — Outlier Check")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "amount_boxplot.png"))
    plt.close()

    plt.figure(figsize=(6, 4))
    plt.hist(df["Age"], bins=20, color="#FF9800", edgecolor="white")
    plt.title("Customer Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "age_distribution.png"))
    plt.close()

    return revenue_by_cat, orders_by_cat, monthly, anomalies


# --------------------------------------------------------------------------
# 4. Hypothesis testing
# --------------------------------------------------------------------------
def hypothesis_tests(df: pd.DataFrame, output_dir: str):
    print("=" * 70)
    print("STEP 4: HYPOTHESIS TESTING & VALIDATION")
    print("=" * 70)

    # H1: Returning customers spend more per transaction than new customers
    returning = df.loc[df["IsReturningCustomer"] == 1, "Amount"]
    new = df.loc[df["IsReturningCustomer"] == 0, "Amount"]
    t_stat, p_val = stats.ttest_ind(returning, new, equal_var=False)
    print(f"H1: Returning vs new customer spend — "
          f"mean returning=£{returning.mean():.2f}, mean new=£{new.mean():.2f}, "
          f"t={t_stat:.2f}, p={p_val:.4f} "
          f"({'reject H0 — significant difference' if p_val < 0.05 else 'fail to reject H0'})")

    # H2: Age correlates with spending amount
    corr, p_val2 = stats.pearsonr(df["Age"], df["Amount"])
    print(f"H2: Age vs Amount correlation — r={corr:.3f}, p={p_val2:.4f} "
          f"({'significant' if p_val2 < 0.05 else 'not significant'})")

    # H3: Product category and region are independent (chi-square test)
    contingency = pd.crosstab(df["Region"], df["ProductCategory"])
    chi2, p_val3, dof, _ = stats.chi2_contingency(contingency)
    print(f"H3: Region vs ProductCategory independence — chi2={chi2:.2f}, dof={dof}, p={p_val3:.4f} "
          f"({'dependent (reject independence)' if p_val3 < 0.05 else 'independent (fail to reject)'})")

    # H4: Rating differs by returning-customer status (does satisfaction drive loyalty?)
    rating_returning = df.loc[df["IsReturningCustomer"] == 1, "Rating"].dropna()
    rating_new = df.loc[df["IsReturningCustomer"] == 0, "Rating"].dropna()
    t_stat4, p_val4 = stats.ttest_ind(rating_returning, rating_new, equal_var=False)
    print(f"H4: Rating — returning vs new — mean returning={rating_returning.mean():.2f}, "
          f"mean new={rating_new.mean():.2f}, t={t_stat4:.2f}, p={p_val4:.4f} "
          f"({'significant' if p_val4 < 0.05 else 'not significant'})")
    print()

    # Visual support: scatter of Age vs Amount, and box comparison by loyalty
    plt.figure(figsize=(6, 5))
    plt.scatter(df["Age"], df["Amount"], alpha=0.3, color="#673AB7")
    plt.title("Age vs Transaction Amount")
    plt.xlabel("Age")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "age_vs_amount_scatter.png"))
    plt.close()

    plt.figure(figsize=(5, 5))
    plt.boxplot([new, returning], tick_labels=["New", "Returning"])
    plt.title("Spend: New vs Returning Customers")
    plt.ylabel("Amount")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "spend_new_vs_returning.png"))
    plt.close()

    return {
        "returning_vs_new_spend": (t_stat, p_val),
        "age_vs_amount_corr": (corr, p_val2),
        "region_category_chi2": (chi2, p_val3),
        "rating_returning_vs_new": (t_stat4, p_val4),
    }


def write_summary(df, revenue_by_cat, orders_by_cat, anomalies, test_results, output_dir):
    lines = [
        "EDA SUMMARY — Customer Transactions",
        "=" * 40,
        f"Rows analyzed (after cleaning): {len(df)}",
        f"Date range: {df['PurchaseDate'].min().date()} to {df['PurchaseDate'].max().date()}",
        "",
        "Top category by revenue: " + revenue_by_cat.idxmax() +
        f" (£{revenue_by_cat.max():,.2f})",
        "Most frequent category by orders: " + orders_by_cat.idxmax() +
        f" ({orders_by_cat.max()} orders)",
        f"Amount anomalies flagged (IQR): {len(anomalies)}",
        "",
        "Hypothesis test results:",
    ]
    labels = {
        "returning_vs_new_spend": "Returning vs new customer spend (t-test)",
        "age_vs_amount_corr": "Age vs Amount (Pearson correlation)",
        "region_category_chi2": "Region vs Category independence (chi-square)",
        "rating_returning_vs_new": "Rating: returning vs new (t-test)",
    }
    for key, (stat_val, p_val) in test_results.items():
        sig = "SIGNIFICANT (p<0.05)" if p_val < 0.05 else "not significant"
        lines.append(f"  - {labels[key]}: stat={stat_val:.3f}, p={p_val:.4f} -> {sig}")

    text = "\n".join(lines)
    path = os.path.join(output_dir, "summary.txt")
    with open(path, "w") as f:
        f.write(text)
    print(f"Saved summary -> {path}")
    print("\n" + text)


def main():
    parser = argparse.ArgumentParser(description="Run general-purpose EDA pipeline.")
    parser.add_argument("--input", default=os.path.join(os.path.dirname(__file__), "..", "data", "customer_transactions.csv"))
    parser.add_argument("--output-dir", default=os.path.join(os.path.dirname(__file__), "..", "outputs"))
    args = parser.parse_args()

    df_raw = pd.read_csv(args.input)

    print_research_questions()
    explore_structure(df_raw)
    detect_data_issues(df_raw)
    df = clean_data(df_raw)

    revenue_by_cat, orders_by_cat, monthly, anomalies = trends_and_patterns(df, args.output_dir)
    test_results = hypothesis_tests(df, args.output_dir)
    write_summary(df, revenue_by_cat, orders_by_cat, anomalies, test_results, args.output_dir)

    cleaned_path = os.path.join(args.output_dir, "customer_transactions_cleaned.csv")
    df.to_csv(cleaned_path, index=False)
    print(f"\nSaved cleaned dataset -> {cleaned_path}")


if __name__ == "__main__":
    main()
