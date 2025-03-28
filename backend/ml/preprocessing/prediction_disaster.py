import pandas as pd
import joblib



class DisasterPredictionModel1:

    def __init__(self):
        pass

    def predict_disaster_type(self,test_data):

        # Load the trained model
        with open("disaster_type_model.pkl", "rb") as file:
            model = joblib.load(file)

        # Load the feature names used in training
        with open("features.pkl", "rb") as f:
            train_features = joblib.load(f)

        # Load the Label Encoders
        with open("label_encoders.pkl", "rb") as le_file:
            label_encoders = joblib.load(le_file)

        # Load the correct LabelEncoder for Disaster Type
        disaster_label_encoder = label_encoders.get("Disaster Type")  # Ensure correct column name


        # Ensure test data matches model's expected feature set
        test_data = test_data.reindex(columns=train_features, fill_value=0)

        # Predict using the trained model
        predicted_labels = model.predict(test_data)

        # Convert numerical label to disaster name
        predicted_disasters = disaster_label_encoder.inverse_transform(predicted_labels)

        # Output predictions
        for i, disaster in enumerate(predicted_disasters):
            # print(f"Test Case {i+1}: Predicted Disaster Type - {disaster}")
            print(disaster)
            return disaster
        




        # Sample Test Data (Ensure it follows the encoded format)
