import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))


from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from config import Config  # Assuming you have a Config class defined in backend/config.py
from database import init_db, bcrypt
from models.user import User
from models.donation import Donation

app = Flask(__name__)

# Set up CORS for your frontend
CORS(app, 
     origins=["http://localhost:5173"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     supports_credentials=True,
     max_age=3600)

# Set up caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# Load Flask configuration from backend/config.py
app.config.from_object(Config)

# Initialize the database and other services
init_db(app)
bcrypt.init_app(app)

# Register blueprints
from routes.auth_routes import auth_bp
from routes.news_routes import news_bp
from routes.donation_routes import donation_bp

import routes.news_routes
routes.news_routes.cache = cache

app.register_blueprint(auth_bp)
app.register_blueprint(news_bp)
app.register_blueprint(donation_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
