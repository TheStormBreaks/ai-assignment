ML project for microbiology_cultures_microbial_resistance.csv

Usage:

1. Create virtual env and install requirements:

 # Machine Learning Project: Microbiology Cultures — Predicting Time-to-Resistance

## Overview

This repository contains an end-to-end example machine learning project developed for an academic assignment. The goal is to predict `resistant_time_to_culturetime` — a continuous variable measuring the time (presumably in hours or days) from culture collection to when resistance was observed — using microbiology culture records containing organism names, antibiotics, timestamps, and identifiers.

The project demonstrates the full ML workflow: data exploration, cleaning and preprocessing, feature engineering, model selection and justification, training, evaluation, persistence of artifacts, and reproducible instructions to reproduce results locally.

Contents
- `run_ml.py` — main script that loads the CSV, preprocesses data, trains a Random Forest regressor, evaluates it, and writes a brief report and the trained model.
- `requirements.txt` — Python package dependencies.
- `microbiology_cultures_microbial_resistance.csv` — original dataset (not included in this folder by default; use path to your copy).

---

## Dataset Summary

Observed columns (from the provided CSV):

- `anon_id`: anonymized patient identifier.
- `pat_enc_csn_id_coded`: coded encounter/visit identifier.
- `order_proc_id_coded`: coded order or procedure identifier.
- `order_time_jittered_utc`: timestamp of order/collection (UTC, jittered for privacy).
- `organism`: organism name isolated in culture (string; many distinct species and groups).
- `antibiotic`: antibiotic/drug tested (string; many distinct antibiotics; multiple classes).
- `resistant_time_to_culturetime`: numeric target measuring time between culture time and observed resistance (treated as continuous in this project).

Notes and assumptions about the data:

- Timestamps appear timezone-qualified (e.g., `2020-12-18 01:18:00+00:00`). The field name contains `jittered`, indicating the times have been altered slightly for privacy; this still allows extraction of calendar features (year, month, day, hour, weekday).
- `organism` and `antibiotic` are high-cardinality categorical variables. Many rare organisms and antibiotics exist — we handle them by grouping low-frequency categories into an `Other` bucket.
- Some rows may have missing or malformed fields; the pipeline converts numeric fields with coercion and drops invalid target rows.

---

## Project Objective and Problem Formulation

The assignment allows either classification or regression. For this dataset we treat the problem as a regression task:

- Target: `resistant_time_to_culturetime` (continuous). The problem is to predict the expected time to resistance given the organism, antibiotic, and metadata.

Rationale for regression:

- The target is numeric and naturally modeled as continuous.
- Predicting a time value can be useful for planning clinical workflows and prioritizing interventions.

If you prefer a classification framing (e.g., "resistant within X days"), you can convert the target to a binary or multi-class label (thresholding by clinically meaningful time windows) and then choose classification algorithms instead.

---

## Data Exploration and Preprocessing (Implemented in `run_ml.py`)

High-level preprocessing steps included in the script:

1. Loading and basic inspection
	- Uses `pandas.read_csv(..., low_memory=False)` to load the data and inspect datatypes and sample rows.

2. Parsing and extracting time features
	- Parses `order_time_jittered_utc` with `pd.to_datetime(..., errors='coerce')`.
	- Extracts `year`, `month`, `day`, `hour`, and `weekday` for temporal patterns.

3. Target handling
	- Coerces `resistant_time_to_culturetime` to numeric and drops rows where the target is missing or negative.

4. Handling high-cardinality categorical variables
	- For `organism` and `antibiotic`, the code keeps only the top N frequent categories (defaults: top 20 each) and replaces all others with `Other`.
	- Converts these columns to categorical and then one-hot encodes them with `pd.get_dummies(..., drop_first=True)`.

5. Dropping identifiers
	- Drops `anon_id`, `pat_enc_csn_id_coded`, `order_proc_id_coded`, and the raw `order_time_jittered_utc` (after extracting features) to avoid leaking identifiers.

6. Numeric NaN handling
	- Fills remaining numeric NaNs with column medians.

7. Final split
	- Produces `X` (features) and `y` (target) for modeling.

Design choices and justification:

- Grouping low-frequency categories reduces dimensionality and overfitting risk caused by many one-hot columns with few samples.
- One-hot encoding is straightforward for tree-based models; other encodings (target encoding, embeddings) could be used for improved performance in production.
- Median imputation is robust for numeric columns when missingness is not too large.

---

## Model Selection and Justification

Selected algorithm: Random Forest Regressor (`sklearn.ensemble.RandomForestRegressor`).

Why Random Forest (justification):

- Handles mixed data types (after one-hot encoding) and is robust to unscaled features — no feature standardization is needed.
- Naturally models non-linear relationships and interactions between features which are expected in microbiology data (organism × antibiotic interactions).
- Resistant to overfitting in many settings due to ensemble averaging; easy to train and interpret partial feature importances.
- Reasonable default performance without extensive hyperparameter tuning, making it a good choice for initial experiments and educational assignments.

Alternative algorithms to consider:

