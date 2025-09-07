import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from config import Config
from database import init_db, bcrypt, create_tables
from models.user import User
from models.donation import Donation

app = Flask(__name__)

# Enable CORS
CORS(app,
     origins=[
         "http://localhost:5173",
         "https://disasterpredict.vercel.app",
         "https://disaster-predict-1nfpgalad-tina-pudaris-projects.vercel.app"
     ],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)

# Load config
app.config.from_object(Config)

# Set up caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# Initialize the database and services
init_db(app)
bcrypt.init_app(app)

# Register blueprints
from routes.auth_routes import auth_bp
from routes.news_routes import news_bp, register_cache
from routes.donation_routes import donation_bp
from routes.prediction_routes import prediction_bp

# Inject cache into routes
register_cache(cache)

app.register_blueprint(auth_bp)
app.register_blueprint(news_bp)
app.register_blueprint(donation_bp, url_prefix='/api')
app.register_blueprint(prediction_bp, url_prefix='/api')

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    create_tables(app)
    print("Initialized the database.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
