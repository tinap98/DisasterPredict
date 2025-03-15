from flask import Flask, jsonify, request
from flask_cors import CORS  
from flask_caching import Cache
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
    "methods": ["GET"],
    "allow_headers": ["Content-Type"]
}})
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)