from flask import Blueprint, request, jsonify
from ml.predict import predict_disaster

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Endpoint for disaster prediction
    Expects JSON with:
    - year
    - mag_scale_index
    - dis_mag_value
    - country_code_index
    - longitude
    - latitude
    """
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'preflight'})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    return predict_disaster(request)