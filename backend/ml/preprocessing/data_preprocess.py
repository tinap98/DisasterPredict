import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.feature_selection import VarianceThreshold
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TARGET_COL = 'Disaster Type'

# Updated list of columns to drop based on domain knowledge and dataset structure
INITIAL_DROP_COLS = [
    "Reconstruction Costs ('000 US$)", "Reconstruction Costs, Adjusted ('000 US$)",
    "AID Contribution ('000 US$)", "Insured Damage ('000 US$)",
    "Insured Damage, Adjusted ('000 US$)", "Total Damage ('000 US$)",
    "Total Damage, Adjusted ('000 US$)", "No. Homeless",
    "Latitude", "Longitude", "River Basin", "Event Name", "External IDs",
    "Associated Types", "Origin", "Admin Units", "Location",
    "Start Day", "End Day", "Magnitude Scale", "DisNo."
]

def load_data():
    """Load the raw Excel file and drop non-essential columns."""
    file_path = "../datasets/public_emdat.xlsx"
    if not os.path.exists(file_path):
        logging.error("File not found: %s", file_path)
        raise FileNotFoundError(file_path)
    try:
        df = pd.read_excel(file_path, sheet_name='EM-DAT Data')
        df.drop(columns=INITIAL_DROP_COLS, inplace=True, errors='ignore')
        logging.info("Data loaded successfully with shape: %s", df.shape)
    except Exception as e:
        logging.error("Error loading data: %s", str(e))
        raise
    return df

def process_dates(df):
    """Convert date columns to datetime and extract useful features."""
    for col in ["Entry Date", "Last Update"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    if "Entry Date" in df.columns:
        df["Entry Year"] = df["Entry Date"].dt.year
        df["Entry Month"] = df["Entry Date"].dt.month
    df.drop(columns=["Entry Date", "Last Update"], errors='ignore', inplace=True)
    return df

def handle_missing_values(df):
    """Impute missing values for numeric and categorical features."""
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Missing')
        else:
            df[col] = df[col].fillna(df[col].median())
    return df

def encode_features(df):
    """Label encode all categorical features, grouping rare levels."""
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        counts = df[col].value_counts(normalize=True)
        mask = df[col].isin(counts[counts > 0.01].index)
        df.loc[~mask, col] = 'Other'
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str)).astype(int)
    return df

def scale_features(df):
    """Scale numerical features (excluding the target)."""
    numerical_cols = df.select_dtypes(include=np.number).columns.drop(TARGET_COL, errors='ignore')
    scaler = RobustScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df

def remove_redundant_features(df):
    """Remove constant features using VarianceThreshold."""
    constant_filter = VarianceThreshold(threshold=0)
    constant_filter.fit(df)
    df = df.loc[:, constant_filter.get_support()]
    return df

def main():
    df = load_data()
    df = process_dates(df)
    df = handle_missing_values(df)
    df = encode_features(df)
    df = scale_features(df)
    df = remove_redundant_features(df)
    
    if TARGET_COL not in df.columns:
        logging.error("Target column '%s' missing after preprocessing", TARGET_COL)
        raise ValueError("Target column missing")
    if df[TARGET_COL].dtype not in [np.int64, np.int32]:
        logging.error("Target column is not integer encoded")
        raise TypeError("Target must be integer-encoded")
    
    output_path = "../processed/disaster_data_processed.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    logging.info("Preprocessed data saved to %s", output_path)

if __name__ == "__main__":
    main()
