
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Login from './components/Login';
import Signup from './components/Signup';
import LandingPage from './components/LandingPage';
import DisasterNewsComponent from './components/DisasterNewsComponent';
import MapComponent from './components/MapComponent';
import DonationForm from './components/DonationForm';
import DisasterPrediction from './components/DisasterPrediction';
import Navbar from './components/Navbar'; // Make sure this is the updated Navbar

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      const mockUser = { id: 1, name: "Test User" }; // Replace with real fetch
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

  const AuthenticatedLayout = () => (
    <>
      <Navbar isAuthenticated={isAuthenticated} handleLogout={handleLogout} />
      <Outlet />
    </>
  );

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <Router>
      <Toaster position="top-center" />
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={!isAuthenticated ? <Login setIsAuthenticated={setIsAuthenticated} setCurrentUser={setCurrentUser} /> : <Navigate to="/home" replace />} />
        <Route path="/signup" element={!isAuthenticated ? <Signup /> : <Navigate to="/home" replace />} />

        {/* Authenticated Routes */}
        <Route element={<AuthenticatedLayout />}>
          <Route path="/home" element={<LandingPage isAuthenticated={isAuthenticated} handleLogout={handleLogout} currentUser={currentUser} />} />
          <Route path="/disaster-news" element={isAuthenticated ? <DisasterNewsComponent /> : <Navigate to="/login" replace />} />
          <Route path="/disaster-map" element={isAuthenticated ? <MapComponent /> : <Navigate to="/login" replace />} />
          <Route path="/donate" element={isAuthenticated && currentUser ? <DonationForm userId={currentUser.id} /> : <Navigate to="/login" replace />} />
          <Route path="/predict-disaster" element={isAuthenticated ? <DisasterPrediction currentUser={currentUser} /> : <Navigate to="/login" replace />} />
        </Route>

        {/* Root Redirect */}
        <Route path="/" element={<Navigate to={isAuthenticated ? "/home" : "/login"} replace />} />
      </Routes>
    </Router>
  );
};

export default App;
