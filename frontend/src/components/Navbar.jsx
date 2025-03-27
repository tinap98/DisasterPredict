import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-teal-600 text-white py-4 px-6 flex justify-between items-center shadow-md">
      {/* Logo */}
      <h2 className="text-lg font-semibold">DisasterPredict</h2>

      {/* Navigation Links */}
      <div className="space-x-6">
        <Link to="/" className="hover:underline">
          Home
        </Link>
        <Link to="/disaster-news" className="hover:underline">
          Disaster News
        </Link>
        <Link to="/disaster-map" className="hover:underline">
          Disaster Map
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
