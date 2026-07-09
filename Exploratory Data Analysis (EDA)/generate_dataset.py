"""
generate_dataset.py

Generates a synthetic 'customer_transactions.csv' dataset (1000 rows) for
the general-purpose EDA project. Includes realistic messiness on purpose
(missing values, duplicate rows, inconsistent category casing, a handful of
extreme outliers, and a few impossible values) so the "detect data issues"
step in eda.py has real problems to find.
"""

import os
import numpy as np
import pandas as pd
from datetime import timedelta

rng = np.random.default_rng(7)
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "customer_transactions.csv")

N = 1000

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Clothing", "Home & Garden", "Beauty", "Sports", "Books"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Cash"]

start_date = pd.Timestamp("2025-01-01")

customer_id = np.arange(1, N + 1)
age = rng.integers(18, 75, size=N)
gender = rng.choice(["Male", "Female", "Other"], size=N, p=[0.47, 0.47, 0.06])
region = rng.choice(REGIONS, size=N)
category = rng.choice(CATEGORIES, size=N, p=[0.22, 0.2, 0.15, 0.13, 0.15, 0.15])
is_returning = rng.choice([0, 1], size=N, p=[0.55, 0.45])

# Returning customers spend a bit more on average (built-in real signal)
base_amount = rng.gamma(shape=2.2, scale=18, size=N) + is_returning * 8
amount = np.round(base_amount, 2)

quantity = rng.integers(1, 6, size=N)
rating = rng.choice([1, 2, 3, 4, 5], size=N, p=[0.05, 0.08, 0.17, 0.35, 0.35])
payment_method = rng.choice(PAYMENT_METHODS, size=N)

purchase_offsets = rng.integers(0, 180, size=N)
purchase_date = [start_date + timedelta(days=int(d)) for d in purchase_offsets]

df = pd.DataFrame({
    "CustomerID": customer_id,
    "Age": age,
    "Gender": gender,
    "Region": region,
    "PurchaseDate": purchase_date,
    "ProductCategory": category,
    "Amount": amount,
    "Quantity": quantity,
    "Rating": rating,
    "PaymentMethod": payment_method,
    "IsReturningCustomer": is_returning,
})

# --- Inject realistic data issues ---

# 1. Missing values scattered across several columns
for col, frac in [("Age", 0.02), ("Amount", 0.015), ("Rating", 0.03), ("Region", 0.01)]:
    idx = rng.choice(df.index, size=int(N * frac), replace=False)
    df.loc[idx, col] = np.nan

# 2. Inconsistent categorical casing/whitespace (a common real-world issue)
inconsistent_idx = rng.choice(df.index, size=25, replace=False)
df.loc[inconsistent_idx, "Region"] = df.loc[inconsistent_idx, "Region"].str.lower()
inconsistent_idx2 = rng.choice(df.index, size=15, replace=False)
df.loc[inconsistent_idx2, "ProductCategory"] = " " + df.loc[inconsistent_idx2, "ProductCategory"] + " "

# 3. A handful of extreme outliers in Amount
outlier_idx = rng.choice(df.index, size=6, replace=False)
df.loc[outlier_idx, "Amount"] = df.loc[outlier_idx, "Amount"] * rng.uniform(8, 15, size=6)

# 4. A few impossible/invalid values (negative amount, unrealistic age)
bad_idx = rng.choice(df.index, size=4, replace=False)
df.loc[bad_idx[:2], "Amount"] = -abs(df.loc[bad_idx[:2], "Amount"])
df.loc[bad_idx[2:], "Age"] = 130

# 5. Duplicate rows
dupes = df.sample(n=12, random_state=3)
df = pd.concat([df, dupes], ignore_index=True)

# Shuffle
df = df.sample(frac=1, random_state=11).reset_index(drop=True)

df.to_csv(OUTPUT_PATH, index=False)
print(f"Generated {OUTPUT_PATH} with {len(df)} rows (includes intentional data issues)")
