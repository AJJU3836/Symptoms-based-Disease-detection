"""
predictor.py — ML Prediction Module
=====================================
Loads the saved model (.pkl) and metadata, then predicts disease(s)
from a list of symptom names using weighted feature vectors.
"""

import os
import json
import joblib
import numpy as np

BASE       = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE, "disease_model.pkl")
META_PATH  = os.path.join(BASE, "model_meta.json")

_model = None
_meta  = None


def _load():
    global _model, _meta
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "ML model not found. Run: python app/ml/train_model.py"
            )
        _model = joblib.load(MODEL_PATH)
        with open(META_PATH, "r") as f:
            _meta = json.load(f)


def predict_diseases(selected_symptoms: list, top_n: int = 5) -> list:
    """
    Given a list of symptom strings, returns a list of dicts:
        [{"disease": str, "confidence": float, "rank": int}, ...]
    """
    _load()
    from app.ml.preprocess import symptoms_to_vector

    all_symptoms = _meta["all_symptoms"]
    vector = symptoms_to_vector(selected_symptoms, all_symptoms)

    if hasattr(_model, "predict_proba"):
        proba   = _model.predict_proba(vector)[0]
        classes = _model.classes_

        # Sort descending by probability
        top_idx = np.argsort(proba)[::-1][:top_n]
        predictions = []
        rank = 1
        for i in top_idx:
            conf = round(float(proba[i]) * 100, 2)
            if conf > 0.5:   # at least 0.5% probability
                predictions.append({
                    "disease":    str(classes[i]),
                    "confidence": conf,
                    "rank":       rank,
                })
                rank += 1

        if not predictions:
            # Fallback to top class if all probabilities were very small
            top1 = top_idx[0]
            predictions.append({
                "disease":    str(classes[top1]),
                "confidence": round(float(proba[top1]) * 100, 2),
                "rank":       1,
            })
    else:
        pred = _model.predict(vector)[0]
        predictions = [{"disease": str(pred), "confidence": 100.0, "rank": 1}]

    return predictions


def get_disease_info(disease_name: str) -> dict:
    """Returns description and precautions for a disease."""
    import pandas as pd
    desc_path = os.path.join(BASE, "data", "symptom_description.csv")
    prec_path = os.path.join(BASE, "data", "symptom_precaution.csv")

    description = ""
    precautions = []

    try:
        desc_df = pd.read_csv(desc_path)
        row = desc_df[desc_df["Disease"].str.strip().str.lower() == str(disease_name).strip().lower()]
        if not row.empty:
            description = str(row.iloc[0]["Description"])
    except Exception:
        pass

    try:
        prec_df = pd.read_csv(prec_path)
        row = prec_df[prec_df["Disease"].str.strip().str.lower() == str(disease_name).strip().lower()]
        if not row.empty:
            for col in ["Precaution_1", "Precaution_2", "Precaution_3", "Precaution_4"]:
                val = row.iloc[0].get(col, "")
                if val and str(val).strip() and str(val).strip().lower() != "nan":
                    precautions.append(str(val).strip().replace("_", " ").title())
    except Exception:
        pass

    return {"description": description, "precautions": precautions}


def get_model_info() -> dict:
    """Returns model metadata for the admin performance page."""
    _load()
    return _meta
