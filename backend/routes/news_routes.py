from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from services.news_service import get_newsapi_news, get_guardian_news, standardize_article

news_bp = Blueprint('news', __name__, url_prefix='/api')

cache = None

@news_bp.route('/disaster-news')
def get_disaster_news():

    if cache:
        @cache.cached(timeout=3600)  
        def get_cached_disaster_news(limit, query):
            try:
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
                
                return all_articles
            except Exception as e:
                current_app.logger.error(f"Error in disaster news endpoint: {str(e)}")
                return {"error": str(e)}, 500
        
        limit = int(request.args.get('limit', 5))
        query = request.args.get('query', 'natural disasters')
        
        result = get_cached_disaster_news(limit, query)
        

        if isinstance(result, tuple) and len(result) == 2:
            return jsonify(result[0]), result[1]
        return jsonify(result)
    else:

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
            current_app.logger.error(f"Error in disaster news endpoint: {str(e)}")
            return jsonify({"error": str(e)}), 500

@news_bp.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})