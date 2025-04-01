import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = ({ isAuthenticated, handleLogout }) => {
  const navigate = useNavigate();

  // Function to handle restricted navigation
  const handleRestrictedAccess = (e, route) => {
    if (!isAuthenticated) {
      e.preventDefault(); // Prevent default navigation
      navigate("/signup"); // Redirect to Register page
    }
  };

  return (
    <nav className="bg-teal-600 text-white py-4 px-6 flex justify-between items-center shadow-md">
      {/* Logo */}
      <h2 className="text-lg font-semibold">DisasterPredict</h2>

      {/* Navigation Links */}
      <div className="space-x-6 flex items-center">
        <Link to="/home" className="hover:underline">
          Home
        </Link>
        
        {/* Restricted Links */}
        <Link to="/disaster-news" onClick={(e) => handleRestrictedAccess(e, "/disaster-news")} className="hover:underline">
          Disaster News
        </Link>
        <Link to="/disaster-map" onClick={(e) => handleRestrictedAccess(e, "/disaster-map")} className="hover:underline">
          Disaster Map
        </Link>
        <Link to="/donate" onClick={(e) => handleRestrictedAccess(e, "/donate")} className="hover:underline font-semibold text-yellow-300">
          Donate
        </Link>
      </div>

      {/* Authentication Buttons */}
      <div>
        {isAuthenticated ? (
          <button 
            onClick={handleLogout} 
            className="bg-red-500 px-4 py-2 rounded-md text-white hover:bg-red-700 transition"
          >
            Logout
          </button>
        ) : (
          <div className="space-x-4">
            <Link 
              to="/login" 
              className="bg-amber-500 px-4 py-2 rounded-md text-white hover:bg-amber-600 transition"
            >
              Login
            </Link>
            <Link 
              to="/signup" 
              className="bg-amber-500 px-4 py-2 rounded-md text-white hover:bg-amber-600 transition"
            >
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
