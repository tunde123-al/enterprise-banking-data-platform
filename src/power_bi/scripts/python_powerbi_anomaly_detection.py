"""
Power BI Python visual: anomaly detection on transaction amount distribution.

Run inside a Power BI Python Visual. The input DataFrame `dataset` must contain
a numeric `Amount` column (optionally grouped per `AccountID`).

Uses a robust z-score against the median absolute deviation so the detection
is not distorted by the heavy-tailed transaction distribution itself.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

amount = pd.to_numeric(dataset["Amount"], errors="coerce").dropna()  # noqa: F821

if amount.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.text(0.5, 0.5, "No transaction rows", ha="center")
    plt.show()
else:
    median = amount.median()
    mad = np.median(np.abs(amount - median))
    # MAD-based robust z-score; 4.5 threshold is a conservative outlier cut.
    robust_z = 0.6745 * (amount - median) / (mad if mad > 0 else 1.0)
    flags = robust_z.abs() > 4.5
    outlier_count = int(flags.sum())
    tail = amount[flags].max() if outlier_count else median

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(amount, bins=100, color="#4472C4", alpha=0.75)
    ax.axvline(median, color="green", linestyle="--", label=f"Median ${median:,.0f}")
    if outlier_count:
        ax.axvline(tail, color="red", linestyle="--",
                   label=f"Max flagged ${tail:,.0f}")
    ax.set_yscale("log")
    ax.set_xlabel("Transaction amount (USD)")
    ax.set_ylabel("Frequency (log scale)")
    ax.set_title(f"Transaction amount outliers (robust z-score): {outlier_count} flagged")
    ax.legend()
    plt.tight_layout()
    plt.show()  # Power BI renders the active figure