import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import json
import joblib

class DisasterDataPreprocessor:
    def __init__(self, filepath):
        """
        Initialize the preprocessor with the disaster dataset
        
        Args:
            filepath (str): Path to the Excel file containing disaster data
        """
        # Read the Excel file
        self.df = pd.read_excel('ml\datasets\public_emdat.xlsx')
        
        # Preprocessing configuration
        self.preprocessing_config = {
            'key_features': [
                'Disaster Group', 'Disaster Subgroup', 'Disaster Type', 
                'Disaster Subtype', 'Country', 'Region', 'Start Year', 
                'Start Month', 'Total Deaths', 'Total Affected', 
                'No. Affected', 'No. Homeless'
            ],
            'categorical_features': [
                'Disaster Group', 'Disaster Subgroup', 'Disaster Type', 
                'Disaster Subtype', 'Country', 'Region'
            ],
            'numerical_features': [
                'Start Year', 'Start Month', 'Total Deaths', 
                'Total Affected', 'No. Affected', 'No. Homeless'
            ]
        }
    
    def clean_data(self):
        """
        Clean and prepare the dataset
        
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        # Select key features
        df_cleaned = self.df[self.preprocessing_config['key_features']].copy()
        
        # Handle missing values
        # For numerical columns, fill with median
        numerical_features = self.preprocessing_config['numerical_features']
        df_cleaned[numerical_features] = df_cleaned[numerical_features].fillna(df_cleaned[numerical_features].median())
        
        # For categorical columns, fill with most frequent value
        categorical_features = self.preprocessing_config['categorical_features']
        df_cleaned[categorical_features] = df_cleaned[categorical_features].fillna(df_cleaned[categorical_features].mode().iloc[0])
        
        # Create a binary target variable (disaster severity)
        df_cleaned['Disaster_Severity'] = np.where(
            (df_cleaned['Total Deaths'] > 10) | 
            (df_cleaned['Total Affected'] > 1000), 
            1, 0
        )
        
        return df_cleaned
    
    def encode_features(self, df):
        """
        Encode categorical features
        
        Args:
            df (pd.DataFrame): Input dataframe
        
        Returns:
            tuple: Encoded features and label encoder dictionaries
        """
        # Prepare label encoders for categorical features
        label_encoders = {}
        df_encoded = df.copy()
        
        for feature in self.preprocessing_config['categorical_features']:
            le = LabelEncoder()
            df_encoded[feature] = le.fit_transform(df_encoded[feature].astype(str))
            label_encoders[feature] = {
                'classes': list(le.classes_),
                'feature_name': feature
            }
        
        return df_encoded, label_encoders
    
    def prepare_model_data(self):
        """
        Prepare data for model training
        
        Returns:
            dict: Prepared data for model training
        """
        # Clean the data
        df_cleaned = self.clean_data()
        
        # Encode features
        df_encoded, label_encoders = self.encode_features(df_cleaned)
        
        # Split features and target
        X = df_encoded.drop('Disaster_Severity', axis=1)
        y = df_encoded['Disaster_Severity']
        
        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale numerical features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Save preprocessing artifacts
        preprocessing_info = {
            'label_encoders': label_encoders,
            'feature_names': list(X.columns),
            'target_feature': 'Disaster_Severity'
        }
        
        # Save preprocessing info
        with open('disaster_preprocessing_info.json', 'w') as f:
            json.dump(preprocessing_info, f)
        
        joblib.dump(scaler, 'scaler.joblib')
        
        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train,
            'y_test': y_test,
            'scaler': scaler
        }

# Example usage
if __name__ == '__main__':
    preprocessor = DisasterDataPreprocessor('public_emdat.xlsx')
    model_data = preprocessor.prepare_model_data()
    print("Data preprocessed successfully!")