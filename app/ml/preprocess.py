"""
preprocess.py — Data Preprocessing Module
==========================================
Loads the symptom-disease CSV dataset, cleans it, encodes symptoms as binary
feature vectors, and returns train/test splits ready for model training.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")


def load_and_preprocess():
    """
    Load dataset.csv, clean it, and return:
        X_train, X_test, y_train, y_test, all_symptoms, all_diseases
    """
    # ── Load dataset ────────────────────────────────────────────────────────
    df = pd.read_csv(os.path.join(DATA_DIR, "dataset.csv"))

    # ── Clean column names & string values ──────────────────────────────────
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    df["Disease"] = df["Disease"].str.strip()

    # ── Extract feature columns (all except 'Disease') ──────────────────────
    symptom_cols = [c for c in df.columns if c != "Disease"]
    all_symptoms = symptom_cols          # list of symptom names
    all_diseases = sorted(df["Disease"].unique().tolist())

    # ── Apply symptom severity weights ──────────────────────────────────────
    try:
        sev_df = pd.read_csv(os.path.join(DATA_DIR, "symptom_severity.csv"))
        sev_df["Symptom"] = sev_df["Symptom"].str.strip()
        weight_map = dict(zip(sev_df["Symptom"], sev_df["weight"]))
        for col in symptom_cols:
            w = weight_map.get(col, 1)
            df[col] = df[col] * w
    except Exception:
        pass   # if severity file missing, use raw binary values

    # ── Feature matrix & labels ─────────────────────────────────────────────
    X = df[symptom_cols].values.astype(np.float32)
    y = df["Disease"].values

    # ── Train / Test split (80 / 20, stratified) ────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"[Preprocess] Dataset shape : {df.shape}")
    print(f"[Preprocess] Train samples : {len(X_train)}")
    print(f"[Preprocess] Test  samples : {len(X_test)}")
    print(f"[Preprocess] Diseases      : {len(all_diseases)}")
    print(f"[Preprocess] Symptoms      : {len(all_symptoms)}")

    return X_train, X_test, y_train, y_test, all_symptoms, all_diseases


def symptoms_to_vector(selected_symptoms, all_symptoms):
    """
    Convert a list of symptom name strings to a weighted feature vector.
    Used at prediction time.
    """
    try:
        sev_path = os.path.join(DATA_DIR, "symptom_severity.csv")
        sev_df = pd.read_csv(sev_path)
        sev_df["Symptom"] = sev_df["Symptom"].str.strip()
        weight_map = dict(zip(sev_df["Symptom"], sev_df["weight"]))
    except Exception:
        weight_map = {}

    # Normalise input: lowercase + replace spaces with underscores
    selected_norm = [s.strip().lower().replace(" ", "_") for s in selected_symptoms]

    vector = []
    for sym in all_symptoms:
        if sym in selected_norm:
            vector.append(float(weight_map.get(sym, 1)))
        else:
            vector.append(0.0)
    return np.array(vector, dtype=np.float32).reshape(1, -1)
