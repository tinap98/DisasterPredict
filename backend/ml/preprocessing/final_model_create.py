from disaster_prediction_model import DisasterPredictionModel
from prediction_disaster import DisasterPredictionModel1
import json
import pandas as pd
import joblib

if __name__ == "__main__":

    # Load the label encoders for Country and Region
    label_encoders = joblib.load('label_encoders.joblib')  # Adjust the path as needed

    # Test data for prediction
    test_data = pd.DataFrame([{
        'Magnitude': 200, 'Latitude': 14.381, 'Longitude': -90.601,
        'Start Year': 2000, 'Start Month': 1, 'Start Day': 16,
        'Country': 59, 'Region': 2, 'Magnitude Scale': 0
    }])

    # Initialize the models
    seviarity_model = DisasterPredictionModel()
    disaster_model = DisasterPredictionModel1()

    # Predict the disaster type using the disaster_model
    name = disaster_model.predict_disaster_type(test_data)

    # Extract encoded country and region values
    c = test_data['Country'].iloc[0]
    r = test_data['Region'].iloc[0]

    # Access the country and region encoders
    country_encoder = label_encoders['Country']
    region_encoder = label_encoders['Region']

    # Convert numeric values to actual country and region names using the label encoders
    country_name = country_encoder['classes'][c]  # Manual reverse transformation
    region_name = region_encoder['classes'][r]    # Manual reverse transformation
    
    # Print the predicted disaster type, country, and region with actual names
    print(f"Disaster Type  : {name}")
    print(f"Country        : {country_name}")
    print(f"Region         : {region_name}\n")
    
    # Train the severity model and get training metrics
    training_metrics = seviarity_model.train_model()
    # print("Model Training Metrics:")
    # print(json.dumps(training_metrics, indent=2))
    
    # Prepare sample input for severity prediction
    sample_input = {
        'Disaster Type': name,
        'Country': country_name,
        'Region': region_name,
        'Start Year': 2023,
        'Start Month': 8
    }
    
    # Predict the severity of the disaster
    prediction = seviarity_model.predict_disaster(sample_input)
    print("\nSample Prediction:")
    print(json.dumps(prediction, indent=2))
