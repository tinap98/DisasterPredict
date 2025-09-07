from flask import Blueprint, jsonify, request, current_app, make_response
from datetime import datetime, timedelta
import jwt

auth_bp = Blueprint('auth', __name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://disasterpredict.vercel.app'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    response = make_response(jsonify({
        'success': True,
        'message': 'Registration successful',
        'user': {
            'username': data.get('username', 'guest'),
            'email': data.get('email', 'guest@example.com')
        }
    }))
    
    return add_cors_headers(response)

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Generate a dummy token
    token = jwt.encode(
        {
            'username': data.get('username', 'guest'),
            'exp': datetime.utcnow() + timedelta(days=1)
        },
        'dummy-secret-key',
        algorithm='HS256'
    )

    response = make_response(jsonify({
        'success': True,
        'message': 'Login successful',
        'token': token,
        'username': data.get('username', 'guest')
    }))
    
    return add_cors_headers(response)