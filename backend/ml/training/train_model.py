import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from config import PATHS, MODEL_CONFIG
import matplotlib.pyplot as plt
import seaborn as sns

def train_model():
    # Load processed data
    X_train = joblib.load(os.path.join(PATHS['processed'], 'X_train.pkl'))
    y_train = joblib.load(os.path.join(PATHS['processed'], 'y_train.pkl'))
    X_test = joblib.load(os.path.join(PATHS['processed'], 'X_test.pkl'))
    y_test = joblib.load(os.path.join(PATHS['processed'], 'y_test.pkl'))

    # Initialize and train model
    model = RandomForestClassifier(**MODEL_CONFIG)
    print("🔄 Training disaster classification model...")
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, os.path.join(PATHS['models'], 'disaster_classifier.pkl'))
    print(f"✅ Model saved to {PATHS['models']}/disaster_classifier.pkl")
    
    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    # Generate predictions
    y_pred = model.predict(X_test)
    
    # Classification report
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Confusion matrix
    plt.figure(figsize=(12, 10))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Disaster Type Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig(os.path.join(PATHS['reports'], 'confusion_matrix.png'))
    print(f"📈 Confusion matrix saved to {PATHS['reports']}/confusion_matrix.png")

if __name__ == "__main__":
    model, X_test, y_test = train_model()
    evaluate_model(model, X_test, y_test)