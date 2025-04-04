import React from "react";
import { Link } from "react-router-dom";

const LandingPage = ({ isAuthenticated, handleLogout }) => {
  return (
    <div className="bg-custom min-h-screen flex flex-col">
      {/* Navbar */}
      <nav className="navbar flex justify-between items-center px-6">
        <h2 className="text-lg font-semibold">DisasterPredict</h2>
        <div className="space-x-6 flex items-center">
        {["Home", "Predict Disaster", "Disaster News", "Disaster Map", "Donate"].map((item, index) => (
            <Link
              key={index}
              to={
                item === "Home"
                  ? "/home"
                  : item === "Predict Disaster"
                  ? "/predict-disaster"
                  : item === "Disaster News"
                  ? "/disaster-news"
                  : item === "Disaster Map"
                  ? "/disaster-map"
                  : "/donate"
              }
              className="relative group transition duration-300"
            >
              {item}
              <span className="absolute left-0 bottom-0 w-0 h-[2px] bg-amber-500 transition-all duration-300 group-hover:w-full"></span>
            </Link>
          ))}
        </div>

        {/* Auth Buttons */}
        {isAuthenticated ? (
          <button onClick={handleLogout} className="btn-primary">
            Logout
          </button>
        ) : (
          <div className="space-x-4">
            <Link to="/login" className="btn-primary">Login</Link>
            <Link to="/signup" className="btn-primary">Signup</Link>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center text-center px-6 flex-grow mt-20 pb-10 relative z-10">
        <h1 className="text-4xl font-bold text-amber-500">Welcome to DisasterPredict</h1>
        <p className="mt-4 text-lg max-w-2xl text-gray-200">
          Stay informed with real-time disaster tracking and news updates powered by NASA and other reliable sources.
        </p>
      </div>

      {/* Donate Section */}
      <div className="flex flex-col items-center pb-10">
        <h2 className="text-2xl font-semibold text-center mb-4">Support Relief Efforts</h2>
        <Link 
            to={isAuthenticated ? "/donate" : "/login"} 
            className="donate-button"
        >
       Donate Now
      </Link>
      </div>
    </div>
  );
};

export default LandingPage;
