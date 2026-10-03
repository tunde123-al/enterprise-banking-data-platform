"""
Power BI Python visual: customer wealth & activity segmentation (K-Means).

Run inside a Power BI Python Visual. The input DataFrame `dataset` must contain
normalised numeric features, for example:

    TotalDepositBalance | LifetimeTransactionVolume | LifetimeTransactionCount

Requirements (Power BI Python environment): pandas, scikit-learn, matplotlib, seaborn.
If sklearn is unavailable the script degrades to a matplotlib scatter.
"""

import matplotlib.pyplot as plt
import pandas as pd

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except Exception:  # pragma: no cover - Power BI runners may lack sklearn
    SKLEARN_AVAILABLE = False

# --- data preparation -------------------------------------------------------
feature_cols = ["TotalDepositBalance", "LifetimeTransactionVolume", "LifetimeTransactionCount"]
for col in feature_cols:
    if col not in dataset.columns:  # noqa: F821  (dataset injected by Power BI)
        dataset[col] = 0.0

features = dataset[feature_cols].fillna(0.0)

N_CLUSTERS = 4
if SKLEARN_AVAILABLE and len(features) >= N_CLUSTERS:
    scaled = StandardScaler().fit_transform(features)
    model = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    dataset["Segment"] = model.fit_predict(scaled)
    labels = {
        0: "High value / active",
        1: "Low value / dormant",
        2: "Mid value / builders",
        3: "High value / inactive",
    }
    dataset["SegmentLabel"] = dataset["Segment"].map(labels)
    title = "Customer segments (K-Means on standardised features)"
else:  # pragma: no cover - fallback when sklearn is not installed
    dataset["SegmentLabel"] = "All customers"
    title = "Customer distribution (sklearn unavailable - showing raw scatter)"

# --- visualisation ----------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
for segment, group in dataset.groupby("SegmentLabel"):
    ax.scatter(
        group["TotalDepositBalance"],
        group["LifetimeTransactionVolume"],
        s=group["LifetimeTransactionCount"].clip(lower=1) * 0.4,
        alpha=0.6,
        label=segment,
    )
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Total deposit balance (USD)")
ax.set_ylabel("Lifetime transaction volume (USD)")
ax.set_title(title)
ax.legend()
plt.tight_layout()
plt.show()  # Power BI renders the active figure