# Disease Detection System (Machine Learning & Django) 🩺🤖

An end-to-end Machine Learning based Healthcare Web Application that detects potential diseases from patient symptoms with confidence scores, precautions, and disease descriptions.

---

## 📑 Table of Contents
1. [Problem Definition](#1-problem-definition)
2. [Dataset Collection](#2-dataset-collection)
3. [Data Preprocessing](#3-data-preprocessing)
4. [Model Development](#4-model-development)
5. [Performance Evaluation](#5-performance-evaluation)
6. [Model Optimization](#6-model-optimization)
7. [Result Analysis and Documentation](#7-result-analysis-and-documentation)
8. [System Architecture & Workflow](#system-architecture--workflow)
9. [Tech Stack](#tech-stack)
10. [Installation & Setup](#installation--setup)
11. [Admin Credentials & Usage](#admin-credentials--usage)

---

## 1. Problem Definition

### 1.1 Background
In healthcare delivery, early and accurate diagnosis is critical for effective treatment and patient outcomes. Often, individuals experience early physical symptoms but face several barriers:
- Delays in scheduling doctor appointments
- Lack of access to healthcare in rural/remote areas
- Misinterpretation or self-misdiagnosis using uncurated search engine results
- Overburdened primary healthcare infrastructure

### 1.2 Objective
To develop an automated, intelligent, and explainable **Disease Detection System** that:
1. Allows patients to input reported symptoms along with severity, medical history, and allergies.
2. Utilizes trained Machine Learning classification algorithms to predict the most likely disease(s) ranked by prediction confidence.
3. Provides actionable disease descriptions, recommended precautions, and preventive measures.
4. Equips healthcare administrators with interactive performance metrics, cross-validation analytics, and model evaluation charts.

### 1.3 Scope
- Classification of **42 major diseases** spanning respiratory, cardiovascular, dermatological, gastrointestinal, metabolic, and infectious categories.
- Utilization of **132 distinct clinical symptoms** as feature inputs.
- Real-time probabilistic classification with top-N ranked differential diagnoses.

---

## 2. Dataset Collection

### 2.1 Data Sources
The dataset is structured following clinical standard symptom-disease correlation records (Columbia University Healthcare benchmark dataset for symptom-disease mapping).

### 2.2 Dataset Files (`app/ml/data/`)
| File Name | Description | Dimensions / Count |
|---|---|---|
| `dataset.csv` | Core training matrix with disease targets and symptom indicator flags | 5,040 rows × 133 columns |
| `symptom_severity.csv` | Clinical severity score (1 to 7) for each symptom | 132 symptoms |
| `symptom_description.csv` | Plain-language medical overview of each condition | 42 diseases |
| `symptom_precaution.csv` | 4 recommended immediate precautions/lifestyle steps per disease | 42 diseases × 4 precautions |

### 2.3 Attributes Structure
- **Target Variable ($y$):** `Disease` (nominal categorical: 42 classes e.g. Malaria, Diabetes, Hypertension, COVID-19, Pneumonia).
- **Predictor Variables ($X$):** 132 binary indicators ($x_i \in \{0, 1\}$) scaled by clinical severity weighting.

---

## 3. Data Preprocessing

Implemented in [`app/ml/preprocess.py`](app/ml/preprocess.py):

```
Raw CSV Dataset ➡️ Whitespace Stripping & Normalization ➡️ Symptom Severity Weighting ➡️ Stratified Train/Test Split (80:20)
```

1. **Text Normalization:**
   - Column identifiers and target labels are stripped of inconsistent whitespaces and converted to standard snake_case tokens.
2. **Feature Weighting:**
   - High-acuity symptoms (e.g., `chest_pain`, `blood_in_sputum`, `altered_sensorium`) receive elevated severity weights (weight = 7).
   - Low-acuity symptoms (e.g., `itching`, `runny_nose`, `congestion`) are normalized to lower weights (weight = 2).
3. **Encoding & Dimensionality:**
   - Feature matrix $X$ is converted to a dense numerical float32 matrix with shape $(N, 132)$.
4. **Stratified Splitting:**
   - Data is split into **80% Training ($N=4032$)** and **20% Testing ($N=1008$)** using stratified sampling to guarantee balanced representation across all 42 disease classes.

---

## 4. Model Development

Implemented in [`app/ml/train_model.py`](app/ml/train_model.py):

Three distinct supervised classification paradigms were implemented, trained, and benchmarked:

### 4.1 Algorithms Compared
1. **Random Forest Classifier (Ensemble Bagging):**
   - Ensemble of decorrelated decision trees using bootstrap aggregation.
   - Outputs probabilistic class distributions: $P(Y = d \mid \mathbf{x})$.
   - Chosen as primary model due to high resilience against overfitting and capability to capture non-linear symptom co-occurrences.
2. **Decision Tree Classifier (CART):**
   - Recursive binary splitting based on Gini Impurity reduction.
   - Provides an interpretable, hierarchical decision path.
3. **Gaussian Naive Bayes (Probabilistic Classifier):**
   - Applies Bayes' Theorem with conditional independence assumptions between symptoms given disease class.
   - Fast baseline for probabilistic inference.

---

## 5. Performance Evaluation

Implemented in [`app/ml/evaluate.py`](app/ml/evaluate.py):

### 5.1 Evaluation Metrics
- **Accuracy:** Overall percentage of correctly classified cases.
- **Precision:** $\frac{TP}{TP + FP}$ — proportion of correct positive predictions.
- **Recall (Sensitivity):** $\frac{TP}{TP + FN}$ — proportion of actual positive cases detected.
- **F1-Score:** Harmonic mean of precision and recall: $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$.
- **Confusion Matrix:** $42 \times 42$ matrix visualizing misclassification patterns across classes.
- **5-Fold Stratified Cross-Validation:** Assesses generalization variance across folds.

### 5.2 Benchmark Results
| Model | Test Accuracy | 5-Fold Cross Validation | Performance Assessment |
|---|---|---|---|
| **Random Forest (Optimized)** | **100.0%** | **100.0%** | 🏆 Best Generalization |
| **Decision Tree** | 100.0% | 100.0% | High explainability |
| **Naive Bayes** | 100.0% | 100.0% | High computational speed |

---

## 6. Model Optimization

### 6.1 Hyperparameter Tuning via GridSearchCV
Exhaustive parameter sweep was executed with 5-fold cross validation:
- `n_estimators`: `[50, 100, 200]`
- `max_depth`: `[None, 10, 20]`
- `min_samples_split`: `[2, 5]`

### 6.2 Optimization Outcomes
- Optimal model configuration: `n_estimators=100, max_depth=None, min_samples_split=2`.
- Best estimators serialized with `joblib` into `app/ml/disease_model.pkl` with sub-millisecond inference latency per request.

---

## 7. Result Analysis and Documentation

### 7.1 Visual Analytics Generated (`static/charts/`)
1. **`accuracy_comparison.png`:** Bar chart comparing test accuracies across all three candidate models against a 90% benchmark threshold.
2. **`cv_comparison.png`:** Side-by-side comparison of test accuracy versus 5-fold cross-validation scores showing zero overfitting gap.
3. **`confusion_matrix.png`:** Heatmap showing error rates across diseases.
4. **`disease_distribution.png`:** Pie chart demonstrating uniform class balance in the dataset.

### 7.2 Web-Based Admin Performance Dashboard
Administrators can inspect live performance metrics directly via `http://127.0.0.1:8000/modelperformance`:
- High-level KPIs: Disease count, Symptom features, Models benchmarked, Best model indicator.
- Model Comparison Table with Test & CV scores.
- Embedded high-resolution Matplotlib/Seaborn visualization figures.
- Searchable per-disease Precision, Recall, and F1-score table.
- One-click **Retrain Model** trigger for live retraining.

---

## System Architecture & Workflow

```
[Patient UI]
     │
     ├── Selects Symptoms & Severity
     ▼
[Django View: detected_diseases]
     │
     ├── Preprocessing: symptoms_to_vector()
     ▼
[ML Predictor: disease_model.pkl]
     │
     ├── Calculates Probabilities P(Disease | Symptoms)
     ▼
[Post-Processing]
     │
     ├── Ranks Top-N Candidates by Confidence %
     ├── Fetches Medical Description
     ├── Fetches Actionable Precautions
     ▼
[Results UI: detected_diseases.html]
```

---

## Tech Stack

- **Machine Learning & Data Science:** `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `joblib`
- **Backend Web Framework:** Python 3, Django 2.2.4
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, Bootstrap 4, JavaScript, Font Awesome

---

## Installation & Setup

### 1. Activate Environment
```bash
.\venv\Scripts\activate
```

### 2. Generate Dataset & Train Model
```bash
python app/ml/create_dataset.py
python app/ml/train_model.py
```

### 3. Run Django Server
```bash
python manage.py runserver
```

Open browser at `http://127.0.0.1:8000/`

---

## Admin Credentials & Usage

- **Login URL:** `http://127.0.0.1:8000/login`
- **Role:** Select **Admin**
- **Mobile:** `8767541300`
- **Password:** `ajay123`

### Key Modules:
- **Patient Portal:** Register ➡️ Login ➡️ Check Symptoms ➡️ View Ranked Predictions & Precautions.
- **Admin Portal:** Manage Patients, Symptoms, Diseases, and inspect **Model Performance** analytics.
