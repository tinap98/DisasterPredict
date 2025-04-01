import os
import sys
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the project root (D:\DisasterPredict\backend) to sys.path
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
logging.info("Added project root to sys.path: %s", project_root)

# Now import configuration settings from ml.config
from ml.config import PATHS, MODEL_CONFIG

def validate_paths():
    """Ensure all required processed data files exist."""
    required = [
        (PATHS['processed'], 'X_train.pkl'),
        (PATHS['processed'], 'y_train.pkl'),
        (PATHS['processed'], 'X_test.pkl'),
        (PATHS['processed'], 'y_test.pkl')
    ]
    for path, file in required:
        full_path = Path(path) / file
        if not full_path.exists():
            logging.error("Missing file: %s", full_path)
            raise FileNotFoundError(f"Missing: {full_path}")
    logging.info("All required data files are present.")

def main():
    validate_paths()
    
    processed_path = Path(PATHS['processed'])
    X_train = joblib.load(processed_path / 'X_train.pkl')
    y_train = joblib.load(processed_path / 'y_train.pkl')
    X_test = joblib.load(processed_path / 'X_test.pkl') 
    y_test = joblib.load(processed_path / 'y_test.pkl')
    
    # Train the RandomForest model with settings from configuration
    model = RandomForestClassifier(**MODEL_CONFIG)
    logging.info("Training model...")
    model.fit(X_train, y_train)
    
    # Save the trained model
    models_dir = Path(PATHS['models'])
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / 'disaster_classifier.pkl'
    joblib.dump(model, model_path)
    logging.info("Model saved to %s", model_path)
    
    # Evaluate on the test set
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, zero_division=0)
    logging.info("Classification Report:\n%s", report)
    print(report)
    
    # Plot and save the confusion matrix
    plt.figure(figsize=(12, 10))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    reports_dir = Path(PATHS['reports'])
    reports_dir.mkdir(parents=True, exist_ok=True)
    confusion_path = reports_dir / 'confusion_matrix.png'
    plt.savefig(confusion_path)
    plt.close()
    logging.info("Confusion matrix saved to %s", confusion_path)

if __name__ == "__main__":
    main()