- Gradient Boosting (XGBoost, LightGBM, CatBoost): often gives superior predictive performance and can handle categorical variables more efficiently; especially valuable if model accuracy is the priority.
- Linear models (Ridge/Lasso): useful as a baseline; they are more interpretable but may underperform if relationships are strongly non-linear.
- Neural networks: useful for large datasets and when learning embeddings for high-cardinality categorical features; higher complexity and training cost.

Model hyperparameters used in this project
- `n_estimators=100`, `random_state=42`, `n_jobs=-1`.

Note: For a production-quality model, perform hyperparameter tuning (grid search / randomized search / Bayesian optimization) and cross-validation.

---

## Training and Evaluation

Train-test split
- The script uses a randomized 80/20 train/test split (`sklearn.model_selection.train_test_split`) with `random_state=42` to produce reproducible splits.

Baseline
- A simple baseline is computed: predict the median of the target for all samples. This baseline MAE serves as a lower bar for performance.

Evaluation metrics (regression)
- Mean Absolute Error (MAE): average absolute error; easy to interpret in the same units as the target.
- Root Mean Squared Error (RMSE): penalizes larger errors more than MAE.
- R-squared (R2): fraction of variance explained by the model.

The script prints and saves these metrics in `report.txt`.

---

## Example output snippet (format)

```
--- Evaluation
Baseline MAE (median): 123.456
RandomForest MAE: 98.123
RandomForest RMSE: 150.456
RandomForest R2: 0.35
```

Interpretation guidance:

- MAE tells you the average absolute deviation between predicted and observed time to resistance. If MAE is large relative to typical clinical decision thresholds, the model may not be suitable for automated decisions.
- R2 values near 0 indicate the model explains little variance; negative values indicate worse than predicting the mean.

---

## Saving Artifacts

- The trained model is saved via `joblib.dump()` to `ml_project/rf_model.joblib` (path configurable via `--outdir`).
- A simple textual report with the evaluation metrics is saved as `ml_project/report.txt`.

---

## How to Run (reproducible instructions)

1. Create a Python virtual environment and install dependencies:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

On non-Windows (bash):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the training script (adjust CSV path if necessary):

```powershell
python run_ml.py --csv "C:\Users\Sumi\OneDrive\Desktop\Documents\GitHub\ai-assignment\microbiology_cultures_microbial_resistance.csv" --outdir C:\Users\Sumi\OneDrive\Desktop\Documents\GitHub\ai-assignment\ml_project\output
```

3. Inspect outputs in the `--outdir` folder (model and `report.txt`).

---

## Suggestions for Extended Analysis

1. Exploratory Data Analysis (EDA)
	- Visualize distribution of `resistant_time_to_culturetime` (histogram + log-scale if heavy-tailed).
	- Analyze frequency of `organism` and `antibiotic` pairs and cross-tabulate to find common combinations.
	- Time-series exploration: trends across `year` and `month`.

2. Better categorical handling
	- Use target encoding (mean encoding) for `organism` and `antibiotic` with proper cross-validation folds to reduce leakage.
	- Consider `CatBoost` or `LightGBM` which support categorical features natively.

3. Imbalanced targets and robust metrics
	- If the target distribution is heavily skewed or contains long tails, consider training on a log-transformed target and back-transforming predictions.
	- Use quantile regression to predict prediction intervals and capture heteroscedasticity.

4. Model selection and hyperparameter tuning
	- Use cross-validated search (RandomizedSearchCV, Optuna) to tune number of trees, max depth, learning rate (for boosting), and regularization parameters.

5. Interpretability and feature importance
	- Use permutation importance, SHAP values, or partial dependence plots to identify which organisms, antibiotics, or temporal features are most predictive.

6. Alternative task framing: classification
	- Convert the problem to predict whether resistance occurs within clinically meaningful windows (e.g., within 7 days) and apply classifiers such as RandomForestClassifier or XGBoost classifier.

---

## Limitations, Ethical & Practical Considerations

- Data quality: clinical datasets are often noisy, contain mislabeling, and may have artifacts introduced by data collection and de-identification (jittering timestamps).
- Data leakage risk: ensure identifiers and features that leak future information are removed; the script drops obvious identifier columns but a deeper audit may be necessary.
- Model generalization: models trained on one institution's data may not generalize to others due to differing laboratory protocols and patient populations.
- Privacy and safety: ensure compliance with institutional review board (IRB) rules and data use agreements when using clinical data. De-identified datasets may still pose re-identification risks when combined with other data.

---

## Reproducibility & Next Steps

- Run the script with the provided commands to reproduce training and evaluation results.
- For a full assignment submission, consider adding a Jupyter notebook that walks through EDA, preprocessing experiments, hyperparameter tuning, and plots of results.

If you want, I can:
- Run the training here and save the produced `report.txt` and `rf_model.joblib` (requires installing packages).
- Add a Jupyter notebook with EDA and more visualizations.
- Convert the regression to a classification experiment and compare results.

---

Author: Project generated by an assistant; adapt and cite as needed for academic work.
