import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import LandingPage from './components/LandingPage';
import DisasterNewsComponent from './components/DisasterNewsComponent';
import MapComponent from './components/MapComponent';
import DonationForm from './components/DonationForm';
import DisasterPrediction from './components/DisasterPrediction.jsx';
const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      // In real app, you would fetch user data from the token
      const mockUser = { id: 1, name: "Test User" };
      setCurrentUser(mockUser);
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    setCurrentUser(null);
  };

  if (isLoading) {
    return <div className="min-h-screen bg-gray-100 flex items-center justify-center">Loading...</div>;
  }

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
            element={
              <LandingPage 
                isAuthenticated={isAuthenticated} 
                handleLogout={handleLogout} 
                currentUser={currentUser} 
              />
            } 
          />
          <Route 
            path="/disaster-news" 
            element={isAuthenticated ? <DisasterNewsComponent /> : <Navigate to="/login" replace />} 
          />
          <Route 
            path="/disaster-map" 
            element={isAuthenticated ? <MapComponent /> : <Navigate to="/login" replace />} 
          />
          <Route 
            path="/donate" 
            element={
              isAuthenticated && currentUser ? 
                <DonationForm userId={currentUser.id} /> : 
                <Navigate to="/login" replace />
            } 
          />
          <Route 
            path="/predict-disaster" 
            element={
              isAuthenticated ? 
                <DisasterPrediction currentUser={currentUser} /> : 
                <Navigate to="/login" replace />
            }
          />
          <Route 
            path="/" 
            element={<Navigate to={isAuthenticated ? "/home" : "/login"} replace />} 
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;