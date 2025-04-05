import React from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = ({ isAuthenticated, handleLogout }) => {
  const location = useLocation();

  const navLink = (label, path) => (
    <Link
      to={path}
      className={`relative group transition duration-300 ${
        location.pathname === path ? "text-amber-400 font-semibold" : ""
      }`}
    >
      {label}
      <span className="absolute left-0 bottom-0 w-0 h-[2px] bg-amber-500 transition-all duration-300 group-hover:w-full"></span>
    </Link>
  );

  return (
    <nav className="navbar flex justify-between items-center px-6 py-4 bg-black text-white shadow-lg">
      <h2 className="text-lg font-semibold">DisasterPredict</h2>

      <div className="space-x-6 flex items-center">
        {navLink("Home", "/home")}
        {navLink("Predict Disaster", "/predict-disaster")}
        {navLink("Disaster News", "/disaster-news")}
        {navLink("Disaster Map", "/disaster-map")}
        {navLink("Donate", "/donate")}
      </div>

      {isAuthenticated ? (
        <button
          onClick={handleLogout}
          className="bg-amber-500 text-black font-semibold px-4 py-2 rounded-md hover:bg-amber-600 transition-all duration-300"
        >
          Logout
        </button>
      ) : (
        <div className="space-x-4">
          <Link
            to="/login"
            className="bg-amber-500 text-black font-semibold px-4 py-2 rounded-md hover:bg-amber-600 transition-all duration-300"
          >
            Login
          </Link>
          <Link
            to="/signup"
            className="bg-amber-500 text-black font-semibold px-4 py-2 rounded-md hover:bg-amber-600 transition-all duration-300"
          >
            Signup
          </Link>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
