from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from services.news_service import get_newsapi_news, get_guardian_news, standardize_article

news_bp = Blueprint('news', __name__, url_prefix='/api')

cache = None  # Will be set by app.py


def register_cache(c):
    global cache
    cache = c


def get_cached_disaster_news(limit, query):
    cache_key = f"disaster_news:{query}:{limit}"
    
    if cache:
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

    try:
        newsapi_articles = get_newsapi_news(limit, query)
        guardian_articles = get_guardian_news(limit, query)

        all_articles = []
        if newsapi_articles:
            all_articles.extend([standardize_article(item, "newsapi") for item in newsapi_articles])
        if guardian_articles:
            all_articles.extend([standardize_article(item, "guardian") for item in guardian_articles])

        all_articles = sorted(all_articles, key=lambda x: x.get('published', ''), reverse=True)[:limit]

        if cache:
            cache.set(cache_key, all_articles, timeout=3600)

        return all_articles
    except Exception as e:
        current_app.logger.error(f"Error in disaster news endpoint: {str(e)}")
        return {"error": str(e)}, 500


@news_bp.route('/disaster-news')
def get_disaster_news():
    try:
        limit = int(request.args.get('limit', 5))
        query = request.args.get('query', 'natural disasters')

        result = get_cached_disaster_news(limit, query)

        if isinstance(result, tuple) and len(result) == 2:
            return jsonify(result[0]), result[1]
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error in disaster news endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500


@news_bp.route('/health')
def health_check():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})
