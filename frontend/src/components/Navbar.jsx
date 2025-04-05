import React from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar = ({ isAuthenticated, handleLogout }) => {
  const location = useLocation();

  const navItems = [
    { label: "Home", path: "/home" },
    { label: "Predict Disaster", path: "/predict-disaster" },
    { label: "Disaster News", path: "/disaster-news" },
    { label: "Disaster Map", path: "/disaster-map" },
    { label: "Donate", path: "/donate" },
  ];

  return (
    <nav className="navbar flex justify-between items-center px-6 py-4 bg-black text-white shadow-lg">
      <h2 className="text-lg font-semibold">DisasterPredict</h2>

      <div className="space-x-6 flex items-center">
        {navItems.map(({ label, path }) => (
          <Link
            key={path}
            to={path}
            className={`relative group transition duration-300 ${
              location.pathname === path ? "text-amber-400 font-semibold" : ""
            }`}
          >
            {label}
            <span className="absolute left-0 bottom-0 w-0 h-[2px] bg-amber-500 transition-all duration-300 group-hover:w-full"></span>
          </Link>
        ))}
      </div>

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
  );
};

export default Navbar;
