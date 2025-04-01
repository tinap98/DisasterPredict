import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
import logging
from sklearn.model_selection import TimeSeriesSplit, StratifiedKFold
from sklearn.preprocessing import PowerTransformer
from sklearn.ensemble import IsolationForest
from imblearn.under_sampling import TomekLinks
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import mutual_info_classif, SelectKBest

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RANDOM_STATE = 42
TARGET_COL = 'Disaster Type'
FEATURE_SELECTION_K = 15  # Select top 15 features based on mutual information
SAVE_PATHS = {
    'data': '../processed/',
    'models': '../models/',
    'reports': '../reports/',
    'figures': '../reports/figures/',
    'feature_importance': '../reports/feature_importance/'
}

def create_directories():
    for path in SAVE_PATHS.values():
        os.makedirs(path, exist_ok=True)
create_directories()

def load_and_validate_data():
    """Load processed data and run basic validations."""
    file_path = os.path.join(SAVE_PATHS['data'], "disaster_data_processed.csv")
    if not os.path.exists(file_path):
        logging.error("Processed data file not found: %s", file_path)
        raise FileNotFoundError(file_path)
    df = pd.read_csv(file_path)
    if df.empty:
        logging.error("Loaded data is empty.")
        raise ValueError("Data is empty")
    if TARGET_COL not in df.columns:
        logging.error("Target column '%s' missing", TARGET_COL)
        raise ValueError("Target column missing")
    if not pd.api.types.is_integer_dtype(df[TARGET_COL]):
        logging.error("Target column is not integer encoded")
        raise TypeError("Target must be integer-encoded")
    logging.info("Data validation passed. Shape: %s", df.shape)
    logging.info("Target distribution:\n%s", df[TARGET_COL].value_counts())
    return df

def analyze_features(df):
    """Analyze feature correlations and select top features using mutual information."""
    numerical = df.select_dtypes(include=np.number).columns.tolist()
    
    # Plot high correlations
    corr_matrix = df[numerical].corr().abs()
    plt.figure(figsize=(18, 12))
    sns.heatmap(corr_matrix.where(corr_matrix > 0.8), annot=False, cmap='coolwarm')
    plt.title("High Correlation Features (>0.8)")
    high_corr_path = os.path.join(SAVE_PATHS['figures'], "high_correlation.png")
    plt.savefig(high_corr_path)
    plt.close()
    logging.info("High correlation plot saved to %s", high_corr_path)
    
    # Mutual Information feature selection
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL].astype(int)
    selector = SelectKBest(mutual_info_classif, k=FEATURE_SELECTION_K)
    selector.fit(X, y)
    selected_features = X.columns[selector.get_support()].tolist()
    logging.info("Selected features: %s", selected_features)
    
    # Save selected features
    selected_features_path = os.path.join(SAVE_PATHS['feature_importance'], "selected_features.csv")
    pd.DataFrame({'feature': selected_features}).to_csv(selected_features_path, index=False)
    logging.info("Selected features saved to %s", selected_features_path)
    
    return df[selected_features + [TARGET_COL]]

def handle_class_imbalance(X, y):
    """Balance class distribution using SMOTE followed by TomekLinks cleaning."""
    class_distribution = {
        4: 3000,  # Adjusted based on analysis
        7: 2500,
        2: 800,
        6: 500
    }
    smote = SMOTE(sampling_strategy=class_distribution, random_state=RANDOM_STATE, k_neighbors=5)
    X_res, y_res = smote.fit_resample(X, y)
    tomek = TomekLinks(sampling_strategy='majority')
    X_clean, y_clean = tomek.fit_resample(X_res, y_res)
    logging.info("Optimized class distribution:\n%s", y_clean.value_counts())
    return X_clean, y_clean

def prepare_datasets(df):
    """Sort data temporally and perform a train/test split along with outlier removal."""
    if 'Entry Year' not in df.columns:
        logging.error("Entry Year column is missing. Cannot perform temporal split.")
        raise ValueError("Entry Year column missing")
    df = df.sort_values('Entry Year')
    train_size = 0.7
    split_idx = int(len(df) * train_size)
    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()
    
    # Outlier detection on training data
    iso = IsolationForest(contamination=0.02, random_state=RANDOM_STATE)
    mask = iso.fit_predict(train.drop(columns=[TARGET_COL]))
    train_clean = train[mask == 1]
    
    X_train = train_clean.drop(columns=[TARGET_COL])
    y_train = train_clean[TARGET_COL]
    X_test = test.drop(columns=[TARGET_COL])
    y_test = test[TARGET_COL]
    
    # Save splits with consistent naming
    joblib.dump(X_train, os.path.join(SAVE_PATHS['data'], "X_train.pkl"))
    joblib.dump(y_train, os.path.join(SAVE_PATHS['data'], "y_train.pkl"))
    joblib.dump(X_test, os.path.join(SAVE_PATHS['data'], "X_test.pkl"))
    joblib.dump(y_test, os.path.join(SAVE_PATHS['data'], "y_test.pkl"))
    
    logging.info("Temporal datasets prepared. Training shape: %s, Test shape: %s", X_train.shape, X_test.shape)
    return X_train, X_test, y_train, y_test

def create_validation_sets(X_train, y_train):
    """Save TimeSeriesSplit and StratifiedKFold objects for later use."""
    tscv = TimeSeriesSplit(n_splits=5)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    joblib.dump(tscv, os.path.join(SAVE_PATHS['models'], "tscv_strategy.pkl"))
    joblib.dump(skf, os.path.join(SAVE_PATHS['models'], "skf_strategy.pkl"))
    logging.info("Validation strategies saved")

def transform_features(X_train, X_test):
    """Transform features using a PowerTransformer based on the selected feature list."""
    selected_features_path = os.path.join(SAVE_PATHS['feature_importance'], "selected_features.csv")
    selected_df = pd.read_csv(selected_features_path)
    selected = selected_df['feature'].tolist()
    
    missing_train = [col for col in selected if col not in X_train.columns]
    missing_test = [col for col in selected if col not in X_test.columns]
    if missing_train or missing_test:
        logging.error("Missing features in data - Train: %s, Test: %s", missing_train, missing_test)
        raise ValueError(f"Missing features in data - Train: {missing_train}, Test: {missing_test}")
    
    X_train = X_train[selected]
    X_test = X_test[selected]
    
    pt = PowerTransformer(method='yeo-johnson', standardize=True)
    X_train_trans = pt.fit_transform(X_train)
    X_test_trans = pt.transform(X_test)
    
    joblib.dump(pt, os.path.join(SAVE_PATHS['models'], "power_transformer.pkl"))
    return X_train_trans, X_test_trans

def run_preparation_pipeline():
    df = load_and_validate_data()
    df_selected = analyze_features(df)
    X_train, X_test, y_train, y_test = prepare_datasets(df_selected)
    X_balanced, y_balanced = handle_class_imbalance(X_train, y_train)
    create_validation_sets(X_balanced, y_balanced)
    X_train_trans, X_test_trans = transform_features(X_balanced, X_test)
    
    logging.info("Enhanced Preparation Complete!")
    logging.info("Training shape: %s, Test shape: %s", X_train_trans.shape, X_test_trans.shape)
    features = pd.read_csv(os.path.join(SAVE_PATHS['feature_importance'], "selected_features.csv")).values.flatten().tolist()
    logging.info("Feature names: %s", features)

if __name__ == "__main__":
    run_preparation_pipeline()
