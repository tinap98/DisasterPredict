import pandas as pd
from pathlib import Path
import joblib
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DisasterPredictor:
    def __init__(self):
        # Resolve directories relative to this file (backend/ml/prediction)
        self.models_dir = Path(__file__).resolve().parents[1] / 'models'
        self.reports_dir = Path(__file__).resolve().parents[1] / 'reports'
        
        # Load model artifacts
        try:
            self.model = joblib.load(self.models_dir / 'disaster_classifier.pkl')
            self.transformer = joblib.load(self.models_dir / 'power_transformer.pkl')
            logging.info("Model and transformer loaded successfully.")
        except Exception as e:
            logging.error("Error loading artifacts: %s", str(e))
            raise

        # Load and validate selected features from the feature importance file
        features_file = self.reports_dir / 'feature_importance' / 'selected_features.csv'
        try:
            self.feature_names = pd.read_csv(features_file)['feature'].tolist()
            logging.info(f"✅ Loaded {len(self.feature_names)} features from {features_file}")
        except Exception as e:
            logging.error("Error loading feature names: %s", str(e))
            raise

    def predict(self, input_data):
        try:
            # Validate input features
            missing = [f for f in self.feature_names if f not in input_data]
            if missing:
                error_msg = f'Missing features: {missing}'
                logging.error(error_msg)
                return {'error': error_msg}
            
            # Create DataFrame with correct feature order
            input_df = pd.DataFrame([input_data], columns=self.feature_names)
            
            # Transform features and predict
            transformed = self.transformer.transform(input_df)
            prediction = self.model.predict(transformed)[0]
            probabilities = self.model.predict_proba(transformed)[0]
            
            result = {
                'prediction': int(prediction),
                'confidence': float(probabilities.max()),
                'probabilities': {str(i): float(p) for i, p in enumerate(probabilities)}
            }
            logging.info("Prediction successful.")
            return result
        except Exception as e:
            logging.error("Prediction error: %s", str(e))
            return {'error': str(e)}

if __name__ == "__main__":
    # Test the predictor directly
    logging.info("🚀 Testing Disaster Predictor...")
    
    # Sample input should match the selected features from the updated pipeline:
    # ['Classification Key', 'Disaster Subgroup', 'Disaster Subtype', 'ISO', 'Country',
    #  'Subregion', 'Region', 'Magnitude', 'End Year', 'End Month', 'Total Deaths',
    #  'No. Injured', 'No. Affected', 'Total Affected', 'Entry Year']
    sample_input = {
        "Classification Key": 5,
        "Disaster Subgroup": 2,
        "Disaster Subtype": 1,
        "ISO": 840,
        "Country": 230,
        "Subregion": 15,
        "Region": 3,
        "Magnitude": 4.5,
        "End Year": 2023,      # Updated key: use End Year instead of Start Month
        "End Month": 7,
        "Total Deaths": 10,
        "No. Injured": 50,
        "No. Affected": 1000,
        "Total Affected": 1050,
        "Entry Year": 2023
    }
    
    predictor = DisasterPredictor()
    result = predictor.predict(sample_input)
    logging.info("🔮 Prediction Result:")
    print(result)
