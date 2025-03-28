from flask import Blueprint, request, jsonify
from models.donation import Donation
from database import db
import time
import random

donation_bp = Blueprint('donations', __name__)

def _build_cors_preflight_response():
    response = jsonify({"message": "Preflight Accepted"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response

@donation_bp.route('/donate', methods=['POST', 'OPTIONS'])
def create_donation():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        if 'user_id' not in data or 'amount' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate amount
        try:
            amount = float(data['amount'])
            if amount <= 0:
                raise ValueError
        except ValueError:
            return jsonify({"error": "Invalid amount"}), 400

        time.sleep(1.5)
        
        transaction_id = f"TX{random.randint(100000000, 999999999)}"
        
        donation = Donation(
            user_id=data['user_id'],
            amount=amount,
            currency=data.get('currency', 'USD'),
            payment_method=data.get('payment_method', 'credit_card'),
            transaction_id=transaction_id
        )
        
        db.session.add(donation)
        db.session.commit()

        response = jsonify({
            'message': 'Donation successful!',
            'transaction_id': transaction_id,
            'amount': donation.amount,
            'currency': donation.currency
        })
        
        # Add CORS headers to main response
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        
        return response, 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@donation_bp.route('/donations/<int:user_id>', methods=['GET'])
def get_user_donations(user_id):
    try:
        donations = Donation.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': d.id,
            'amount': float(d.amount),
            'currency': d.currency,
            'date': d.created_at.isoformat()
        } for d in donations]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500