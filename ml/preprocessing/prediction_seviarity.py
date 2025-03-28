from disaster_prediction_model import DisasterPredictionModel
from prediction_disaster import DisasterPredictionModel1
import json
import pandas as pd


if __name__ == "__main__":

    test_data = pd.DataFrame([{
        'Magnitude': 200, 'Latitude': 14.381, 'Longitude': -90.601,
        'Start Year': 2000, 'Start Month': 1, 'Start Day': 16,
        'Country': 79, 'Region': 1, 'Magnitude Scale': 0
    }])




    seviarity_model = DisasterPredictionModel()
    disaster_model = DisasterPredictionModel1()

    name = disaster_model.predict_disaster_type(test_data)

    training_metrics = seviarity_model.train_model()
    print("Model Training Metrics:")
    print(json.dumps(training_metrics, indent=2))
    sample_input = {
        'Disaster Group': 'Natural',
        'Disaster Subgroup': 'Meteorological',
        'Disaster Type': name,
        'Country': 'United States',
        'Region': 'North America',
        'Start Year': 2023,
        'Start Month': 8
    }
    prediction = seviarity_model.predict_disaster(sample_input)
    print("\nSample Prediction:")
    print(json.dumps(prediction, indent=2))