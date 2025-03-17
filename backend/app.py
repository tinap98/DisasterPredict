from flask import Flask, jsonify, request
from flask_cors import CORS  
from flask_caching import Cache
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from database import db, bcrypt, init_db, User
import jwt

load_dotenv()
app = Flask(__name__)

CORS(app, 
     origins=["http://localhost:5173"], 
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True,
     max_age=3600)
     
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://root:password@localhost/disasterpredict')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-fallback-key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)
bcrypt.init_app(app)

NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
GUARDIAN_KEY = os.getenv('GUARDIAN_KEY')

def get_guardian_news(limit=10, query="disaster OR flood OR earthquake OR tsunami OR wildfire"):
    """getting disaster news from the Guardian API"""
    try:
        response = requests.get(
            "https://content.guardianapis.com/search",
            params={
                "q": query,
                "section": "world|environment|us-news",
                "show-fields": "thumbnail,trailText",
                "page-size": limit,
                "api-key": GUARDIAN_KEY
            },
            timeout=10 
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'results' in data['response']:
                return data['response']['results']
        
        app.logger.error(f"Guardian API error: {response.status_code}, {response.text}")
        return []
    except Exception as e:
        app.logger.error(f"Guardian API exception: {str(e)}")
        return []

def get_newsapi_news(limit=10, query="natural disasters"):
    """getting disaster news from the NewsAPI"""
    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "apiKey": NEWSAPI_KEY,
                "pageSize": limit,
                "language": "en",
                "sortBy": "publishedAt"
            },
            timeout=10  
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'articles' in data:
                return data['articles']
        
        app.logger.error(f"NewsAPI error: {response.status_code}, {response.text}")
        return []
    except Exception as e:
        app.logger.error(f"NewsAPI exception: {str(e)}")
        return []

def standardize_article(item, source="unknown"):
    """Standardization of both of em api's data"""
    if source == "guardian":
        return {
            "title": item.get('webTitle', 'No title'),
            "url": item.get('webUrl', '#'),
            "image": item.get('fields', {}).get('thumbnail'),
            "content": item.get('fields', {}).get('trailText', 'No description available'),
            "source": "The Guardian",
            "published": item.get('webPublicationDate'),
            "id": item.get('id', '')
        }
    else:  
        return {
            "title": item.get('title', 'No title'),
            "url": item.get('url', '#'),
            "image": item.get('urlToImage'),
            "content": item.get('description', 'No description available'),
            "source": item.get('source', {}).get('name', source),
            "published": item.get('publishedAt'),
            "id": item.get('url', '') 
        }

@app.route('/api/disaster-news')
@cache.cached(timeout=3600)  
def get_disaster_news():
    try:
        limit = int(request.args.get('limit', 5))
        query = request.args.get('query', 'natural disasters')
        
        newsapi_articles = get_newsapi_news(limit, query)
        guardian_articles = get_guardian_news(limit, query)
        
        all_articles = []
        
        if newsapi_articles:
            all_articles.extend([standardize_article(item, "newsapi") for item in newsapi_articles])
        
        if guardian_articles:
            all_articles.extend([standardize_article(item, "guardian") for item in guardian_articles])
        
        all_articles = sorted(
            all_articles, 
            key=lambda x: x.get('published', ''), 
            reverse=True
        )[:limit]
        
        return jsonify(all_articles)
    
    except Exception as e:
        app.logger.error(f"Error in disaster news endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username exists'}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email exists'}), 409

    try:
        hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing credentials'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    try:
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user_id': user.id,
            'username': user.username
        }), 200
    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Token generation failed'}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)