import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import LandingPage from './components/LandingPage';
import DisasterNewsComponent from './components/DisasterNewsComponent';
import MapComponent from './components/MapComponent';
import DonationForm from './components/DonationForm';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem('authToken')
  );
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      setIsAuthenticated(true);
      setCurrentUser({ id: 1, name: "User" }); // Mock user
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    setCurrentUser(null);
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route 
            path="/login" 
            element={!isAuthenticated ? 
              <Login setIsAuthenticated={setIsAuthenticated} setCurrentUser={setCurrentUser} /> : 
              <Navigate to="/home" replace />} 
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
            path="/donate" 
            element={<DonationForm userId={currentUser?.id} />} // ✅ No auth check
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
