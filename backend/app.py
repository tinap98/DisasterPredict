from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from config import Config
from database import init_db, bcrypt

app = Flask(__name__)

CORS(app, 
     origins=["http://localhost:5173"], 
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True,
     max_age=3600)
     
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

app.config.from_object(Config)

init_db(app)
bcrypt.init_app(app)

from routes.auth_routes import auth_bp
from routes.news_routes import news_bp

import routes.news_routes
routes.news_routes.cache = cache

app.register_blueprint(auth_bp)
app.register_blueprint(news_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)