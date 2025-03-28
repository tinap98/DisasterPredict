import numpy as np
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix
)
from disaster_preprocessing import DisasterDataPreprocessor

class DisasterPredictionModel:
    def __init__(self, preprocessing_path='ml\datasets\public_emdat.xlsx'):
        self.preprocessor = DisasterDataPreprocessor(preprocessing_path)
        self.model = None
        self.preprocessing_info = None
    
    def train_model(self):
        model_data = self.preprocessor.prepare_model_data()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.model.fit(model_data['X_train'], model_data['y_train'])
        y_pred = self.model.predict(model_data['X_test'])
        metrics = {
            'accuracy': accuracy_score(model_data['y_test'], y_pred),
            'classification_report': classification_report(model_data['y_test'], y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(model_data['y_test'], y_pred).tolist()
        }
        joblib.dump(self.model, 'disaster_prediction_model.joblib')
        with open('disaster_preprocessing_info.json', 'r') as f:
            self.preprocessing_info = json.load(f)
        return metrics
    
    def predict_disaster(self, input_data):
        if self.model is None:
            self.model = joblib.load('disaster_prediction_model.joblib')
        if not self.preprocessing_info:
            with open('disaster_preprocessing_info.json', 'r') as f:
                self.preprocessing_info = json.load(f)
        prepared_input = self._prepare_input(input_data)
        prediction = self.model.predict(prepared_input)
        prediction_proba = self.model.predict_proba(prepared_input)
        return {
            'disaster_likelihood': int(prediction[0]),
            'confidence': float(prediction_proba[0].max()),
            'severity_class': 'High Risk' if prediction[0] == 1 else 'Low Risk'
        }
    
    def _prepare_input(self, input_data):
        df_input = pd.DataFrame([input_data])
        expected_features = self.preprocessing_info['feature_names']
        for feature in expected_features:
            if feature not in df_input.columns:
                df_input[feature] = 0
        df_input = df_input[expected_features]
        for feature, feature_info in self.preprocessing_info['label_encoders'].items():
            le = LabelEncoder()
            le.classes_ = np.array(feature_info['classes'])
            df_input[feature] = df_input[feature].apply(lambda x: x if x in le.classes_ else le.classes_[0])
            df_input[feature] = le.transform(df_input[feature].astype(str))
        scaler = joblib.load('scaler.joblib')
        return scaler.transform(df_input)

if __name__ == '__main__':
    disaster_model = DisasterPredictionModel()
    training_metrics = disaster_model.train_model()
    print("Model Training Metrics:")
    print(json.dumps(training_metrics, indent=2))
    sample_input = {
        'Disaster Group': 'Natural',
        'Disaster Subgroup': 'Meteorological',
        'Disaster Type': 'Storm',
        'Country': 'United States',
        'Region': 'North America',
        'Start Year': 2023,
        'Start Month': 8
    }
    prediction = disaster_model.predict_disaster(sample_input)
    print("\nSample Prediction:")
    print(json.dumps(prediction, indent=2))