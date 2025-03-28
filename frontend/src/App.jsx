import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import Dashboard from './components/Dashboard';
import DonationForm from './components/DonationForm';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem('authToken')
  );
  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    setIsAuthenticated(!!token);
    // In real app, fetch user data from token
    if (token) setCurrentUser({ id: 1, name: "User" }); // Mock user
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    setIsAuthenticated(false);
    setCurrentUser(null);
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" 
          element={!isAuthenticated ? 
            <Login setIsAuthenticated={setIsAuthenticated} setCurrentUser={setCurrentUser} /> : 
            <Navigate to="/dashboard" replace />} 
        />
        <Route path="/signup" 
          element={!isAuthenticated ? <Signup /> : <Navigate to="/dashboard" replace />} 
        />
        <Route path="/dashboard" 
          element={isAuthenticated ? 
            <Dashboard handleLogout={handleLogout} user={currentUser} /> : 
            <Navigate to="/login" replace />} 
        />
        <Route path="/donate" 
          element={isAuthenticated ? 
            <DonationForm userId={currentUser?.id} /> : 
            <Navigate to="/login" replace />} 
        />
        <Route path="/" 
          element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />} 
        />
      </Routes>
    </Router>
  );
};

export default App;