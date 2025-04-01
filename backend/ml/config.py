import os
from pathlib import Path

# BASE_DIR now points to the directory containing this file (i.e. backend/ml)
BASE_DIR = Path(__file__).resolve().parent

PATHS = {
    'raw_data': BASE_DIR / 'datasets/public_emdat.xlsx',
    'processed': BASE_DIR / 'processed',
    'models': BASE_DIR / 'models',
    'reports': BASE_DIR / 'reports',
    'features': BASE_DIR / 'reports/feature_importance/selected_features.csv'
}

MODEL_CONFIG = {
    'n_estimators': 500,
    'max_depth': 12,
    'class_weight': 'balanced',
    'random_state': 42,
    'n_jobs': -1
}
