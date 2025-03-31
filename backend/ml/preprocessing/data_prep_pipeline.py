import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
from sklearn.model_selection import TimeSeriesSplit, StratifiedKFold
from sklearn.preprocessing import PowerTransformer
from sklearn.ensemble import IsolationForest
from imblearn.under_sampling import TomekLinks
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import mutual_info_classif, SelectKBest

# Enhanced configuration
RANDOM_STATE = 42
TARGET_COL = 'Disaster Type'
FEATURE_SELECTION_K = 15  # Based on MI scores
SAVE_PATHS = {
    'data': '../processed/',
    'models': '../models/',
    'reports': '../reports/',
    'figures': '../reports/figures/',
    'feature_importance': '../reports/feature_importance/'
}

# Create directories
def create_directories():
    for path in SAVE_PATHS.values():
        os.makedirs(path, exist_ok=True)
create_directories()

def load_and_validate_data():
    """Load and validate processed data"""
    df = pd.read_csv(f"{SAVE_PATHS['data']}disaster_data_processed.csv")
    
    # Validation checks
    assert df.shape[0] == 10330, "Unexpected row count"
    assert TARGET_COL in df.columns, "Target column missing"
    assert pd.api.types.is_integer_dtype(df[TARGET_COL]), \
        "Target must be integer-encoded"
    
    print(f"✅ Data validation passed\nTarget distribution:\n{df[TARGET_COL].value_counts()}")
    return df

def analyze_features(df):
    """Enhanced feature analysis with selection threshold"""
    numerical = df.select_dtypes(include=np.number).columns.tolist()
    
    # Correlation matrix with threshold
    corr_matrix = df[numerical].corr().abs()
    plt.figure(figsize=(18, 12))
    sns.heatmap(corr_matrix.where(corr_matrix > 0.8), annot=False, cmap='coolwarm')
    plt.title("High Correlation Features (>0.8)")
    plt.savefig(f"{SAVE_PATHS['figures']}high_correlation.png")
    plt.close()
    
    # Mutual information feature selection
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL].astype(int)
    selector = SelectKBest(mutual_info_classif, k=FEATURE_SELECTION_K)
    selector.fit(X, y)
    
    selected_features = X.columns[selector.get_support()].tolist()
    print(f"Selected features: {selected_features}")
    
    # Save with proper header
    pd.DataFrame({'feature': selected_features}).to_csv(
        f"{SAVE_PATHS['feature_importance']}selected_features.csv",
        index=False
    )
    
    return df[selected_features + [TARGET_COL]]

def handle_class_imbalance(X, y):
    """Improved balancing preserving natural distribution"""
    class_distribution = {
        4: 3000,  # Original: 4130
        7: 2500,   # Original: 2700
        2: 800,    # Original: 879
        6: 500     # Original: 50
    }
    
    smote = SMOTE(
        sampling_strategy=class_distribution,
        random_state=RANDOM_STATE,
        k_neighbors=5
    )
    X_res, y_res = smote.fit_resample(X, y)
    
    # Gentle cleaning
    tomek = TomekLinks(sampling_strategy='majority')
    X_clean, y_clean = tomek.fit_resample(X_res, y_res)
    
    print(f"Optimized class distribution:\n{y_clean.value_counts()}")
    return X_clean, y_clean



def prepare_datasets(df):
    """Enhanced temporal validation"""
    df = df.sort_values('Entry Year')
    
    # 70-30 split for better test evaluation
    train_size = 0.7
    split_idx = int(len(df) * train_size)
    
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    
    # Outlier detection only on training
    iso = IsolationForest(
        contamination=0.02,  # Slightly higher for disaster data
        random_state=RANDOM_STATE
    )
    train_clean = train[iso.fit_predict(train.drop(TARGET_COL, axis=1)) == 1]
    
    # Prepare final splits
    X_train = train_clean.drop(columns=[TARGET_COL])
    y_train = train_clean[TARGET_COL]
    X_test = test.drop(columns=[TARGET_COL])
    y_test = test[TARGET_COL]
    
    # Save raw splits
    joblib.dump(X_train, f"{SAVE_PATHS['data']}X_train_raw.pkl")
    joblib.dump(y_train, f"{SAVE_PATHS['data']}y_train_raw.pkl")
    
    print("📂 Temporal datasets prepared")
    return X_train, X_test, y_train, y_test

def create_validation_sets(X_train, y_train):
    """Create validation strategies"""
    tscv = TimeSeriesSplit(n_splits=5)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    
    joblib.dump(tscv, f"{SAVE_PATHS['models']}tscv_strategy.pkl")
    joblib.dump(skf, f"{SAVE_PATHS['models']}skf_strategy.pkl")
    
    print("🔄 Validation strategies saved")

def transform_features(X_train, X_test):
    """Feature transformation with selection"""
    # Load selected features
    selected_df = pd.read_csv(f"{SAVE_PATHS['feature_importance']}selected_features.csv")
    selected = selected_df['feature'].tolist()
    
    # Validate features exist
    missing_train = [col for col in selected if col not in X_train.columns]
    missing_test = [col for col in selected if col not in X_test.columns]
    
    if missing_train or missing_test:
        raise ValueError(f"Missing features in data - Train: {missing_train}, Test: {missing_test}")
    
    X_train = X_train[selected]
    X_test = X_test[selected]
    
    pt = PowerTransformer(method='yeo-johnson', standardize=True)
    X_train_trans = pt.fit_transform(X_train)
    X_test_trans = pt.transform(X_test)
    
    joblib.dump(pt, f"{SAVE_PATHS['models']}power_transformer.pkl")
    return X_train_trans, X_test_trans

def run_preparation_pipeline():
    df = load_and_validate_data()
    df = analyze_features(df)  # Now handles feature selection
    X_train, X_test, y_train, y_test = prepare_datasets(df)
    X_balanced, y_balanced = handle_class_imbalance(X_train, y_train)
    create_validation_sets(X_balanced, y_balanced)
    X_train_trans, X_test_trans = transform_features(X_balanced, X_test)
    
    print("\n🚀 Enhanced Preparation Complete!")
    print(f"Training shape: {X_train_trans.shape}, Test shape: {X_test_trans.shape}")
    print(f"Feature names: {pd.read_csv(SAVE_PATHS['feature_importance'] + 'selected_features.csv').values.flatten().tolist()}")

if __name__ == "__main__":
    run_preparation_pipeline()

