import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATHS = {
    'processed': os.path.join(BASE_DIR, 'processed'),
    'models': os.path.join(BASE_DIR, 'models'),
    'reports': os.path.join(BASE_DIR, 'reports'),
    'features': os.path.join(BASE_DIR, 'reports/feature_importance/selected_features.csv')
}

MODEL_CONFIG = {
    'n_estimators': 500,
    'max_depth': 12,
    'class_weight': 'balanced',
    'random_state': 42,
    'n_jobs': -1
}