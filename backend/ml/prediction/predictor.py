import os
import sys
import joblib
import numpy as np
import pandas as pd

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.config import PATHS  # Adjusted import path

class DisasterPredictor:
    def __init__(self):
        # Load model and transformer
        self.model = joblib.load(os.path.join(PATHS['models'], 'disaster_classifier.pkl'))
        self.transformer = joblib.load(os.path.join(PATHS['models'], 'power_transformer.pkl'))
        
        # Load feature names
        self.feature_names = pd.read_csv(PATHS['features'])['feature'].tolist()

    def predict(self, input_data):
        try:
            # Validate input features
            if not all(feat in input_data for feat in self.feature_names):
                missing = [feat for feat in self.feature_names if feat not in input_data]
                raise ValueError(f"Missing features: {missing}")
            
            # Prepare feature array
            features = [input_data[feat] for feat in self.feature_names]
            
            # Transform and predict
            transformed = self.transformer.transform([features])
            prediction = self.model.predict(transformed)[0]
            probabilities = self.model.predict_proba(transformed)[0]
            
            return {
                'disaster_type': int(prediction),
                'confidence': float(np.max(probabilities)),
                'probabilities': {str(i): float(p) for i, p in enumerate(probabilities)}
            }
        except Exception as e:
            return {'error': str(e)}

# For testing purposes
if __name__ == "__main__":
    predictor = DisasterPredictor()
    sample_input = {
        'Classification Key': 5,
        'Disaster Subgroup': 2,
        'Disaster Subtype': 1,
        'ISO': 840,
        'Country': 230,
        'Subregion': 15,
        'Region': 3,
        'Magnitude': 4.5,
        'Start Month': 7,
        'End Month': 7,
        'Total Deaths': 10,
        'No. Injured': 50,
        'No. Affected': 1000,
        'Total Affected': 1050,
        'Entry Year': 2023
    }
    print("Sample prediction:", predictor.predict(sample_input))