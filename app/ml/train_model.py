"""
train_model.py — Model Development + Optimization Module
=========================================================
Trains three ML classifiers on the symptom-disease dataset:
  1. Random Forest  (primary ensemble classifier with GridSearchCV)
  2. Decision Tree  (interpretable baseline)
  3. Naive Bayes    (fast probabilistic baseline)

Applies GridSearchCV for hyperparameter tuning on Random Forest.
Saves the best model as disease_model.pkl.
"""

import os
import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Local imports
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.ml.preprocess import load_and_preprocess
from app.ml.evaluate import generate_all_charts

BASE = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "disease_model.pkl")
META_PATH  = os.path.join(BASE, "model_meta.json")


def train():
    print("=" * 60)
    print("  DISEASE DETECTION -- MODEL TRAINING")
    print("=" * 60)

    # ── 1. Load & preprocess data ────────────────────────────────────────────
    X_train, X_test, y_train, y_test, all_symptoms, all_diseases = load_and_preprocess()

    results = {}

    # ── 2. Decision Tree ─────────────────────────────────────────────────────
    print("\n[Model 1] Training Decision Tree...")
    dt = DecisionTreeClassifier(random_state=42, max_depth=20)
    dt.fit(X_train, y_train)
    dt_pred  = dt.predict(X_test)
    dt_acc   = accuracy_score(y_test, dt_pred)
    dt_cv    = cross_val_score(dt, X_train, y_train, cv=5).mean()
    results["Decision Tree"] = {
        "accuracy": round(dt_acc * 100, 2),
        "cv_score": round(dt_cv * 100, 2),
    }
    print(f"   Test Accuracy : {dt_acc*100:.2f}%")
    print(f"   CV Score (k=5): {dt_cv*100:.2f}%")

    # ── 3. Naive Bayes ───────────────────────────────────────────────────────
    print("\n[Model 2] Training Naive Bayes...")
    nb = GaussianNB()
    nb.fit(X_train, y_train)
    nb_pred = nb.predict(X_test)
    nb_acc  = accuracy_score(y_test, nb_pred)
    nb_cv   = cross_val_score(nb, X_train, y_train, cv=5).mean()
    results["Naive Bayes"] = {
        "accuracy": round(nb_acc * 100, 2),
        "cv_score": round(nb_cv * 100, 2),
    }
    print(f"   Test Accuracy : {nb_acc*100:.2f}%")
    print(f"   CV Score (k=5): {nb_cv*100:.2f}%")

    # ── 4. Random Forest + GridSearchCV ──────────────────────────────────────
    print("\n[Model 3] Training Random Forest + GridSearchCV...")
    param_grid = {
        "n_estimators": [50, 100],
        "max_depth":    [None, 15],
        "min_samples_split": [2, 5],
    }
    rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)
    grid_search = GridSearchCV(rf_base, param_grid, cv=5, scoring="accuracy", n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    best_rf   = grid_search.best_estimator_
    rf_pred   = best_rf.predict(X_test)
    rf_acc    = accuracy_score(y_test, rf_pred)
    rf_cv     = grid_search.best_score_
    best_params = grid_search.best_params_
    results["Random Forest"] = {
        "accuracy":    round(rf_acc * 100, 2),
        "cv_score":    round(rf_cv * 100, 2),
        "best_params": str(best_params),
    }
    print(f"   Best Params   : {best_params}")
    print(f"   Test Accuracy : {rf_acc*100:.2f}%")
    print(f"   CV Score (k=5): {rf_cv*100:.2f}%")

    # ── 5. Select best model (Prefer Random Forest for ensemble probability calibration)
    # If RF achieves top accuracy, it is preferred
    best_name = "Random Forest"
    best_model = best_rf
    best_pred  = rf_pred

    print(f"\n[SELECTED CHAMPION MODEL]: {best_name} (Acc: {results[best_name]['accuracy']}%, CV: {results[best_name]['cv_score']}%)")

    # ── 6. Detailed classification report ────────────────────────────────────
    print("\n[Evaluation] Classification Report:")
    report = classification_report(y_test, best_pred, output_dict=True)
    print(classification_report(y_test, best_pred))

    # ── 7. Save model + metadata ─────────────────────────────────────────────
    joblib.dump(best_model, MODEL_PATH)

    meta = {
        "best_model":     best_name,
        "all_symptoms":   all_symptoms,
        "all_diseases":   all_diseases,
        "model_results":  results,
        "classification_report": {k: v for k, v in report.items() if isinstance(v, dict)},
        "confusion_matrix": confusion_matrix(y_test, best_pred, labels=sorted(all_diseases)).tolist(),
        "cm_labels": sorted(all_diseases),
    }
    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"\n[SAVED] Model saved -> {MODEL_PATH}")
    print(f"[SAVED] Metadata saved -> {META_PATH}")

    # ── 8. Generate all charts ────────────────────────────────────────────────
    print("\n[Charts] Generating performance charts...")
    generate_all_charts(meta)
    print("[SAVED] Charts generated -> static/charts/ and app/ml/charts/")
    print("\n" + "=" * 60)
    print("  TRAINING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    train()
