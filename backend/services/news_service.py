import requests
from flask import current_app
from config import Config

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
                "api-key": Config.GUARDIAN_KEY
            },
            timeout=10 
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and 'results' in data['response']:
                return data['response']['results']
        
        current_app.logger.error(f"Guardian API error: {response.status_code}, {response.text}")
        return []
    except Exception as e:
        current_app.logger.error(f"Guardian API exception: {str(e)}")
        return []

def get_newsapi_news(limit=10, query="natural disasters"):
    """getting disaster news from the NewsAPI"""
    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "apiKey": Config.NEWSAPI_KEY,
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
        
        current_app.logger.error(f"NewsAPI error: {response.status_code}, {response.text}")
        return []
    except Exception as e:
        current_app.logger.error(f"NewsAPI exception: {str(e)}")
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