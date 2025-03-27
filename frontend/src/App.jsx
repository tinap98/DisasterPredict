import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import LandingPage from './components/LandingPage';
import DisasterNewsComponent from './components/DisasterNewsComponent';
import MapComponent from './components/MapComponent';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem('authToken')
  );

  useEffect(() => {
    setIsAuthenticated(!!localStorage.getItem('authToken'));
  }, []);

  useEffect(() => {
    const handleStorageChange = () => {
      setIsAuthenticated(!!localStorage.getItem('authToken'));
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route 
            path="/login" 
            element={!isAuthenticated ? <Login setIsAuthenticated={setIsAuthenticated} /> : <Navigate to="/home" replace />} 
          />
          <Route 
            path="/signup" 
            element={!isAuthenticated ? <Signup /> : <Navigate to="/home" replace />} 
          />
          <Route 
            path="/home" 
            element={<LandingPage isAuthenticated={isAuthenticated} handleLogout={handleLogout} />} 
          />
          <Route 
            path="/disaster-news" 
            element={<DisasterNewsComponent />} 
          />
          <Route 
            path="/disaster-map" 
            element={<MapComponent />} 
          />
          <Route 
            path="/" 
            element={<Navigate to="/home" replace />} 
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
