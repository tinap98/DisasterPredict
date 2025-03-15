import React, { useState, useEffect } from 'react';
import "../styles/DisasterNews.css";

const DisasterNewsComponent = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const placeholderImage = '/images/placeholder_disaster_img.jpg';

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://127.0.0.1:5000/api/disaster-news'); 
        if (!response.ok) {
          throw new Error(`Error fetching news: ${response.status}`);
        }
        
        const data = await response.json();
        setNews(data);
      } catch (err) {
        console.error('Failed to fetch news:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
    const intervalId = setInterval(fetchNews, 30 * 60 * 1000);
    return () => clearInterval(intervalId);
  }, []);

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date';
    try {
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('en-US', {
        year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
      }).format(date);
    } catch (e) {
      return dateString;
    }
  };

  const truncateContent = (content, maxLength = 120) => {
    if (!content) return 'No description available';
    return content.length > maxLength ? `${content.substring(0, maxLength)}...` : content;
  };

  if (loading) {
    return (
      <div className="disaster-news-container">
        <h2>Latest Disaster News</h2>
        <div className="news-loading"><p>Loading latest disaster news...</p></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="disaster-news-container">
        <h2>Latest Disaster News</h2>
        <div className="news-error">
          <p>Sorry, we couldn't load the latest news. Please try again later.</p>
          <p>Error: {error}</p>
        </div>
      </div>
    );
  }

  if (news.length === 0) {
    return (
      <div className="disaster-news-container">
        <h2>Latest Disaster News</h2>
        <div className="news-empty"><p>No disaster news found at this time. Please come back later.</p></div>
      </div>
    );
  }

  return (
    <div className="disaster-news-container">
      <h2>Latest Disaster News</h2>
      <div className="news-list">
        {news.map((article) => (
          <a
            key={article.id || article.url}
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="news-item"
          >
            <div className="news-image">
              <img 
                src={article.image || placeholderImage} 
                alt={article.title}
                onError={(e) => { e.target.onerror = null; e.target.src = placeholderImage; }}
              />
            </div>
            <div className="news-content">
              <h3>{article.title}</h3>
              <p className="news-description">{truncateContent(article.content)}</p>
              <div className="news-meta">
                <span className="news-source">{article.source}</span>
                <span className="news-date">{formatDate(article.published)}</span>
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default DisasterNewsComponent;
