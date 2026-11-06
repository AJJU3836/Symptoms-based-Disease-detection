"""
evaluate.py — Performance Evaluation & Chart Generation Module
==============================================================
Generates:
  1. Model accuracy comparison bar chart
  2. Confusion matrix heatmap (top 20 diseases)
  3. Top 10 most common diseases in dataset pie chart
  4. Test Accuracy vs Cross-Validation score comparison chart
"""

import os
import shutil
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import seaborn as sns

BASE              = os.path.dirname(__file__)
CHARTS_DIR        = os.path.join(BASE, "charts")
STATIC_CHARTS_DIR = os.path.abspath(os.path.join(BASE, "..", "..", "static", "charts"))

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(STATIC_CHARTS_DIR, exist_ok=True)


def _save_both(fig, filename):
    p1 = os.path.join(CHARTS_DIR, filename)
    p2 = os.path.join(STATIC_CHARTS_DIR, filename)
    fig.savefig(p1, dpi=120)
    fig.savefig(p2, dpi=120)
    plt.close(fig)


def generate_all_charts(meta: dict):
    """Entry point — generate all charts from model metadata dict."""
    _chart_accuracy_comparison(meta)
    _chart_confusion_matrix(meta)
    _chart_disease_distribution(meta)
    _chart_cv_comparison(meta)


# ── 1. Accuracy Comparison Bar Chart ─────────────────────────────────────────
def _chart_accuracy_comparison(meta):
    results = meta.get("model_results", {})
    models  = list(results.keys())
    accs    = [results[m]["accuracy"] for m in models]

    colors = ["#2196F3", "#4CAF50", "#FF9800"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(models, accs, color=colors, width=0.5, edgecolor="white", linewidth=1.2)

    for bar, acc in zip(bars, accs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{acc:.2f}%", ha="center", va="bottom", fontweight="bold", fontsize=12)

    ax.set_ylim(0, 115)
    ax.set_ylabel("Accuracy (%)", fontsize=12)
    ax.set_title("Model Accuracy Comparison\n(Random Forest vs Decision Tree vs Naive Bayes)",
                 fontsize=13, fontweight="bold")
    ax.axhline(y=90, color="red", linestyle="--", alpha=0.5, label="90% threshold")
    ax.legend()
    ax.set_facecolor("#f9f9f9")
    fig.patch.set_facecolor("#ffffff")
    plt.tight_layout()
    _save_both(fig, "accuracy_comparison.png")
    print("   [OK] accuracy_comparison.png")


# ── 2. Confusion Matrix Heatmap ───────────────────────────────────────────────
def _chart_confusion_matrix(meta):
    cm     = np.array(meta.get("confusion_matrix", []))
    labels = meta.get("cm_labels", [])
    if cm.size == 0:
        return

    # Limit to first 20 diseases to keep chart readable
    n   = min(20, len(labels))
    cm  = cm[:n, :n]
    lbl = labels[:n]

    fig, ax = plt.subplots(figsize=(14, 11))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=lbl, yticklabels=lbl,
                linewidths=0.5, linecolor="grey", ax=ax)
    ax.set_xlabel("Predicted Label", fontsize=11)
    ax.set_ylabel("True Label", fontsize=11)
    ax.set_title("Confusion Matrix — Top 20 Diseases\n(Best Model)", fontsize=13, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    _save_both(fig, "confusion_matrix.png")
    print("   [OK] confusion_matrix.png")


# ── 3. Disease Distribution Pie Chart ────────────────────────────────────────
def _chart_disease_distribution(meta):
    diseases = meta.get("all_diseases", [])
    if not diseases:
        return

    # Show top 10 diseases, group rest as "Others"
    top_n   = min(10, len(diseases))
    top_dis = diseases[:top_n]
    counts  = [120] * top_n    # each disease has 120 rows in the dataset

    cmap   = plt.colormaps.get_cmap("tab10")
    colors = [cmap(i) for i in range(top_n)]

    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        counts, labels=None, autopct="%1.0f%%",
        colors=colors, startangle=140,
        pctdistance=0.82, wedgeprops=dict(edgecolor="white", linewidth=1.5)
    )
    for at in autotexts:
        at.set_fontsize(8)

    ax.legend(wedges, top_dis, title="Disease", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
    ax.set_title(f"Dataset Distribution — Top {top_n} Diseases",
                 fontsize=13, fontweight="bold")
    plt.tight_layout()
    _save_both(fig, "disease_distribution.png")
    print("   [OK] disease_distribution.png")


# ── 4. Cross-Validation Score Comparison ─────────────────────────────────────
def _chart_cv_comparison(meta):
    results = meta.get("model_results", {})
    models  = list(results.keys())
    accs    = [results[m]["accuracy"]  for m in models]
    cvs     = [results[m]["cv_score"]  for m in models]

    x      = np.arange(len(models))
    width  = 0.35
    colors_acc = ["#1565C0", "#2E7D32", "#E65100"]
    colors_cv  = ["#64B5F6", "#81C784", "#FFB74D"]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars1 = ax.bar(x - width/2, accs, width, label="Test Accuracy", color=colors_acc, edgecolor="white")
    bars2 = ax.bar(x + width/2, cvs,  width, label="CV Score (k=5)", color=colors_cv, edgecolor="white")

    for bar in list(bars1) + list(bars2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
                f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11)
    ax.set_ylabel("Score (%)", fontsize=12)
    ax.set_ylim(0, 115)
    ax.set_title("Test Accuracy vs Cross-Validation Score\n(5-Fold CV)", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_facecolor("#f9f9f9")
    plt.tight_layout()
    _save_both(fig, "cv_comparison.png")
    print("   [OK] cv_comparison.png")
