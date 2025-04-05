import React, { useState, useEffect } from 'react';

const DisasterNewsComponent = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const placeholderImage = '/images/placeholder_disaster_img.jpg';

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/disaster-news`); 
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
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <p className="text-xl text-amber-400">Loading latest disaster news...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center">
        <p className="text-xl text-amber-400">Sorry, we couldn't load the latest news.</p>
        <p className="text-md text-amber-300">Error: {error}</p>
      </div>
    );
  }

  if (news.length === 0) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <p className="text-xl text-amber-400">No disaster news found at this time. Please come back later.</p>
      </div>
    );
  }

  return (
    <div className="bg-black text-white min-h-screen px-6 py-10">
      <h2 className="text-center text-3xl font-semibold text-amber-400 mb-6">
        Latest Disaster News
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {news.map((article) => (
          <a
            key={article.id || article.url}
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-800 border border-amber-400 rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition transform duration-300"
          >
            <img 
              src={article.image || placeholderImage} 
              alt={article.title}
              onError={(e) => { e.target.onerror = null; e.target.src = placeholderImage; }}
              className="w-full h-48 object-cover"
            />
            <div className="p-5">
              <h3 className="text-lg font-bold text-white">{article.title}</h3>
              <p className="text-sm text-gray-300 mt-2">{truncateContent(article.content)}</p>
              <div className="mt-4 flex justify-between text-sm text-amber-300">
                <span>{article.source}</span>
                <span>{formatDate(article.published)}</span>
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default DisasterNewsComponent;
