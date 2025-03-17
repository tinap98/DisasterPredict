import React, { useState, useEffect } from 'react';
import MapComponent from './MapComponent';
import DisasterNewsComponent from './DisasterNewsComponent';
import { fetchDisasters } from './nasa';
import '../index.css';

const Dashboard = ({ handleLogout }) => {
  const [disasters, setDisasters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('map');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async (category) => {
    try {
      setLoading(true);
      const data = await fetchDisasters(category);
      
      if (data.length === 0) {
        setError('No current disasters found');
      } else {
        setError(null);
      }
      
      setDisasters(data);
    } catch (err) {
      setError('Failed to load disaster data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="dashboard-header">
        <h1>NASA Real-Time Disaster Tracker</h1>
        <button onClick={handleLogout} className="logout-button">
          Logout
        </button>
      </div>

      <div className="app-tabs">
        <button 
          className={`tab-button ${activeTab === 'map' ? 'active' : ''}`}
          onClick={() => setActiveTab('map')}
        >
          Disaster Map
        </button>
        <button 
          className={`tab-button ${activeTab === 'news' ? 'active' : ''}`}
          onClick={() => setActiveTab('news')}
        >
          Disaster News
        </button>
      </div>

      {activeTab === 'map' && (
        <>
          <div className="controls">
            <select onChange={(e) => loadData(e.target.value)}>
              <option value="">All Disasters</option>
              <option value="wildfires">Wildfires</option>
              <option value="severeStorms">Severe Storms</option>
              <option value="volcanoes">Volcanoes</option>
              <option value="earthquakes">Earthquakes</option>
              <option value="landslides">Landslides</option>
              <option value="floods">Floods</option>
            </select>
          </div>
          
          {loading && <div className="loading">Loading live data from NASA...</div>}
          
          {error && (
            <div className="error">
              {error} - Try refreshing the page or check <a href="https://eonet.gsfc.nasa.gov/" target="_blank" rel="noreferrer">NASA EONET</a>
            </div>
          )}
          
          {!loading && !error && <MapComponent disasters={disasters} />}
        </>
      )}

      {activeTab === 'news' && <DisasterNewsComponent />}
    </div>
  );
};

export default Dashboard;