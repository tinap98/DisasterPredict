from flask import Blueprint, jsonify, request, current_app
from datetime import datetime, timedelta
import jwt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Always return success without checking database
    return jsonify({
        'message': 'User created successfully',
        'user': {
            'username': data['username'],
            'email': data['email']
        }
    }), 201

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing credentials'}), 400

    # Generate a dummy token without checking credentials
    token = jwt.encode(
        {
            'username': data['username'],
            'exp': datetime.utcnow() + timedelta(days=1)
        },
        'dummy-secret-key',
        algorithm='HS256'
    )

    return jsonify({
        'token': token,
        'username': data['username']
    }), 200