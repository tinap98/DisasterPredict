import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.feature_selection import VarianceThreshold

# Configuration
TARGET_COL = 'Disaster Type'  # Add target column definition
INITIAL_DROP_COLS = [
    'Reconstruction Costs (\'000 US$)', 'Reconstruction Costs, Adjusted (\'000 US$)',
    'AID Contribution (\'000 US$)', 'Insured Damage (\'000 US$)', 
    'Insured Damage, Adjusted (\'000 US$)', 'Total Damage (\'000 US$)',
    'Total Damage, Adjusted (\'000 US$)', 'No. Homeless',
    'Latitude', 'Longitude', 'River Basin', 'Event Name', 'External IDs',
    'Associated Types', 'Origin', 'Admin Units', 'Location',
    'Start Day', 'End Day', 'Magnitude Scale'
]

def load_data():
    """Load and initial processing of raw data"""
    file_path = "../datasets/public_emdat.xlsx"
    df = pd.ExcelFile(file_path).parse('EM-DAT Data')
    df.drop(columns=INITIAL_DROP_COLS + ["DisNo."], inplace=True, errors='ignore')
    return df

def process_dates(df):
    """Handle date-related columns"""
    df["Entry Date"] = pd.to_datetime(df["Entry Date"], errors="coerce")
    df["Last Update"] = pd.to_datetime(df["Last Update"], errors="coerce")
    df["Entry Year"] = df["Entry Date"].dt.year
    df["Entry Month"] = df["Entry Date"].dt.month
    df.drop(columns=["Entry Date", "Last Update"], inplace=True)
    return df

def handle_missing_values(df):
    """Impute missing values"""
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Missing')
        else:
            df[col] = df[col].fillna(df[col].median())
    return df

def encode_features(df):
    """Label encode categorical features"""
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        # Handle rare categories
        counts = df[col].value_counts(normalize=True)
        mask = df[col].isin(counts[counts > 0.01].index)
        df.loc[~mask, col] = 'Other'
        
        # Encode and ensure integer type
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str)).astype(int)
    return df

def scale_features(df):
    """Scale numerical features (excluding target)"""
    numerical_cols = df.select_dtypes(include=np.number).columns.drop(TARGET_COL, errors='ignore')
    scaler = RobustScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df

def remove_redundant_features(df):
    """Remove constant features"""
    constant_filter = VarianceThreshold(threshold=0)
    constant_filter.fit(df)
    df = df.loc[:, constant_filter.get_support()]
    return df

def main():
    # Pipeline
    df = load_data()
    df = process_dates(df)
    df = handle_missing_values(df)
    df = encode_features(df)
    df = scale_features(df)
    df = remove_redundant_features(df)
    
    # Final validation
    assert df[TARGET_COL].dtype == np.int64, "Target must be integer-encoded"
    df.to_csv("../processed/disaster_data_processed.csv", index=False)

if __name__ == "__main__":
    main()