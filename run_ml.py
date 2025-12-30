import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os


def summarize_df(df):
    """Print a very small summary of a DataFrame for quick inspection.

    This helper is intentionally lightweight: it shows shape, dtypes and missing
    value counts so the user can quickly verify column names and detect
    obvious issues before preprocessing.
    """
    print("Shape:", df.shape)
    print("Columns:")
    print(df.dtypes)
    print("Missing values per column:\n", df.isnull().sum())


def preprocess(df, top_n_org=20, top_n_ab=20):
    """Preprocess the raw dataset and return feature matrix X and target y.

    Steps performed:
    - Work on a copy of the DataFrame to avoid side-effects.
    - Parse datetime column `order_time_jittered_utc` and extract calendar features
      (year, month, day, hour, weekday). Jittering should not prevent using
      coarse-grained time features.
    - Coerce the target `resistant_time_to_culturetime` to numeric and drop
      rows where the target is missing or invalid (negative values).
    - Reduce cardinality of categorical columns (`organism`, `antibiotic`) by
      keeping only the `top_n` frequent values and grouping the rest into
      an `Other` category to avoid explosion of one-hot encoded columns.
    - Drop direct identifiers to reduce leakage risk.
    - One-hot encode the retained categorical columns.
    - Impute remaining numeric NaNs with column medians.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw input DataFrame loaded from CSV.
    top_n_org : int
        Number of top frequent organisms to keep; others mapped to 'Other'.
    top_n_ab : int
        Number of top frequent antibiotics to keep; others mapped to 'Other'.

    Returns
    -------
    X : pandas.DataFrame
        Feature matrix ready for model input.
    y : pandas.Series
        Target vector (`resistant_time_to_culturetime`).
    """

    # Work on a copy to keep original raw df intact
    df = df.copy()

    # 1) Datetime parsing and feature extraction
    if 'order_time_jittered_utc' in df.columns:
        # coerce invalid parses to NaT
        df['order_time_jittered_utc'] = pd.to_datetime(df['order_time_jittered_utc'], errors='coerce')
        # Extract common calendar features which may capture seasonal or hourly patterns
        df['year'] = df['order_time_jittered_utc'].dt.year
        df['month'] = df['order_time_jittered_utc'].dt.month
        df['day'] = df['order_time_jittered_utc'].dt.day
        df['hour'] = df['order_time_jittered_utc'].dt.hour
        df['weekday'] = df['order_time_jittered_utc'].dt.weekday

    # 2) Target cleaning: ensure numeric and remove invalid samples
    target = 'resistant_time_to_culturetime'
    # Convert target to numeric (coerce non-numeric to NaN)
    df[target] = pd.to_numeric(df[target], errors='coerce')
    # Drop rows where target is missing
    df = df[df[target].notna()]
    # Drop rows with negative values if they exist (assume negative is invalid)
    df = df[df[target] >= 0]

    # 3) Reduce categorical cardinality for `organism` and `antibiotic`
    for col, topn in [('organism', top_n_org), ('antibiotic', top_n_ab)]:
        if col in df.columns:
            # Keep only the top `topn` frequent categories, map others to 'Other'
            top = df[col].value_counts().nlargest(topn).index
            df[col] = df[col].where(df[col].isin(top), other='Other')
            # Mark as categorical to help memory and later processing
            df[col] = df[col].astype('category')

    # 4) Drop identifier-like columns to avoid leaking information
    drop_cols = [c for c in ['anon_id', 'pat_enc_csn_id_coded', 'order_proc_id_coded', 'order_time_jittered_utc'] if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    # 5) One-hot encode categorical features
    # We selected one-hot because tree-based models handle sparse/dense encoded
    # features well and this is a simple, transparent encoding for teaching.
    cat_cols = [c for c in ['organism', 'antibiotic'] if c in df.columns]
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # 6) Impute remaining numeric NaNs using column medians (robust to outliers)
    # `numeric_only=True` keeps pandas behavior explicit
    df = df.fillna(df.median(numeric_only=True))

    # 7) Separate features and target
    X = df.drop(columns=[target])
    y = df[target]
    return X, y


def main():
    """Main entrypoint: parse arguments, run preprocessing, train and evaluate model.

    The script writes two artifacts to `--outdir`: a `joblib` saved model and a
    short `report.txt` summarizing evaluation metrics.
    """
    parser = argparse.ArgumentParser()
    # Default csv path is set to the dataset location in this workspace; change
    # if you keep the CSV elsewhere.
    parser.add_argument('--csv', type=str, default=r"C:\Users\Sumi\OneDrive\Desktop\Documents\GitHub\ai-assignment\microbiology_cultures_microbial_resistance.csv")
    parser.add_argument('--outdir', type=str, default='ml_project')
    # Sampling options for fast, approximate runs
    parser.add_argument('--sample-frac', type=float, default=None,
                        help='If set, randomly sample this fraction of rows (0-1) before processing.')
    parser.add_argument('--sample-size', type=int, default=None,
                        help='If set, randomly sample this many rows before processing (overrides --sample-frac).')
    args = parser.parse_args()

    # Ensure output directory exists (no-op if already present)
    os.makedirs(args.outdir, exist_ok=True)

    print('Loading CSV (this may take a moment)...')
    # Use low_memory=False to avoid dtype inference issues across chunks
    df = pd.read_csv(args.csv, low_memory=False)

    # If the user requested sampling, take a random sample to speed up
    # preprocessing and model training. `--sample-size` takes precedence
    # over `--sample-frac` when both are provided.
    if args.sample_size is not None:
        n = args.sample_size
        if n <= 0:
            raise ValueError('--sample-size must be > 0')
        n = min(n, len(df))
        print(f'Sampling {n} rows (sample-size) from {len(df)} total rows...')
        df = df.sample(n=n, random_state=42)
    elif args.sample_frac is not None:
        frac = args.sample_frac
        if not (0 < frac <= 1.0):
            raise ValueError('--sample-frac must be between 0 (exclusive) and 1 (inclusive)')
        print(f'Sampling fraction {frac} of rows from {len(df)} total rows...')
        df = df.sample(frac=frac, random_state=42)

    # Quick summary and sampling to help the user confirm the dataset loaded
    print('\n--- Data summary ---')
    summarize_df(df.head(0))
    print('\nSample rows:\n', df.head(10))

    print('\nComputing basic statistics...')
    print(df.describe(include='all'))

    # Preprocess and obtain feature matrix and target vector
    print('\nPreprocessing...')
    X, y = preprocess(df)
    print('Feature matrix shape:', X.shape)

    # Baseline model: predict median target for all samples. This is a simple
    # reference point used to check that our model improves over naive
    # prediction.
    baseline_pred = np.median(y)
    baseline_mae = np.mean(np.abs(y - baseline_pred))

    # Train/test split: we use a single random hold-out for a simple evaluation.
    # For more robust estimates use cross-validation.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest regressor. This is a strong, interpretable baseline
    # for tabular data and works well without feature scaling.
    print('Training RandomForestRegressor...')
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Predict on the held-out test set and compute standard regression metrics
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    print('\n--- Evaluation ---')
    print(f'Baseline MAE (median): {baseline_mae:.3f}')
    print(f'RandomForest MAE: {mae:.3f}')
    print(f'RandomForest RMSE: {rmse:.3f}')
    print(f'RandomForest R2: {r2:.3f}')

    # Persist the trained model artifact and a short text report summarizing
    # the evaluation. These are intentionally minimal; for production use,
    # consider saving preprocessing pipeline objects and version metadata.
    model_path = os.path.join(args.outdir, 'rf_model.joblib')
    joblib.dump(model, model_path)
    print('Saved model to', model_path)

    report = os.path.join(args.outdir, 'report.txt')
    with open(report, 'w', encoding='utf8') as f:
        f.write('Dataset: ' + args.csv + '\n')
        f.write('\nBaseline MAE (median): {:.3f}\n'.format(baseline_mae))
        f.write('RandomForest MAE: {:.3f}\n'.format(mae))
        f.write('RandomForest RMSE: {:.3f}\n'.format(rmse))
        f.write('RandomForest R2: {:.3f}\n'.format(r2))
        f.write('\nModel saved to: {}\n'.format(model_path))
    print('Report saved to', report)


if __name__ == '__main__':
    main()
