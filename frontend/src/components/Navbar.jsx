import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { toast } from "react-hot-toast";

const Navbar = ({ isAuthenticated, handleLogout }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleRestrictedAccess = (e, route) => {
    if (!isAuthenticated) {
      e.preventDefault();
      toast("Please sign up to access that page.");
      navigate("/signup", { state: { from: route } });
    }
  };

  const navLinkStyle = (path) =>
    `hover:underline ${location.pathname === path ? "underline text-yellow-300 font-semibold" : ""}`;

  return (
    <nav className="bg-teal-600 text-white py-4 px-6 flex justify-between items-center shadow-md">
      {/* Logo */}
      <h2 className="text-lg font-semibold">DisasterPredict</h2>

      {/* Navigation Links */}
      <div className="space-x-6 flex items-center">
        <Link to="/home" className={navLinkStyle("/home")}>
          Home
        </Link>

        {/* Restricted Links */}
        <Link
          to="/disaster-news"
          onClick={(e) => handleRestrictedAccess(e, "/disaster-news")}
          className={navLinkStyle("/disaster-news")}
          title="Requires Login"
        >
          Disaster News
        </Link>
        <Link
          to="/disaster-map"
          onClick={(e) => handleRestrictedAccess(e, "/disaster-map")}
          className={navLinkStyle("/disaster-map")}
          title="Requires Login"
        >
          Disaster Map
        </Link>
        <Link
          to="/predict-disaster"
          onClick={(e) => handleRestrictedAccess(e, "/predict-disaster")}
          className={navLinkStyle("/predict-disaster")}
          title="Requires Login"
        >
          Predict Disaster
        </Link>
        <Link
          to="/donate"
          onClick={(e) => handleRestrictedAccess(e, "/donate")}
          className={navLinkStyle("/donate")}
          title="Requires Login"
        >
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
