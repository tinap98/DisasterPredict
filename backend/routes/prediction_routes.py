from flask import Blueprint, request, jsonify
from ml.prediction.predictor import DisasterPredictor  # Import using the ML package structure

prediction_bp = Blueprint('prediction', __name__)
predictor = DisasterPredictor()

@prediction_bp.route('/disaster', methods=['POST'])
def predict_disaster():
    try:
        data = request.json
        result = predictor.predict(data)
        
        if 'error' in result:
            return jsonify(result), 400
            
        return jsonify({
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'probabilities': result['probabilities']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
